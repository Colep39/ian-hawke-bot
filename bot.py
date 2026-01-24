import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import time
import logging
from discord.ext import tasks

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_ID = int(os.getenv("AI_SERVER_ID"))
USER_ID= int(os.getenv("SAM_USER_ID"))
GENERAL_CHANNEL_ID = int(os.getenv('GENERAL_CHANNEL_ID'))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# we don't want keyword spam, so we set a cooldown
KEYWORD_COOLDOWNS = {}
COOLDOWN_SECONDS = 30

# health monitoring
@tasks.loop(minutes=5)
async def heartbeat():
    logging.info("Heartbeat: bot is alive")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    logging.info("Bot started successfully")

    if not heartbeat.is_running():
        heartbeat.start()

    if not daily_reminder.is_running():
        daily_reminder.start()

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)



@tasks.loop(hours=167)
async def daily_reminder():
    channel_id = GENERAL_CHANNEL_ID
    channel = bot.get_channel(channel_id)

    if channel:
        await channel.send("Daily reminder: stay on top of your work!")


# /say command, usable by admins to anonymously send a message to any channel as the one and only Ian Hawke
@bot.tree.command(name="say", description="Make Ian Hawke say something anonymously")
@commands.has_permissions(administrator=True)
@app_commands.describe(
    message="What should Ian Hawke say?",
    channel="Which channel should the message be sent to?"
)
async def say(interaction: discord.Interaction, message: str, channel: discord.TextChannel):
    await interaction.response.send_message("Message sent ✅", ephemeral=True)
    await channel.send(message)

# /addkeyword command, usable by admins to add keyword responses
@bot.tree.command(name="addkeyword", description="Add a keyword response")
@commands.has_permissions(administrator=True)
@app_commands.describe(
    keyword="Word or phrase to listen for",
    response="Response Ian Hawke should send"
)
async def addkeyword(interaction: discord.Interaction, keyword: str, response: str):
    KEYWORD_RESPONSES[keyword.lower()] = response
    await interaction.response.send_message(
        f"Keyword `{keyword}` added ✅",
        ephemeral=True
    )

@bot.tree.command(name="removekeyword", description="Remove a keyword response")
@commands.has_permissions(administrator=True)
@app_commands.describe(keyword="Keyword to remove")
async def removekeyword(interaction: discord.Interaction, keyword: str):
    removed = KEYWORD_RESPONSES.pop(keyword.lower(), None)

    if removed:
        await interaction.response.send_message(
            f"Keyword `{keyword}` removed 🗑️",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            f"Keyword `{keyword}` not found ❌",
            ephemeral=True
        )

KEYWORD_RESPONSES = {
    "automata": "Those Who Freak Das",
    "3340": "Those Who Freak Das",
    "haul": "how about you haul yourself some bitches",
    "CS": "bingo bango bongo, bish bash bosh",
    "john": "those who John Barnes",
    "barnes": "those who John Barnes",
    "follow": "those who follow",
    "everybody follows": "those who follow",
}

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    content = message.content.lower()

    current_time = time.time()

    for keyword, response in KEYWORD_RESPONSES.items():
        if keyword in content:
            last_used = KEYWORD_COOLDOWNS.get(keyword, 0)

            if current_time - last_used >= COOLDOWN_SECONDS:
                await message.channel.send(response)
                KEYWORD_COOLDOWNS[keyword] = current_time

            break

    
    # example of targeting a specific users message
    TARGET_USER_ID = USER_ID # a certain persons discord ID
    if message.author.id == TARGET_USER_ID:
        if "exam" in content:
            await message.channel.send("Uh oh 👀")


    await bot.process_commands(message)


bot.run(TOKEN)
