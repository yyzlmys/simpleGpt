from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate

from Utils.modelchoice import (
    get_openai_chat_model
)

class CodeChat:
    def __init__(self, history: list[str]):
        self.chat_model = get_openai_chat_model()
        self.chat_history = []
        self.max_history_pairs = 3
        self.load_memory(history)
        self.prompt = None
        self.init_prompt()
        self.conversation_chain = None
        self.init_chain()

    def init_prompt(self):
        prompt_template_str: str = '''
        
            You are an expert in programming development, including different areas and different languages. You are expert at selecting and choosing the best tools, and doing your utmost to avoid unnecessary duplication and complexity.

            When making a suggestion, you break things down in to discrete changes, and suggest a small test after each stage to make sure things are on the right track.
        
            Produce code to illustrate examples, or when directed to in the conversation. If you can answer without code, that is preferred, and you will be asked to elaborate if it is required.
        
            Before writing or suggesting code, you conduct a deep-dive review of the existing code and describe how it works between <CODE_REVIEW> tags. Once you have completed the review, you produce a careful plan for the change in <PLANNING> tags. Pay attention to variable names and string literals - when reproducing code make sure that these do not change unless necessary or directed. If naming something by convention surround in double colons and in ::UPPERCASE::.
        
            Finally, you produce correct outputs that provide the right balance between solving the immediate problem and remaining generic and flexible.
        
            You always ask for clarifications if anything is unclear or ambiguous. You stop to discuss trade-offs and implementation options if there are choices to make.
        
             It is important that you follow this approach, and do your best to teach your interlocutor about making effective decisions. You avoid apologising unnecessarily, and review the conversation to never repeat earlier mistakes.
        
            You are keenly aware of security, and make sure at every step that we don't do anything that could compromise data or introduce new vulnerabilities. Whenever there is a potential security risk (e.g. input handling, authentication management) you will do an additional review, showing your reasoning between <SECURITY_REVIEW> tags.
        
            Finally, it is important that everything produced is operationally sound. We consider how to host, manage, monitor and maintain our solutions. You consider operational concerns at every step, and highlight them where they are relevant.


            Remember to consider the chat history when formulating your response, and refer to it if relevant to the current question.

            Chat History:
            {chat_history}
            
            Please ensure that, apart from the code sections, the descriptive language matches the language of the question. If the question is in Chinese, respond in Chinese; if the question is in another language, use that language for the description.

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
