import discord
from discord import app_commands
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import time
import logging
import datetime

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_ID = int(os.getenv("AI_SERVER_ID"))
USER_ID = int(os.getenv("SAM_USER_ID"))
GENERAL_CHANNEL_ID = int(os.getenv("GENERAL_CHANNEL_ID"))
JESTER_ID = int(os.getenv("JESTER_USER_ID"))

BOT_VERSION = "1.2.2"
START_TIME = datetime.datetime.now(datetime.timezone.utc)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# we don't want keyword spam, so we set a cooldown
KEYWORD_COOLDOWNS = {}
COOLDOWN_SECONDS = 10

KEYWORD_RESPONSES = {
    "automata": "Those Who Freak Das",
    "3340": "Those Who Freak Das",
    "haul": "how about you haul yourself some bitches",
    "cs": "bingo bango bongo, bish bash bosh",
    "john": "those who John Barnes",
    "barnes": "those who John Barnes",
    "follow": "those who follow",
    "everybody follows": "those who follow",
    "database": "Uma my beloved",
}

# --- single-message reply guard (helps prevent accidental double sends per message) ---
PROCESSED_MESSAGE_IDS = {}
PROCESSED_TTL_SECONDS = 60


def _seen_recently(message_id: int) -> bool:
    now = time.time()
    # cleanup old ids
    expired = [mid for mid, ts in PROCESSED_MESSAGE_IDS.items() if now - ts > PROCESSED_TTL_SECONDS]
    for mid in expired:
        PROCESSED_MESSAGE_IDS.pop(mid, None)

    if message_id in PROCESSED_MESSAGE_IDS:
        return True

    PROCESSED_MESSAGE_IDS[message_id] = now
    return False


# health monitoring
@tasks.loop(minutes=5)
async def heartbeat():
    logging.info("Heartbeat: bot is alive")


@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user} (pid={os.getpid()})")
    logging.info("Bot started successfully")

    # Dynamic status showing version
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"v{BOT_VERSION}",
        )
    )

    if not heartbeat.is_running():
        heartbeat.start()

    try:
        synced = await bot.tree.sync()
        logging.info(f"Synced {len(synced)} commands")
    except Exception as e:
        logging.exception(e)


# /say command
@bot.tree.command(name="say", description="Make Ian Hawke say something anonymously")
@commands.has_permissions(administrator=True)
@app_commands.describe(
    message="What should Ian Hawke say?",
    channel="Which channel should the message be sent to?",
)
async def say(interaction: discord.Interaction, message: str, channel: discord.TextChannel):
    await interaction.response.send_message("Message sent", ephemeral=True)
    await channel.send(message)


# /version command
@bot.tree.command(name="version", description="Check bot version and uptime")
async def version(interaction: discord.Interaction):
    uptime = datetime.datetime.now(datetime.timezone.utc) - START_TIME
    uptime_str = str(uptime).split(".")[0]

    await interaction.response.send_message(
        f"**Ian Hawke**\n"
        f"Version: `{BOT_VERSION}`\n"
        f"Uptime: `{uptime_str}`",
        ephemeral=True,
    )


# /addkeyword command
@bot.tree.command(name="addkeyword", description="Add a keyword response")
@commands.has_permissions(administrator=True)
@app_commands.describe(
    keyword="Word or phrase to listen for",
    response="Response Ian Hawke should send",
)
async def addkeyword(interaction: discord.Interaction, keyword: str, response: str):
    KEYWORD_RESPONSES[keyword.lower()] = response
    await interaction.response.send_message(f"Keyword `{keyword}` added", ephemeral=True)


# /removekeyword command
@bot.tree.command(name="removekeyword", description="Remove a keyword response")
@commands.has_permissions(administrator=True)
@app_commands.describe(keyword="Keyword to remove")
async def removekeyword(interaction: discord.Interaction, keyword: str):
    removed = KEYWORD_RESPONSES.pop(keyword.lower(), None)

    if removed:
        await interaction.response.send_message(f"Keyword `{keyword}` removed", ephemeral=True)
    else:
        await interaction.response.send_message(f"Keyword `{keyword}` not found", ephemeral=True)


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # Guard against accidental double-processing within the same process
    if _seen_recently(message.id):
        return

    content = message.content.lower()
    now = time.time()

    # targeting a specific user (we know who)
    if message.author.id == USER_ID:
        if "exam" in content:
            await message.channel.send("Sam will fail his exams lol")
            await bot.process_commands(message)
            return
        elif "task" in content:
            await message.channel.send("Sam is cooked for this task")
            await bot.process_commands(message)
            return
        elif "cole" in content:
            await message.channel.send("Keep my sons name out of your mouth!")
            await bot.process_commands(message)
            return
        elif any(word in content for word in ["calculate", "calculator", "math", "numbers", "number", "numerical"]):
            await message.channel.send("Sam wishes he could calculate those numbers like Santi does")
            await bot.process_commands(message)
            return

        
    if message.author.id == JESTER_ID:
        if "eick" in content:
            await message.channel.send("Jester does not follow")
            await bot.process_commands(message)
            return
        elif "sam" in content:
            await message.channel.send("Jester is a simp for Sam")
            await bot.process_commands(message)
            return
        elif "cole" in content:
            await message.channel.send("Jester wishes he was Cole")
            await bot.process_commansd(message)
            return
    
    # keyword responses with cooldown
    for keyword, response in KEYWORD_RESPONSES.items():
        if keyword in content:
            last_used = KEYWORD_COOLDOWNS.get(keyword, 0)
            if now - last_used >= COOLDOWN_SECONDS:
                await message.channel.send(response)
                KEYWORD_COOLDOWNS[keyword] = now
            await bot.process_commands(message)
            return

    await bot.process_commands(message)


bot.run(TOKEN)
