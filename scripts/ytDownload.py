from yt_dlp import YoutubeDL
import json
import os
import concurrent
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from itertools import chain


class staticFunc:
    @staticmethod
    def pathInfo(filePath: str, parentCond: bool = False):
        if "/" in filePath:
            splitter = "/"
        if "\\" in filePath:
            splitter = "\\"
        fullPathArray = filePath.split(splitter)
        file = fullPathArray[-1]
        if parentCond:
            parentPath = splitter.join(fullPathArray[0:-1])
            return file, parentPath
        else:
            return file

    @staticmethod
    def validate(filePath: str, Error: bool = False):
        currentPath = os.getcwd()
        file, parentPath = staticFunc.pathInfo(filePath, parentCond=True)
        try:
            os.chdir(parentPath)
            files = os.listdir()
            os.chdir(currentPath)
            if file in files:
                return True
            else:
                return False
        except Exception as e:
            os.chdir(currentPath)
            if Error:
                return False
            else:
                return False

    @staticmethod
    def renameFile(parentPath, id, ext, title):
        os.rename(f"/{parentPath}/{id}.{ext}", f"/{parentPath}/{title}.{ext}")

    @staticmethod
    def renameTitle(title: str):
        forbidChar = ["|", "\\", "/", "?", ".", '"', ":"]
        for char in forbidChar:
            title = title.replace(char, "-")
        return title

    @staticmethod
    def assignThreads(result, threadNum, debug: bool = False):
        """
        :param result:
        :param threadNum:
        :return <list <tuple <link: <str>, title: <str>, id: <str>>>>:
        """
        baseLink = "https://www.youtube.com/watch?v="
        threadCounter = 0
        threadsEnqueue = [[] for thread in range(0, threadNum)]
        try:
            for entry in result["entries"]:
                if entry == None:
                    continue
                link = f"{baseLink}{entry['id']}"
                title = staticFunc.renameTitle(entry["title"])
                id = entry["id"]
                threadsEnqueue[threadCounter].append((link, title, id))
                if debug == True:
                    print(f"Enqueued {title} to thread #{threadCounter}")
                if (threadCounter + 1) == threadNum:
                    threadCounter = 0
                else:
                    threadCounter += 1
        except KeyError:
            link = f"{baseLink}{result['id']}"
            title = staticFunc.renameTitle(result["title"])
            id = result["id"]
            threadsEnqueue[threadCounter].append((link, title, id))
            if debug == True:
                print(f"Enqueued {title} to thread #{threadCounter}")
        return threadsEnqueue


class youtubeDownload:
    downloadCount = 0
    result = None
    threadsEnqueue = []
    overallProgress = None
    trackingProgress = None
    individualProgress = []
    description = []

    def __init__(self, config: dict, url: str, ext: str, dlFolder: str, threadNum: int = 1, debug: bool = False):
        self.audio_downloader = YoutubeDL(config)
        self.downloadFolder = dlFolder
        self.ext = ext
        self.debug = debug
        self.url = url
        self.threadNum = threadNum
        if "\\" in str(os.getcwd()):
            self.downloadFolder = self.downloadFolder.replace("/", "\\")
        dataFuture = self.urlData()

    def getEnqueueNum(self, threadEnqueue):
        for i in range(len(self.threadsEnqueue)):
            if self.threadsEnqueue[i] == threadEnqueue:
                return i

    def progressBarInit(self):
        trackNum = 0
        for i in range(0, len(self.threadsEnqueue)):
            trackNum += len(self.threadsEnqueue[i])
        self.trackingProgress = tqdm(desc="Overall Completion", colour="GREEN", smoothing=1, unit="video",
                                     total=trackNum)
        self.overallProgress = tqdm(desc="Thread Completion", colour="BLUE",
                                    bar_format='{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} thread(s)',
                                    total=len(self.threadsEnqueue))
        for i in range(0, len(self.threadsEnqueue)):
            trackNum += len(self.threadsEnqueue[i])
            self.individualProgress.append(tqdm(desc="",
                                                bar_format=f"Thread #{i} Status: " + '{percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} video(s)',
                                                unit="video(s)", total=len(self.threadsEnqueue[i])))
            self.description.append(tqdm(desc="No videos downloaded rn!", bar_format=f"Thread #{i} video: " + '{desc}'))

    def statusBarUpdate(self, title: str, status: str, enqueueNum):
        if status == "downloading":
            self.description[enqueueNum].set_description(f"Downloading: [{title}]", refresh=True)
        if status == "downloaded":
            self.description[enqueueNum].set_description(f"Downloaded: [{title}]", refresh=True)

    def progressBarUpdate(self, enqueueNum: int, updateType: str):
        if updateType == "thread":
            self.individualProgress[enqueueNum].update(1)
            self.trackingProgress.update(1)
            self.individualProgress[enqueueNum].refresh()
            self.trackingProgress.refresh()
        elif updateType == "overall":
            self.overallProgress.update(1)
            self.overallProgress.refresh()

    def runTask(self, threadEnqueue):
        for index in range(len(threadEnqueue)):
            url, title, id = threadEnqueue[index]
            if self.downloadFolder not in str(os.getcwd()):
                os.chdir(self.downloadFolder)
            if "\\" in str(os.getcwd()):
                parentPath = "/".join(str(os.getcwd()).split("\\")[1:])
            else:
                parentPath = "/".join(str(os.getcwd()).split("/")[1:])
            if staticFunc.validate(f"/{parentPath}/{id}.{self.ext}") == True:
                staticFunc.renameFile(parentPath=parentPath, id=id, ext=self.ext, title=title)
                if self.debug == False:
                    self.progressBarUpdate(updateType="thread", enqueueNum=self.getEnqueueNum(threadEnqueue=threadEnqueue))
                    self.statusBarUpdate(title=title, status="downloaded", enqueueNum=self.getEnqueueNum(threadEnqueue=threadEnqueue))
                else:
                    print(f"[{index + 1}] | Video: {title} downloaded...")
                continue
            if staticFunc.validate(f"/{parentPath}/{title}.{self.ext}") == True:
                if self.debug == False:
                    self.progressBarUpdate(updateType="thread", enqueueNum=self.getEnqueueNum(threadEnqueue=threadEnqueue))
                    self.statusBarUpdate(title=title, status="downloaded", enqueueNum=self.getEnqueueNum(threadEnqueue=threadEnqueue))
                else:
                    print(f"[{index + 1}] | Video: {title} downloaded...")
                continue
            try:
                if self.debug == False:
                    self.statusBarUpdate(title=title, status="downloading", enqueueNum=self.getEnqueueNum(threadEnqueue=threadEnqueue))
                if self.debug == True:
                    print(f"[{index + 1}] Starting video download for {title}")
                    print(url)
                self.audio_downloader.extract_info(url)
            except Exception as e:
                Value = True
                if "HTTP" in str(e):
                    try:
                        os.remove(f"/{parentPath}/{id}.{self.ext}.part")
                    except:
                        a = 0
                    while Value == True:
                        try:
                            self.audio_downloader.extract_info(url)
                            break
                        except Exception as e:
                            if "HTTP" not in str(e):
                                Value = False
                                break
                            else:
                                try:
                                    os.remove(f"/{parentPath}/{id}.{self.ext}.part")
                                except:
                                    a = 0
                else:
                    if self.debug == True:
                        print(f"[{index + 1}] Video: {title} failed to download because:\n{e}")
            try:
                staticFunc.renameFile(parentPath=parentPath, id=id, ext=self.ext, title=title)
            except FileNotFoundError:
                print(parentPath, f"{id}.{self.ext} to {title}.{self.ext}")
            self.downloadCount = self.downloadCount + 1
            if self.debug == False:
                self.progressBarUpdate(updateType="thread", enqueueNum=self.getEnqueueNum(threadEnqueue=threadEnqueue))
                self.statusBarUpdate(title=title, status="downloaded", enqueueNum=self.getEnqueueNum(threadEnqueue=threadEnqueue))
            else:
                print(f"[{index + 1}] | Video: {title} downloaded...")
        self.progressBarUpdate(updateType="overall", enqueueNum=self.getEnqueueNum(threadEnqueue=threadEnqueue))

    def urlData(self, export: bool = False):
        threads = []
        # Extract playlist/video data
        print(f"Getting playlist data for: {self.url}")
        self.result = self.audio_downloader.extract_info(self.url, False)
        print(f"Playlist data downloaded")
        if export == True:
            with open(f"{self.downloadFolder}/exportList.json", "w") as f:
                json.dump(self.result, f, indent=4)
        self.threadsEnqueue = staticFunc.assignThreads(self.result, self.threadNum, self.debug)
        if self.debug == False:
            self.progressBarInit()
        with ThreadPoolExecutor() as executor:
            [threads.append(executor.submit(self.runTask, threadEnqueue)) for threadEnqueue in self.threadsEnqueue]
            concurrent.futures.wait(threads)
            executor.shutdown()
        return threads
