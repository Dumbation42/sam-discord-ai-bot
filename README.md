# SAM, a fork of freeGPT-discord

Discord chatbot and image generator powered by freeGPT.

Join the SAM support server for help with setting up the bot, access to the official nsfw prompt blacklist, and access to beta updates.

https://discord.gg/gNvqqdzF

## Getting Started:

1. **Download the Source Code:** Start by downloading the bot's source code. ``git clone https://github.com/Dumbation42/sam-discord-ai-bot``

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
