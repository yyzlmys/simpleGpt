from typing import List, Dict
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate, ChatPromptTemplate
from .modelchoice import (
    get_spark_chat_model,
    get_zhipu_chat_model,
    get_openai_chat_model,
    get_tongyi_chat_model,
    get_qianfan_chat_model
)
import json

class TitleSummaryChat:
    def __init__(self, chat_model: BaseChatModel, examples_dir: str):
        self.chat_model = chat_model
        self.examples = self.get_examples_from_json(examples_dir)

    @classmethod
    def get_examples_from_json(cls, file_path: str) -> List[Dict[str, str]]:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def get_few_shot_examples(self, prompt_template_str: str) -> str:
        prompt_template_sample: PromptTemplate = PromptTemplate.from_template(
            template=prompt_template_str
        )
        self.few_shot_prompt_template = FewShotPromptTemplate(
            examples=self.examples,
            example_prompt=prompt_template_sample,
            suffix=''
        )
        return self.few_shot_prompt_template.format()


    def get_few_shot_prompt_template(self, prompt_template_str: str) -> FewShotPromptTemplate:
        prompt_template_sample: PromptTemplate = PromptTemplate.from_template(
            template=prompt_template_str
        )
        self.few_shot_prompt_template = FewShotPromptTemplate(
            examples=self.examples,
            example_prompt=prompt_template_sample,
            suffix='Question：{HumanMessage}\nAnswer：{AIMessage}\nTitle：',
            input_variables=['HumanMessage', 'AIMessage']
        )

    def get_result_by_prompt(self, human_message: str, ai_message: str) -> str:
        system_template_str = '''你是一个对话总结专家，擅长总结一轮对话的标题，并且不超过8个字。\n
        以下是几组样例：\n
        <examples> \n
        {examples} \n
        <\examples> \n
        注意：你只需要给出最终结果，不需要给出任何解释，也不要使用类似于双引号。
        '''
        system_template_prompt = SystemMessagePromptTemplate.from_template(system_template_str)

        human_template_str = '请总结下面这段对话的标题\nQuestion：{HumanMessage}\nAnswer：{AIMessage}'
        human_template_prompt = HumanMessagePromptTemplate.from_template(human_template_str)

        chat_prompt = ChatPromptTemplate.from_messages([
            system_template_prompt,
            human_template_prompt
        ])
        prompt_template_str: str = 'Question：{HumanMessage}\nAnswer：{AIMessage}\nTitle：{title}'
        chat_model_input = chat_prompt.format_prompt(
            examples=self.get_few_shot_examples(prompt_template_str),
            HumanMessage=human_message,
            AIMessage=ai_message
        )

        return self.chat_model.invoke(chat_model_input).content



class NameUtil:
    @classmethod
    def summary(cls, message1, message2):
        title_summary_chat = TitleSummaryChat(get_zhipu_chat_model(), '/root/fastApi/Utils/examples.json')
        return title_summary_chat.get_result_by_prompt(message1, message2)







