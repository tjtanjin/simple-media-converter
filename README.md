<p align="center">
  <img width=300 src="https://raw.githubusercontent.com/tjtanjin/simple-media-converter/master/assets/app_logo.png" />
  <h1 align="center">Simple Media Converter</h1>
</p>

<p align="center">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fmy-api.tjtanjin.com%3A2999%2Faggregator%2Fapi%2Fv1%2Fget%2Fsmc_files_converted" />
</p>

## Table of Contents
* [Introduction](#introduction)
* [Features](#features)
* [Technologies](#technologies)
* [Setup](#setup)
* [Deployment](#deployment)
* [Team](#team)
* [Contributing](#contributing)
* [Others](#others)

### Introduction
Simple Media Converter is a telegram bot that allows users to upload files (videos, images and even telegram stickers!) to have them converted to the format they desire. With support for a wide variety of formats, this bot brings about a lot of convenience for those looking to just make a simple file conversion! In fact, convenience is what drove me to embark on this project and I hope to add more functionalities and conversion types to the bot in the near future. You may check out the bot at the link below:
```
https://t.me/SimpleMediaConverterBot
```

### Features
Simple Media Converter currently accepts 3 types of input (videos, images and telegram stickers). Supported formats for each type can be found within the [.env.template](https://github.com/tjtanjin/simple-media-converter/blob/master/.env.template) file. By default, all supported formats are included within the template, but you can always remove any of the formats as desired.

If you require support for additional formats that are not yet available in the application, feel free to open an issue or even better, make a pull request and help make the project better!

### Technologies
Technologies used by Simple Media Converter are as below:
##### Done with:

<p align="center">
  <img height="150" width="150" src="https://logos-download.com/wp-content/uploads/2016/10/Python_logo_icon.png"/>
</p>
<p align="center">
Python
</p>

##### Project Repository
```
https://github.com/tjtanjin/simple-media-converter
```

### Setup
The following section will guide you through setting up your own Simple Media Converter (**[telegram](https://web.telegram.org/) account required**).
* First, head over to [BotFather](https://t.me/BotFather) and create your own telegram bot with the `/newbot` command. After choosing an appropriate name and telegram handle for your bot, note down the **bot token** provided to you.
* Next, `cd` to the directory of where you wish to store the project and clone this repository. An example is provided below:
```
$ cd /home/user/exampleuser/projects/
$ git clone https://github.com/tjtanjin/simple-media-converter.git
```
* Once the project has been cloned, `cd` into it and install required dependencies with the following command:
```
$ python3 -m pip install --no-cache-dir -r requirements.txt
```
* Following which, create (or copy) a `.env` file at the root of the project using the provided `.env.template`. In order to run the bot, the bare minimum that needs to be done is for you to replace the **BOT_TOKEN** variable within the `.env` file with the token you received from [BotFather](https://t.me/BotFather).
* You can also feel free to modify the other variables as you deem fit. Clear descriptions for the variables have been included in the `.env.template` file.
* Once you are done with configuration, you may then head to the root of the project and execute the following command to launch your bot:
```
$ python3 main.py
```
* If you wish to host your telegram bot online 24/7, do checkout the guide [here](https://gist.github.com/tjtanjin/ce560069506e3b6f4d70e570120249ed).

### Deployment
*to be updated*

### Team
* [Tan Jin](https://github.com/tjtanjin)

### Contributing
If you have code to contribute to the project, open a pull request and describe clearly the changes and what they are intended to do (enhancement, bug fixes etc). Alternatively, you may simply raise bugs or suggestions by opening an issue.

### Others
For any questions regarding the implementation of the project, please drop an email to: cjtanjin@gmail.com.
