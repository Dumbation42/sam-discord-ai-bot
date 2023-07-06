import asyncio
import discord
import freeGPT
import aiosqlite
from discord.ext import commands
from discord import app_commands


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="i don't want to set one...", intents=intents, help_command=None
)

models = ["gpt3", "gpt4", "alpaca_7b"]
db = None


@bot.event
async def on_ready():
    """
    Performs necessary actions when the bot is ready.
    """
    global db
    db = await aiosqlite.connect("database.db")
    async with db.cursor() as cursor:
        await cursor.execute(
            "CREATE TABLE IF NOT EXISTS datastorage(guilds INTEGER, channels INTEGER, model TEXT)"
        )
    await db.commit()
    print(f"{bot.user.name} connected to Discord.")
    sync_commands = await bot.tree.sync()
    print(f"Synced {len(sync_commands)} command(s).")
    while True:
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(bot.guilds)} servers | /help",
            ),
        )
        await asyncio.sleep(300)


@bot.tree.command(name="help", description="Get help.")
async def help(interaction):
    """
    Sends an embed with bot information.
    """
    embed = discord.Embed(
        title="Help Menu",
        description=f"Available models: `{', '.join(models)}`",
        color=0x00FFFF,
    )
    embed.add_field(
        name="setup",
        value="Usage: `/setup {model}`",
    )
    embed.add_field(name="reset", value="Usage: `/reset`")
    embed.set_footer(text="Powered by https://github.com/Ruu3f/freeGPT")
    view = discord.ui.View()
    view.add_item(
        discord.ui.Button(
            label="Invite Me",
            url="https://dsc.gg/freeGPT",
        )
    )
    view.add_item(
        discord.ui.Button(
            label="Server",
            url="https://discord.gg/XH6pUGkwRr",
        )
    )
    view.add_item(
        discord.ui.Button(
            label="Source Code",
            url="https://github.com/Ruu3f/freeGPT-discord-bot",
        )
    )
    await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(name="setup", description="Setup the chatbot.")
@app_commands.checks.has_permissions(manage_channels=True)
@app_commands.checks.bot_has_permissions(manage_channels=True)
@app_commands.describe(model=f"Model to use. Choose between {', '.join(models)}")
async def setup(interaction, model: str):
    """
    Set up the chatbot.
    """
    if model.lower() not in models:
        await interaction.response.send_message(
            f"**Error:** Model not found! Choose a model between `{', '.join(models)}`."
        )
        return

    cursor = await db.execute(
        "SELECT channels, model FROM datastorage WHERE guilds = ?",
        (interaction.guild.id,),
    )
    data = await cursor.fetchone()
    if data:
        await interaction.response.send_message(
            "**Error:** The chatbot is already set up. Use the `/reset` command to fix this error."
        )
        return

    if model.lower() in models:
        channel = await interaction.guild.create_text_channel(
            f"{model}-chat", slowmode_delay=10
        )

        await db.execute(
            "INSERT OR REPLACE INTO datastorage (guilds, channels, model) VALUES (?, ?, ?)",
            (
                interaction.guild.id,
                channel.id,
                model,
            ),
        )
        await db.commit()
        await interaction.response.send_message(
            f"**Success:** The chatbot has been set up. The channel is {channel.mention}."
        )
    else:
        await interaction.response.send_message(
            f"**Error:** Model not found! Choose a model between `{', '.join(models)}`."
        )


@bot.tree.command(name="reset", description="Reset the chatbot.")
@app_commands.checks.has_permissions(manage_channels=True)
async def reset(interaction):
    """
    Resets the chatbot.
    """
    cursor = await db.execute(
        "SELECT channels, model FROM datastorage WHERE guilds = ?",
        (interaction.guild.id,),
    )
    data = await cursor.fetchone()
    if not data:
        await interaction.response.send_message(
            "**Error:** The chatbot is not set up. Use the `/setup` command to fix this error."
        )
        return

    await db.execute(
        "DELETE FROM datastorage WHERE guilds = ?", (interaction.guild.id,)
    )
    await db.commit()
    await interaction.response.send_message("**Success:** The chatbot has been reset.")


@bot.event
async def on_message(message):
    """
    Reply to the message if the bot is set up.
    """
    if message.author == bot.user:
        return

    cursor = await db.execute(
        "SELECT channels, model FROM datastorage WHERE guilds = ?", (message.guild.id,)
    )
    data = await cursor.fetchone()
    if data:
        channel_id, model = data
        if message.channel.id == channel_id:
            await message.channel.edit(slowmode_delay=10)
            async with message.channel.typing():
                try:
                    resp = await getattr(freeGPT, model.lower()).Completion.create(
                        prompt=message.content
                    )
                    await message.reply(resp)
                except Exception:
                    await message.reply(Exception)


TOKEN = ""
asyncio.run(bot.run(TOKEN))
