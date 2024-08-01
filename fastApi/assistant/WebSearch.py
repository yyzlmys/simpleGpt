from collections import deque
from langchain.agents import create_react_agent, AgentExecutor, AgentOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from typing import Union
import re
from Utils.modelchoice import (
    get_zhipu_chat_model,
)

class SearchWithReferences:
    def __init__(self):
        self.search = GoogleSerperAPIWrapper(k=3)
        self.last_results = []

    def search_with_refs(self, query: str) -> str:
        results = self.search.results(query)
        self.last_results = results.get('organic', [])
        # pprint(results)
        if 'answerBox' in results:
            return results['answerBox']['answer']

            # 如果没有 answerBox，则回退到使用 organic 结果
        if 'organic' in results:
            snippets = [result['snippet'] for result in results['organic']]
            return ' '.join(snippets)

        return 'No good search result found'

    def get_format_references(self) -> str:
        references = [{'title': item['title'], 'link': item['link']} for item in self.last_results[:3]]
        if not references:
            return ""
        formatted_refs = "\n## 参考资料：\n"
        for i, ref in enumerate(references, 1):
            formatted_refs += f"- [{ref['title']}]({ref['link']})  \n"
        self.last_results = []
        return formatted_refs


class MyAgentOutputParser(AgentOutputParser):
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        if "AI:" in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split("AI:")[-1].strip()},
                log=llm_output,
            )

        regex = r"Action: (.*?)[\n]*Action Input: (.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if match:
            action = match.group(1).strip()
            action_input = match.group(2).strip()
            return AgentAction(tool=action, tool_input=action_input, log=llm_output)

        raise ValueError(f"Could not parse LLM output: `{llm_output}`")


class WebSearchChat:
    def __init__(self, history: list[str]):
        self.chat_model = get_zhipu_chat_model()
        self.search_with_references = SearchWithReferences()
        self.tools = None
        self.agent_prompt = None
        self.agent_output_parser = MyAgentOutputParser()
        self.agent = None
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.agent_executor = None

        self.load_memory(history)
        self.init_tools()
        self.init_agent_prompt()
        self.init_agent()
        self.init_agent_executor()

    def init_tools(self):
        tool = Tool(
            name='WebSearch',
            description='Useful for when you need to answer questions about current events or current time. '
                        'You should ask targeted questions',
            func=self.search_with_references.search_with_refs
        )
        self.tools = [tool]

    def init_agent_prompt(self):
        prompt_template_str: str = '''

                  You are an intelligent question answering robot, \n
                  and when I ask a question, you can use the following tools if you think it is useful.\n

                  {tools}

                  Remember to consider the chat history when formulating your response, and refer to it if relevant to the current question.

                  Chat History:
                  {chat_history}

                  You should always use the tool if you think it is necessary.\n
                  To use a tool, please use the following format:\n

                  Thought: Do I need to use a tool? Yes\n
                  Action: the action to take, should be one of [{tool_names}]\n
                  Action Input: the input to the action\n
                  Observation: the result of the action\n

                  if you do not need to use a tool, you MUST use the format:\n

                  Thought: Do I need to use a tool? No\n
                  AI: [your response here]\n

                  Important: If the user questions or challenges any information from the chat history, you should thoroughly reconsider your approach. This may involve using tools again to solve the problem, even if you've used them before. Always prioritize providing the most accurate and up-to-date information.

                  Begin!

                  Question: {input}
                  {agent_scratchpad}

        '''
        self.agent_prompt = PromptTemplate.from_template(prompt_template_str)

    def init_agent(self):
        self.agent = create_react_agent(
            llm=self.chat_model,
            tools=self.tools,
            prompt=self.agent_prompt,
            output_parser=self.agent_output_parser
        )

    def load_memory(self, history: list[str]):
        for i in range(0, len(history), 2):
            if i + 1 < len(history):
                human_message = history[i]
                ai_message = history[i + 1]
                self.memory.chat_memory.add_message(HumanMessage(content=human_message))
                self.memory.chat_memory.add_message(AIMessage(content=ai_message))
            else:
                self.memory.chat_memory.add_message(HumanMessage(content=history[i]))

    def init_agent_executor(self):
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=False,
            max_iterations=5,
            handle_parsing_errors=True
        )

    async def get_answer(self, question: str):
        ai_response_started = False
        window = deque(maxlen=4)
        async for event in self.agent_executor.astream_events(
            input={'input': question},
            version="v2",
        ):
            kind = event["event"]

            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    if not ai_response_started:
                        for char in content:
                            if ai_response_started:
                                yield char
                            else:
                                window.append(char)
                                if ''.join(window) == "AI: ":
                                    ai_response_started = True
                    else:
                        yield content


        # Get references
        references = self.search_with_references.get_format_references()
        yield references



