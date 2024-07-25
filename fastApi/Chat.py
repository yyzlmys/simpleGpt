import os
from langchain.agents import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chains import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


# 环境变量
os.environ["ZHIPUAI_API_KEY"] = "ed6fbd504f7c288c2184de79f8fe5d34.RhC4WOlJt8MocUbk"
os.environ["SERPAPI_API_KEY"] = "d2de951e94b9cb687f86da940c5152002568b15ef1d199f5341c42c6ff903a98"
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"

class Chat:
    def __init__(self):
        # 初始化
        self.chat_model = ChatZhipuAI() # 模型
        self.text_splitter = RecursiveCharacterTextSplitter() # 分词
        self.history = None # 历史记录数组
        self.base_dir = None # 文件路径
        self.vector_store = None # 向量存储
        self.agent = None

    # 加载文件
    def load_documents_from_base_dir(self, base_dir):
        txt_documents = []

        def type_list():
            return {
                'd0cf11e0a1b11ae10000': 'doc',
                '255044462d312e350d0a': 'pdf',
                '504b0304140006000800': 'docx',
            }

        def bytes2hex(bytes):
            num = len(bytes)
            hexstr = u""
            for i in range(num):
                t = u"%x" % bytes[i]
                if len(t) % 2:
                    hexstr += u"0"
                hexstr += t
            return hexstr.upper()

        def filetype(filename):
            with open(filename, 'rb') as binfile:
                bins = binfile.read(20)
            bins = bytes2hex(bins).lower()
            tl = type_list()
            ftype = 'unknown'
            for hcode in tl.keys():
                lens = len(hcode)
                if bins[0:lens] == hcode:
                    ftype = tl[hcode]
                    break
            if ftype == 'unknown':
                bins = bins[0:5]
                for hcode in tl.keys():
                    if len(hcode) > 5 and bins == hcode[0:5]:
                        ftype = tl[hcode]
                        break
            return ftype

        for filename in os.listdir(base_dir):
            file_path = os.path.join(base_dir, filename)
            file_type = filetype(file_path)

            if file_type == 'pdf':
                loader = PyPDFLoader(file_path)
                txt_documents.extend(loader.load())
            elif file_type == 'docx':
                loader = Docx2txtLoader(file_path)
                txt_documents.extend(loader.load())

        for filename in os.listdir(base_dir):
            file_path = os.path.join(base_dir, filename)
            if filename.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")
                txt_documents.extend(loader.load())

        return txt_documents

    # 初始化向量数据库
    def initialize_vector_store(self, documents):
        embeddings = HuggingFaceEmbeddings(model_name="/root/m3e", model_kwargs={'device': "cpu"})
        chunked_documents = self.text_splitter.split_documents(documents=documents)
        self.vector_store = FAISS.from_documents(documents=chunked_documents, embedding=embeddings)

    # 创建检索链
    def create_retriever_chain(self):

        prompt = ChatPromptTemplate.from_messages([
            ("system", """
                  You are an intelligent question answering robot, \n
                  and when I ask a question, you will provide me with an answer by calling different tools in the agent\n
                  and referencing chat_history.\n
                  You will prioritize using tools and then use your knowledge base if information cannot be retrieved\n
                  To use a tool, please use the following format:\n
                  ```
                  Thought: Do I need to use a tool? Yes\n
                  Action: the action to take, should be one of [Search, Calculator, retrieval_tool, txt_retrieval_tool]\n
                  Action Input: the input to the action\n
                  Observation: the result of the action\n
                 ```
                 if you do not need to use a tool, you MUST use the format:\n
                 ```
                 Thought: Do I need to use a tool? No\n
                 AI: [your response here]\n
                 ```
                Answer the user's questions based on the below context:\n
                {context}\n
                 """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
        ])

        retriever = self.vector_store.as_retriever()
        retriever_chain = create_history_aware_retriever(self.chat_model, retriever, prompt)
        document_chain = create_stuff_documents_chain(self.chat_model, prompt)
        retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)
        return retrieval_chain

    def create_tool(self, name, description, retrieval_chain):
        def retrieval_tool(query):
            return retrieval_chain.invoke({
                "chat_history": self.history,
                "input": query,
                "context": ""
            })["answer"]

        return Tool(name=name, description=description, func=retrieval_tool)

    def initialize_agent_tools(self, name, description):
        tools = load_tools(tool_names=["serpapi"], llm=self.chat_model)
        if self.base_dir != None:
            documents = self.load_documents_from_base_dir(self.base_dir)
            self.initialize_vector_store(documents)
            retrieval_chain = self.create_retriever_chain()
            retrieval_tool_instance = self.create_tool(name,
                                                       description,
                                                       retrieval_chain)
            tools.append(retrieval_tool_instance)

        self.agent = initialize_agent(
            tools=tools,
            llm=self.chat_model,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
        )

    # 加载历史记录，从数据库中传来的 history_array 那里读取到 history 中
    def load_history_from_array(self, history_array):
        self.history = []
        for i in range(0, len(history_array), 2):
            human_message = HumanMessage(content=history_array[i])
            ai_message = AIMessage(content=history_array[i + 1]) if i + 1 < len(history_array) else None
            self.history.append(human_message)
            if ai_message:
                self.history.append(ai_message)


    def libId2dir(self, libId):
        if libId != None:
            return "/root/shixun/lib" + str(libId)
            # return "D:/shixun/lib" + str(libId)
        else:
            return None

    # 处理第一条消息
    async def isFirst(self, skt, question, libId, history_arr, name, description):
        self.base_dir = self.libId2dir(libId)
        self.load_history_from_array(history_arr)
        self.initialize_agent_tools(name, description)

        response = self.agent.invoke({
            "input": question,
            "chat_history": self.history,
        })

        ai_message = response["output"]
        self.history.append(HumanMessage(content=question))
        self.history.append(AIMessage(content=ai_message))

        await skt.send_text(ai_message)

        print(ai_message)
        return ai_message

    # 处理后续消息
    async def notFirst(self, skt, question):
        response = self.agent.invoke({
            "input": question,
            "chat_history": self.history,
        })

        ai_message = response["output"]
        self.history.append(HumanMessage(content=question))
        self.history.append(AIMessage(content=ai_message))

        await skt.send_text(ai_message)

        print(ai_message)
        return ai_message













































