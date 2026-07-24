import discord
from discord.ext import commands, tasks
import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Database file
DB_FILE = "gambling_data.json"
ADMIN_ID = 1193618034691162223

# ==================== DATABASE FUNCTIONS ====================

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {"users": {}, "shop_inventory": {}}

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ==================== SHOP CONFIG ====================

SHOP_ITEMS = {
    "lucky_charm": {
        "price": 500_000_000, 
        "name": "🍀 Bùa may mắn", 
        "effect": "x1.2 multiplier"
    },
    "golden_coin": {
        "price": 1_000_000_000, 
        "name": "🪙 Đồng xu vàng", 
        "effect": "x1.5 multiplier"
    },
    "dragon_scale": {
        "price": 2_000_000_000, 
        "name": "🐉 Vảy rồng", 
        "effect": "x2.0 multiplier"
    },
    "fortune_egg": {
        "price": 3_000_000_000, 
        "name": "🥚 Quả trứng may mắn", 
        "effect": "Tự động thắng 1 game"
    },
}

# ==================== GAMBLING CLASS ====================

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
        items = data.get("items", {})
        
        if items.get("lucky_charm", 0) > 0:
            multiplier *= 1.2
        if items.get("golden_coin", 0) > 0:
            multiplier *= 1.5
        if items.get("dragon_scale", 0) > 0:
            multiplier *= 2.0
        
        return multiplier

gambling = GamblingBot()

# ==================== EVENTS ====================

@bot.event
async def on_ready():
    global ADMIN_ID
    print(f'✅ {bot.user} đã sẵn sàng!')
    print(f'📊 Đang chạy trên {len(bot.guilds)} server')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Lệnh không tồn tại! Dùng `!help` để xem danh sách lệnh")
    else:
        await ctx.send(f"❌ Lỗi: {str(error)}")

# ==================== BASIC COMMANDS ====================

@bot.command(name='vi', help='Xem ví tiền của bạn')
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
    
    embed.set_footer(text="Kiếm tiền bằng !w <công việc>")
    await ctx.send(embed=embed)

@bot.command(name='w', help='Làm việc để kiếm tiền (!w <job>)')
async def work(ctx, job: str = "default"):
    user_id = ctx.author.id
    now = datetime.now()
    
    # Check cooldown (120 seconds / 2 minutes)
    if user_id in gambling.last_work:
        time_diff = (now - gambling.last_work[user_id]).total_seconds()
        if time_diff < 120:
            remaining = int(120 - time_diff)
            await ctx.send(f"⏰ Chưa thể làm việc. Hãy chờ {remaining}s nữa!")
            return
    
    gambling.last_work[user_id] = now
    money_earned = random.randint(1000, 2000)
    gambling.add_user_money(user_id, money_earned)
    
    jobs_desc = {
        "default": "🧑‍💻 Lập trình",
        "fishing": "🎣 Đánh cá",
        "mining": "⛏️ Khai thác",
        "farming": "🌾 Nông nghiệp",
        "chef": "👨‍🍳 Nấu ăn",
        "design": "🎨 Thiết kế",
        "gaming": "🎮 Chơi game"
    }
    
    job_name = jobs_desc.get(job.lower(), jobs_desc["default"])
    
    embed = discord.Embed(title=job_name, color=0x00FF00)
    embed.add_field(name='💵 Kiếm được', value=f'**{money_earned:,}** 2zer011 Coin', inline=False)
    embed.set_footer(text=f"Chờ 2 phút để làm việc tiếp")
    
    await ctx.send(embed=embed)

@bot.command(name='shop', help='Xem cửa hàng item')
async def shop(ctx):
    embed = discord.Embed(title='🏪 Cửa hàng item may mắn', color=0xFF6B6B)
    embed.description = 'Mua item để tăng tiền thắng!'
    
    for item_id, info in SHOP_ITEMS.items():
        price_str = f"{info['price']:,}".replace(',', '.')
        embed.add_field(
            name=f"{info['name']}",
            value=f"💰 {price_str} coin\n✨ {info['effect']}",
            inline=False
        )
    
    embed.add_field(name='\n🛒 Mua item:', value='`!buy <item_id>`', inline=False)
    embed.set_footer(text="VD: !buy lucky_charm")
    
    await ctx.send(embed=embed)

@bot.command(name='buy', help='Mua item (!buy <item_id>)')
async def buy(ctx, item_id: str):
    if item_id not in SHOP_ITEMS:
        await ctx.send(f"❌ Item không tồn tại!\n**Item có sẵn:** lucky_charm, golden_coin, dragon_scale, fortune_egg")
        return
    
    item = SHOP_ITEMS[item_id]
    user_money = gambling.get_user_money(ctx.author.id)
    
    if user_money < item["price"]:
        need = item["price"] - user_money
        await ctx.send(f"❌ Không đủ tiền!\n**Cần:** {item['price']:,}\n**Có:** {user_money:,}\n**Thiếu:** {need:,}")
        return
    
    gambling.set_user_money(ctx.author.id, user_money - item["price"])
    gambling.add_item(ctx.author.id, item_id)
    
    embed = discord.Embed(title='✅ Mua thành công', color=0x00FF00)
    embed.add_field(name='Item', value=item['name'], inline=False)
    embed.add_field(name='Giá', value=f"{item['price']:,}", inline=False)
    
    await ctx.send(embed=embed)

# ==================== GAMES ====================

@bot.command(name='flip', help='Tung đồng xu (!flip <tiền cược>)')
async def flip(ctx, bet: int):
    if bet <= 0:
        await ctx.send("❌ Cược phải lớn hơn 0!")
        return
    
    user_money = gambling.get_user_money(ctx.author.id)
    if user_money < bet:
        await ctx.send(f"❌ Không đủ tiền cược! (Có: {user_money:,})")
        return
    
    gambling.set_user_money(ctx.author.id, user_money - bet)
    
    result = random.choice(['heads', 'tails'])
    guess = random.choice(['heads', 'tails'])
    
    multiplier = gambling.get_multiplier(ctx.author.id)
    
    if result == guess:
        winnings = int(bet * 2 * multiplier)
        tax = int(winnings * 0.05)
        actual_win = winnings - tax
        
        gambling.add_user_money(ctx.author.id, actual_win)
        if ADMIN_ID:
            gambling.add_user_money(ADMIN_ID, tax)
        
        await ctx.send(f"🪙 **THẮNG!** {guess.upper()}\n💰 Thắng: {winnings:,} (-5% tax: {actual_win:,})")
    else:
        await ctx.send(f"❌ **THUA!** Kết quả: {result.upper()}")

@bot.command(name='dice', help='Tung xúc xắc (!dice <tiền cược> <1-6>)')
async def dice(ctx, bet: int, guess: int):
    if bet <= 0 or guess < 1 or guess > 6:
        await ctx.send("❌ Dùng: !dice <tiền cược> <số 1-6>")
        return
    
    user_money = gambling.get_user_money(ctx.author.id)
    if user_money < bet:
        await ctx.send(f"❌ Không đủ tiền cược! (Có: {user_money:,})")
        return
    
    gambling.set_user_money(ctx.author.id, user_money - bet)
    
    result = random.randint(1, 6)
    multiplier = gambling.get_multiplier(ctx.author.id)
    
    if result == guess:
        winnings = int(bet * 6 * multiplier)
        tax = int(winnings * 0.05)
        actual_win = winnings - tax
        gambling.add_user_money(ctx.author.id, actual_win)
        if ADMIN_ID:
            gambling.add_user_money(ADMIN_ID, tax)
        
        await ctx.send(f"🎲 **THẮNG!** Kết quả: {result}\n💰 Thắng: {winnings:,} (-5% tax: {actual_win:,})")
    else:
        await ctx.send(f"❌ **THUA!** Kết quả: {result} (bạn đoán {guess})")

@bot.command(name='taixiu', help='Tài/Xỉu (!taixiu <tiền cược> <tai|xiu>)')
async def taixiu(ctx, bet: int, choice: str):
    if bet <= 0 or choice.lower() not in ['tai', 'xiu']:
        await ctx.send("❌ Dùng: !taixiu <tiền cược> <tai|xiu>")
        return
    
    user_money = gambling.get_user_money(ctx.author.id)
    if user_money < bet:
        await ctx.send(f"❌ Không đủ tiền cược! (Có: {user_money:,})")
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
        if ADMIN_ID:
            gambling.add_user_money(ADMIN_ID, tax)
        
        await ctx.send(f"🎲 **THẮNG!** {dice1} + {dice2} = {total} ({result.upper()})\n💰 Thắng: {winnings:,} (-5% tax: {actual_win:,})")
    else:
        await ctx.send(f"❌ **THUA!** {dice1} + {dice2} = {total} ({result.upper()})")

@bot.command(name='plane', help='Máy bay (!plane <tiền cược>)')
async def plane(ctx, bet: int):
    if bet <= 0:
        await ctx.send("❌ Cược phải > 0!")
        return
    
    user_money = gambling.get_user_money(ctx.author.id)
    if user_money < bet:
        await ctx.send(f"❌ Không đủ tiền cược! (Có: {user_money:,})")
        return
    
    gambling.set_user_money(ctx.author.id, user_money - bet)
    
    multiplier = gambling.get_multiplier(ctx.author.id)
    crash_point = round(random.uniform(1.0, 10.0), 2)
    your_multiply = round(random.uniform(1.0, 10.0), 2)
    
    if your_multiply < crash_point:
        winnings = int(bet * your_multiply * multiplier)
        tax = int(winnings * 0.05)
        actual_win = winnings - tax
        gambling.add_user_money(ctx.author.id, actual_win)
        if ADMIN_ID:
            gambling.add_user_money(ADMIN_ID, tax)
        
        await ctx.send(f"✈️ **THẮNG!** Bay được {your_multiply}x trước crash {crash_point}x\n💰 Thắng: {winnings:,} (-5% tax: {actual_win:,})")
    else:
        await ctx.send(f"❌ **THUA!** Máy bay crash ở {crash_point}x")

@bot.command(name='jackpot', help='Máy jackpot (!jackpot <tiền cược>)')
async def jackpot(ctx, bet: int):
    if bet <= 0:
        await ctx.send("❌ Cược phải > 0!")
        return
    
    user_money = gambling.get_user_money(ctx.author.id)
    if user_money < bet:
        await ctx.send(f"❌ Không đủ tiền cược! (Có: {user_money:,})")
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
        if ADMIN_ID:
            gambling.add_user_money(ADMIN_ID, tax)
        
        await ctx.send(f"🎰 **JACKPOT!!!** {reels_display}\n💰 Thắng: {winnings:,} (-5% tax: {actual_win:,})")
    elif reels[0] == reels[1] or reels[1] == reels[2]:
        winnings = int(bet * 3 * multiplier)
        tax = int(winnings * 0.05)
        actual_win = winnings - tax
        gambling.add_user_money(ctx.author.id, actual_win)
        if ADMIN_ID:
            gambling.add_user_money(ADMIN_ID, tax)
        
        await ctx.send(f"🎰 **THẮNG!** {reels_display}\n💰 Thắng: {winnings:,} (-5% tax: {actual_win:,})")
    else:
        await ctx.send(f"❌ **THUA!** {reels_display}")

@bot.command(name='domin', help='Dò mìn (!domin <tiền cược> <số bom 1-24>)')
async def minesweeper(ctx, bet: int, num_bombs: int):
    if bet <= 0 or num_bombs < 1 or num_bombs > 24:
        await ctx.send("❌ Dùng: !domin <tiền cược> <số bom 1-24>\nSố bom càng cao, hệ số thắng càng lớn!")
        return
    
    user_money = gambling.get_user_money(ctx.author.id)
    if user_money < bet:
        await ctx.send(f"❌ Không đủ tiền cược! (Có: {user_money:,})")
        return
    
    gambling.set_user_money(ctx.author.id, user_money - bet)
    
    # Create board: 0 = safe, 1 = bomb
    board = [0] * (25 - num_bombs) + [1] * num_bombs
    random.shuffle(board)
    
    # Simulate revealing 5 squares
    revealed_indices = random.sample(range(25), 5)
    revealed = [False] * 25
    for idx in revealed_indices:
        revealed[idx] = True
    
    # Check if any bomb was revealed
    bomb_hit = any(board[i] == 1 for i in range(25) if revealed[i])
    
    multiplier = gambling.get_multiplier(ctx.author.id)
    coefficient = 1 + (num_bombs * 0.15)
    
    if bomb_hit:
        board_display = ""
        for i in range(25):
            if i % 5 == 0:
                board_display += "\n"
            if revealed[i]:
                board_display += "💣 " if board[i] == 1 else "✅ "
            else:
                board_display += "❓ "
        
        await ctx.send(f"💣 **THUA!** Bạn trúng bom!\n{board_display}")
    else:
        winnings = int(bet * coefficient * multiplier)
        tax = int(winnings * 0.05)
        actual_win = winnings - tax
        gambling.add_user_money(ctx.author.id, actual_win)
        if ADMIN_ID:
            gambling.add_user_money(ADMIN_ID, tax)
        
        board_display = ""
        for i in range(25):
            if i % 5 == 0:
                board_display += "\n"
            if revealed[i]:
                board_display += "✅ "
            else:
                board_display += "❓ "
        
        await ctx.send(f"✅ **THẮNG!** {num_bombs} bom, Hệ số {coefficient:.2f}x\n{board_display}\n💰 Thắng: {winnings:,} (-5% tax: {actual_win:,})")

# ==================== ADMIN COMMANDS ====================

@bot.command(name='add', help='[ADMIN] Cộng tiền cho user')
async def add_money(ctx, user: discord.User, amount: int):
    global ADMIN_ID
    
    if ADMIN_ID is None:
        ADMIN_ID = ctx.author.id
    
    if ctx.author.id != ADMIN_ID:
        await ctx.send("❌ Chỉ admin mới dùng được!")
        return
    
    if amount < 0:
        await ctx.send("❌ Số tiền phải >= 0!")
        return
    
    gambling.add_user_money(user.id, amount)
    await ctx.send(f"✅ Đã cộng {amount:,} cho {user.mention}\nSố dư hiện tại: {gambling.get_user_money(user.id):,}")

@bot.command(name='set', help='[ADMIN] Set tiền cho user')
async def set_money(ctx, user: discord.User, amount: int):
    global ADMIN_ID
    
    if ADMIN_ID is None:
        ADMIN_ID = ctx.author.id
    
    if ctx.author.id != ADMIN_ID:
        await ctx.send("❌ Chỉ admin mới dùng được!")
        return
    
    if amount < 0:
        await ctx.send("❌ Số tiền phải >= 0!")
        return
    
    gambling.set_user_money(user.id, amount)
    await ctx.send(f"✅ Đặt số dư {user.mention} = {amount:,}")

@bot.command(name='init', help='[ADMIN] Khởi tạo tiền cho user')
async def init_user(ctx, user: discord.User, amount: int = 10000):
    global ADMIN_ID
    
    if ADMIN_ID is None:
        ADMIN_ID = ctx.author.id
    
    if ctx.author.id != ADMIN_ID:
        await ctx.send("❌ Chỉ admin mới dùng được!")
        return
    
    gambling.set_user_money(user.id, amount)
    await ctx.send(f"✅ Khởi tạo {amount:,} cho {user.mention}")

@bot.command(name='admin', help='[ADMIN] Đặt admin')
async def set_admin(ctx, user: discord.User):
    global ADMIN_ID
    
    if ADMIN_ID is None:
        ADMIN_ID = ctx.author.id
    
    if ctx.author.id != ADMIN_ID:
        await ctx.send("❌ Chỉ admin mới dùng được!")
        return
    
    ADMIN_ID = user.id
    await ctx.send(f"✅ Đặt {user.mention} làm admin")

@bot.command(name='info', help='[ADMIN] Thông tin user')
async def user_info(ctx, user: discord.User = None):
    global ADMIN_ID
    
    if ADMIN_ID is None:
        ADMIN_ID = ctx.author.id
    
    if ctx.author.id != ADMIN_ID:
        await ctx.send("❌ Chỉ admin mới dùng được!")
        return
    
    target = user or ctx.author
    data = gambling.get_user_data(target.id)
    
    embed = discord.Embed(title=f"📊 Thông tin {target.name}", color=0x00FF00)
    embed.add_field(name="💰 Tiền", value=f"{data['money']:,}", inline=False)
    
    items = data.get("items", {})
    if items:
        items_text = ""
        for item_id, count in items.items():
            if count > 0 and item_id in SHOP_ITEMS:
                items_text += f"{SHOP_ITEMS[item_id]['name']} x{count}\n"
        if items_text:
            embed.add_field(name="📦 Vật phẩm", value=items_text, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='stats', help='[ADMIN] Thống kê toàn server')
async def stats(ctx):
    global ADMIN_ID
    
    if ADMIN_ID is None:
        ADMIN_ID = ctx.author.id
    
    if ctx.author.id != ADMIN_ID:
        await ctx.send("❌ Chỉ admin mới dùng được!")
        return
    
    db = load_db()
    total_users = len(db["users"])
    total_money = sum(u.get("money", 0) for u in db["users"].values())
    
    embed = discord.Embed(title="📊 Thống kê server", color=0x0099FF)
    embed.add_field(name="👥 Tổng user", value=total_users, inline=True)
    embed.add_field(name="💰 Tổng tiền", value=f"{total_money:,}", inline=True)
    
    if ADMIN_ID:
        admin_money = gambling.get_user_money(ADMIN_ID)
        embed.add_field(name="💵 Tiền admin", value=f"{admin_money:,}", inline=True)
    
    await ctx.send(embed=embed)

# ==================== RUN BOT ====================

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ Lỗi: Không tìm thấy DISCORD_TOKEN trong .env")
        print("Vui lòng tạo file .env và thêm: DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE")
    else:
        bot.run(DISCORD_TOKEN)
