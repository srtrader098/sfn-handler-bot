import random
import string
import datetime
import asyncio
import os
from telegram import Bot
from telegram.constants import ParseMode

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
BOT_USERNAME = "@SFN_MiningBot"
POST_INTERVAL = 1800

NAMES = [
    "Liam Smith", "Zayd V.", "Aarav Sharma", "Budi Santoso", "Rahul Das",
    "Siti Aminah", "John Doe", "Arjun Kapoor", "Rizky Pratama", "Tanvir Ahmed",
    "Nguyen Van An", "Adebayo Okafor", "Maria Santos", "Chen Wei", "Fatima Khan",
    "Somchai Prasert", "Aung Ko", "Rahim Uddin", "Karim Hossain", "Priya Patel",
    "Juan Dela Cruz", "Muhammad Ali", "Suresh Kumar", "Dewi Lestari", "Hasan Mahmud",
    "Ayesha Siddiqua", "Ravi Verma", "Nabila Putri", "Imran Khan", "Shakib Al Hasan",
    "David Miller", "Sarah Johnson", "Michael Brown", "Aisha Bello", "Omar Farooq",
    "Linh Tran", "Putra Wijaya", "Nurul Islam", "Sabbir Rahman", "Anika Tabassum"
]

NETWORKS = ["TON", "TRC20", "ERC20", "BNB Smart Chain (BEP20)", "SOL", "POL"]
ASSET = "USDT"

def generate_uid():
    return f"62{''.join(random.choices(string.digits, k=7))}"

def generate_txid():
    return ''.join(random.choices("0123456789abcdef", k=64))

def generate_post():
    name = random.choice(NAMES)
    uid = generate_uid()
    txid = generate_txid()
    amount = round(random.uniform(1.0, 100.0), 2)
    network = random.choice(NETWORKS)
    post_type = random.choice(["DEPOSIT", "WITHDRAWAL", "NFT BUY"])

    if post_type == "DEPOSIT":
        header = "🎉 <b>NEW DEPOSIT CONFIRMED!</b>"
    elif post_type == "WITHDRAWAL":
        header = "✅ <b>WITHDRAWAL COMPLETE!</b>"
    else:
        header = "🖼️ <b>NFT PURCHASE SUCCESS!</b>"

    return (
        f"{header}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>User:</b> {name}\n"
        f"🆔 <b>UID:</b> <code>{uid}</code>\n\n"
        f"💰 <b>Amount:</b> ${amount}\n"
        f"💎 <b>Asset:</b> {ASSET}\n"
        f"🌐 <b>Network:</b> {network}\n"
        f"🔗 <b>TXID:</b> <code>{txid}</code>\n\n"
        f"✅ <b>Status:</b> PAID\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💳 <b>Paid by:</b> {BOT_USERNAME}"
    )

async def main():
    bot = Bot(token=BOT_TOKEN)
    print("🚀 বট চালু হয়েছে...")
    while True:
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=generate_post(), parse_mode=ParseMode.HTML)
            print(f"✅ পোস্ট সফল: {datetime.datetime.now()}")
        except Exception as e:
            print(f"❌ এরর: {e}")
        await asyncio.sleep(POST_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
