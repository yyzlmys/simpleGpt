import asyncio
import aiohttp
from langchain_core.documents import Document
from .TextReader import TextReader
from langchain_community.document_loaders import WebBaseLoader

class WebPageAssistant:
    def __init__(self):
        self.docs = None

    async def init_docs(self, url: str):
        self.docs = await self.load_docs(url)

    @classmethod
    async def load_docs(cls, url: str) -> list[Document]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(url, timeout=10) as response:
                    response.raise_for_status()

                loader = WebBaseLoader(web_path=url)
                docs = await asyncio.to_thread(loader.load)
                return docs

        except Exception as e:
            print(f"Error loading docs: {e}")
            return None

    def is_have_docs(self):
        return self.docs is not None

    def get_answer(self, question: str) -> str:
        reader = TextReader()
        ans = reader.get_answer(question, self.docs)
        return ans