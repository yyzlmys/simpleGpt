from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import TokenTextSplitter
from Util.modelchoise import (
    get_openai_chat_model,
    get_zhipu_chat_model
)
class TextReader:
    """
    This class can process super long information, but it is also spend many tokens.
    """
    def __init__(self):
        self.chat_model = get_zhipu_chat_model(temperature=0)
        self.summarize_chain = None
        self.init_summarize_chain()
        self.cleanup_chain = None
        self.init_cleanup_chain()

    def splitter_docs(self, docs: list[Document], token_limit=3000) -> list[Document]:
        text_splitter = TokenTextSplitter(chunk_size=token_limit, chunk_overlap=100)
        combined_text = " ".join([doc.page_content for doc in docs])
        combined_doc = Document(page_content=combined_text)
        return text_splitter.split_documents([combined_doc])

    def init_summarize_chain(self):
        prompt_template = """You are a intelligent assistant.
        I will give you the following context and question, you MUST answer the question according to the context.
        Question: {question}
        <context>
        {text}
        </context>
        """
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["question", "text"]
        )

        refine_template = (
            "You are a intelligent assistant."
            "I will give you a question, your job is to produce a final answer\n"
            "Question: {question}"
            "We have provided an existing answer up to a certain point: {existing_answer}\n"
            "We have the opportunity to refine the existing answer"
            "(only if needed) with some more context below.\n"
            "------------\n"
            "{text}\n"
            "------------\n"
            "Given the new context, refine the original answer"
            "If the context isn't useful, return the original answer."
        )
        refine_prompt = PromptTemplate(
            template=refine_template,
            input_variables=["question", "existing_answer", "text"]
        )
        self.summarize_chain = load_summarize_chain(
            llm=self.chat_model,
            chain_type="refine",
            question_prompt=prompt,
            refine_prompt=refine_prompt,
            return_intermediate_steps=True,
            input_key="input_documents",
            output_key="output_text",
        )

    def init_cleanup_chain(self):
        cleanup_template = """
        你的任务是清理和优化以下文本，去除所有与回答问题无关的内容，如处理过程的描述或元信息。
        只保留与问题"{question}"直接相关的信息，并以简洁、清晰的方式呈现。

        原文本：
        {text}

        清理后的文本：
        """
        cleanup_prompt = PromptTemplate(template=cleanup_template, input_variables=["question", "text"])
        self.cleanup_chain = cleanup_prompt | self.chat_model

    def get_answer(self, question: str, docs: list[Document]) -> str:
        docs = self.splitter_docs(docs=docs, token_limit=100000)
        result = self.summarize_chain.invoke({"input_documents": docs, "question": question})
        ans = result['output_text']
        result = self.cleanup_chain.invoke({"question": question, 'text': ans})
        ans = result.content
        return ans
