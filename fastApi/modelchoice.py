import os
# 各种 系统环境变量的 各种设置
def os_setenv():
    # 设置各种 LLM 的 Aks&Sks

    # OpenAI
    os.environ["OPENAI_API_KEY"] ="sk-l6lQirAI1ch1NCouM1DGFY3UA61hl6k3kbdM374UgM9XNaXm"
    os.environ["OPENAI_API_BASE"] ="https://api.chatanywhere.tech/v1"

    # Baidu Wenxin/Qianfan
    os.environ["QIANFAN_AK"] = "h5oW9XOwRIJLobarMw7YN3tV"
    os.environ["QIANFAN_SK"] = "lduvpmV7X1hAOc3tGIiYzIa0w2k0ShAq"

    # Sparkllm
    os.environ["IFLYTEK_SPARK_APP_ID"] = "aa338022"
    os.environ["IFLYTEK_SPARK_API_KEY"] = "01a991ecfec4587c6a6289f11edc73ed"
    os.environ["IFLYTEK_SPARK_API_SECRET"] = "ZmYwMmM2Y2Y2NDY4YjZkMzJlYzEyMjYy"
    os.environ["IFLYTEK_SPARK_API_URL"] = "wss://spark-api.xf-yun.com/v3.1/chat"
    os.environ["IFLYTEK_SPARK_llm_DOMAIN"] = "generalv3"

    # Zhipuai
    os.environ["ZHIPUAI_API_KEY"] = "ed6fbd504f7c288c2184de79f8fe5d34.RhC4WOlJt8MocUbk"

    # TongyiQwen
    os.environ["DASHSCOPE_API_KEY"] = 'sk-964cdc16522b4899b6943eb9d4be8c21'

    pass


def get_openai_chat_model():
    from langchain_openai import ChatOpenAI
    # langchain API https://python.langchain.com/v0.2/docs/integrations/chat/openai/
    chat_model_openai = ChatOpenAI(
        # openai API https://platform.openai.com/docs/models
        # model="gpt-4o",
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    return chat_model_openai

def get_qianfan_chat_model():
    # 导包，baidu qianfan
    from langchain_community.chat_models import QianfanChatEndpoint
    # 生成 baiduqianfan chat_model
    chat_model_qianfan = QianfanChatEndpoint(
        temperature=0.8,
        model="ernie-bot-turbo",
        verbose=True,
    )
    return chat_model_qianfan

def get_spark_chat_model():
    from langchain_community.chat_models import ChatSparkLLM
    chat_model_spark = ChatSparkLLM(
        temperature=0.8,
    )
    return chat_model_spark


def get_zhipu_chat_model():
    from langchain_community.chat_models import ChatZhipuAI
    chat_model_zhipuai = ChatZhipuAI(
        model="glm-4",
        temperature=0.8,
    )
    return chat_model_zhipuai

def get_tongyiqwen_chat_model():
    from langchain_community.chat_models.tongyi import ChatTongyi
    chat_model_tongyiqwen = ChatTongyi(
        temperature=0.8,
    )
    return chat_model_tongyiqwen


