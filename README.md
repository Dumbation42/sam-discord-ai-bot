# SAM, a fork of freeGPT-discord

Discord chatbot and image generator powered by freeGPT.

Join the SAM support server for help with setting up the bot and access to beta updates.

https://discord.gg/gNvqqdzF

## Getting Started:

1. **Download the Source Code:** Start by downloading the bot's source code.

2. **Install Dependencies:** Open your terminal and run:
```pip install -r requirements.txt```
this might not install everything, in that case run the script and install the dependancys until it quits giving errors
3. **Application Setup:**
    - Create a new application on the [Discord Developer Portal](https://discord.com/developers).
    - In the app's settings, enable the `message content` intent and copy the token.

4. **Get your Huggingface token:** Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) and create a token with 'Read' role and copy it.

5. **Add Your Bot Token and Huggingface Token:** Paste the copied tokens in bot.py:
  ```python
  HF_TOKEN = "yourHuggingFaceToken"
  TOKEN = "yourBotToken"
  ```

6. **Run the Bot:** Open your terminal and run:
```cd sam-discord-ai-bot/src ```
```python bot.py```

# Difference between freeGPT-discord and SAM
- One of my largest issues with the original project was its lack of content filtering on image generation, allowing for anything, including illegal content, to be created. The initial reasoning behind this fork was to fix this issue by creating a blacklist that is compared to any prompt given to the image generator. If anything on the list is found in the prompt, the prompt is discarded before any image generation actually begins. (Please note that this method is not the best and a better solution is in the works. If something on the list is found within a word (a** in massive), then the prompt still gets detected as matching with blacklist)

- SAM-based discord bots are able to have more personality in their responses. There is a "prefix" variable created to be inserted right before this prompt. While anything can go in there, the purpose of the variable is to allow for you to ask the ai to respond in a certain way (example: respond as if you were a kind gentleman from great britain during the renaissance era)

- SAM bots have the ability to be pinged, and respond as if the /ask command was used.
