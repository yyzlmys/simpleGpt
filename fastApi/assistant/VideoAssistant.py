from langchain_community.document_loaders import BiliBiliLoader, YoutubeLoader
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api import NoTranscriptFound, YouTubeTranscriptApi

from Util.modelchoise import (
    get_openai_chat_model,
    get_zhipu_chat_model
)

class VideoAssistant:
    """
    This class can process the video information, which is actually to extract video subtitles as context for the llm.
    Important: Because the window token limit, this class can't use the free 'gpt-4o-mini'(only have 4K), we recommend to use zhipuai(have 128K).
    """
    def __init__(self, history: list[str]):
        self.chat_model = get_zhipu_chat_model()
        self.chat_history = []
        self.max_history_pairs = 5
        self.load_memory(history)
        self.prompt = None
        self.init_prompt()
        self.conversation_chain = None
        self.init_chain()
        self.subtitle = None

    def init_prompt(self):
        prompt_template_str: str = '''
        
        You are an intelligent question answering robot, \n
        and when I ask a question, you should think it step by step and answer my question.\n
    
        Important: you should answer the question according the following subtitle information, which is from a video.
        <subtitle>
        {subtitle}
        </subtitle>
    
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

    def init_bilibili_video(self, video_url: str):
        SESSDATA = "0f00c213%2C1738140166%2C91131%2A82CjB8XCHcEOkK8gP1OeojgdJJGbhI-MipkVOoKvKSAiMXSpUbJZkSSnysQ4V6QsBRI6wSVlJzX0pxLUZieHhwQlNNNmdlZ1QyRndqSFNaTUFBZGZaRTI2MWhGMkNlaHlrZE90UmxWaTY2d2ZxWm9nVXZSX1RocnZDdS1yU0hFd1R1MldCUUpteVpnIIEC"
        BUVID3 = "E560893E-C386-0454-4C9A-82221C7175CA65691infoc"
        BILI_JCT = "1efb137e133084406ea4e6c1c6d49320"
        try:
            loader = BiliBiliLoader(
                [
                    video_url,
                ],
                sessdata=SESSDATA,
                bili_jct=BILI_JCT,
                buvid3=BUVID3,
            )
            docs = loader.load()
            if not docs[0].page_content == '':
                self.subtitle = docs[0].page_content
        except Exception as e:
            self.subtitle = None

    def init_youtube_video(self, video_url: str):
        try:
            # 首先尝试获取英文字幕
            loader = YoutubeLoader.from_youtube_url(
                video_url,
                add_video_info=True,
                language=["en"]
            )
            docs = loader.load()
        except NoTranscriptFound:
            try:
                # 如果没有英文字幕，尝试获取中文字幕
                loader = YoutubeLoader.from_youtube_url(
                    video_url,
                    add_video_info=True,
                    language=["zh-Hans"]
                )
                docs = loader.load()
            except NoTranscriptFound:
                # 如果中文字幕也没有，尝试获取任何可用的字幕
                video_id = video_url.split("v=")[1]
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                first_available_transcript = next(iter(transcript_list))
                transcript = first_available_transcript.fetch()

                # 将字幕转换为文本
                subtitle_text = " ".join([entry['text'] for entry in transcript])

                # 创建一个包含字幕的文档
                docs = [Document(page_content=subtitle_text, metadata={"source": video_url})]

        if docs and docs[0].page_content:
            self.subtitle = docs[0].page_content

    def is_have_data(self):
        return self.subtitle is not None

    async def get_answer(self, question: str):
        response: str = ''
        async for chunk in self.conversation_chain.astream(
                input={
                    'input': question,
                    'chat_history': self.chat_history,
                    'subtitle': self.subtitle
                }
        ):
            yield chunk.content
            response += chunk.content
        self.add_to_chat_history(question, response)
