import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

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

KEYWORD_RESPONSES = {
    "automata": "Those Who Freak Das",
    "3340": "Those Who Freak Das",
    "haul": "how about you haul yourself some bitches"
}

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    content = message.content.lower()

    for keyword, response in KEYWORD_RESPONSES.items():
        if keyword in content:
            await message.channel.send(response)
            break
    
    # example of targeting a specific users message
    TARGET_USER_ID = 123456789012345678
    if message.author.id == TARGET_USER_ID:
        if "exam" in content:
            await message.channel.send("Uh oh 👀")


    await bot.process_commands(message)


bot.run(TOKEN)
