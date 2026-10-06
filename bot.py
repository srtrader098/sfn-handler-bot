import random
import string
import datetime
import asyncio
import os
from telegram import Bot
from telegram.constants import ParseMode

# ================= সেটিংস =================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
BOT_USERNAME = "@SFN_MiningBot"
POST_INTERVAL = 1800   # ৩০ মিনিট (সেকেন্ডে)
# ==========================================

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

    # শুধু Date (Time ছাড়া)
    now = datetime.datetime.utcnow()
    date_str = now.strftime("%d %b %Y")

    # প্রিমিয়াম হেডার
    if post_type == "DEPOSIT":
        header = "💎 <b>DEPOSIT VERIFIED</b>"
        sub = "🔒 <i>Transaction Successfully Confirmed</i>"
    elif post_type == "WITHDRAWAL":
        header = "✅ <b>WITHDRAWAL APPROVED</b>"
        sub = "🔒 <i>Payment Successfully Processed</i>"
    else:
        header = "🖼️ <b>NFT PURCHASED</b>"
        sub = "🔒 <i>Asset Successfully Transferred</i>"

    return (
        f"┏━━━━━━━━━━━━━━━━━━━━┓\n"
        f"   {header}\n"
        f"   {sub}\n"
        f"┗━━━━━━━━━━━━━━━━━━━━┛\n\n"
        f"👤 <b>User</b>       ➜  {name}\n"
        f"🆔 <b>UID</b>        ➜  <code>{uid}</code>\n"
        f"📅 <b>Date</b>       ➜  {date_str}\n\n"
        f"💰 <b>Amount</b>     ➜  <b>${amount}</b>\n"
        f"💵 <b>Asset</b>      ➜  {ASSET}\n"
        f"🌐 <b>Network</b>    ➜  {network}\n\n"
        f"🔗 <b>TXID</b>\n"
        f"<code>{txid}</code>\n\n"
        f"┌────────────────────┐\n"
        f"   ✅ <b>STATUS: PAID</b> ✅\n"
        f"└────────────────────┘\n\n"
        f"💳 <b>Paid by:</b> {BOT_USERNAME}"
    )

async def main():
    bot = Bot(token=BOT_TOKEN)
    print("🚀 বট চালু হয়েছে...")
    while True:
        try:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=generate_post(),
                parse_mode=ParseMode.HTML
            )
            print(f"✅ পোস্ট সফল: {datetime.datetime.now()}")
        except Exception as e:
            print(f"❌ এরর: {e}")
        await asyncio.sleep(POST_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
