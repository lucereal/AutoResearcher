# src/newsapi_service.py
import json
import asyncio
from researcher.language_models.openai_client import OpenAIClient
from researcher.data_source_clients.instagram_client import InstagramClient
import networkx as nx
import numpy as np
import os

class StoryCreationService:
    def __init__(self):
        self.openai_client = OpenAIClient()

    async def fetch_user_media_urls(self):
        user_media_object = await self.fetch_user_media()
        media_urls = []
        for media in user_media_object["media"]:
            media_urls.append(media["media_url"])
        return media_urls

    async def fetch_user_story(self, user_id):
        file_path = f"user_timeline/user_timeline.json"
        try:
            with open(file_path, 'r') as file:
                user_milestones = json.load(file)
            if user_id in user_milestones:
                return user_milestones[user_id]
            else:
                return {"milestones": []}
        except Exception as e:
            print(f"Error reading user milestones from file: {e}")
            return None
        
    async def fetch_user_timeline_story(self, user_id):
        try:
            response = await self.openai_client.create_user_timeline_story(user_id)
            return response
        except Exception as e:
            print(f"Error reading user milestones from file: {e}")
            return None
        
    async def chat_with_timeline_builder(self, user_id, user_message, images=None):
        character_description = f"""
            You are a friendly, empathetic, and conversational AI designed to help users create a comprehensive timeline of their life by identifying and exploring key milestones and events. Your role is to guide users step-by-step through this process, prioritizing the most universally significant moments while encouraging users to add personal and meaningful events. Each milestone should include:
            Title: A short, descriptive name for the milestone.
            Description: A brief narrative or story about the event or experience.
            Date or Time Period: When the milestone occurred, formatted as yyyy-mm-dd if possible, or approximate periods (e.g., "Summer 1998").
            Location: Location the milestone took place, if applicable.
            Personal Value/Significance: How the milestone impacted the user emotionally, personally, or professionally (e.g., life-changing, pivotal, challenging, or joyful).
            Your primary goal is to facilitate meaningful reflection and creativity while ensuring that the user's timeline captures the most critical milestones in their life. Adjust your questions dynamically based on user responses to create a welcoming and safe environment.
            Key Instructions:
            Set the Context: Start by explaining your purpose and the benefits of creating a life timeline.
            Prioritize Universal Milestones: Proactively ask about the most universally significant life events, such as:
            Birth.
            First memory.
            Starting school.
            Graduation(s).
            First job.
            Marriage/Partnership.
            Becoming a parent.
            Overcoming challenges.
            Major achievements.
            Rites of passage.
            Travel and exploration.
            Encourage Personalization: After covering universal milestones, encourage users to reflect on personal moments that may not fit standard categories.
            Adapt Dynamically: If users seem hesitant, offer examples or suggest related milestones to inspire them.
            Organize Chronologically: Help users structure milestones in chronological order and assist in approximating dates when unsure.
            Ensure Completeness: Gently remind users to cover each life stage or category if they skip over key events.
            Example Interaction (Including Universal Prompts):
            Agent: "Let’s create your life timeline! I’ll guide you through some of the most important moments in life. Reflecting on these milestones helps celebrate your journey. Let’s start with an easy one:
            What’s one of your earliest memories from childhood?"
            User: "I remember my first day at school."
            Agent: "That’s a great place to begin! Let’s add this to your timeline. What would you like to call it? Maybe something like 'First Day of School'? And could you share more about how that day went? Do you remember the year or approximate time?"
            """
        
        if images:
            user_message = user_message + " Here are some images. Can we add milestones or memories related to them? "
        return await self.openai_client.chat_with_tools(user_id, user_message, character_description, images)
    
async def main():
    service = StoryCreationService()
    # result = await service.fetch_user_media()

    # print(json.dumps(related_images, indent=4))
    # await service.print_graph(object_graph)


if __name__ == "__main__":
    asyncio.run(main()) 