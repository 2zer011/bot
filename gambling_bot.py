import discord
from discord.ext import commands, tasks
import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, Tuple

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Database file
DB_FILE = "gambling_data.json"
ADMIN_ID = None  # Sẽ được set khi bot start

# Load/Save database
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {"users": {}, "shop_inventory": {}}

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Shop items
SHOP_ITEMS = {
    "lucky_charm": {"price": 500000000, "name": "🍀 Bùa may mắn", "effect": "x1.2 multiplier"},
    "golden_coin": {"price": 1000000000, "name": "🪙 Đồng xu vàng", "effect": "x1.5 multiplier"},
    "dragon_scale": {"price": 2000000000, "name": "🐉 Vảy rồng", "effect": "x2.0 multiplier"},
    "fortune_egg": {"price": 3000000000, "name": "🥚 Quả trứng may mắn", "effect": "Tự động thắng 1 game"},
}

class GamblingBot:
    def __init__(self):
        self.cooldowns = {}
        self.last_work = {}
    
    def get_user_money(self, user_id: str) -> int:
        db = load_db()
        return db["users"].get(str(user_id), {}).get("money", 0)
    
    def set_user_money(self, user_id: str, amount: int):
        db = load_db()
        user_id = str(user_id)
        if user_id not in db["users"]:
            db["users"][user_id] = {"money": 0, "items": {}}
        db["users"][user_id]["money"] = max(0, amount)
        save_db(db)
    
    def add_user_money(self, user_id: str, amount: int):
        current = self.get_user_money(user_id)
        self.set_user_money(user_id, current + amount)
    
    def get_user_data(self, user_id: str) -> dict:
        db = load_db()
        return db["users"].get(str(user_id), {"money": 0, "items": {}})
    
    def add_item(self, user_id: str, item_id: str, amount: int = 1):
        db = load_db()
        user_id = str(user_id)
        if user_id not in db["users"]:
            db["users"][user_id] = {"money": 0, "items": {}}
        
        if "items" not in db["users"][user_id]:
            db["users"][user_id]["items"] = {}
        
        current = db["users"][user_id]["items"].get(item_id, 0)
        db["users"][user_id]["items"][item_id] = current + amount
        save_db(db)
    
    def remove_item(self, user_id: str, item_id: str, amount: int = 1) -> bool:
        db = load_db()
        user_id = str(user_id)
        if user_id not in db["users"] or "items" not in db["users"][user_id]:
            return False
        
        current = db["users"][user_id]["items"].get(item_id, 0)
        if current >= amount:
            db["users"][user_id]["items"][item_id] = current - amount
            save_db(db)
            return True
        return False
    
    def get_multiplier(self, user_id: str) -> float:
        data = self.get_user_data(user_id)
        multiplier = 1.0
        
        if data.get("items", {}).get("lucky_charm", 0) > 0:
            multiplier *= 1.2
        if data.get("items", {}).get("golden_coin", 0) > 0:
            multiplier *= 1.5
        if data.get("items", {}).get("dragon_scale", 0) > 0:
            multiplier *= 2.0
        
        return multiplier

gambling = GamblingBot()

# Events
@bot.event
async def on_ready():
    global ADMIN_ID
    print(f'{bot.user} đã sẵn sàng!')

# Commands
@bot.command(name='vi', help='Xem ví tiền')
async def wallet(ctx):
    user_data = gambling.get_user_data(ctx.author.id)
    money = user_data["money"]
    items = user_data.get("items", {})
    
    embed = discord.Embed(title=f'💰 Ví của {ctx.author.name}', color=0xFFD700)
    embed.add_field(name='2zer011 Coin', value=f'```{money:,}```', inline=False)
    
    if items:
        items_text = ""
        for item_id, count in items.items():
            if count > 0 and item_id in SHOP_ITEMS:
                items_text += f"{SHOP_ITEMS[item_id]['name']} x{count}\n"
        if items_text:
            embed.add_field(name='📦 Vật phẩm', value=items_text, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='w', help='Làm việc để kiếm tiền')
async def work(ctx, job: str = "default"):
    user_id = ctx.author.id
    now = datetime.now()
    
    # Check cooldown (2 minutes)
    if user_id in gambling.last_work:
        if (now - gambling.last_work[user_id]).total_seconds() < 120:
            remaining = 120 - int((now - gambling.last_work[user_id]).total_seconds())
            await ctx.send(f"⏰ Chưa thể làm việc. Hãy chờ {remaining}s nữa!")
            return
    
    gambling.last_work[user_id] = now
    money_earned = random.randint(1000, 2000)
    gambling.add_user_money(user_id, money_earned)
    
    jobs_desc = {
        "default": "🧑‍💻 Làm việc hợp đồng",
        "fishing": "🎣 Đánh cá",
        "mining": "⛏️ Khai thác",
        "farming": "🌾 Nông nghiệp"
    }
    
    job_name = jobs_desc.get(job, jobs_desc["default"])
    await ctx.send(f"{job_name}\n💵 Kiếm được: **{money_earned:,}** 2zer011 Coin!")

@bot.command(name='shop', help='Xem cửa hàng')
async def shop(ctx):
    embed = discord.Embed(title='🏪 Cửa hàng item may mắn', color=0xFF6B6B)
    
    for item_id, info in SHOP_ITEMS.items():
        embed.add_field(
            name=f"{info['name']} - {info['price']:,} coin",
            value=f"Effect: {info['effect']}",
            inline=False
        )
    
    embed.add_field(name='\nMua item:', value='`!buy <item_id>`', inline=False)
    embed.set_footer(text="Item ID: lucky_charm, golden_coin, dragon_scale, fortune_egg")
    await ctx.send(embed=embed)

@bot.command(name='buy', help='Mua item từ shop')
async def buy(ctx, item_id: str):
    if item_id not in SHOP_ITEMS:
        await ctx.send("❌ Item không tồn tại!")
        return
    
    item = SHOP_ITEMS[item_id]
    user_money = gambling.get_user_money(ctx.author.id)
    
    if user_money < item["price"]:
        await ctx.send(f"❌ Không đủ tiền! Cần {item['price']:,}, bạn có {user_money:,}")
        return
    
    gambling.set_user_money(ctx.author.id, user_money - item["price"])
    gambling.add_item(ctx.author.id, item_id)
    
    await ctx.send(f"✅ Mua thành công {item['name']}!")

# ==================== GAMES ====================

@bot.command(name='flip', help='Tung đồng xu')
async def flip(ctx, bet: int):
    if bet <= 0:
        await ctx.send("❌ Cược phải lớn hơn 0!")
        return
    
    user_money = gambling.get_user_money(ctx.author.id)
    if user_money < bet:
        await ctx.send(f"❌ Không đủ tiền cược!")
        return
    
    gambling.set_user_money(ctx.author.id, user_money - bet)
    
    result = random.choice(['heads', 'tails'])
    choice = random.choice(['heads', 'tails'])
    
    multiplier = gambling.get_multiplier(ctx.author.id)
    
    if result == choice:
        winnings = int(bet * 2 * multiplier)
        tax = int(winnings * 0.05)
        actual_win = winnings - tax
        gambling.add_user_money(ctx.author.id, actual_win)
        gambling.add_user_money(ADMIN_ID, tax)
        
        await ctx.send(f"🎲 **THẮNG!** {choice.upper()}\n💰 Thắng: {winnings:,} (sau tax 5%: {actual_win:,})")
    else:
        await ctx.send(f"❌ **THUA!** Kết quả: {result.upper()}")

@bot.command(name='dice', help='Tung xúc xắc (1-6)')
async def dice(ctx, bet: int, guess: int):
    if bet <= 0 or guess < 1 or guess > 6:
        await ctx.send("❌ Cược phải > 0 và số đoán 1-6!")
        return
    
    user_money = gambling.get_user_money(ctx.author.id)
    if user_money < bet:
        await ctx.send("❌ Không đủ tiền cược!")
        return
    
    gambling.set_user_money(ctx.author.id, user_money - bet)
    
    result = random.randint(1, 6)
    multiplier = gambling.get_multiplier(ctx.author.id)
    
    if result == guess:
        winnings = int(bet * 6 * multiplier)
        tax = int(winnings * 0.05)
        actual_win = winnings - tax
        gambling.add_user_money(ctx.author.id, actual_win)
        gambling.add_user_money(ADMIN_ID, tax)
        
        await ctx.send(f"🎲 **THẮNG!** Kết quả: {result}\n💰 Thắng: {winnings:,} (sau tax: {actual_win:,})")
    else:
        await ctx.send(f"❌ **THUA!** Kết quả: {result} (bạn đoán {guess})")

@bot.command(name='taixiu', help='Tài/Xỉu')
async def taixiu(ctx, bet: int, choice: str):
    if bet <= 0 or choice.lower() not in ['tai', 'xiu']:
        await ctx.send("❌ Dùng: !taixiu <tiền cược> <tai|xiu>")
        return
    
    user_money = gambling.get_user_money(ctx.author.id)
    if user_money < bet:
        await ctx.send("❌ Không đủ tiền cược!")
        return
    
    gambling.set_user_money(ctx.author.id, user_money - bet)
    
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    total = dice1 + dice2
    result = 'tai' if total > 7 else 'xiu'
    
    multiplier = gambling.get_multiplier(ctx.author.id)
    
    if result == choice.lower():
        winnings = int(bet * 2 * multiplier)
        tax = int(winnings * 0.05)
        actual_win = winnings - tax
        gambling.add_user_money(ctx.author.id, actual_win)
        gambling.add_user_money(ADMIN_ID, tax)
        
        await ctx.send(f"🎲 **THẮNG!** {dice1} + {dice2} = {total} ({result.upper()})\n💰 Thắng: {winnings:,} (sau tax: {actual_win:,})")
    else:
        await ctx.send(f"❌ **THUA!** {dice1} + {dice2} = {total} ({result.upper()})")

@bot.command(name='plane', help='Máy bay')
async def plane(ctx, bet: int):
    if bet <= 0:
        await ctx.send("❌ Cược phải > 0!")
        return
    
    user_money = gambling.get_user_money(ctx.author.id)
    if user_money < bet:
        await ctx.send("❌ Không đủ tiền cược!")
        return
    
    gambling.set_user_money(ctx.author.id, user_money - bet)
    
    multiplier = gambling.get_multiplier(ctx.author.id)
    crash = random.uniform(1.0, 10.0)
    your_choice = random.uniform(1.0, 10.0)
    
    if your_choice < crash:
        winnings = int(bet * your_choice * multiplier)
        tax = int(winnings * 0.05)
        actual_win = winnings - tax
        gambling.add_user_money(ctx.author.id, actual_win)
        gambling.add_user_money(ADMIN_ID, tax)
        
        await ctx.send(f"✈️ **THẮNG!** Máy bay bay được {your_choice:.2f}x trước crash\n💰 Thắng: {winnings:,} (sau tax: {actual_win:,})")
    else:
        await ctx.send(f"❌ **THUA!** Máy bay crash ở {crash:.2f}x")

@bot.command(name='jackpot', help='Máy jackpot')
async def jackpot(ctx, bet: int):
    if bet <= 0:
        await ctx.send("❌ Cược phải > 0!")
        return
    
    user_money = gambling.get_user_money(ctx.author.id)
    if user_money < bet:
        await ctx.send("❌ Không đủ tiền cược!")
        return
    
    gambling.set_user_money(ctx.author.id, user_money - bet)
    
    reels = [random.randint(1, 7) for _ in range(3)]
    multiplier = gambling.get_multiplier(ctx.author.id)
    
    emoji_map = {1: "🍒", 2: "🍋", 3: "🍊", 4: "🍓", 5: "⭐", 6: "💎", 7: "🎰"}
    reels_display = " ".join([emoji_map[r] for r in reels])
    
    if reels[0] == reels[1] == reels[2]:
        winnings = int(bet * 20 * multiplier)
        tax = int(winnings * 0.05)
        actual_win = winnings - tax
        gambling.add_user_money(ctx.author.id, actual_win)
        gambling.add_user_money(ADMIN_ID, tax)
        
        await ctx.send(f"🎰 **JACKPOT!!!** {reels_display}\n💰 Thắng: {winnings:,} (sau tax: {actual_win:,})")
    elif reels[0] == reels[1] or reels[1] == reels[2]:
        winnings = int(bet * 3 * multiplier)
        tax = int(winnings * 0.05)
        actual_win = winnings - tax
        gambling.add_user_money(ctx.author.id, actual_win)
        gambling.add_user_money(ADMIN_ID, tax)
        
        await ctx.send(f"🎰 **THẮNG!** {reels_display}\n💰 Thắng: {winnings:,} (sau tax: {actual_win:,})")
    else:
        await ctx.send(f"❌ **THUA!** {reels_display}")

@bot.command(name='domin', help='Dò mìn - !domin <tiền cược> <số bom>')
async def minesweeper(ctx, bet: int, num_bombs: int):
    if bet <= 0 or num_bombs < 1 or num_bombs > 24:
        await ctx.send("❌ Dùng: !domin <tiền cược> <số bom 1-24>")
        return
    
    user_money = gambling.get_user_money(ctx.author.id)
    if user_money < bet:
        await ctx.send("❌ Không đủ tiền cược!")
        return
    
    gambling.set_user_money(ctx.author.id, user_money - bet)
    
    # Tạo bàn chơi
    board = [0] * (25 - num_bombs) + [1] * num_bombs
    random.shuffle(board)
    
    revealed = [False] * 25
    multiplier = gambling.get_multiplier(ctx.author.id)
    current_win = bet
    
    # Reveal 5 ô ngẫu nhiên
    safe_count = 0
    for i in range(25):
        if board[i] == 0:
            revealed[i] = True
            safe_count += 1
            if safe_count >= 5:
                break
    
    # Check nếu hit bomb
    bomb_hit = False
    for i in range(25):
        if revealed[i] and board[i] == 1:
            bomb_hit = True
            break
    
    if bomb_hit:
        await ctx.send(f"💣 **THUA!** Bạn trúng bom!")
    else:
        # Tính hệ số tiền dựa vào số bom
        coefficient = 1 + (num_bombs * 0.15)
        winnings = int(current_win * coefficient * multiplier)
        tax = int(winnings * 0.05)
        actual_win = winnings - tax
        gambling.add_user_money(ctx.author.id, actual_win)
        gambling.add_user_money(ADMIN_ID, tax)
        
        board_display = ""
        for i in range(25):
            if i % 5 == 0:
                board_display += "\n"
            if revealed[i]:
                board_display += "✅ " if board[i] == 0 else "💣 "
            else:
                board_display += "❓ "
        
        await ctx.send(f"✅ **THẮNG!** Số bom: {num_bombs}, Hệ số: {coefficient:.2f}x\n{board_display}\n💰 Thắng: {winnings:,} (sau tax: {actual_win:,})")

# ==================== ADMIN COMMANDS ====================

@bot.command(name='add', help='[ADMIN] Cộng tiền cho user')
async def add_money(ctx, user: discord.User, amount: int):
    global ADMIN_ID
    
    if ADMIN_ID is None:
        ADMIN_ID = ctx.author.id
    
    if ctx.author.id != ADMIN_ID:
        await ctx.send("❌ Chỉ admin mới dùng được lệnh này!")
        return
    
    gambling.add_user_money(user.id, amount)
    await ctx.send(f"✅ Đã cộng {amount:,} cho {user.mention}")

@bot.command(name='set', help='[ADMIN] Set tiền cho user')
async def set_money(ctx, user: discord.User, amount: int):
    global ADMIN_ID
    
    if ADMIN_ID is None:
        ADMIN_ID = ctx.author.id
    
    if ctx.author.id != ADMIN_ID:
        await ctx.send("❌ Chỉ admin mới dùng được lệnh này!")
        return
    
    gambling.set_user_money(user.id, amount)
    await ctx.send(f"✅ Đã set tiền {user.mention} thành {amount:,}")

@bot.command(name='init', help='[ADMIN] Khởi tạo tiền cho user')
async def init_user(ctx, user: discord.User, amount: int = 10000):
    global ADMIN_ID
    
    if ADMIN_ID is None:
        ADMIN_ID = ctx.author.id
    
    if ctx.author.id != ADMIN_ID:
        await ctx.send("❌ Chỉ admin mới dùng được lệnh này!")
        return
    
    gambling.set_user_money(user.id, amount)
    await ctx.send(f"✅ Khởi tạo {amount:,} cho {user.mention}")

@bot.command(name='admin', help='[ADMIN] Set admin')
async def set_admin(ctx, user: discord.User):
    global ADMIN_ID
    
    if ADMIN_ID is None:
        ADMIN_ID = ctx.author.id
    
    if ctx.author.id != ADMIN_ID:
        await ctx.send("❌ Chỉ admin mới dùng được lệnh này!")
        return
    
    ADMIN_ID = user.id
    await ctx.send(f"✅ Đặt {user.mention} làm admin")

@bot.command(name='info', help='[ADMIN] Thông tin user')
async def user_info(ctx, user: discord.User):
    global ADMIN_ID
    
    if ADMIN_ID is None:
        ADMIN_ID = ctx.author.id
    
    data = gambling.get_user_data(user.id)
    embed = discord.Embed(title=f"Thông tin {user.name}", color=0x00FF00)
    embed.add_field(name="Tiền", value=f"{data['money']:,}", inline=False)
    embed.add_field(name="Item", value=str(data.get("items", {})), inline=False)
    
    await ctx.send(embed=embed)

# Run bot
bot.run("YOUR_TOKEN_HERE")
