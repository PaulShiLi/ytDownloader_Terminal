from scripts.ytDownload import youtubeDownload
import argparse
import sys
import os

if "/" in str(os.getcwd()):
    sys.path.insert(0, f"{os.getcwd()}/ytDownloader_Terminal/scripts")
if "\\" in str(os.getcwd()):
    sys.path.insert(0, f"{os.getcwd()}\\ytDownloader_Terminal\\scripts")


def startDownload(ytLink, filetype, fileformat, downloadFolder, threadNum, debug, optionalAudio=None):
    outtmpl = f'{downloadFolder}/%(id)s.{fileformat}'
    print(outtmpl)
    input()
    if "\\" in str(os.getcwd()):
        outtmpl = f'{downloadFolder}\\%(id)s.{fileformat}'
    if filetype == "af":
        config = {
            'format': f'bestaudio[ext={fileformat}]/best',
            'extractaudio': True,
            'audioformat': fileformat,
            'audioquality': 0,
            'outtmpl': outtmpl,
            'restrictfilenames': True,
            'noplaylist': False,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            'noprogress': True
        }
    elif filetype == "vf":
        if optionalAudio == None:
            optionalAudio = "mp3"
        config = {
            'format': f'bv*[ext={fileformat}]+ba[ext={optionalAudio}]/b[ext={fileformat}]',
            'outtmpl': outtmpl,
            'restrictfilenames': True,
            'noplaylist': False,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
            'noprogress': True
        }
    youtubeDownload(config=config, url=ytLink, ext=fileformat, dlFolder=downloadFolder, threadNum=threadNum,
                    debug=debug)


def main():
    youtubeDownload(input("Enter your youtube link:\n"))


class parse:
    def read(args):
        argList = [str(args.read[n]) for n in len(args)]
        return argList

    def argSetup():
        # Create Parser Object
        parser = argparse.ArgumentParser(description="Youtube Downloader")

        # Defining arguments for the parser object
        parser.add_argument("-l", "--link", help="Youtube link | i.e: \"https://www.youtube.com/watch?v=someRandomVideo\"", type=str)
        parser.add_argument("-t", "--threads", default=4, help="Number of threads when downloading YouTube links | "
                                                               "Default: 4", type=int)
        parser.add_argument("-d", "--downloadPath", default=f"{os.getcwd()}/ytDownloader_Terminal/Downloads",
                            help=f"Include custom download path | Default: {os.getcwd()}/ytDownloader_Terminal/Downloads",
                            type=str)
        parser.add_argument("-f", "--extension", help=f"Extension for output file", type=str)
        parser.add_argument("-afv", "--audioext-video", help=f"Extension for video audio", type=str)
        parser.add_argument("-v", "--video", action='store_true', help="Change default audio download to video | "
                                                                       "Default: False")
        parser.add_argument("-db", "--debug", action='store_true', help="Enable debug | "
                                                                        "Default: False")

        # parse the arguments from standard input
        args = parser.parse_args()
        if args.video == True:
            if args.extension == None:
                args.extension = "mp4"
            if args.audioext_video == None:
                args.audioext_video = "mp3"
            startDownload(ytLink=args.link, filetype="vf", fileformat=args.extension, downloadFolder=args.downloadPath,
                          threadNum=args.threads, debug=args.debug, optionalAudio=args.audioext_video)
        else:
            if args.extension == None:
                args.extension = "mp3"
            startDownload(ytLink=args.link, filetype="af", fileformat=args.extension, downloadFolder=args.downloadPath,
                          threadNum=args.threads, debug=args.debug)


if __name__ == "__main__":
    parse.argSetup()
