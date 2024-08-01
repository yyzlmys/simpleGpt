from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate

from Utils.modelchoice import (
    get_zhipu_chat_model
)

class TemplateChat:
    def __init__(self, history: list[str], system_prompt: str, max_history_pairs = 5):
        self.chat_model = get_zhipu_chat_model()
        self.chat_history = []
        self.max_history_pairs = max_history_pairs
        self.load_memory(history)
        self.prompt = None
        self.init_prompt(system_prompt)
        self.conversation_chain = None
        self.init_chain()

    def init_prompt(self, system_prompt: str):
        prompt_template_str: str = system_prompt
        prompt_template_str += '''
        
            Every time you answer, carefully consider the above requirements and make sure you meet the above requirements before answering.
            Remember to consider the chat history when formulating your response, and refer to it if relevant to the current question.

            Chat History:
            {chat_history}
            
            Please ensure that, the language of your answer should match the language of the question. If the question is in Chinese, respond in Chinese; if the question is in another language, use that language for the description.
            
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
                self.add_to_chat_history(human_message, ai_message)
            else:
                self.add_to_chat_history(history[i], None)

    def add_to_chat_history(self, human_message: str, ai_message: str | None):
        self.chat_history.append(HumanMessage(content=human_message))
        if ai_message:
            self.chat_history.append(AIMessage(content=ai_message))

        while len(self.chat_history) > self.max_history_pairs * 2:
            self.chat_history.pop(0)
            if len(self.chat_history) > 0:
                self.chat_history.pop(0)

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
        self.add_to_chat_history(question, response)
