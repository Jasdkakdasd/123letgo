import discord
import random
import asyncio
from flask import Flask
from threading import Thread

# ==============================
# 🔥 CONFIG (ตั้งค่าต่างๆ)
TOKEN = "YOUR_BOT_TOKEN"  # 🔑 ใส่โทเค็นบอทตรงนี้
TARGET_CHANNEL_ID = 123456789012345678  # 📝 ใส่ไอดีห้องแชทที่ต้องการให้บอททำงาน
MUSIC_BOTS = [881638722487324722, 123456789012345678, 987654321098765432]  # 🎵 ใส่ไอดีบอทเพลงที่ต้องการเตะ
DELAY_KICK = 2  # ⏳ ตั้งเวลาดีเลย์ก่อนเตะ (วินาที)

# ==============================
# 🤖 ตั้งค่า Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.voice_states = True  # ให้บอทเห็นว่าใครอยู่ในช่องเสียง

client = discord.Client(intents=intents)

# ==============================
# 🤬 คำด่ากวนตีนๆ
curse_words = [
    "เปิดบอทเพลงพ่อง 💩", 
    "เปิดทำไม บอทมีชีวิตเหรอ 🐵", 
    "เสียงมึงไม่เพราะเอง แล้วโทษบอท? 🤡", 
    "ฟังเสียงตัวเองไปก่อนเถอะ 😆", 
    "เปิดบอททุกวัน บ้านมึงไม่มีเพลงฟังเหรอ 🎧"
]

# ==============================
# 🌐 ระบบ Keep Alive (กันบอทดับบน Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ==============================
# 🎧 ฟังก์ชันตรวจจับและเตะบอทเพลง
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # ไม่ตอบข้อความตัวเอง

    if message.channel.id == TARGET_CHANNEL_ID:
        if "m!p" in message.content.lower() or "เปิดบอทเพลง" in message.content.lower():
            try:
                await message.delete()  # ลบข้อความ
                response = random.choice(curse_words)  # สุ่มคำด่า
                await message.channel.send(response)  # ส่งคำด่า 🤣

                # ✅ เช็คทุกช่องเสียงว่ามีบอทในลิสต์ไหม
                for vc in message.guild.voice_channels:
                    for member in vc.members:
                        if member.id in MUSIC_BOTS:
                            await asyncio.sleep(DELAY_KICK)  # ดีเลย์ 2 วินาที
                            await member.move_to(None)  # เตะบอทออกจากช่องเสียง
                            print(f"🔊 เตะ {member.name} ออกจาก {vc.name}")
                            await message.channel.send(f"👢 เตะ {member.name} ออกจากช่องเสียง!")

            except discord.Forbidden:
                print("❌ บอทไม่มีสิทธิ์ลบข้อความหรือเตะบอท")
            except discord.HTTPException:
                print("⚠️ มีปัญหาในการลบข้อความหรือเตะบอท")

# ==============================
# 🚀 รันบอท + กันบอทดับ
keep_alive()  # เปิดเซิร์ฟ Flask กันบอทดับ
client.run(TOKEN)  # รันบอท
