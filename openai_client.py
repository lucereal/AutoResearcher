import os
import openai
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

class MenuItem(BaseModel):
    name: str
    description: str
    price: str

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

# This is the function that we want the model to be able to call
    def get_order_status(order_id: str) -> str:
        return "Your order is on the way!";
  

    def breakdown_menu_line(self, menu_line):
        try:

            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_order_status",
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
                        },
                    }
                }
            ]

            instructions = "Your job is to parse and breakdown menu items into the following properties: name, description, price."
            system_message = {"role": "system", "content": instructions}
            user_message = {"role": "user", "content": menu_line}
            messages = [system_message,user_message]

            completion = openai.beta.chat.completions.parse(
                model="gpt-4o",
                messages=messages,
                response_format=MenuItem,
                tools=tools
            )

            response_msg = completion.choices[0].message
            if response_msg.parsed:
                return response_msg.parsed
            elif response_msg.refusal:
                # handle refusal
                print("structured response not possible")
                return response_msg.refusal
        except Exception as e:
            # Handle edge cases
            if type(e) == openai.LengthFinishReasonError:
                # Retry with a higher max tokens
                print("Too many tokens: ", e)
                pass
            else:
                # Handle other exceptions
                print(e)
                pass
        return None
    
    def get_order_status(self, menu_line):
        try:

            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_order_status",
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
                        },
                    }
                }
            ]

            instructions = "You are a helpful assistant!"
            system_message = {"role": "system", "content": instructions}
            
            user_message = {"role": "user", "content": "What is my order status?"}
            messages = [system_message,user_message]

            completion = openai.beta.chat.completions.parse(
                model="gpt-4o",
                messages=messages,
                response_format=MenuItem,
                tools=tools
            )

            # if(completion)
            # # Extract the arguments for get_delivery_date
            # # Note this code assumes we have already determined that the model generated a function call. See below for a more production ready example that shows how to check if the model generated a function call
            # tool_call = response.choices[0].message.tool_calls[0]
            # arguments = json.loads(tool_call['function']['arguments'])
            response_msg = completion.choices[0].message
            if response_msg.parsed:
                return response_msg.parsed
            elif response_msg.refusal:
                # handle refusal
                print("structured response not possible")
                return response_msg.refusal
        except Exception as e:
            # Handle edge cases
            if type(e) == openai.LengthFinishReasonError:
                # Retry with a higher max tokens
                print("Too many tokens: ", e)
                pass
            else:
                # Handle other exceptions
                print(e)
                pass
        return None

# Example usage:
client = OpenAIClient()
menu_line = "- Migas - Totopos, scrambled eggs, duck fat refried beans, chorizo, queso fresco, cilantro, avocado crema, salsa cruda (gf, contains dairy) $6"
menu_item = client.breakdown_menu_line(menu_line)
print(menu_item)