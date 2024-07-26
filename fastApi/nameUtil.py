from typing import List, Dict
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from modelchoice import (
    os_setenv,
    get_spark_chat_model,
    get_zhipu_chat_model,
    get_openai_chat_model,
    get_qianfan_chat_model
)
import json

class TitleSummaryChat:
    def __init__(self, chat_model: BaseChatModel, examples_dir: str):
        os_setenv()
        self.chat_model = chat_model
        self.examples = self.get_examples_from_json(examples_dir)

    @classmethod
    def get_examples_from_json(cls, file_path: str) -> List[Dict[str, str]]:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def get_few_shot_prompt_template(self, prompt_template_str: str) -> FewShotPromptTemplate:
        prompt_template_sample: PromptTemplate = PromptTemplate.from_template(
            template=prompt_template_str
        )
        self.few_shot_prompt_template = FewShotPromptTemplate(
            examples=self.examples,
            example_prompt=prompt_template_sample,
            suffix='HumanMessage：{HumanMessage}\nAIMessage：{AIMessage}\nTitle：',
            input_variables=['HumanMessage', 'AIMessage']
        )

    def get_result(self, human_message: str, ai_message: str) -> str:
        chat_model_input = self.few_shot_prompt_template.format(
            HumanMessage=human_message,
            AIMessage=ai_message
        )
        return self.chat_model.invoke(chat_model_input).content


class NameUtil:
    @classmethod
    def summary(cls, message1, message2):
        prompt_template_str: str = 'HumanMessage：{HumanMessage}\nAIMessage：{AIMessage}\nTitle：{title}'
        title_summary_chat = TitleSummaryChat(get_zhipu_chat_model(), '/root/fastApi/examples.json')
        title_summary_chat.get_few_shot_prompt_template(prompt_template_str)
        return title_summary_chat.get_result(message1, message2)







