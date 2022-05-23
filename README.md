# Discord React Bot
Have you ever wanted to express how deeply you appreciate your friends? 
With this tool you can totally do it! Imagine your friend waking up and 
seeing that all his messages are covered with the chosen emotes, just 
like that:

![alt text](https://github.com/savkorlev/discord_reactbot/blob/main/Cutie.png?raw=true)

How cute! :3


## Prerequisites
[Python 3](https://www.python.org/) is needed to run the script.

[Selenium](https://www.selenium.dev/) is the only additional module that is 
used in the script. If you have Selenium installed you can skip the setting 
up step.

## Setting up

### Installing the modules
Open the Windows Command Prompt and type in:
```python
cd "path/to/a/script/folder"
pip install -r requirements.txt
```

### Adding the required emojis to favourites
To insure that the script is running correctly you need to add all the 
emojis you want to put to favourites in discord. To do that right click 
the emoji and click "add to favourites".

## Running the software
After the set up is done, type in:
```python
python main.py
```

## Remarks and limitations

### First
Limitations, extensions and improvements potential: Check the TODOs.

### Second
Current precision level for sleeping time is 0.5 seconds. 
Current step is 1.5 seconds.
