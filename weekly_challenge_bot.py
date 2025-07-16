import discord
import json
from discord.ext import commands, tasks
import os

TOKEN = os.getenv("TOKEN")  # Secure token usage
CHANNEL_ID = 1394737075613335582  # Replace with your actual channel ID

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def current_tags():
    start = (week_index * 3) % len(challenges)
    return [extract_tag(c) for c in challenges[start:start+3]]

def extract_tag(challenge_text):
    lines = challenge_text.split('\n')
    for line in lines:
        if '🧪 Tag:' in line:
            return line.split(':')[1].strip()
    return None

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

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == CHALLENGE_UPLOAD_CHANNEL_ID:
        content = message.content.lower()

        for tag in current_tags():  # ← we'll define this in a sec
            if tag.lower() in content:
                await award_xp(message.author, tag)
                await message.add_reaction("✅")
                break

    await bot.process_commands(message)

XP_FILE = "user_xp.json"

def load_xp():
    if os.path.exists(XP_FILE):
        with open(XP_FILE, "r") as f:
            return json.load(f)
    return {}

def save_xp(data):
    with open(XP_FILE, "w") as f:
        json.dump(data, f)

async def award_xp(user, tag):
    xp_data = load_xp()
    user_id = str(user.id)
    if user_id not in xp_data:
        xp_data[user_id] = 0

    xp_data[user_id] += 10  # XP per challenge
    save_xp(xp_data)

    try:
        await user.send(f"✅ Great job completing `{tag}` challenge! You've earned 10 XP.")
    except:
        pass

CHALLENGE_UPLOAD_CHANNEL_ID = YOUR_CHANNEL_ID  # Replace with actual uploads channel ID

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == CHALLENGE_UPLOAD_CHANNEL_ID:
        content = message.content.lower()

        for tag in current_tags():
            if tag.lower() in content:
                await award_xp(message.author, tag)
                await message.add_reaction("✅")
                break

    await bot.process_commands(message)

@bot.command()
async def xp(ctx):
    xp_data = load_xp()
    user_id = str(ctx.author.id)
    xp = xp_data.get(user_id, 0)
    await ctx.send(f"🌟 {ctx.author.display_name}, you have `{xp}` XP.")

bot.run(TOKEN)
