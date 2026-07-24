# 🔧 Advanced - Tùy chỉnh Bot

Hướng dẫn cho những ai muốn customize bot theo ý muốn.

## 📝 Thêm Game Mới

### Bước 1: Tạo function game

```python
@bot.command(name='newgame', help='Mô tả game')
async def new_game(ctx, bet: int):
    # Kiểm tra cược
    if bet <= 0:
        await ctx.send("❌ Cược phải > 0!")
        return
    
    # Kiểm tra tiền
    user_money = gambling.get_user_money(ctx.author.id)
    if user_money < bet:
        await ctx.send(f"❌ Không đủ tiền!")
        return
    
    # Trừ tiền cược
    gambling.set_user_money(ctx.author.id, user_money - bet)
    
    # Logic game
    result = random.random() > 0.5  # 50% thắng
    
    # Tính multiplier và item buff
    multiplier = gambling.get_multiplier(ctx.author.id)
    
    # Xử lý thắng/thua
    if result:
        winnings = int(bet * 3 * multiplier)  # 3x hệ số
        tax = int(winnings * 0.05)
        actual_win = winnings - tax
        
        gambling.add_user_money(ctx.author.id, actual_win)
        if ADMIN_ID:
            gambling.add_user_money(ADMIN_ID, tax)
        
        await ctx.send(f"✅ **THẮNG!** Thắng {actual_win:,} coin!")
    else:
        await ctx.send(f"❌ **THUA!**")
```

---

## 🎨 Thay đổi Thông số Game

### Tăng/giảm hệ số thắng

```python
# Thay đây
winnings = int(bet * 3 * multiplier)  # 3x

# Thành
winnings = int(bet * 5 * multiplier)  # 5x (cao hơn)
```

### Thay đổi tax %

```python
# File: bot_updated.py, line ~420
tax = int(winnings * 0.05)  # 5%

# Thành
tax = int(winnings * 0.10)  # 10% tax
```

### Thay đổi cooldown work

```python
# File: bot_updated.py, line ~180
if time_diff < 120:  # 2 phút = 120 giây

# Thành
if time_diff < 60:   # 1 phút
```

### Thay đổi tiền kiếm từ work

```python
# File: bot_updated.py, line ~192
money_earned = random.randint(1000, 2000)

# Thành
money_earned = random.randint(5000, 10000)  # Cao hơn
```

---

## 🛍️ Thêm Item Shop

### Bước 1: Thêm item vào SHOP_ITEMS

```python
SHOP_ITEMS = {
    "existing_item": {...},
    
    # Thêm item mới
    "lucky_ring": {
        "price": 750_000_000, 
        "name": "💍 Vòng may mắn", 
        "effect": "x1.3 multiplier"
    },
}
```

### Bước 2: Thêm logic buff vào get_multiplier

```python
def get_multiplier(self, user_id: str) -> float:
    data = self.get_user_data(user_id)
    multiplier = 1.0
    items = data.get("items", {})
    
    # Items cũ
    if items.get("lucky_charm", 0) > 0:
        multiplier *= 1.2
    
    # Item mới
    if items.get("lucky_ring", 0) > 0:
        multiplier *= 1.3
    
    return multiplier
```

---

## 🎮 Thay đổi Tên Game/Lệnh

### Rename lệnh

```python
# Cũ
@bot.command(name='flip')
async def flip(ctx, bet: int):

# Mới
@bot.command(name='coinflip', aliases=['flip', 'coin'])
async def flip(ctx, bet: int):
```

Giờ người chơi có thể gõ: `!coinflip`, `!flip`, hoặc `!coin`

---

## 💾 Backup & Restore Database

### Backup
```python
import shutil
import datetime

def backup_db():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy(DB_FILE, f"backup_gambling_data_{timestamp}.json")
```

### Restore
```python
def restore_db(backup_file):
    shutil.copy(backup_file, DB_FILE)
    print(f"✅ Restored from {backup_file}")
```

---

## 📊 Thêm Leaderboard

```python
@bot.command(name='leaderboard')
async def leaderboard(ctx, top: int = 10):
    db = load_db()
    users = []
    
    for user_id, data in db["users"].items():
        users.append((user_id, data["money"]))
    
    users.sort(key=lambda x: x[1], reverse=True)
    
    embed = discord.Embed(title=f"🏆 Top {top} Giàu nhất", color=0xFFD700)
    
    for i, (user_id, money) in enumerate(users[:top], 1):
        try:
            user = await bot.fetch_user(int(user_id))
            embed.add_field(
                name=f"#{i} {user.name}",
                value=f"{money:,} coin",
                inline=False
            )
        except:
            pass
    
    await ctx.send(embed=embed)
```

---

## 🔐 Reset Toàn Bộ Database

```python
@bot.command(name='resetdb')
async def reset_db(ctx):
    global ADMIN_ID
    
    if ctx.author.id != ADMIN_ID:
        await ctx.send("❌ Admin only!")
        return
    
    # Backup trước
    import shutil
    shutil.copy(DB_FILE, f"{DB_FILE}.backup")
    
    # Reset
    save_db({"users": {}, "shop_inventory": {}})
    
    await ctx.send("✅ Database đã reset! Backup: gambling_data.json.backup")
```

---

## 🎯 Custom Messages

### Thay đổi embed colors

```python
# Mặc định
embed = discord.Embed(title='...', color=0xFFD700)  # Gold

# Màu khác
0xFF0000  # Red
0x00FF00  # Green
0x0000FF  # Blue
0xFFFFFF  # White
0x000000  # Black
```

### Thay đổi emoji

Tìm file và thay thế emoji:

```python
# Thắng
"✅ **THẮNG!**" → "🎉 **THẮNG RỒI!**"

# Thua
"❌ **THUA!**" → "😢 **THUA MẤT RỒI!**"

# Tiền
"💰" → "💵"
"💵" → "💸"
```

---

## 🔄 Multi-Server Support

Bot mặc định hỗ trợ nhiều server. Mỗi user có account riêng (dùng user_id).

Nếu muốn per-server economy:

```python
def get_user_money(self, user_id: str, guild_id: str) -> int:
    db = load_db()
    key = f"{guild_id}_{user_id}"
    return db["users"].get(key, {}).get("money", 0)
```

---

## 📈 Thêm Statistics Tracking

```python
def get_user_stats(self, user_id: str) -> dict:
    db = load_db()
    return db["users"].get(str(user_id), {}).get("stats", {
        "games_played": 0,
        "wins": 0,
        "losses": 0,
        "total_earned": 0,
        "total_lost": 0,
    })

def update_stats(self, user_id: str, won: bool, amount: int):
    db = load_db()
    user_id = str(user_id)
    
    if "stats" not in db["users"][user_id]:
        db["users"][user_id]["stats"] = {
            "games_played": 0, "wins": 0, "losses": 0,
            "total_earned": 0, "total_lost": 0
        }
    
    stats = db["users"][user_id]["stats"]
    stats["games_played"] += 1
    
    if won:
        stats["wins"] += 1
        stats["total_earned"] += amount
    else:
        stats["losses"] += 1
        stats["total_lost"] += amount
    
    save_db(db)
```

---

## 🚀 Deploy Production

### Heroku
```bash
# 1. Tạo Heroku account + install CLI

# 2. Login
heroku login

# 3. Create app
heroku create your-bot-name

# 4. Set config vars
heroku config:set DISCORD_TOKEN=your_token

# 5. Deploy
git push heroku main
```

Cần file `Procfile`:
```
worker: python bot_updated.py
```

### Replit
1. Upload code
2. Tạo `.env` với token
3. Click "Run"

---

## 🐛 Debug Mode

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Command error: {error}")
    await ctx.send(f"❌ Error: {error}")
```

---

## 📦 Export Database

```python
import json

@bot.command(name='export')
async def export_db(ctx):
    global ADMIN_ID
    if ctx.author.id != ADMIN_ID:
        return
    
    db = load_db()
    with open('export.json', 'w') as f:
        json.dump(db, f, indent=2)
    
    await ctx.send(file=discord.File('export.json'))
```

---

**Happy coding! 🚀**
