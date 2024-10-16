from typing import Optional
from pytubefix import YouTube
from pytubefix import exceptions

import os
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip

class YouTubeClient:
    def __init__(self):
        pass

    def on_complete(self, file_path:str):
        """
        On download complete handler function.
        
        Parameters:
        file_path (str): The file handle where the media is being written to.
        """
        chunk_duration=20*60

        if os.path.exists(file_path):
            print(f"Audio file loaded: {file_path}")
            audio = AudioFileClip(file_path)

            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_dir = os.path.join("audio_data", base_name)
            os.makedirs(output_dir, exist_ok=True)

            duration = audio.duration
            start = 0
            chunk_num = 1

            while start < duration:
                end = min(start + chunk_duration, duration)
                chunk = audio.subclip(start, end)
                chunk.write_audiofile(os.path.join(output_dir, f"{base_name}_chunk_{chunk_num}.mp3"))

                start += chunk_duration
                chunk_num += 1
        else:
            print(f"File not found: {file_path}")

    def download_audio_mp4(self, url):
        """
        Downloads the highest resolution MP4 stream of the YouTube video.
        """
        try:
            yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
            stream = yt.streams.filter(only_audio=True, progressive=False, file_extension='mp4').order_by('abr').first()
            if stream:
                print(f"File size: {stream.filesize_mb} MB")
                new_file_name = stream.default_filename.replace(" ", "_")
                stream.download("audio_data", new_file_name)
                stream.on_complete = self.on_complete("audio_data/" +new_file_name)
                print(f"Downloaded: {stream.default_filename}")
            else:
                print(f"No suitable stream found for {url}")
        except exceptions.VideoUnavailable:
            print(f'Video {url} is unavailable, skipping.')
        except Exception as e:
            print(f'An error occurred: {e}')

# Example usage:
if __name__ == "__main__":
    client = YouTubeClient()
    
    # audio_data\Crypto,_Web_3_&_AI_Explained!_How_To_Earn_Money_By_Making_Projects!_Escaping_Class_11th_&_12_Science.mp4
    # 'audio_data/Crypto,_Web_3_&_AI_Explained!_How_To_Earn_Money_By_Making_Projects!_Escaping_Class_11th_&_12_Science.mp4'
    client.on_complete("audio_data/temp.mp4")

    # Download the highest resolution MP4 stream
    client.download_audio_mp4('https://www.youtube.com/watch?v=dVgN63Ydqrc')