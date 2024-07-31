from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from Utils.modelchoice import (
    os_setenv,
    get_zhipu_chat_model,
)

class DefaultChat:
    def __init__(self, history: list[str]):
        os_setenv()
        self.chat_model = get_zhipu_chat_model()
        self.chat_history = []
        self.load_memory(history)
        self.prompt = None
        self.init_prompt()
        self.conversation_chain = None
        self.init_chain()

    def init_prompt(self):
        prompt_template_str: str = '''

              You are an intelligent question answering robot, \n
              and when I ask a question, you should think it step by step and answer my question.\n

              Remember to consider the chat history when formulating your response, and refer to it if relevant to the current question.

              Chat History:
              {chat_history}
              
              Question:{input}

            '''
        self.prompt = PromptTemplate.from_template(prompt_template_str)

    def init_chain(self):
        self.conversation_chain = self.prompt | self.chat_model

    def load_memory(self, history: list[str]):
        for i in range(0, len(history), 2):
            if i + 1 < len(history):
                human_message = history[i]
                ai_message = history[i + 1]
                self.chat_history.append(HumanMessage(content=human_message))
                self.chat_history.append(AIMessage(content=ai_message))
            else:
                self.chat_history.append(HumanMessage(content=history[i]))

    async def get_answer(self, question: str):
        response: str = ''
        async for chunk in self.conversation_chain.astream(
            input={
                'input': question,
                'chat_history': self.chat_history
            }
        ):
            yield chunk.content
            response += chunk.content
        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=response))
