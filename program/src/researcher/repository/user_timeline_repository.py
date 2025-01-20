import json
import asyncio
import networkx as nx
import numpy as np
import os
from typing import List
from fastapi import UploadFile
import uuid

class UserTimelineRepository:

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

    async def read_user_timeline(self, user_id):
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
    
    async def read_universal_milestones(self):
        file_path = f"user_timeline/universal_milestones.json"
        try:
            with open(file_path, 'r') as file:
                universal_milestones = json.load(file)
            return universal_milestones
        except Exception as e:
            print(f"Error reading user milestones from file: {e}")
            return None

    async def write_user_milestones(self, user_id, user_milestones):
        file_path = f"user_timeline/user_timeline.json"
        try:
            # Ensure the file exists and contains valid JSON
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                with open(file_path, 'w') as file:
                    json.dump({}, file)

            with open(file_path, 'r') as file:
                user_timeline = json.load(file)
            if user_timeline is None:
                user_timeline = {}
            
            if user_id not in user_timeline:
                user_timeline[user_id] = {"milestones": []}
            
            user_timeline[user_id]["milestones"].append(user_milestones)

            with open(file_path, 'w') as file:
                json.dump(user_timeline, file, indent=4)
            return user_timeline
        except Exception as e:
            print(f"Error writing user milestones to file: {e}")

    async def update_user_milestone_store(self, user_id, user_milestone):
        file_path = f"user_timeline/user_timeline.json"
        try:
            # Ensure the file exists and contains valid JSON
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                with open(file_path, 'w') as file:
                    json.dump({}, file)

            with open(file_path, 'r') as file:
                user_timeline = json.load(file)
            if user_timeline is None:
                user_timeline = {}
            
            if user_id not in user_timeline:
                return {"success":False, "message": "User not found."}
            
     
            # Find user milestone with matching user_milestone["id"] and update it
            for i, milestone in enumerate(user_timeline[user_id]["milestones"]):
                if str(milestone["id"]) == str(user_milestone["id"]):
                    user_timeline[user_id]["milestones"][i] = user_milestone
                    break
            
            with open(file_path, 'w') as file:
                json.dump(user_timeline, file, indent=4)
            return user_timeline
        except Exception as e:
            print(f"Error writing user milestones to file: {e}")

    async def delete_user_milestone_store(self, user_id, user_milestone):
        file_path = f"user_timeline/user_timeline.json"
        try:
            # Ensure the file exists and contains valid JSON
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                with open(file_path, 'w') as file:
                    json.dump({}, file)

            with open(file_path, 'r') as file:
                user_timeline = json.load(file)
            if user_timeline is None:
                user_timeline = {}
            
            if user_id not in user_timeline:
                return {"success":False, "message": "User not found."}
            
     
            # Find user milestone with matching user_milestone["id"] and del it
            for i, milestone in enumerate(user_timeline[user_id]["milestones"]):
                if str(milestone["id"]) == str(user_milestone["id"]):
                    del user_timeline[user_id]["milestones"][i]
                    break
            
            with open(file_path, 'w') as file:
                json.dump(user_timeline, file, indent=4)
            return user_timeline
        except Exception as e:
            print(f"Error writing user milestones to file: {e}")

    async def write_user_media_to_timeline(self, user_id, message_id, media_paths):
        file_path = f"user_timeline/user_timeline.json"
        try:
            # Ensure the file exists and contains valid JSON
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                return {"success":False, "message": "Timeline file not found."}
            
            with open(file_path, 'r') as file:
                user_timeline = json.load(file)
            if user_timeline is None:
                user_timeline = {}
            
            if user_id not in user_timeline:
                user_timeline[user_id] = {"milestones": [], "media": []}
            
            media_obj = {"message_id": message_id, "media": media_paths}
            user_timeline[user_id]["media"].append(media_obj)

            with open(file_path, 'w') as file:
                json.dump(user_timeline, file, indent=4)
            return user_timeline
        except Exception as e:
            print(f"Error writing user milestones to file: {e}")        

    async def save_user_images(self, user_id: str, user_images: List[UploadFile], folder_path: str) -> List[str]:
        saved_image_paths = []
        os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists

        for image in user_images:
            # Generate a unique filename
            short_uuid = uuid.uuid4().hex[:8]
            unique_filename = f"{user_id}_{short_uuid}{os.path.splitext(image.filename)[1]}"
            file_path = os.path.join(folder_path, unique_filename)

            # Save the image to the specified folder
            with open(file_path, "wb") as file:
                content = await image.read()
                file.write(content)

            saved_image_paths.append(file_path)

        return saved_image_paths 
   
async def main():
    service = UserTimelineRepository()



if __name__ == "__main__":
    asyncio.run(main()) 