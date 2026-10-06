import random
import string
import datetime
import os
import asyncio
from telegram import Bot
from telegram.constants import ParseMode

# ================= সেটিংস =================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
BOT_USERNAME = "@SFN_MiningBot"
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

NFTS = [
    {"name": "SFN Elite Pass",                "price": 3,  "special": False},
    {"name": "SFN Infinity Pro",              "price": 5,  "special": False},
    {"name": "SFN Century",                   "price": 10, "special": False},
    {"name": "SFN Zenith",                    "price": 15, "special": False},
    {"name": "SFN Nova",                      "price": 20, "special": False},
    {"name": "SFN Phoenix [Special Edition]", "price": 25, "special": True},
    {"name": "SFN Aurora [Special Edition]",  "price": 30, "special": True},
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
    network = random.choice(NETWORKS)
    post_type = random.choice(["DEPOSIT", "WITHDRAWAL", "NFT BUY"])

    now = datetime.datetime.utcnow()
    date_str = now.strftime("%d %b %Y")

    # ========== DEPOSIT ==========
    if post_type == "DEPOSIT":
        amount = round(random.uniform(5.0, 500.0), 2)
        return (
            f"💎 <b>DEPOSIT VERIFIED</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>User</b>     ›  {name}\n"
            f"🆔 <b>UID</b>      ›  <code>{uid}</code>\n"
            f"📅 <b>Date</b>     ›  {date_str}\n"
            f"💰 <b>Amount</b>   ›  <b>${amount}</b>\n"
            f"💵 <b>Asset</b>    ›  {ASSET}\n"
            f"🌐 <b>Network</b>  ›  {network}\n"
            f"🔗 <b>TXID</b>\n"
            f"<code>{txid}</code>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"✅ <b>STATUS: PAID</b>\n"
            f"💳 <b>Paid by:</b> {BOT_USERNAME}"
        )

    # ========== WITHDRAWAL ==========
    elif post_type == "WITHDRAWAL":
        amount = round(random.uniform(3.0, 300.0), 2)
        return (
            f"✅ <b>WITHDRAWAL APPROVED</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>User</b>     ›  {name}\n"
            f"🆔 <b>UID</b>      ›  <code>{uid}</code>\n"
            f"📅 <b>Date</b>     ›  {date_str}\n"
            f"💰 <b>Amount</b>   ›  <b>${amount}</b>\n"
            f"💵 <b>Asset</b>    ›  {ASSET}\n"
            f"🌐 <b>Network</b>  ›  {network}\n"
            f"🔗 <b>TXID</b>\n"
            f"<code>{txid}</code>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"✅ <b>STATUS: PAID</b>\n"
            f"💳 <b>Paid by:</b> {BOT_USERNAME}"
        )

    # ========== NFT BUY ==========
    else:
        weights = [3 if n["special"] else 1 for n in NFTS]
        nft = random.choices(NFTS, weights=weights, k=1)[0]
        nft_name = nft["name"]
        nft_price = nft["price"]

        if nft["special"]:
            header = "🌟 <b>PREMIUM NFT PURCHASED</b>"
            badge = "👑 <b>SPECIAL EDITION</b>"
        else:
            header = "🖼️ <b>NFT PURCHASED</b>"
            badge = "🏅 <b>VERIFIED PURCHASE</b>"

        return (
            f"{header}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🎁 <b>NFT</b>      ›  <b>{nft_name}</b>\n"
            f"{badge}\n"
            f"👤 <b>User</b>     ›  {name}\n"
            f"🆔 <b>UID</b>      ›  <code>{uid}</code>\n"
            f"📅 <b>Date</b>     ›  {date_str}\n"
            f"💰 <b>Price</b>    ›  <b>${nft_price}</b>\n"
            f"💵 <b>Asset</b>    ›  {ASSET}\n"
            f"🌐 <b>Network</b>  ›  {network}\n"
            f"🔗 <b>TXID</b>\n"
            f"<code>{txid}</code>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"✅ <b>STATUS: PAID</b>\n"
            f"💳 <b>Paid by:</b> {BOT_USERNAME}"
        )

async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=generate_post(),
            parse_mode=ParseMode.HTML
        )
        print(f"✅ পোস্ট সফল: {datetime.datetime.now()}")
    except Exception as e:
        print(f"❌ এরর: {e}")

if __name__ == "__main__":
    asyncio.run(main())
