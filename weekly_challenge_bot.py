import discord
from discord.ext import commands, tasks
import os

TOKEN = os.getenv("MTM5NDk0MjA2MDQ2MDc2OTQwMQ.GrJZ0E.BtS48GrH6YBXS_q3kopDjuTtSp2Mo-ZMOgSado")  # Secure token usage
CHANNEL_ID = 1394737075613335582  # Replace with your actual channel ID

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

challenges = [
    '🎯 Challenge 1: Velocity Sync Only\n🎞️ Use ONLY velocity syncing (no effects, no transitions).\n🧪 Tag: #velocityOnly',
    '🎯 Challenge 2: Text-Driven Edit\n📝 Use typography/dialogues as your main storytelling element.\n🧪 Tag: #textEdit',
    # (Add more challenges here...)
]

week_index = 0

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    post_challenges.start()

@tasks.loop(hours=168)  # Every 7 days
async def post_challenges():
    global week_index
    channel = bot.get_channel(CHANNEL_ID)
    start = (week_index * 3) % len(challenges)
    selected = challenges[start:start+3]
    
    for i, ch in enumerate(selected):
        embed = discord.Embed(
            title=f"📅 Weekly Challenge #{start + i + 1}",
            description=ch,
            color=0x00ffae
        )
        await channel.send(embed=embed)
    
    week_index += 1

bot.run(TOKEN)
