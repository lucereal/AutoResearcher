import asyncio
import json
import os
from openai import AsyncOpenAI
from openai import OpenAI
from dotenv import load_dotenv 
from pydantic import BaseModel
from typing import List


# Load environment variables from .env file
load_dotenv()

class IsWebPageUsable(BaseModel):
    isUsable: bool

class IsNewsPreviewUsable(BaseModel):
    isUsable: bool

class QueryListResult(BaseModel):
    queryList: List[str]
    
    def print_query_list(self):
        print("Query List:")
        for index, query in enumerate(self.queryList, start=1):
            print(f"{index}. {query}")

class OpenAIClient:
    _openai_model = None
    _openai_model_mini = None
    _openai = None
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self._openai = AsyncOpenAI(api_key=self.api_key)
        self._openai_model = "gpt-4o"
        self._openai_model_mini = "gpt-4o-mini"
        self._openai_model_dalle3 = "dall-e-3"
  

    async def is_news_article_preview_usable(self, article_preview, topic_query):
        title = article_preview["title"]
        description = article_preview["description"]
        content_preview = article_preview["rawContent"]
        try:
            system_instructions = f"""You are a research assistant. 
            Your task is to evaluate whether a news article preview is usable for generating a summary related to a specific topic.
            You should tell me if the article preview contains relevant and sufficient data to create a meaningful summary that will bring value to the client.
            Your evaluation will focus on the relevance and value of the content based on the provided topic."""

            user_query = f"""
            Please evaluate the following news article preview based on the given topic:

            **Topic**: [{topic_query}]

            **Article Preview**: 
            - **Title**: [{title}]
            - **Description**: [{description}]
            - **First 200 characters of content**: [{content_preview}]

            Assess if:
            1. The article preview is related to the topic provided.
            2. The content is relevant and sufficient to create a summary that will bring value to a client interested in this topic.
            3. The preview suggests the article has enough depth to be worth exploring further.

            Provide a brief evaluation based on these criteria.
            """
            system_message = {"role": "system", "content": system_instructions}
            user_message = {"role": "user", "content": user_query}
            messages = [system_message,user_message]

            completion = await self._openai.beta.chat.completions.parse(
                model=self._openai_model_mini,
                messages=messages,
                response_format=IsNewsPreviewUsable
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
            
    async def create_phrases_on_topic(self, topic_query):
        try:
            system_instructions = """You are a research assistant. Your task is to take a user-provided topic and create 
                related search phrases that can be used to gather relevant, high-quality media and data. The phrases should be very concise (2 words or less), 
                specific, and useful for gathering insights relevant to business professionals."""

            user_query = f"""
            Given the topic "{topic_query}", generate a list of concise search phrases (2 words or less) for gathering relevant, high-quality data and insights. These phrases should focus on:

            1. Recent trends and developments (preferably from the past year),
            2. Key figures or companies involved,
            3. Statistics, facts, and challenges,
            4. Expert opinions, case studies, and emerging issues.

            Additional Requirements:
            - Avoid using dates or time-specific terms in the phrases.
            - Keep the phrases concise and actionable, no more than 2 words.
            - If the topic is broad, break it down into 3-5 relevant subtopics.
            - Ensure the phrases are industry-specific and suitable for business professionals.
            - Prioritize phrases related to recent developments and practical insights, without including dates or vague terms.
            - The phrases should cover a mix of data types such as statistics, expert opinions, news articles, and industry reports.

            Example: 
            If the topic is 'AI in healthcare', generate search phrases such as:
            - 'AI surgery'
            - 'AI diagnostics'
            - 'AI pharma'
            """
            system_message = {"role": "system", "content": system_instructions}
            user_message = {"role": "user", "content": user_query}
            messages = [system_message,user_message]

            completion = await self._openai.beta.chat.completions.parse(
                model=self._openai_model_mini,
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
    
    async def create_queries_on_topic(self, topic_query):
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

            completion = await self._openai.beta.chat.completions.parse(
                model=self._openai_model_mini,
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

    async def summarize_youtube_data(self, youtube_data, topic_query):
        try:
            system_instructions = f"""You are a research assistant. 
            You are tasked with summarizing a youtube audio transcript based on a specific topic provided by the user.
            The goal is to provide a concise, insightful summary of the youtube audio data with a strong focus on the latest developments related to the given topic. 
            The summary should be informative, highlighting key points, emerging trends, and relevant data that will keep the reader up-to-date with recent changes and updates on the topic. 
            Keep the summary focused and relevant to the user's needs.

            Instructions:

            1. Topic: {topic_query}
            2. Review the youtube audio transcript carefully.
            3. Focus on summarizing the most recent developments, key trends, and any data points that directly relate to the topic.
            4. Ensure the summary is clear, concise, and relevant for a weekly update, highlighting important changes or trends.
            5. Use a professional tone, suitable for clients who are keeping up with industry developments.
            6. If the page contains redundant information or general context not directly relevant to the topic, omit it and focus on actionable insights and updates.
                        
            """

            user_query = f"""
            Here is the information you need to summarize:\n\n
            **Topic**: [{topic_query}]\n\n
            **Youtube Audio Transcript**: [{youtube_data}]\n\n
            Please provide a summary focused on the most recent developments and key insights related to the topic."
            """
            system_message = {"role": "system", "content": system_instructions}
            user_message = {"role": "user", "content": user_query}
            messages = [system_message,user_message]

            completion = await self._openai.chat.completions.create(
                model=self._openai_model_mini,
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
    
    async def summarize_web_page_data(self, web_page_data, topic_query):
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
            6. Format the summary using Markdown with the following structure:
                - # for title
                - ## for section headings
                - **Bold** for important points
                - Bullet points for key takeaways or lists
                - [Link](URL) format for links (if applicable)
            7. If the page contains redundant information or general context not directly relevant to the topic, omit it and focus on actionable insights and updates.
                        
            """

            user_query = f"""
            Here is the information you need to summarize for, in Markdown format:\n\n
            **Topic**: [{topic_query}]\n\n
            **Web Page Data**: [{web_page_data}]\n\n
            Please provide a summary focused on the most recent developments and key insights related to the topic."
            """
            system_message = {"role": "system", "content": system_instructions}
            user_message = {"role": "user", "content": user_query}
            messages = [system_message,user_message]

            completion = await self._openai.chat.completions.create(
                model=self._openai_model_mini,
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

    async def bulletpoint_web_page_data(self, web_page_data, topic_query):
        try:
            system_instructions = f"""You are a research assistant. 
            You are tasked with summarizing a web page based on a specific topic provided by the user. The web page contains both text and table data.
            The goal is to provide a clear and concise list of bullet points that highlight only the most important and relevant information related to the given topic.
            Focus on extracting key actionable insights, recent trends, and relevant data, keeping each bullet point short and to the point.

            Instructions:

            1. Topic: {topic_query}
            2. Review the web page data carefully, including any text and table data.
            3. Create a **concise list of bullet points**, focusing only on the most important developments, trends, and data related to the topic.
            4. Keep the bullet points short—just a few words or one brief sentence for each point.
            5. Use a professional tone, suitable for clients who need quick, high-impact information.
            6. Format the list of bullet points in Markdown.
            - # for title
            - ## for section headings
            - **Bold** for important points
            - Bullet points for key takeaways or lists            
            7. Omit any redundant information or general context that does not provide immediate value.

            """

            user_query = f"""
            Here is the information you need to summarize in **concise bullet points** using Markdown format:\n\n
            **Topic**: [{topic_query}]\n\n
            **Web Page Data**: [{web_page_data}]\n\n
            Please provide a concise list of bullet points focused only on the most important developments and key insights related to the topic, and format it in Markdown."""

            system_message = {"role": "system", "content": system_instructions}
            user_message = {"role": "user", "content": user_query}
            messages = [system_message,user_message]

            completion = await self._openai.chat.completions.create(
                model=self._openai_model_mini,
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

    async def executive_summary_web_page_data(self, web_page_data, topic_query):
        try:
            system_instructions = f"""
            You are a highly skilled research assistant tasked with creating concise executive summaries of web pages based on a specific topic provided by the user. The goal is to deliver a high-level overview with actionable insights tailored for decision-makers.

            ### Instructions:
            1. **Topic**: {topic_query}  
            Analyze the web page carefully, including both text and table data. Extract only the most critical and impactful information.  
            2. **Summary Requirements**:  
            - Highlight **key insights**, **recent developments**, and **actionable takeaways** related to the topic.  
            - Focus on **broad trends**, **major initiatives**, and **solutions**, omitting overly detailed or redundant information.  
            - Write in a **professional tone**, suitable for decision-makers who need a quick, high-level overview.  

            3. **Formatting** (Markdown):  
            - Use `##` for section headings (e.g., Key Insights, Major Developments, Actionable Takeaways).  
            - Use **bold** for emphasis and bullet points for clarity.  
            - Include hyperlinks in `[Link](URL)` format, if applicable.  
            - **Do not include a title like "Executive Summary."**

            4. **Style Guidelines**:  
            - Keep it concise and focused: no more than 2-3 bullet points per section.  
            - Prioritize **impactful insights** and **actionable recommendations** over minor details.  
            - Ensure clarity and readability for quick skimming.

            5. **Output Objective**:  
            Deliver a well-organized and polished executive summary in Markdown format that highlights only the most important information, avoiding unnecessary details.
            """

            user_query = f"""
            Here is the information you need to create a **concise executive summary** for, in Markdown format:\n\n
            **Topic**: [{topic_query}]\n\n
            **Web Page Data**: [{web_page_data}]\n\n
            Please provide a concise executive summary focusing only on high-level insights, broad trends, and actionable takeaways related to the topic, formatted in Markdown."""

            system_message = {"role": "system", "content": system_instructions}
            user_message = {"role": "user", "content": user_query}
            messages = [system_message,user_message]

            completion = await self._openai.chat.completions.create(
                model=self._openai_model_mini,
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

    async def summarize_topic_summaries(self, topic_query, summaries_list):
        try:

            system_instructions = f"""
            You are a highly skilled research assistant tasked with synthesizing a **detailed yet concise executive summary** based on a list of summaries provided by the user. Your goal is to deliver a **high-level overview** that captures the most critical insights, trends, and actionable takeaways, ensuring the summary is tailored for decision-makers.

            ### Instructions:
            1. **Topic**: {topic_query}  
            Carefully analyze the provided list of summaries and extract only the most impactful information, ensuring all meaningful insights are included.  

            2. **Guidelines for Structuring the Summary**:  
            - Use the following sections **only if the data provides meaningful content for that section**:  
                - **Key Insights**: High-level trends or data points framing the topic.  
                - **Major Developments**: Recent updates, innovations, or events.  
                - **Trends and Patterns**: Recurring themes or shifts across the sources.  
                - **Actionable Takeaways**: Specific recommendations or practical steps for decision-makers.  
                - **Opportunities and Risks**: Areas of growth or caution.  
                - **Noteworthy Examples or Case Studies**: Relatable real-world applications or notable projects.  
            - If a section lacks meaningful impact, omit it. Consolidate overlapping points into a single clear passage.

            3. **Formatting Requirements** (Markdown):  
            - Use `##` for section headings (e.g., Key Insights, Major Developments).  
            - Use **bold** for critical points and bullet points for clarity.  
            - Include `[Link](URL)` format for hyperlinks, if applicable.  
            - **Do not include a title like "Executive Summary."**

            4. **Style and Tone**:  
            - Use a **professional and neutral tone** suitable for decision-makers.  
            - Ensure clarity, conciseness, and coherence throughout.  
            - Structure content for quick skimming, with concise bullet points or short paragraphs.

            5. **Output Objective**:  
            Provide a **polished executive summary** in Markdown format that:  
            - Touches on every meaningful topic or insight from the provided summaries.  
            - Combines similar points into a single cohesive narrative to avoid redundancy.  
            - Highlights actionable, high-level information without delving into unnecessary detail.  

            6. **Additional Notes**:  
            - Avoid directly copying phrasing from the summaries—reword and synthesize for coherence and conciseness.  
            - Highlight actionable takeaways and big-picture trends for decision-making purposes.  
            - Omit sections that lack impactful content, ensuring the final summary remains concise and focused.  
            """
            user_query = f"""
            Here is the information you need to create a **concise executive summary** for, in Markdown format:\n\n
            **Topic**: [{topic_query}]\n\n
            **List of Summaries**: [{summaries_list}]\n\n
            Please provide a concise executive summary focusing only on high-level insights, broad trends, and actionable takeaways related to the topic, formatted in Markdown.
            """
            system_message = {"role": "system", "content": system_instructions}
            user_message = {"role": "user", "content": user_query}
            messages = [system_message,user_message]

            completion = await self._openai.chat.completions.create(
                model=self._openai_model_mini,
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
        
    async def key_figures_web_page_data(self, web_page_data, topic_query):
        try:
            system_instructions = f"""You are a research assistant. 
            You are tasked with reviewing a web page based on a specific topic provided by the user. The web page contains both text and table data. 
            Your goal is to identify and list key figures (such as influential people) and companies mentioned within the web page that are relevant to the given topic.
            Focus on extracting the most relevant names of individuals and organizations that play a significant role in the developments or trends discussed.

            Instructions:

            1. Topic: {topic_query}
            2. Review the web page data carefully, including any text and table data.
            3. Focus on identifying and listing the key figures (such as important people, executives, or experts) and companies (including organizations or businesses) that are relevant to the topic.
            4. Ensure the list is clear, concise, and relevant for a weekly update, prioritizing names that are closely tied to recent developments and important trends.
            5. Use a professional tone, suitable for clients who are keeping up with industry players and developments.
            6. Format the summary using Markdown with the following structure:
                - # for title
                - ## for section headings
                - **Bold** for important points
                - Bullet points for key takeaways or lists
                - [Link](URL) format for links (if applicable)
                - Use two spaces at the end of a line for line breaks instead of '\\n'
                - Avoid using special characters like '\\n'
            7. If the page contains irrelevant or minor mentions of individuals or companies, omit them and focus only on the most significant names.

            """

            user_query = f"""
            Here is the information you need to review for, in Markdown format::\n\n
            **Topic**: [{topic_query}]\n\n
            **Web Page Data**: [{web_page_data}]\n\n
            Please provide a list of key figures and companies mentioned in the web page that are relevant to the topic."
            """

            system_message = {"role": "system", "content": system_instructions}
            user_message = {"role": "user", "content": user_query}
            messages = [system_message,user_message]

            completion = await self._openai.chat.completions.create(
                model=self._openai_model_mini,
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


    async def is_web_page_data_usable(self, web_page_data, topic_query):
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

            completion = await self._openai.beta.chat.completions.parse(
                model=self._openai_model_mini,
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

    async def get_order_status(self):
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

            completion = await self._openai.chat.completions.create(
                model=self._openai_model_mini,
                messages=messages,
                tools=tools
            )

            response_msgs = self.handle_completion_with_tools(completion, messages, tools)
            return response_msgs
        except Exception as e:
            print(e)
            pass
        return None
    
    async def handle_completion_with_tools(self, completion, messages, tools):
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
                response = await self._openai.chat.completions.create( 
                    model=self._openai_model_mini,
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

    async def transcribe_audio_file(self, audio_file_path):
        try:
            async with open(audio_file_path, "rb") as audio_file:
                transcription = await self._openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcription.text
        except Exception as e:
            print(e)
            pass
        return None

    
    async def transcribe_audio_file_chunks(self, audio_file_paths: List[str]) -> List[str]:
        transcriptions = []
        for file_path in audio_file_paths:
            transcription_text = await self.transcribe_audio_file(file_path)
            if transcription_text:
                transcriptions.append(transcription_text)
        return transcriptions
    

    async def query_images(self, query_text, image_urls):
        try:
            user_query = {"type": "text", "text": query_text}
            user_images = [{"type": "image_url", "image_url": {"url": image_url}} for image_url in image_urls]
            user_message = {"role": "user", "content": [user_query] + user_images}
            messages = [user_message]

            completion = await self._openai.chat.completions.create(
                model=self._openai_model_mini,
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

    async def create_image(self, query_text):
        try:
            response = await self._openai.images.generate(
                model=self._openai_model_dalle3,
                prompt=query_text,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            if response.data:
                response_url = response.data[0].url
                return response_url
            else:
                # handle refusal
                print("finish reason not stop")
                return None
        except Exception as e:
            print(e)
            pass
        return None

    async def build_user_character_on_images(self, image_urls):
        system_query = """
        You are a character analyst assistant specializing in analyzing images. Your task is to extract insightful and accurate observations from a user's profile image to help infer their character traits. 

        Instructions:
        1. **Image Analysis**:
        - Carefully analyze the provided images to identify:
            - The setting, objects, and activities depicted.
            - The facial expression, pose, attire, and visible emotions of the person.
            - Any contextual clues that suggest the person's personality traits, interests, or behaviors.
        - Avoid making unsupported assumptions or generalizations.

        2. **Character Traits**:
        - Infer possible character traits based on the images (e.g., sociability, creativity, adventurousness).
        - Use the visual evidence to support your observations.

        3. **Ethical Considerations**:
        - Only base your analysis on visible, factual details in the images.
        - Avoid speculative conclusions not supported by the images.
        - Ensure privacy and avoid including sensitive or speculative information.
        - Maintain a neutral, professional tone and avoid stereotypes.

        Your goal is to provide a clear and insightful summary of the person's character based on the images provided.

        """

        # user_query = """
        # Please analyze the following data and provide a character summary in Markdown format.

        # **Images**:
        # [Upload or describe the images here]

        # **Comments**:
        # [Include user comments here]

        # Focus on identifying character traits, emotional cues, and any observable patterns. Combine insights from both the images and comments for a comprehensive description. Format the response with headings, bold key points, and bullet points for clarity.
        # """

        result = await self.query_images(system_query, image_urls)
        return result
    

    
async def run_web_page_data_example():
    # Example usage:
    client = OpenAIClient()

    # audio_file_path = "audio_data/cefef2bd-973c-472b-96d4-cd9699c0987c/cefef2bd-973c-472b-96d4-cd9699c0987c_chunk_1.mp3"
    # transcription_text = client.transcribe_audio_file(audio_file_path)
    # print(transcription_text)

    with open("results/Smart_Cities_and_Urban_Planning_results_with_summaries.json", "r") as json_file:
        data = json.load(json_file)
            
    topic = "Smart Cities and Urban Planning"

    for query_results in data["query_results"]:
            print("Summarizing sources for query: " + query_results["query"])
            for item in query_results["results"]:
                web_page_data = item["content"]["data"]
                # print("\tchecking if " + item["link"] + " is usable")
                # Call the is_web_page_data_usable function
                is_usable = await client.is_web_page_data_usable(web_page_data, topic)
                print("\t" + item["url"] + " is usable: " + str(is_usable))
                if is_usable:
                    # Call the summarize_web_page_data function
                    summary = await client.executive_summary_web_page_data(web_page_data, topic)
                    with open("results/results.txt", "w") as results_file:
                        results_file.write(summary)

                    print("summary:")
                    print(summary[:200]+"...")

async def run_image_analysis_example():
    client = OpenAIClient()
    image_url_1 = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    image_url_2 = "https://scontent-dfw5-1.cdninstagram.com/v/t51.29350-15/470461632_1322703858909267_8052317554819076319_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=101&ccb=1-7&_nc_sid=18de74&_nc_ohc=vlclYeC-LpkQ7kNvgHFyxFw&_nc_zt=23&_nc_ht=scontent-dfw5-1.cdninstagram.com&edm=ANQ71j8EAAAA&_nc_gid=AVQ2UFqyw-8eQWzpJ6f1-JY&oh=00_AYAaUxNYUZJTvZReFFFyc53_S0N1Z4BDb290D_DaRo1kDw&oe=6768FDAB"
    image_url_3 = "https://scontent-dfw5-1.cdninstagram.com/v/t51.29350-15/470473773_1262689361644407_6324166405197155981_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=101&ccb=1-7&_nc_sid=18de74&_nc_ohc=jfAn-8WSCP8Q7kNvgGgbQc_&_nc_zt=23&_nc_ht=scontent-dfw5-1.cdninstagram.com&edm=ANQ71j8EAAAA&_nc_gid=AmtEIPO5Vk_qxBhz3MXWEm1&oh=00_AYBPK5E3SbpL7-iqVHV39jWNBqTVSEMr7v2uDLyahC3_Mg&oe=6768F5C6"
    image_url_4 = "https://scontent-dfw5-1.cdninstagram.com/v/t51.29350-15/470726453_937668675182054_4739961380761145078_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=105&ccb=1-7&_nc_sid=18de74&_nc_ohc=VIgL_cfX9SEQ7kNvgFYP0Mz&_nc_zt=23&_nc_ht=scontent-dfw5-1.cdninstagram.com&edm=ANQ71j8EAAAA&_nc_gid=Amm96Rx-65xv1mHNUDc51Ro&oh=00_AYBI032AbQ1_PCV88dIcSe3lkY0AyiRdjxXb3DUtADMFJQ&oe=6768E789"
    image_url_5 = "https://scontent-dfw5-2.cdninstagram.com/v/t51.29350-15/470352611_611116558115507_3414044199832226079_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=102&ccb=1-7&_nc_sid=18de74&_nc_ohc=DwzUw4pPNWcQ7kNvgHsmW5N&_nc_zt=23&_nc_ht=scontent-dfw5-2.cdninstagram.com&edm=ANQ71j8EAAAA&_nc_gid=A5OJa2vi7RZWuPirmz8KPD7&oh=00_AYA04OndsUxgjmBMQc_qWElhqDL3P8hKxFxZgltwYfFSJA&oe=67690968"
    image_url_6 = "https://scontent-dfw5-1.cdninstagram.com/v/t51.29350-15/470347395_1779171625954831_449535914185449904_n.jpg?stp=dst-jpg_e35_tt6&_nc_cat=109&ccb=1-7&_nc_sid=18de74&_nc_ohc=y_C-qJw5VEEQ7kNvgG_tE9X&_nc_zt=23&_nc_ht=scontent-dfw5-1.cdninstagram.com&edm=ANQ71j8EAAAA&_nc_gid=A5fkaKMBTqXWn5_R3h-mA69&oh=00_AYAv_G2CcNKFn4ky84q6iJvsm-Q9wl8GkGwfU1hxCIvcMQ&oe=67691092"
    image_url_7 = "https://cdn.outsideonline.com/wp-content/uploads/2019/09/18/man-backpacking-thru-hike_s.jpg"
    
    image_urls = [image_url_1, image_url_2, image_url_3, image_url_4, image_url_5, image_url_6, image_url_7]
    result = await client.build_user_character_on_images(image_urls)
    print(result)
    return result

# Example usage:
async def main():
    # Example usage:
    client = OpenAIClient()
    query = "a red siamese cat"
    # query_prompt = await run_image_analysis_example()
    artistic_styles = ["impressionism", "surrealism", "abstract", "cubism", "minimalism", "pop art", "expressionism", "realism"]
    include_artistic_styles=["minimalism"]
    query_prompt = f"""
    Character Description:
    Name: Luna Everly
    Profession: Jazz Musician and Songwriter
    Traits and Personality:
    Creative Soul: Luna sees music as a language of emotions and the core of her existence. Her songs often blend elements of traditional jazz with modern experimental sounds, reflecting her ability to think outside the box.
    Urban Dreamer: Living in NYC, she thrives in the city's chaos, drawing inspiration from the subway's rhythm, the hum of distant sirens, and the whispers of late-night diners.
    Resilient and Ambitious: Despite the competitive music scene, Luna maintains an unwavering belief in her artistry. She often plays at intimate jazz clubs in Greenwich Village and dreams of one day performing at Carnegie Hall.
    Appearance:
    Luna has curly auburn hair that she often styles into a messy bun or lets flow naturally. Her expressive green eyes seem to reflect the city's lights, full of curiosity and depth.
    She dresses in a mix of vintage and bohemian styles, favoring flowy dresses, leather jackets, and ankle boots. Her signature accessory is a silver charm bracelet gifted by her grandmother.
    Lifestyle:
    Luna spends her mornings practicing on her antique upright piano, a gift from a neighbor who heard her singing through thin apartment walls.
    Afternoons are for exploration: walking through Central Park, visiting art galleries, or people-watching from a café in the East Village.
    Her evenings are dedicated to performances, collaborations, and jam sessions, where she feels most alive.
    On her rare days off, she loves to cook Creole dishes, a comforting reminder of home.
    Hobbies and Interests:
    When not immersed in music, Luna enjoys photography, capturing candid moments of city life.
    She's an avid reader, favoring novels about human resilience and poetry collections that inspire her songwriting.
    Luna also volunteers at a local music school, teaching underprivileged kids the basics of playing instruments.
    Philosophy: Luna believes that life is like a jazz improvisation — imperfect, unpredictable, and beautiful when you embrace its chaos. She lives by the mantra, "Play the notes you feel, not the ones you think are expected."
    """
    query_prompt_final = f"""
    Generate a unique and visually abstract image of a character inspired by the following traits. 
    The image should blend artistic interpretation and metaphorical representation of the traits. 
    Avoid including any text, words, or captions in the image. 
    Focus on creating a visually striking and imaginative depiction that captures the essence of the character in a surreal or symbolic way.

    Character Description:
    {query_prompt}

    **Artistic Styles**:
    {include_artistic_styles}

    **Additional Notes for the Image**:
    - Use symbolic elements or abstract forms to represent personality traits (e.g., vibrant colors, textures, or unique environments that reflect character traits).
    - Create a setting in a way that feels fluid and dreamlike.
    - Infuse artistic aesthetics that evoke introspection and creativity.
    - Avoid literal depictions; lean into surreal, artistic, and emotionally resonant imagery.

    The final image should feel like a harmonious blend of the traits, conveying the character's essence through a unique and abstract artistic lens.
    The final image sould not contain any text, words, or captions.
    """
    result = await client.create_image(query_prompt_final)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

# if __name__ == "__main__":
#     # Example usage:
#     client = OpenAIClient()

#     audio_file_path = "audio_data/cefef2bd-973c-472b-96d4-cd9699c0987c/cefef2bd-973c-472b-96d4-cd9699c0987c_chunk_1.mp3"
#     transcription_text = client.transcribe_audio_file(audio_file_path)
#     print(transcription_text)

    # with open("results.json", "r") as json_file:
    #         data = json.load(json_file)
            
    # topic = "cryptocurrency trading"

    # for query_sources in data["sources_data"]:
    #         print("Summarizing sources for query: " + query_sources["query"])
    #         for item in query_sources["sources_data"]:
    #             web_page_data = item["source_data"]
    #             # print("\tchecking if " + item["link"] + " is usable")
    #             # Call the is_web_page_data_usable function
    #             is_usable = client.is_web_page_data_usable(web_page_data, topic)
    #             print("\t" + item["link"] + " is usable: " + str(is_usable))
    #             if is_usable:
    #                 # Call the summarize_web_page_data function
    #                 summary = client.summarize_web_page_data(web_page_data, topic)
    #                 print("summary:")
    #                 print(summary[:200]+"...")



    # user_topic = "Physics of black holes"
    # query_list_response = client.create_queries_on_topic(user_topic)
    # query_list_response.print_query_list()

    # menu_line = "- Migas - Totopos, scrambled eggs, duck fat refried beans, chorizo, queso fresco, cilantro, avocado crema, salsa cruda (gf, contains dairy) $6"
    # menu_item = client.breakdown_menu_line(menu_line)
    # print(menu_item)

    # order_status_response = client.get_order_status()
    # print(client.print_conversion(order_status_response))
