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
MAX_PENDING = 3   # সর্বোচ্চ ৩টি Processing থাকবে

def generate_uid():
    return f"62{''.join(random.choices(string.digits, k=7))}"

def generate_full_txid():
    return ''.join(random.choices("0123456789abcdef", k=64))

def short_txid(full):
    return f"{full[:8]}...{full[-8:]}"

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

def build_post(header, body_lines, status_emoji, status_text, footer_note):
    body = "\n".join(body_lines)
    return (
        f"{header}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{body}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"{status_emoji} <b>Status:</b> {status_text}\n"
        f"{footer_note}"
    )

def make_processing(name, uid, txid, network, date_str, ptype, amount):
    if ptype == "deposit":
        header = "🟡 <b>DEPOSIT PROCESSING</b>"
    else:
        header = "🟡 <b>WITHDRAW PROCESSING</b>"

    body_lines = [
        f"👤 <b>User:</b> {name}",
        f"🆔 <b>UID:</b> <code>{uid}</code>",
        f"📅 <b>Date:</b> {date_str}",
        f"💰 <b>Amount:</b> <b>${amount}</b> | {ASSET}",
        f"🌐 <b>Network:</b> {network}",
        f"🔗 <b>TXID:</b> <code>{txid}</code>",
    ]
    return build_post(
        header, body_lines,
        "⏳", "Processing",
        "🤖 Verifying on blockchain...\n"
        f"💳 {BOT_USERNAME}"
    )

def make_approved(item):
    if item["type"] == "deposit":
        header = "🟢 <b>DEPOSIT APPROVED</b>"
    else:
        header = "🟢 <b>WITHDRAW APPROVED</b>"

    body_lines = [
        f"👤 <b>User:</b> {item['name']}",
        f"🆔 <b>UID:</b> <code>{item['uid']}</code>",
        f"📅 <b>Date:</b> {item['date']}",
        f"💰 <b>Amount:</b> <b>${item['amount']}</b> | {ASSET}",
        f"🌐 <b>Network:</b> {item['network']}",
        f"🔗 <b>TXID:</b> <code>{item['txid']}</code>",
    ]
    return build_post(
        header, body_lines,
        "✅", "Approved",
        f"🤖 <b>Verified by</b> {BOT_USERNAME}"
    )

def make_nft(nft):
    header = "🟣 <b>NFT ACTIVATED</b>" + (" 👑" if nft["special"] else "")
    name = random.choice(NAMES)
    uid = generate_uid()
    txid = short_txid(generate_full_txid())
    network = random.choice(NETWORKS)
    date_str = datetime.datetime.utcnow().strftime("%d %b %Y")

    body_lines = [
        f"🎁 <b>NFT:</b> {nft['name']}",
        f"👤 <b>User:</b> {name}",
        f"🆔 <b>UID:</b> <code>{uid}</code>",
        f"📅 <b>Date:</b> {date_str}",
        f"💰 <b>Amount:</b> <b>${nft['price']}</b> | {ASSET}",
        f"🌐 <b>Network:</b> {network}",
        f"🔗 <b>TXID:</b> <code>{txid}</code>",
    ]
    return build_post(
        header, body_lines,
        "✅", "Active",
        f"🤖 <b>Activated by</b> {BOT_USERNAME}"
    )

def generate_post():
    name = random.choice(NAMES)
    uid = generate_uid()
    txid = short_txid(generate_full_txid())
    network = random.choice(NETWORKS)
    date_str = datetime.datetime.utcnow().strftime("%d %b %Y")

    pending = load_pending()
    nft = pick_nft()
    amount = nft["price"]

    # ==========================================
    # লজিক: ৩টি পোস্টের মধ্যে মিক্স
    # pending ৩টির বেশি হলে → Approved বাধ্যতামূলক
    # pending ০ হলে → Processing বাধ্যতামূলক
    # ==========================================

    if len(pending) >= MAX_PENDING:
        # বাধ্যতামূলক Approved
        item = pending.pop(0)
        save_pending(pending)
        return make_approved(item)

    # র‍্যান্ডম সিদ্ধান্ত: ৪০% Processing, ৩০% Approved, ৩০% NFT
    roll = random.randint(1, 100)

    # pending খালি হলে Approved হবে না
    if len(pending) == 0:
        roll = 50 if roll <= 30 else roll   # Processing বা NFT

    if roll <= 40:
        # নতুন Processing
        ptype = random.choice(["deposit", "withdraw"])
        pending.append({
            "type": ptype,
            "name": name,
            "uid": uid,
            "txid": txid,
            "date": date_str,
            "amount": amount,
            "network": network,
        })
        save_pending(pending)
        return make_processing(name, uid, txid, network, date_str, ptype, amount)

    elif roll <= 70:
        # Approved
        item = pending.pop(0)
        save_pending(pending)
        return make_approved(item)

    else:
        # NFT
        return make_nft(nft)

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
