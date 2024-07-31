import os
from collections import deque
from langchain.agents import create_react_agent, AgentExecutor, AgentOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from typing import Union
import re
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from Utils.modelchoice import (
    os_setenv,
    get_zhipu_chat_model
)

class Retrieval:
    def __init__(self, embedding_model_dir: str, lib_dir: str):
        self.docs = self.load_docs(lib_dir)
        self.text_splitter()
        self.vector_store = self.init_vector_store(embedding_model_dir)
        self.retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        self.last_docs = None

    def load_docs(self, base_dir):
        txt_documents = []

        def type_list():
            return {
                'd0cf11e0a1b11ae10000': 'doc',
                '255044462d312e350d0a': 'pdf',
                '504b0304140006000800': 'docx',
            }

        def bytes2hex(bytes):
            num = len(bytes)
            hex_str = u""
            for i in range(num):
                t = u"%x" % bytes[i]
                if len(t) % 2:
                    hex_str += u"0"
                hex_str += t
            return hex_str.upper()

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

    def text_splitter(self):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
        self.docs = text_splitter.split_documents(self.docs)

    def init_vector_store(self, embedding_model_dir):
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model_dir, model_kwargs={'device': "cpu"})
        return FAISS.from_documents(documents=self.docs, embedding=embeddings)

    def get_similar_docs(self, target_text: str):
        references = self.retriever.invoke(target_text)
        self.format_references(references)
        return references

    def format_references(self, references):
        self.last_docs = "## 参考资料：\n"
        for doc in references:
            source = doc.metadata['source'].split('\\')[-1]
            content = doc.page_content.replace('\n', '\\n')
            self.last_docs += f"- {source}: {content}\n"

    def is_have_references(self):
        return self.last_docs is not None

    def get_references(self):
        ans = self.last_docs
        self.last_docs = None
        return ans


class MyAgentOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        if "AI:" in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split("AI:")[-1].strip()},
                log=llm_output,
            )

        regex = r"Action: (.*?)[\n]*Action Input: (.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if match:
            action = match.group(1).strip()
            action_input = match.group(2).strip()
            return AgentAction(tool=action, tool_input=action_input, log=llm_output)

        raise ValueError(f"Could not parse LLM output: `{llm_output}`")


class LocalSearchChat:
    def __init__(self, history: list[str], embedding_model_dir: str, lib_dir: str):
        os_setenv()
        self.chat_model = get_zhipu_chat_model()
        self.retrieval = Retrieval(embedding_model_dir, lib_dir)
        self.tools = None
        self.agent_prompt = None
        self.agent_output_parser = MyAgentOutputParser()
        self.agent = None
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.agent_executor = None

        self.load_memory(history)
        self.init_tools()
        self.init_agent_prompt()
        self.init_agent()
        self.init_agent_executor()

    def init_tools(self):
        tool = Tool(
            name='LocalSearch',
            description='Useful for when you need to answer questions about the local knowledge base.',
            func=self.retrieval.get_similar_docs
        )
        self.tools = [tool]

    def init_agent_prompt(self):
        prompt_template_str: str = '''

                  You are an intelligent question answering robot, \n
                  and when I ask a question, you can use the following tools if you think it is useful.\n

                  {tools}

                  Remember to consider the chat history when formulating your response, and refer to it if relevant to the current question.

                  Chat History:
                  {chat_history}

                  When users ask for any information, you should always prioritize using tools to get related information unless you think you really don't need them(like programming).\n
                  When you use the tool, you should carefully provide the most relevant sentence or phrase that closely matches the desired information,
                  as the accuracy of this match significantly impacts the effectiveness of the retrieval.
                  You will only adopt the information you retrieve if it is truly useful to the results.
                  To use a tool, please use the following format:\n

                  Thought: Do I need to use a tool? Yes\n
                  Action: the action to take, should be one of [{tool_names}]\n
                  Action Input: the input to the action\n
                  Observation: the result of the action\n

                  if you do not need to use a tool, you MUST use the format:\n

                  Thought: Do I need to use a tool? No\n
                  AI: [your response here]\n

                  Important: If the user questions or challenges any information from the chat history, you should thoroughly reconsider your approach. This may involve using tools again to solve the problem, even if you've used them before. Always prioritize providing the most accurate and up-to-date information.

                  Begin!

                  Question: {input}
                  {agent_scratchpad}
        '''
        self.agent_prompt = PromptTemplate.from_template(prompt_template_str)

    def init_agent(self):
        self.agent = create_react_agent(
            llm=self.chat_model,
            tools=self.tools,
            prompt=self.agent_prompt,
            output_parser=self.agent_output_parser
        )

    def load_memory(self, history: list[str]):
        for i in range(0, len(history), 2):
            if i + 1 < len(history):
                human_message = history[i]
                ai_message = history[i + 1]
                self.memory.chat_memory.add_message(HumanMessage(content=human_message))
                self.memory.chat_memory.add_message(AIMessage(content=ai_message))
            else:
                self.memory.chat_memory.add_message(HumanMessage(content=history[i]))

    def init_agent_executor(self):
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )

    async def get_answer(self, question: str):
        ai_response_started = False
        window = deque(maxlen=4)
        async for event in self.agent_executor.astream_events(
            input={'input': question},
            version="v2",
        ):
            kind = event["event"]

            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    if not ai_response_started:
                        for char in content:
                            if ai_response_started:
                                yield char
                            else:
                                window.append(char)
                                if ''.join(window) == "AI: ":
                                    ai_response_started = True
                    else:
                        yield content


        # Get references
        if self.retrieval.is_have_references():
            references = self.retrieval.get_references()
            yield references
