from typing import Optional
from pytubefix import YouTube
from pytubefix import exceptions
import uuid
import os
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip


class AudioFileData:
    def __init__(self, file_name=None, org_file_name=None, file_id=None, file_size=None, num_chunks=None, chunk_size=None, file_path=None, chunks=None):
        self.file_name = file_name
        self.org_file_name = org_file_name
        self.file_id = file_id
        self.file_size = file_size
        self.num_chunks = num_chunks
        self.chunk_size = chunk_size
        self.file_path = file_path
        self.chunks = chunks
    def to_dict(self):
        return {
            "file_name": self.file_name,
            "org_file_name": self.org_file_name,
            "file_id": self.file_id,
            "file_size": self.file_size,
            "num_chunks": self.num_chunks,
            "chunk_size": self.chunk_size,
            "file_path": self.file_path,
            "chunks": self.chunks
        }
    
class YouTubeClient:
    def __init__(self):
        pass
        self.audio_file_dir = "audio_data"

    def split_audio_into_chunks(self, audio_file_data:AudioFileData):

        chunk_duration=20*60
        if os.path.exists(audio_file_data.file_path):
            print(f"Audio file loaded: {audio_file_data.file_path}")
            audio = AudioFileClip(audio_file_data.file_path)

            base_name = os.path.splitext(os.path.basename(audio_file_data.file_path))[0]
            output_dir = os.path.join(self.audio_file_dir, base_name)
            os.makedirs(output_dir, exist_ok=True)

            duration = audio.duration
            start = 0
            chunk_num = 1
            chunks = []

            print(f"Duration: {duration}")
            print(f"Chunk duration: {chunk_duration}")
            print(f"Number of chunks: {duration/chunk_duration}")
            
            while start < duration:
                end = min(start + chunk_duration, duration)
                chunk = audio.subclip(start, end)
                chunk_filename = os.path.join(output_dir, f"{base_name}_chunk_{chunk_num}.mp3")
                chunk.write_audiofile(chunk_filename)
                chunks.append(chunk_filename)

                start += chunk_duration
                chunk_num += 1
            
            file_size = os.path.getsize(audio_file_data.file_path)
            num_chunks = len(chunks)
            chunk_size = chunk_duration

            audio_file_data.num_chunks = num_chunks
            audio_file_data.chunk_size = chunk_size
            audio_file_data.chunks = chunks
            audio_file_data.file_size = file_size
            audio_file_data.file_name = base_name

            return audio_file_data
        else:
            print(f"File not found: {audio_file_data.file_path}")

    def download_audio(self, url):
        try:
            yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
            stream = yt.streams.filter(only_audio=True, progressive=False, file_extension='mp4').order_by('abr').first()
            if stream:
                print(f"File size: {stream.filesize_mb} MB")
                new_file_name = stream.default_filename.replace(" ", "_")
                file_id = str(uuid.uuid4())
                file_name = f"{file_id}.mp4"
                file_path = os.path.join(self.audio_file_dir, file_name)
                audio_file_data = AudioFileData(
                   file_path=file_path, 
                   file_id = file_id,
                   org_file_name=new_file_name 
                )
                stream.download(self.audio_file_dir, file_name)
                print(f"Downloaded: {stream.default_filename}")
                return self.split_audio_into_chunks(audio_file_data)
                # stream.on_complete = self.split_audio_into_chunks(audio_file_data)
            else:
                print(f"No suitable stream found for {url}")
        except exceptions.VideoUnavailable:
            print(f'Video {url} is unavailable, skipping.')
        except Exception as e:
            print(f'An error occurred: {e}')

    def download_audio_json(self, url):
        audio_file_data = self.download_audio(url)
        if audio_file_data:
            return audio_file_data.to_dict()
        else:
            return None
        
# Example usage:
if __name__ == "__main__":
    client = YouTubeClient()
    
    # audio_data\Crypto,_Web_3_&_AI_Explained!_How_To_Earn_Money_By_Making_Projects!_Escaping_Class_11th_&_12_Science.mp4
    # 'audio_data/Crypto,_Web_3_&_AI_Explained!_How_To_Earn_Money_By_Making_Projects!_Escaping_Class_11th_&_12_Science.mp4'
    # audio_file_data = AudioFileData(
    #     file_path=os.path.join("audio_data", "temp.mp4"), 
    #     file_id = str(uuid.uuid4()) 
    # )
    # audio_file_data = client.split_audio_into_chunks(audio_file_data)
    # print(audio_file_data.file_name)
    # Download the highest resolution MP4 stream
    client.download_audio('https://www.youtube.com/watch?v=dVgN63Ydqrc')