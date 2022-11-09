from yt_dlp import YoutubeDL
import json
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

audioformat = "wav"
downloadFolder = f"{os.getcwd()}/ytDownload_Terminal/Downloads"

audio_downloader = YoutubeDL({
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': audioformat,
    'outtmpl': f'{downloadFolder}/%(id)s.{audioformat}',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
})

class youtubeDownload:
    def __init__(self, url, ext: str = audioformat):
        self.url = url
        self.ext = ext
        self.downloadCount = 0
        #Functions to call
        self.urlData()
        self.download()

    def renameFile(self):
        #Rename file name from youtube id to title
        if downloadFolder not in str(os.getcwd()):
            os.chdir(downloadFolder)
        [os.rename(f"{entry['id']}.{self.ext}", f"{entry['title']}.{self.ext}") for entry in self.result["entries"]]
        os.chdir("../..")

    def renameTitle(self, title: str):
        forbidChar = ["|", "\\", "/", "?", "."]
        for char in forbidChar:
            title = title.replace(char, "-")
        return title

    def urlData(self, export: bool = False):
        #Extract playlist/video data
        print(f"Getting playlist data for: {self.url}")
        self.result = audio_downloader.extract_info(self.url, False)
        print(f"Playlist data downloaded")
        if export == True:
            with open("exportList.json", "w") as f:
                json.dump(self.result, f, indent=4)
        baseLink = "https://www.youtube.com/watch?v="
        print(self.result)
        try:
            self.links = [f"{baseLink}{entry['id']}" for entry in self.result["entries"]]
            self.titles = [self.renameTitle(entry["title"]) for entry in self.result["entries"]]
            self.ids = [entry["id"] for entry in self.result["entries"]]
        except:
            self.links = [f"{baseLink}{self.result['id']}"]
            self.titles = [self.renameTitle(self.result["title"])]
            self.ids = [self.result["id"]]

    def gatherVideo(self, url: str, title: str, id: str, index: int, ext: str = audioformat):
        # Download video
        if downloadFolder not in str(os.getcwd()):
            os.chdir(downloadFolder)
        parentPath = "/".join(str(os.getcwd()).split("\\")[1:])
        try:
            print(f"[{index + 1}] Starting video download for {title}")
            print(url)
            audio_downloader.extract_info(url)
        except Exception as e:
            Value = True
            if "HTTP" in str(e):
                try:
                    os.remove(f"/{parentPath}/{id}.{ext}.part")
                except:
                    a = 0
                while Value == True:
                    try:
                        audio_downloader.extract_info(url)
                        break
                    except Exception as e:
                        if "HTTP" not in str(e):
                            Value = False
                            break
                        else:
                            try:
                                os.remove(f"/{parentPath}/{id}.{ext}.part")
                            except:
                                a = 0
            else:
                print(f"[{index + 1}] Video: {title} failed to download because:\n{e}")
        try:
            os.rename(f"/{parentPath}/{id}.{ext}", f"/{parentPath}/{title}.{ext}")
        except FileNotFoundError:
            print(parentPath, f"{id}.{ext} to {title}.{ext}")
        self.downloadCount = self.downloadCount + 1
        print(f"[{index + 1}] |{self.downloadCount}/{len(self.titles)}| Video: {title} downloaded...")

    async def parallelDownload(self, link, title, id, loop, urlIndex):
        executor = None
        await loop.run_in_executor(executor, self.gatherVideo, link, title, id, urlIndex)

    def download(self):
        #Asyncio parallel processing to speed up download process
        loop = asyncio.get_event_loop()
        tasks = [self.parallelDownload(self.links[urlIndex],  self.titles[urlIndex], self.ids[urlIndex], loop, urlIndex) for urlIndex in range(len(self.links))]
        loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()
        print("All videos are downloaded")
