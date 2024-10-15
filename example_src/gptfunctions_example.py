import openai
import json
import requests

def get_receipt_by_id(receiptId):
    url = 'https://receiptparserservices20230928182301.azurewebsites.net/api/GetReceipt?name=Functions'
    myobj = {'id':receiptId}
    x = requests.post(url, json=myobj)
    x.raise_for_status()
    
    # Convert the content into a dictionary
    receipt_content = x.json()

    # Extract specific properties from receipt_content. 
    # For this example, I assume 'property_name' is a key in the returned content.
    isSuccess = receipt_content.get('isSuccess', False)  # replace 'property_name' with the actual property key
    receiptData = receipt_content.get('receipt', '')
    receipt_info = {
        "receiptId": receiptId,
        "receiptData": receiptData,  # This will store the entire content
        "isSuccess": isSuccess  # Store the extracted property value
    }
    
    return json.dumps(receipt_info)

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": "Get the receipt for 6521e0903b13393d7ccac545?"}]
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
        {
            "name": "get_receipt_by_id",
            "description": "Get a receipt by a receipt id",
            "parameters": {
                "type": "object",
                "properties": {
                    "receiptId": {
                        "type": "string",
                        "description": "The receipt id for the desired receipt",
                    }
                },
                "required": ["receiptId"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
            "get_receipt_by_id" : get_receipt_by_id
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        if(function_name == 'get_receipt_by_id'):
            function_response = function_to_call(
            receiptId=function_args.get("receiptId")
            )
        if(function_name == 'get_current_weather'):    
            function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response


#print(get_receipt_by_id('6521e0903b13393d7ccac545'))
print(run_conversation())