# ytDownloader_Terminal

# About this project

This project aims to provide users the functionality to download YouTube videos from CLI to any formats that they want

# Installation

## Installing for Audio + Video usage

Installation is fairly simple! Just run the command below to install all necessary python modules needed to run this project. ****You will need to install additional software if you are planning on downloading video!***

```bash
pip3 install -r .\ASCII_Bad_Apple_Remastered\requirements.txt
```

## Video usage

This program requires ffmpeg to handle video + audio streams!

Install ffmpeg: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

# Program Documentation

## General Flags

Possible flags to include the flag ****-v****:

```bash
python .\ytDownloader_Terminal\ [-l] [-t] [-d] [-f] [-v] [-db]
```

```bash
* = Arg required
type = <argument type>
() = Comments

  -h, --help            show this help message and exit

* type = <string> (Youtube link has to be public/unlisted and could be either single/playlist)
  -l LINK, --link LINK  Youtube link | i.e: "https://www.youtube.com/watch?v=someRandomVideo"
```

## Audio Download

Here are the flags that could be used for audio download:

```bash
python .\ytDownloader_Terminal\ [-l] [-t] [-d] [-f] [-db]
```

### Flags

```bash
* = Arg required
type = <argument type>
() = Comments

	* type = int (Make sure to not lag out your computer by setting a high value for this one)
	-t THREADS, --threads THREADS
                        Number of threads when downloading YouTube links | Default: 4

	* type = <string> (Download path for files)
  -d DOWNLOADPATH, --downloadPath DOWNLOADPATH
                        Include custom download path | Default: C:\YOUR_PATH_TO_FOLDER/ytDownloader_Terminal/Downloads

	* type = <string> (File extensions could impact sound + video quality due to lossy/lossless compression)
  -f EXTENSION, --extension EXTENSION
                        Extension for output file

	(Disables tqdm loading bars and replace it with text)
  -db, --debug          Enable debug | Default: False
```

## Video Download

To download video, include the

```bash
python .\ytDownloader_Terminal\ -v [-l] [-t] [-d] [-f] [-db]
```

Flags

```bash
* = Arg required
type = <argument type>
() = Comments

	* type = int (Make sure to not lag out your computer by setting a high value for this one)
	-t THREADS, --threads THREADS
                        Number of threads when downloading YouTube links | Default: 4

	* type = <string> (Download path for files)
  -d DOWNLOADPATH, --downloadPath DOWNLOADPATH
                        Include custom download path | Default: C:\YOUR_PATH_TO_FOLDER/ytDownloader_Terminal/Downloads

	* type = <string> (File extensions could impact sound + video quality due to lossy/lossless compression)
  -f EXTENSION, --extension EXTENSION
                        Extension for output file

  -v, --video           Change default audio download to video | Default: False

	(Disables tqdm loading bars and replace it with text)
  -db, --debug          Enable debug | Default: False
```
