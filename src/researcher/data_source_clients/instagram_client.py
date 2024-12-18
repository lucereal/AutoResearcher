import os
import httpx
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio


load_dotenv()


class InstagramClient():

    def __init__(self):
        self.client_id = os.getenv("INSTAGRAM_CLIENT_ID")
        self.client_secret = os.getenv("INSTAGRAM_CLIENT_SECRET")
        self.grant_type = "authorization_code"
        self.redirect_uri = os.getenv("INSTAGRAM_REDIRECT_URI")
        self.a_code = os.getenv("INSTAGRAM_ACCESS_CODE")
        self.auth_url = "https://api.instagram.com/oauth/access_token"
        self.graph_url = "https://graph.instagram.com/v21.0"

    async def get_access_token(self, code, source="local"):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": self.grant_type,
            "redirect_uri": self.redirect_uri,
            "code": code
            }
        
        if source == "local":
            response = {"access_token": self.a_code}
            return response
        else:
            async with httpx.AsyncClient() as client:
                    response = await client.post(self.auth_url, data=data)
                    if response.status_code == 200:
                        return response.json()
                    else:
                        return {"error": response.text}
    
    async def get_user_info(self, access_token):
        url = self.graph_url + f"/me?access_token={access_token}&fields=user_id,username,media_count"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": response.text}

# Example usage:
async def main():
    instagram_client = InstagramClient()
    access_token_response = await instagram_client.get_access_token(None, "local")
    if "access_token" in access_token_response:
        user_info = await instagram_client.get_user_info(access_token_response["access_token"])
        print(user_info)
    else:
        print("Error obtaining access token:", access_token_response["error"])

if __name__ == "__main__":
    asyncio.run(main())