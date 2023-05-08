<p align="center">
  <img src="https://i.imgur.com/risLKv1.jpg" />
  <h1 align="center">Simple Media Converter</h1>
</p>

## Table of Contents
* [Introduction](#introduction)
* [Features](#features)
* [Technologies](#technologies)
* [Setup](#setup)
* [Team](#team)
* [Contributing](#contributing)
* [Others](#others)

### Introduction
Simple Media Converter is a telegram bot that allows users to upload files (videos, images even telegram stickers!) and to have them converted to the format they desire. With support for a wide variety of format, this bot brings about a lot of convenience for those looking to just make a simple file conversion! In fact, convenience is what drove me to embark on this project and I hope to add more functionalities and conversion types to the bot in the near future. You may check out the bot at the link below:
```
https://t.me/SimpleMediaConverterBot
```

### Features
Simple Media Converter currently accepts 3 types of input (videos, images and telegram stickers). The file format for each of these types are as list below:
##### Videos Supported Input:
```
.mp4
.webm
.gif
.avi
.flv
.mov
.mkv
```
##### Videos Supported Output:
```
.mp4
.webm
.gif
.avi
.flv
.mov
.mkv
```
##### Images Supported Input:
```
.png
.jpg
.tiff
.heif
.heic
```
##### Images Supported Output:
```
.png
.jpg
.tiff
.pdf
.webp
.ico
```
##### Static Telegram Stickers Output:
```
All Output Image Types Supported Above
```
##### Animated Telegram Stickers Output:
```
All Output Image/Video Types Supported Above
```

### Technologies
Technologies used by Simple Media Converter are as below:
##### Done with:

<p align="center">
  <img height="150" width="150" src="https://logos-download.com/wp-content/uploads/2016/10/Python_logo_icon.png"/>
</p>
<p align="center">
Python
</p>

##### Deployed on:
<p align="center">
  <img height="150" width="150" src="https://pbs.twimg.com/profile_images/1089877713408557056/aO_IAlp__400x400.jpg" />
</p>
<p align="center">
Upcloud
</p>

##### Project Repository
```
https://github.com/tjtanjin/simple-media-converter
```

### Setup
The following section will guide you through setting up your own Simple Media Converter (telegram account required).
* First, head over to [BotFather](https://t.me/BotFather) and create your own telegram bot with the /newbot command. After choosing an appropriate name and telegram handle for your bot, note down the bot token provided to you.
* Next, cd to the directory of where you wish to store the project and clone this repository. An example is provided below:
```
$ cd /home/user/exampleuser/projects/
$ git clone https://github.com/tjtanjin/simple-media-converter.git
```
* Following which, create a `config` folder and within it, create a `token.json` file, saving the token you received from [BotFather](https://t.me/BotFather) as a value to the key "token" as shown below:
```
{"token": "your bot token here"}
```
* You will also have to create 2 empty folders, input_media and output_media for processing users' sent files:
```
$ mkdir input_media
$ mkdir output_media
```
* Finally, from the base directory of the project, execute the following command and the terminal should print "running..." if everything has been setup correctly!
```
$ python3 main.py
```
* If you wish to host your telegram bot online 24/7, do checkout the guide [here](https://gist.github.com/tjtanjin/ce560069506e3b6f4d70e570120249ed).

### Team
* [Tan Jin](https://github.com/tjtanjin)

### Contributing
If you have code to contribute to the project, open a pull request and describe clearly the changes and what they are intended to do (enhancement, bug fixes etc). Alternatively, you may simply raise bugs or suggestions by opening an issue.

### Others
For any questions regarding the implementation of the project, please drop an email to: cjtanjin@gmail.com.
