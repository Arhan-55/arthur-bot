import discord
from discord.ext import commands, tasks
import os

TOKEN = os.getenv("MTM5NDk0MjA2MDQ2MDc2OTQwMQ.GrJZ0E.BtS48GrH6YBXS_q3kopDjuTtSp2Mo-ZMOgSado")  # Secure token usage
CHANNEL_ID = 1394737075613335582  # Replace with your actual channel ID

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

challenges = [
    # Week 1
    '🎯 Challenge 1: Velocity Sync Only\n🎞️ Use ONLY velocity syncing (no effects, no transitions).\n🧪 Tag: #velocityOnly',
    '🎯 Challenge 2: Text-Driven Edit\n📝 Use typography/dialogues as your main storytelling element.\n🧪 Tag: #textEdit',
    '🎯 Challenge 3: No SFX Challenge\n🔇 Make an edit WITHOUT any sound effects.\n🧪 Tag: #noSFX',

    # Week 2
    '🎯 Challenge 4: Anime Reaction-Only Edit\n🎭 Use only anime reaction shots (shock, cry, smirk).\n🧪 Tag: #reactionEdit',
    '🎯 Challenge 5: No Anime Challenge\n❌ Make an edit using non-anime footage (movies, games, etc).\n🧪 Tag: #noAnime',
    '🎯 Challenge 6: 1 Color Grading Masterpiece\n🎨 Build your entire edit around ONE color tone.\n🧪 Tag: #monoGrade',

    # Week 3
    '🎯 Challenge 7: Mobile Only\n📱 Make your edit using only a mobile app (CapCut, VN, etc).\n🧪 Tag: #mobileBeast',
    '🎯 Challenge 8: Cursed Sync Challenge\n🤯 Sync your edit to a weird/cursed sound.\n🧪 Tag: #cursedSync',
    '🎯 Challenge 9: Zoom Transitions Only\n🔍 Use ONLY zoom transitions.\n🧪 Tag: #zoomOnly',

    # Week 4
    '🎯 Challenge 10: Edit with No Cuts\n✂️ Create a long single-shot edit (no cuts).\n🧪 Tag: #noCutEdit',
    '🎯 Challenge 11: Sync to Dialogues\n🗣️ Cut your edit to the rhythm of dialogue instead of music.\n🧪 Tag: #dialogueSync',
    '🎯 Challenge 12: Cinematic Trailer Style\n🎬 Make an edit like a dramatic movie trailer.\n🧪 Tag: #trailerEdit'
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
