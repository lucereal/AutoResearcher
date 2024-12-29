# src/newsapi_service.py
import json
import asyncio
from researcher.language_models.openai_client import OpenAIClient
from researcher.data_source_clients.instagram_client import InstagramClient
import networkx as nx
import numpy as np
import os

class InstaPersonaService:
    def __init__(self):
        self.instagram_client = InstagramClient()
        self.openai_client = OpenAIClient()

    #make method to fetch user media only
    #make method to build user media object so we can save to file
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
        print("found media urls: ")
        return media_urls
        
    async def save_user_media(self, user_info, user_media):
        directory = "user_media"
        user_object = user_media
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, f"{user_info.user_id}.json")
        with open(file_path, 'w') as file:
            json.dump(user_object, file, indent=4)

    async def read_json_from_file(self, user_id):
        file_path = os.path.join("user_media", f"{user_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        return {}
    
    async def update_json_file(self, user_id, new_data):
        json_object = await self.read_json_from_file(user_id)
        json_object.update(new_data)
        await self.save_json_to_file(user_id, json_object)

    async def create_persona(self, user_media_urls):
        return await self.openai_client.build_user_character_on_images(user_media_urls)
    
    async def create_profile_object_graph(self, user_media_urls):
        G = nx.Graph()
        for image_url in user_media_urls:
            try:
                objects = await self.openai_client.identify_image_objects([image_url])
                for obj in objects:
                    if obj not in G:
                        G.add_node(obj, count=0)
                    G.nodes[obj]['count'] += 1
                for i in range(len(objects)):
                    for j in range(i + 1, len(objects)):
                        if G.has_edge(objects[i], objects[j]):
                            G[objects[i]][objects[j]]['weight'] += 1
                        else:
                            G.add_edge(objects[i], objects[j], weight=1)
            except Exception as e:
                print("Error processing image:", e)
        return G       

    async def print_graph(self, G):
        print("Nodes:")
        for node, data in G.nodes(data=True):
            print(f"{node}: {data}")
        print("\nEdges:")
        for u, v, data in G.edges(data=True):
            print(f"{u} - {v}: {data}")  

    async def graph_to_json(self, G):
        data = nx.node_link_data(G, edges="edges")
        return data
    
    async def add_pos_to_json(self, object_graph, graph_json):
        #pos = nx.spring_layout(object_graph)
        #pos = nx.kamada_kawai_layout(object_graph)
        pos = nx.arf_layout(object_graph, a=3)
        for node in graph_json["nodes"]:
            node["pos"] = [float(coord) for coord in pos[node["id"]].tolist()]
            node["posx"] = node["pos"][0]
            node["posy"] = node["pos"][1]
        return graph_json
 
    async def get_profile_object_graph(self, user_media_urls):
        object_graph = await self.create_profile_object_graph(user_media_urls[0:10])
        graph_json = await self.graph_to_json(object_graph)
        graph_json_pos = await self.add_pos_to_json(object_graph, graph_json)
        return graph_json_pos

    async def chat_with_character(self, user_id, user_message):
        character_description = "You are the character chatbot named. David Lucero. Here is your description of who you are: In a world filled with vibrant colors and eclectic experiences, the individual behind these images resembles a colorful tapestry woven with threads of creativity and joy. Their playful spirit is embodied by a quirky red plush toy—a cherished companion that evokes a sense of whimsy, suggesting a heart that finds delight in the unconventional. Surrounded by furry friends, both mischievous and serene, their home radiates warmth and comfort, much like the cozy, inviting spaces they frequent. Amidst lively gatherings, they enjoy flavorful adventures, from sampling innovative dishes at food festivals to relishing craft beers in serene, nature-infused settings, showcasing their love for both community and culinary exploration. Whether scaling a climbing wall with determined passion or savoring picturesque city views, their adventurous spirit is unwavering. The essence of this individual dances like the neon words on a vibrant wall—alive with color, charm, and an infectious zest for life, grounded by the simple joys and profound connections that they cultivate along the way."

        # will have to buld database for each user instagram. json object with a element for each image. each image will have a list of topics
        # that are in the image, the summary, caption, tagged users, etc
        # the first prompt will gather images that relate the user message and the second prompt will be to 
        # response to the user using the images gathered
        return await self.openai_client.chat(user_id, user_message, character_description)

async def main():
    service = InstaPersonaService()
    result = await service.fetch_user_media()
    persona_result = await service.create_persona(result)

    print(json.dumps(persona_result, indent=4))
    # await service.print_graph(object_graph)


if __name__ == "__main__":
    asyncio.run(main()) 