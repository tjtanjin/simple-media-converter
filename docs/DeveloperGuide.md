<p align="center">
  <img width=300 src="https://raw.githubusercontent.com/tjtanjin/simple-media-converter/master/assets/app_logo.png" />
  <h1 align="center">Simple Media Converter (Developer Guide)</h1>
</p>

## Table of Contents
* [Introduction](#introduction)
* [Navigating this Developer Guide](#navigating-this-developer-guide)
* [Design](#design)
* [Implementation](#implementation)
* [Code Documentation](#code-documentation)
* [Testing](#testing)
* [Final Notes](#final-notes)

<div  style="page-break-after: always;"></div>

## Introduction
First and foremost, if you have yet to go through the project [*README*](https://github.com/tjtanjin/simple-media-converter/blob/master/README.md), then please spare some time on it to give yourself an overview on the project before proceeding.

This developer guide assumes its readers to have at least a **basic understanding** of [Python](https://www.python.org/) and [Python Telegram Bot](https://python-telegram-bot.org/). Otherwise, it is highly recommended for readers to refer to proper tutorial contents for the basics of Python/Python Telegram Bot prior to developing the application. It is also worth noting that this guide serves to cover **chosen/important design considerations** for the project. The designs are not perfect so you are encouraged to **think and explore possible improvements** for the application.

This guide **will not** dive into every single project detail because that is not sustainable in the long run. For simpler implementations that are not covered in this guide, you will find the code comments in the files themselves to be useful.

Finally, to setup the development environment, please refer to the section on [**setup**](https://github.com/tjtanjin/simple-media-converter/blob/master/README.md#setup) in the project [*README*](https://github.com/four-city/fourcity-cms/blob/master/README.md).

  

## Navigating this Developer Guide
Before diving into the rest of the contents in our developer guide, the following are a few important syntaxes to take note of to facilitate your reading:

| Syntax               | Description                                                                       |
|----------------------|-----------------------------------------------------------------------------------|
| `Markdown`           | Denotes functions/commands (e.g. `create_group`, `create_user`, `/start`)         |    
| *Italics*            | Denotes folders/files in the projects (e.g. *main.py*, *services*)                |                                
| **Bold**             | Keywords that are emphasized                                                      |

<div  style="page-break-after: always;"></div>

## Design
### Overview
At a high level overview, the entire project can be (broadly speaking) broken down into **4 components** that are as follows:

- *interactions*
- *services*
- *ui*
- *assets*

If you have taken a look at the project file structure, you would have noticed that the above 4 components are seated in their own folder, making it relatively straightforward to follow.

#### How do the different parts interact with each other?
Let's first begin with an overview before we get a better appreciation for each individual component later in the guide. For a start, *interactions*, as its name suggest, is where handling of user interactions with the bot is done. Sometimes, the bot will show buttons for users to respond with and the creation of these buttons would then fall under the category of *ui*. As the user interacts with the bot, there may be a need to do some processing (such as media conversions) and these processes are handled by *services*. Finally, **non-code related** (yet still imporant) files such as app logo and language translations are kept within the *assets*. Below, we will take a more detailed look at each component.

Note: When dealing with specific features, it is still advisable to **consult code documentation** found within the files themselves for the most accurate information.

### Interactions
Among the 4 components, *interactions* is the **largest and most extensive**. Within this component, we distinguish between **2 types** of interactions:

- *commands*
- *uploads*

As the purpose of this bot is for users to upload and convert files, majority of the *interactions* belong to the category of *uploads* while there are only **2 available *commands***. The `/start` command simply welcomes the user to the bot while the `/help` command shows the user a detailed help message. In both of these instances, there is also no need for the user to provide further feedback/reply.

On the other hand, there currently **4 types of *uploads***. Eager-eyed readers may have noticed that this differs from the **3 types of input** that was stated in the [*README*](https://github.com/four-city/fourcity-cms/blob/master/README.md). The reason for this perceived 'discrepancy' is owing to the *documents* upload which was **not distinguished for users**. 

To understand why there is this difference, we first need to understand that **telegram handles images differently when it is uploaded as an attachment vs when it is dragged and dropped** into the chat. In the case of the former, telegram receives the upload as a document, not as an image. In order to provide users with a seamless experience, there is no need for them to know about the different ways telegram treats user uploads. However, a developer would need to know of these differences and handle them accordingly in order to deliver the best experience.

That said, each command/upload belongs to its own file and important details of their individual implementations may be found **within the code files** themselves.

Finally, all interactions are initialized within *loader.py* file and a lightweight *utils.py* contains miscellaneous functions for cleaning up interactions (e.g. timeouts).

### Services
While *interactions* deal with the bulk of interactions between the user and the bot, the *services* component deal with the **backend details** such as parsing messages to return to the user and performing media conversions. You can think of each file here as a utility folder to perform very specific tasks.

### UI
As the application is rather small, the *ui* component is merely responsible for **creating buttons** that users can interact with. This is done within a single *builder.py* file that contains a handful of helper functions to build the menu for users.

### Assets
Last but not least, the *assets* folder contains non-code related files that are nonetheless still important for the proper functioning of the application. These include the app logo as well as language translation files that are found within the *lang* folder.

A quick glance at the language files, and you will notice many key-value pairs within the files associating a key with a translation in the specified language. As such, adding a new language is actually **very easy**. In fact, the tedious part would be the translation (google translating all of them is a good shortcut but it may not be accurate). The default language is **English (en-US)** and the loading of languages are handled in the *.env* file by the **LANGUAGE** variable.

## Implementation
As this is a lightweight application, there aren't really any significant implementation details to note. We will just look at 2 implementation details but you are free to reach out if you require clarifications anywhere else in the app.

### Media Conversions
Although there are 4 types of uploads, there are only **3 types of media conversions** that the app handles (document is processed into one of the 3 types):

- *images*
- *videos*
- *telegram stickers*

To carry out the conversions, several libraries are used.

To convert between images, **Pillow** (PIL) is used and to convert between videos, **ffmpy** is used. Lastly, telegram sticker conversions may utilize the **rlottie_python** library (or a combination of the previous libraries) depending on the output choice from the user. There is also the **pyheif** library that specifically only deals with HEIF/HEIC images.

It is also worth noting that while media conversions are being carried out, the *ui* component constantly displays a small loader to the user to indicate that the media processing is still being done.

### Dynamic Help Message
The help message is suppose to show a list of available input/output types to users categorized into images, videos and stickers. However, depending on the configurations within the *.env* file, the allowed types would have to be adjusted accordingly.

Thankfully, there is no need to manually update the help message as it reads the configurations and generates the corresponding help message on start. This is trivial work but be cautious when working in this area as even the smallest changes may throw off the entire formatting of the help message.

## Code Documentation
Code documentation is strongly encouraged to ensure that the codebase can be easily maintainable. As a rule of thumb, all `.py` files should have a description of what it does at the top of the file where it is declared.

Functions can be without documentation if they are small, self-explanatory and easy to understand by just looking at the code alone. For larger functions with more logic, it is still advisable to write code comments. In general, the following structure is adopted for writing comments:

```
def convert_image(chat_id, input_type, output_type):
    """
    Converts image of one type to another.
    Args:
        chat_id: use user id to identify image
        input_type: video input type
        output_type: video output type
    """
    <actual code begins...>
"""
```

The above shows an example of a function converting an image from one type to another. Note that it begins with a brief description of what the function does followed by highlighting its 3 parameters and what they are used for. You may look into any of the code files for more examples.

Finally, any leftover tasks or areas in the code to be revisited should be flagged with a comment like the one below:

```
// todo: tj to optimize the calculation code here
```

That way, we can identify what are the tasks to finish up here an optionally, who will be responsible for it.

## Testing
Unfortunately, I have yet to find an ideal way to test telegram bots. However, this section was still created to highlight the importance of needing test cases. I hope to develop a suite of test cases in the future as further improvements for this project.

## Final Notes
The designs in this project are not perfect. Developers are strongly encouraged to continuously seek out area for improvements in the application. I am also always happy to hear about suggestions and feedback, so feel free to reach out!