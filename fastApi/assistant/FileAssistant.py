from langchain_core.documents import Document
from .TextReader import TextReader
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

class FileAssistant:
    def __init__(self):
        self.docs = None

    async def init_docs(self, file_path: str):
        self.docs = await self.load_doc(file_path)

    @classmethod
    async def load_doc(cls, file_path: str) -> list[Document]:
        def type_list():
            return {
                'd0cf11e0a1b11ae10000': 'doc',
                '255044462d312e350d0a': 'pdf',
                '504b0304140006000800': 'docx',
            }

        def bytes2hex(bytes):
            return bytes.hex().upper()

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

        file_type = filetype(file_path)

        if file_type == 'pdf':
            loader = PyPDFLoader(file_path)
        elif file_type == 'docx':
            loader = Docx2txtLoader(file_path)
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        return loader.load()

    def is_have_docs(self):
        return self.docs is not None

    def get_answer(self, question: str) -> str:
        reader = TextReader()
        ans = reader.get_answer(question, self.docs)
        return ans



