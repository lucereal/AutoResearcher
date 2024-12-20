# src/newsapi_service.py
import asyncio
from researcher.language_models.openai_client import OpenAIClient
from researcher.data_source_clients.instagram_client import InstagramClient

class InstaPersonaService:
    def __init__(self):
        self.instagram_client = InstagramClient()
        self.openai_client = OpenAIClient()

    async def fetch_user_media(self):
        media_urls = []
        access_token_response = await self.instagram_client.get_access_token(None, "local")
        if "access_token" in access_token_response:
            user_info = await self.instagram_client.get_user_info(access_token_response["access_token"])
            print(user_info)
            user_media = await self.instagram_client.get_user_media(user_info["user_id"], access_token_response["access_token"])
            print(user_media) 
            for media in user_media["data"]:
                media_details = await self.instagram_client.get_media_details(media["id"], access_token_response["access_token"])
                media_urls.append(media_details["media_url"])
        return media_urls
        
    async def create_persona(self, user_media_urls):
        return await self.openai_client.build_user_character_on_images(user_media_urls)
    
    async def create_persona_visual(self, persona_result):
        return await self.openai_client.build_user_character_on_images(persona_result)

async def main():
    service = InstaPersonaService()
    result = await service.fetch_user_media()
    persona_result = await service.create_persona(result)
    print(result)

if __name__ == "__main__":
    asyncio.run(main()) 