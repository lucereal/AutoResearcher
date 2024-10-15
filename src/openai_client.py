import json
import os
from openai import OpenAI
import openai
from dotenv import load_dotenv 
from pydantic import BaseModel
from typing import List

# Load environment variables from .env file
load_dotenv()

class IsWebPageUsable(BaseModel):
    isUsable: bool

class MenuItem(BaseModel):
    name: str
    description: str
    price: str

class QueryListResult(BaseModel):
    queryList: List[str]
    
    def print_query_list(self):
        print("Query List:")
        for index, query in enumerate(self.queryList, start=1):
            print(f"{index}. {query}")

class OpenAIClient:
    _openai_model = None
    _openai = None
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self._openai = OpenAI(api_key=self.api_key)
        self._openai_model = "gpt-4o-mini"
  

    def breakdown_menu_line(self, menu_line):
        try:
            instructions = "Your job is to parse and breakdown menu items into the following properties: name, description, price."
            system_message = {"role": "system", "content": instructions}
            user_message = {"role": "user", "content": menu_line}
            messages = [system_message,user_message]

            completion = self._openai.beta.chat.completions.parse(
                model=self._openai_model,
                messages=messages,
                response_format=MenuItem
            )

            response_msg = completion.choices[0].message
            if response_msg.parsed:
                return response_msg.parsed
            elif response_msg.refusal:
                # handle refusal
                print("structured response not possible")
                return response_msg.refusal
        except Exception as e:
            print(e)
            pass
        return None

    def create_queries_on_topic(self, topic_query):
        try:
            system_instructions = """You are a research assistant. Your task is to take a user-provided topic and create 
            related queries and questions that can be used to search for relevant media and data. The queries should be 
            detailed and aimed at gathering high-quality insights that would be useful for business professionals."""

            user_query = f"""
            Given the topic "{topic_query}", generate a list of questions or search queries to gather relevant, high-quality data and insights. 
            The questions should aim to clarify the topic and identify key aspects such as:
            1. Recent trends,
            2. Key figures or companies,
            3. Statistics,
            4. Challenges, 
            5. Expert opinions.

            Additional Requirements:
            - The month and year is October 2024, so focus on recent information.
            - Break the topic into smaller subtopics if necessary.
            - The questions should cover a mix of data types such as statistics, case studies, expert opinions, news articles, and industry reports.
            - Prioritize queries related to recent developments and practical insights.
            - Ensure the questions are suitable for business professionals.

            Example: 
            If the topic is 'AI in healthcare', generate questions such as:
            - 'What are the most recent developments in AI-assisted surgeries?'
            - 'What challenges are healthcare providers facing with AI adoption?' 
            - 'Which companies are leading the development of AI solutions in healthcare?'
            """
            system_message = {"role": "system", "content": system_instructions}
            user_message = {"role": "user", "content": user_query}
            messages = [system_message,user_message]

            completion = self._openai.beta.chat.completions.parse(
                model=self._openai_model,
                messages=messages,
                response_format=QueryListResult
            )

            response_msg = completion.choices[0].message
            if response_msg.parsed:
                return response_msg.parsed.queryList
            elif response_msg.refusal:
                # handle refusal
                print("structured response not possible")
                return response_msg.refusal
        except Exception as e:
            print(e)
            pass
        return None


    def summarize_web_page_data(self, web_page_data, topic_query):
        try:
            system_instructions = f"""You are a research assistant. 
            You are tasked with summarizing a web page based on a specific topic provided by the user. The web page contains both text and table data. 
            The goal is to provide a concise, insightful summary of the web page with a strong focus on the latest developments related to the given topic. 
            The summary should be informative, highlighting key points, emerging trends, and relevant data that will keep the reader up-to-date with recent changes and updates on the topic. 
            Keep the summary focused and relevant to the user's needs.

            Instructions:

            1. Topic: {topic_query}
            2. Review the web page data carefully, including any text and table data.
            3. Focus on summarizing the most recent developments, key trends, and any data points that directly relate to the topic.
            4. Ensure the summary is clear, concise, and relevant for a weekly update, highlighting important changes or trends.
            5. Use a professional tone, suitable for clients who are keeping up with industry developments.
            6. If the page contains redundant information or general context not directly relevant to the topic, omit it and focus on actionable insights and updates.
                        
            """

            user_query = f"""
            Here is the information you need to summarize:\n\n
            **Topic**: [{topic_query}]\n\n
            **Web Page Data**: [{web_page_data}]\n\n
            Please provide a summary focused on the most recent developments and key insights related to the topic."
            """
            system_message = {"role": "system", "content": system_instructions}
            user_message = {"role": "user", "content": user_query}
            messages = [system_message,user_message]

            completion = self._openai.chat.completions.create(
                model=self._openai_model,
                messages=messages
            )


            if completion.choices[0].finish_reason == "stop":
                response_msg = completion.choices[0].message.content
                return response_msg
            else:
                # handle refusal
                print("finish reason not stop")
                return None
        except Exception as e:
            print(e)
            pass
        return None

    def is_web_page_data_usable(self, web_page_data, topic_query):
        try:
            system_instructions = f"""You are a research assistant. 
            You are an assistant that evaluates web page data to determine if it is usable for generating a summary related to a specific topic. 
            Your job is to check if there is relevant and sufficient data available to create a meaningful summary that will bring value to the client.        
            """

            user_query = f"""
            Please evaluate the following data based on the given topic:\n\n
            **Topic**: [{topic_query}]\n\n
            **Web Page Data**: [{web_page_data}]\n\n
            Assess if:\n
            1. The web page contains usable data.\n
            2. The data is related to the topic provided.\n
            3. There is enough relevant data to create a summary that brings value to a client interested in this topic.\n\n
            Provide a brief evaluation based on these criteria.
            """
            system_message = {"role": "system", "content": system_instructions}
            user_message = {"role": "user", "content": user_query}
            messages = [system_message,user_message]

            completion = self._openai.beta.chat.completions.parse(
                model=self._openai_model,
                messages=messages,
                response_format=IsWebPageUsable
            )

            if completion.choices[0].finish_reason == "stop":
                if completion.choices[0].message.parsed:
                    return completion.choices[0].message.parsed.isUsable
                else:
                    return None
            else:
                # handle refusal
                print("finish reason not stop")
                return None
        except Exception as e:
            print(e)
            pass
        return None
    
    def get_order_status_tool(self, order_id: str) -> str:
        return "Your order is on the way!";

    def get_order_status(self):
        try:
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_order_status_tool",
                        "description": "Get the status for a customer's order. Call this whenever you need to know the order status, for example when a customer asks 'What is my order status?'",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "order_id": {
                                    "type": "string",
                                    "description": "The customer's order ID.",
                                },
                            },
                            "required": ["order_id"],
                            "additionalProperties": False,
                        }, "strict" : True
                    }
                }
            ]

            instructions = "You are a helpful assistant!"
            system_message = {"role": "system", "content": instructions}
            
            user_message = {"role": "user", "content": "What is my order status? order id = 1234"}
            messages = [system_message,user_message]

            completion = self._openai.chat.completions.create(
                model=self._openai_model,
                messages=messages,
                tools=tools
            )

            response_msgs = self.handle_completion_with_tools(completion, messages, tools)
            return response_msgs
        except Exception as e:
            print(e)
            pass
        return None
    

    def handle_completion_with_tools(self, completion, messages, tools):
        response = completion
        requiresAction = True
        while requiresAction:
            requiresAction = False
            finish_reason = response.choices[0].finish_reason
            if finish_reason == "length":
                requiresAction = False
                #return "The conversation was too long for the context window."
            elif finish_reason == "content_filter":
                requiresAction = False
                #return "The content was filtered due to policy violations."
            elif finish_reason == "tool_calls":
                tool_call = response.choices[0].message.tool_calls[0]
                arguments = json.loads(tool_call.function.arguments)
                order_id = arguments.get('order_id')
                order_status = self.get_order_status_tool(order_id)
                function_call_result_message = {
                    "role": "tool",
                    "content": json.dumps({
                        "order_id": order_id,
                        "order_status": order_status
                    }),
                    "tool_call_id": tool_call.id
                }
                assistant_message = response.choices[0].message
                messages.append(assistant_message)
                messages.append(function_call_result_message)
                requiresAction = True
            elif finish_reason == "stop":
                assistant_message = response.choices[0].message
                messages.append(assistant_message)
                requiresAction = False
            else:
                requiresAction = False
                #return "Unexpected finish_reason: " + finish_reason
            
            if requiresAction:
                response = self._openai.chat.completions.create( 
                    model=self._openai_model,
                    messages=messages,
                    tools=tools
                    )
        return messages   
    
    def print_conversion(self, response_msgs):
        for msg in response_msgs:
            if isinstance(msg, dict):
                if msg.get('role') and msg.get('content'):
                    print(f"{msg['role']}: {msg['content']}")
            elif type(msg).__name__ == "ChatCompletionMessage":
                if msg.role and msg.content:
                    print(f"{msg.role}: {msg.content}")
        return None

if __name__ == "__main__":
    # Example usage:
    client = OpenAIClient()


    with open("results.json", "r") as json_file:
            data = json.load(json_file)
            
    topic = "cryptocurrency trading"

    for query_sources in data["sources_data"]:
            print("Summarizing sources for query: " + query_sources["query"])
            for item in query_sources["sources_data"]:
                web_page_data = item["source_data"]
                # print("\tchecking if " + item["link"] + " is usable")
                # Call the is_web_page_data_usable function
                is_usable = client.is_web_page_data_usable(web_page_data, topic)
                print("\t" + item["link"] + " is usable: " + str(is_usable))
                if is_usable:
                    # Call the summarize_web_page_data function
                    summary = client.summarize_web_page_data(web_page_data, topic)
                    print("summary:")
                    print(summary[:200]+"...")



    # user_topic = "Physics of black holes"
    # query_list_response = client.create_queries_on_topic(user_topic)
    # query_list_response.print_query_list()

    # menu_line = "- Migas - Totopos, scrambled eggs, duck fat refried beans, chorizo, queso fresco, cilantro, avocado crema, salsa cruda (gf, contains dairy) $6"
    # menu_item = client.breakdown_menu_line(menu_line)
    # print(menu_item)

    # order_status_response = client.get_order_status()
    # print(client.print_conversion(order_status_response))
