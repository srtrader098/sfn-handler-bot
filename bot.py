import random
import string
import datetime
import os
import json
import asyncio
from telegram import Bot
from telegram.constants import ParseMode

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
BOT_USERNAME = "@SFN_MiningBot"

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
PENDING_FILE = "pending.json"

def generate_uid():
    return f"62{''.join(random.choices(string.digits, k=7))}"

def generate_txid():
    return ''.join(random.choices("0123456789abcdef", k=64))

def load_pending():
    if os.path.exists(PENDING_FILE):
        try:
            with open(PENDING_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_pending(data):
    with open(PENDING_FILE, "w") as f:
        json.dump(data, f, indent=2)

def pick_nft():
    weights = [3 if n["special"] else 1 for n in NFTS]
    return random.choices(NFTS, weights=weights, k=1)[0]

def generate_post():
    name = random.choice(NAMES)
    uid = generate_uid()
    txid = generate_txid()
    network = random.choice(NETWORKS)
    now = datetime.datetime.utcnow()
    date_str = now.strftime("%d %b %Y")

    pending = load_pending()

    # ==========================================
    # ১. আগের Processing থাকলে → Approved
    # ==========================================
    if pending:
        item = pending.pop(0)
        save_pending(pending)

        if item["type"] == "deposit":
            header = "🟢 <b>DEPOSIT APPROVED</b>"
        elif item["type"] == "withdraw":
            header = "🟢 <b>WITHDRAW APPROVED</b>"
        else:
            header = "🟣 <b>NFT ACTIVATED</b>" + (" 👑" if item.get("special") else "")

        status_text = "Approved" if item["type"] != "nft" else "Active"

        if item["type"] == "nft":
            return (
                f"{header}\n"
                f"━━━━━━━━━━━━━━━\n"
                f"🎁 <b>{item['nft_name']}</b>\n"
                f"👤 {item['name']}\n"
                f"🆔 <code>{item['uid']}</code>\n"
                f"📅 {item['date']}\n"
                f"💰 <b>${item['amount']}</b>  |  {ASSET}\n"
                f"🌐 Network: {item['network']}\n"
                f"🔗 <code>{item['txid']}</code>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"✅ <b>Status:</b> {status_text}\n"
                f"🔒 Activated by {BOT_USERNAME}\n"
                f"💳 {BOT_USERNAME}"
            )
        else:
            return (
                f"{header}\n"
                f"━━━━━━━━━━━━━━━\n"
                f"👤 {item['name']}\n"
                f"🆔 <code>{item['uid']}</code>\n"
                f"📅 {item['date']}\n"
                f"💰 <b>${item['amount']}</b>  |  {ASSET}\n"
                f"🌐 Network: {item['network']}\n"
                f"🔗 <code>{item['txid']}</code>\n"
                f"━━━━━━━━━━━━━━━\n"
                f"✅ <b>Status:</b> {status_text}\n"
                f"🔒 Verified by {BOT_USERNAME}\n"
                f"💳 {BOT_USERNAME}"
            )

    # ==========================================
    # ২. নতুন Processing পোস্ট
    # ==========================================
    nft = pick_nft()
    nft_name = nft["name"]
    nft_price = nft["price"]
    is_special = nft["special"]

    action = random.choice(["deposit", "withdraw", "nft"])
    amount = nft_price

    if action == "deposit":
        header = "🟡 <b>DEPOSIT PROCESSING</b>"
        status_text = "Processing"
        status_emoji = "⏳"
        note = "🤖 Verifying on blockchain..."
        post_type = "deposit"

    elif action == "withdraw":
        header = "🟡 <b>WITHDRAW PROCESSING</b>"
        status_text = "Processing"
        status_emoji = "⏳"
        note = "🤖 Verifying on blockchain..."
        post_type = "withdraw"

    else:
        header = "🟣 <b>NFT ACTIVATED</b>" + (" 👑" if is_special else "")
        status_text = "Active"
        status_emoji = "✅"
        note = f"🔒 Activated by {BOT_USERNAME}"
        post_type = "nft"

    # Processing গুলো pending এ সেভ করি
    if post_type in ["deposit", "withdraw"]:
        pending = load_pending()
        pending.append({
            "type": post_type,
            "name": name,
            "uid": uid,
            "txid": txid,
            "date": date_str,
            "amount": amount,
            "network": network,
        })
        save_pending(pending)

    # NFT হলে আলাদা ফরম্যাট
    if post_type == "nft":
        return (
            f"{header}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🎁 <b>{nft_name}</b>\n"
            f"👤 {name}\n"
            f"🆔 <code>{uid}</code>\n"
            f"📅 {date_str}\n"
            f"💰 <b>${amount}</b>  |  {ASSET}\n"
            f"🌐 Network: {network}\n"
            f"🔗 <code>{txid}</code>\n"
            f"━━━━━━━━━━━━━━━\n"
            f"{status_emoji} <b>Status:</b> {status_text}\n"
            f"{note}\n"
            f"💳 {BOT_USERNAME}"
        )
    else:
        return (
            f"{header}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"👤 {name}\n"
            f"🆔 <code>{uid}</code>\n"
            f"📅 {date_str}\n"
            f"💰 <b>${amount}</b>  |  {ASSET}\n"
            f"🌐 Network: {network}\n"
            f"🔗 <code>{txid}</code>\n"
            f"━━━━━━━━━━━━━━━\n"
            f"{status_emoji} <b>Status:</b> {status_text}\n"
            f"{note}\n"
            f"💳 {BOT_USERNAME}"
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
        await asyncio.sleep(120)

if __name__ == "__main__":
    asyncio.run(main())
