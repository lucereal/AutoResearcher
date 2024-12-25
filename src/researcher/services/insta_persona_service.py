# src/newsapi_service.py
import json
import asyncio
from researcher.language_models.openai_client import OpenAIClient
from researcher.data_source_clients.instagram_client import InstagramClient
import networkx as nx
import numpy as np

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

async def main():
    service = InstaPersonaService()
    result = await service.fetch_user_media()
    graph_json = await service.get_profile_object_graph(result)

    print(json.dumps(graph_json, indent=4))
    # await service.print_graph(object_graph)


if __name__ == "__main__":
    asyncio.run(main()) 