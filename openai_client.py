import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

class MenuItem(BaseModel):
    name: str
    description: str
    price: str

class OpenAIClient:

    _openai = None
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self._openai = OpenAI(api_key=self.api_key)
        print("OpenAIClient initialized")



# This is the function that we want the model to be able to call
    def get_order_status_tool(self, order_id: str) -> str:
        return "Your order is on the way!";
  

    def breakdown_menu_line(self, menu_line):
        print("In breakdown_menu_line")
        try:
            instructions = "Your job is to parse and breakdown menu items into the following properties: name, description, price."
            system_message = {"role": "system", "content": instructions}
            user_message = {"role": "user", "content": menu_line}
            messages = [system_message,user_message]

            completion = self._openai.beta.chat.completions.parse(
                model="gpt-4o",
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
    
    def get_order_status(self):
        print("In get_order_status")
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
                model="gpt-4o",
                messages=messages,
                tools=tools
            )

            response_msgs = self.handle_completion_with_tools(completion, messages, tools)
            return response_msgs[-1].content
        except Exception as e:
            print(e)
            pass
        return None
    

    def handle_completion_with_tools(self, completion, messages, tools):
        print("In handle_completion_with_tools")
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
                messages.append(response.choices[0].message)
                messages.append(function_call_result_message)
                requiresAction = True
            elif finish_reason == "stop":
                messages.append(response.choices[0].message)
                requiresAction = False
            else:
                requiresAction = False
                #return "Unexpected finish_reason: " + finish_reason
            
            if requiresAction:
                response = self._openai.chat.completions.create( 
                    model="gpt-4o",
                    messages=messages,
                    tools=tools
                    )
        return messages   


# Example usage:
client = OpenAIClient()
menu_line = "- Migas - Totopos, scrambled eggs, duck fat refried beans, chorizo, queso fresco, cilantro, avocado crema, salsa cruda (gf, contains dairy) $6"
menu_item = client.breakdown_menu_line(menu_line)
print(menu_item)

order_status_response = client.get_order_status()
print(order_status_response)
