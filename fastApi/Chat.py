import asyncio
import os
from langchain.chains import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from modelchoice import (
    os_setenv,
    get_zhipu_chat_model
)
from nameUtil import NameUtil

class Chat:
    def __init__(self):
        # 初始化
        os_setenv()
        self.chat_model = get_zhipu_chat_model()
        self.text_splitter = RecursiveCharacterTextSplitter() # 分词
        self.history = None # 历史记录数组
        self.base_dir = None # 文件路径
        self.vector_store = None # 向量存储
        self.m3eDir = None
        self.chain = None

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
        embeddings = HuggingFaceEmbeddings(model_name=self.m3eDir, model_kwargs={'device': "cpu"})
        if documents is not None:
            chunked_documents = self.text_splitter.split_documents(documents=documents)
        else:
            chunked_documents = [Document(page_content='you should use your own ability to answer the question.')]
        self.vector_store = FAISS.from_documents(documents=chunked_documents, embedding=embeddings)

    # 创建检索链
    def create_retriever_chain(self):

        prompt = ChatPromptTemplate.from_messages([
            ("system", """
            You are an intelligent question answering robot, \n
            and when I ask a question, you will provide me with an answer by referencing chat_history.\n
            You will prioritize using tools and then use your knowledge base if information cannot be retrieved.\n
            If there are no information about the question, please answer using your own ability.\n
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


    # 加载历史记录，从数据库中传来的 history_array 那里读取到 history 中
    def load_history_from_array(self, history_array):
        self.history = []
        for i in range(0, len(history_array), 2):
            human_message = HumanMessage(content=history_array[i])
            ai_message = AIMessage(content=history_array[i + 1]) if i + 1 < len(history_array) else None
            self.history.append(human_message)
            if ai_message:
                self.history.append(ai_message)

    # 处理第一条消息
    async def isFirst(self, skt, question, libDir, history_arr, m3eDir):
        self.base_dir = libDir
        self.m3eDir = m3eDir
        self.load_history_from_array(history_arr)
        if self.base_dir is not None:
            docs = self.load_documents_from_base_dir(self.base_dir)
        else:
            docs = None
        self.initialize_vector_store(docs)
        self.chain = self.create_retriever_chain()

        i = 0
        ai_message = ''
        for chunk in self.chain.stream({
            "input": question,
            "chat_history": self.history,
            "context": ""
        }):
            i += 1
            if i > 2:
                cur_message = chunk['answer']
                await skt.send_text(cur_message)
                await asyncio.sleep(0.0001)
                ai_message += cur_message

        await skt.close()
        conversationName = None
        if len(history_arr) == 0:
            conversationName = NameUtil.summary(question, ai_message)

        self.history.append(HumanMessage(content=question))
        self.history.append(AIMessage(content=ai_message))

        return ai_message, conversationName

    # 处理后续消息
    async def notFirst(self, skt, question):
        i = 0
        ai_message = ''
        for chunk in self.chain.stream({
            "input": question,
            "chat_history": self.history,
            "context": ""
        }):
            i += 1
            if i > 2:
                cur_message = chunk['answer']
                await skt.send_text(cur_message)
                await asyncio.sleep(0.0001)
                ai_message += cur_message

        self.history.append(HumanMessage(content=question))
        self.history.append(AIMessage(content=ai_message))

        return ai_message