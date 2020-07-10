# Twitch Bot

### Getting Started
Read [this tutorial](https://dev.to/ninjabunny9000/let-s-make-a-twitch-bot-with-python-2nd8) to get all the things you will need before the Python begins. The list includes:
 - A Twitch account that you will setup with an OAuth code and register with Twitch dev
 - Python (I use 3.8 currently)
 - A `.env` file that contains your secrets (**DON'T PUSH IT TO GIT**)
 - A working directory setup with `pipenv`

There are a few issues with the tutorial that I will try and help you with here.

1) The `.env` file should look like this:
```
# .env
TMI_TOKEN=oauth:<oauth_token>
CLIENT_ID=<client_id>
BOT_NICK=<bot_username>
BOT_PREFIX=!
CHANNEL=#<channel_name>
```
The OAuth and client ID are pretty self-explanatory, but the `BOT_NICK` is a badly named variable. It seems to want the username of the account you linked with Twitch dev. Also, the `CHANNEL` needs to be prefixed with a '#'.

2) The following tip only applies if you'll be working in VSCode. My `PATH` did not include some of the binaries that I needed to download (Python, Git), so the integrated terminal in VSCode was telling me that they couldn't be found. You can change that by going to File -> Preferences -> Settings -> Features -> Terminal -> `Integrated > Env:Windows`. Open the `.json` file for editing. Get your current `PATH` env variable by running `$ENV:PATH` in the integrated Powershell terminal in VSCode. Then, edit the `.json` file to be like this (making sure to delimit the ' \\ ' characters):
```
"terminal.integrated.env.windows": {
    "PATH": "<your_current_PATH>;C:\\Other\\EXE\\Path"
    },
```
3) If you manage to get all of that working, and are trying to follow the tutorial yourself instead of using my code, then there comes a part where you are told to run `pipenv run python bot.py` before telling the bot to do anything but `bot.run()`. It will look like it's hanging. If after approx. 30 seconds you haven't gotten an error, then you're fine and it's connecting, but not doing anything to let you know it's working.