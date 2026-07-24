# 📂 Project Structure - 2zer011 Bot

## 📁 Cấu trúc thư mục

```
2zer011_bot/
│
├── 📄 bot_updated.py          ⭐ FILE CHÍNH (Chạy cái này!)
├── 📄 gambling_bot.py          (Phiên bản cũ - không dùng .env)
├── 📄 config.json              (Tùy chỉnh thông số game)
├── 📄 requirements.txt          (Dependencies Python)
│
├── 📋 .env.example             (Template - Copy sang .env)
├── 📋 .env                     (⚠️ KHÔNG share - chứa token)
├── 📋 .gitignore               (Git ignore rules)
│
├── 📚 README.md                📖 Hướng dẫn đầy đủ (BẮT ĐẦU ĐÂY!)
├── 📚 QUICKSTART.md            🚀 Setup nhanh 5 phút
├── 📚 COMMANDS.md              📚 Danh sách tất cả lệnh
├── 📚 ADVANCED.md              🔧 Tùy chỉnh nâng cao
├── 📚 CHANGELOG.md             📝 Lịch sử cập nhật
├── 📚 PROJECT_STRUCTURE.md     📂 File này
│
├── 📊 gambling_data.json       (⚠️ Database - tự tạo)
└── 📦 2zer011_bot.zip         (Archive của project)
```

---

## 🎯 Các file quan trọng

### ⭐ Core Files (Bắt buộc)

| File | Mục đích | Chỉnh sửa |
|------|---------|----------|
| **bot_updated.py** | Bot chính | Nếu cần custom |
| **requirements.txt** | Dependencies | Hiếm khi |
| **.env** | Token Discord | 1 lần setup |

### 📖 Documentation (Hướng dẫn)

| File | Khi nào đọc |
|------|-------------|
| **QUICKSTART.md** | ✅ Lần đầu - Setup nhanh |
| **README.md** | ✅ Cần hiểu chi tiết |
| **COMMANDS.md** | 🎮 Muốn biết tất cả lệnh |
| **ADVANCED.md** | 🔧 Muốn custom bot |
| **CHANGELOG.md** | 📝 Cần biết thay đổi |

### ⚙️ Config Files (Tùy chỉnh)

| File | Dùng để |
|------|---------|
| **config.json** | Tùy chỉnh thông số game (optional) |
| **.gitignore** | Git ignore (nếu dùng Git) |

### 📊 Data Files (Runtime)

| File | Khi nào có |
|------|-----------|
| **.env** | Sau setup - Chứa DISCORD_TOKEN |
| **gambling_data.json** | Sau lần chạy đầu - Database |

---

## 🚀 Quick Start Path (Đường dẫn bắt đầu)

```
1. Giải nén 2zer011_bot.zip
   ↓
2. Đọc QUICKSTART.md (5 phút)
   ↓
3. Tạo file .env + thêm token
   ↓
4. Chạy: python bot_updated.py
   ↓
5. Vào Discord → !vi
   ✅ XONG!
```

---

## 📚 Learning Path (Học tập)

### Level 0: Beginner (Mới)
```
1. QUICKSTART.md      ← Start here
2. COMMANDS.md        ← Học tất cả lệnh
3. Chơi vài game
```

### Level 1: Intermediate (Trung bình)
```
1. README.md          ← Chi tiết
2. COMMANDS.md        ← Chiến lược chơi
3. Admin commands     ← Quản lý
```

### Level 2: Advanced (Nâng cao)
```
1. ADVANCED.md        ← Thêm game
2. config.json        ← Tùy chỉnh
3. bot_updated.py     ← Source code
```

### Level 3: Expert (Chuyên gia)
```
1. CHANGELOG.md       ← Tech debt
2. Source code        ← Deep dive
3. Contribute PR      ← Giúp đỡ
```

---

## 🔍 File Details

### bot_updated.py (Core)
```python
# ~650 lines
# Contains:
- Discord bot setup
- Database functions (load/save)
- Shop items config
- Game logic (6 games)
- Admin commands
- User commands
```

**Tùy chỉnh:**
- Thay đổi multiplier game
- Thêm game mới
- Thay đổi tax %
- Thêm item shop

### requirements.txt (Dependencies)
```
discord.py==2.3.2
python-dotenv==1.0.0
```

**Cài đặt:**
```bash
pip install -r requirements.txt
```

### .env (Environment Variables)
```
DISCORD_TOKEN=your_bot_token_here
```

⚠️ **BẤT CỨU SHARE!**
- Không push lên Git
- Không post publicly
- Không cho ai xem

### config.json (Optional)
```json
{
  "bot": {"prefix": "!"},
  "economy": {
    "work_cooldown_seconds": 120,
    "tax_percentage": 5
  },
  "games": {...},
  "shop": {...}
}
```

**Chưa được sử dụng trong v1.0.0** - Chuẩn bị cho v1.1.0

### gambling_data.json (Database)
```json
{
  "users": {
    "123456789": {
      "money": 50000,
      "items": {
        "lucky_charm": 1,
        "golden_coin": 0
      }
    }
  }
}
```

**Tự tạo sau lần chạy đầu**

---

## 🔄 File Dependencies

```
bot_updated.py
├── Imports: discord, json, os, random, datetime
├── Reads: .env (DISCORD_TOKEN)
├── Reads/Writes: gambling_data.json (database)
└── Optional: config.json (future versions)

requirements.txt
└── discord.py 2.3.2
└── python-dotenv 1.0.0
```

---

## 📊 File Sizes

| File | Size | Zip |
|------|------|-----|
| bot_updated.py | ~20KB | ~5KB |
| gambling_bot.py | ~20KB | ~5KB |
| README.md | ~8KB | ~4KB |
| COMMANDS.md | ~12KB | ~5KB |
| QUICKSTART.md | ~3KB | ~2KB |
| config.json | ~2KB | ~1KB |
| requirements.txt | <1KB | <1KB |
| Total | ~65KB | ~22KB |

---

## 🛠️ Chỉnh sửa hướng dẫn

### Chỉnh sửa lệnh game
→ Sửa trong `bot_updated.py`

### Thêm game mới
→ Thêm function mới trong `bot_updated.py`

### Thay đổi thông số
→ Sửa multiplier trong game functions

### Thêm item shop
→ Thêm vào `SHOP_ITEMS` dict

### Thay đổi prefix (!)
→ Sửa line: `bot = commands.Bot(command_prefix='!')`

### Thay đổi tax %
→ Tìm `tax = int(winnings * 0.05)` → sửa `0.05`

---

## 📤 Deploy Guide

### Local (Development)
```bash
python bot_updated.py
```

### Replit (Easy)
1. Upload ZIP
2. Create .env
3. Click Run

### Heroku (24/7)
1. Create Heroku app
2. Push code
3. Set DISCORD_TOKEN

### VPS (Advanced)
1. SSH vào server
2. Clone repo
3. Setup systemd service

---

## 🔒 Security Checklist

- ✅ Thêm DISCORD_TOKEN vào .env
- ✅ Thêm .env vào .gitignore
- ✅ Không share .env file
- ✅ Regenerate token nếu leak
- ✅ Backup gambling_data.json định kỳ
- ✅ Restrict admin commands

---

## 📝 Common Edits

### Tăng tiền work
```python
# Line ~192
money_earned = random.randint(1000, 2000)
# Thành
money_earned = random.randint(5000, 10000)
```

### Giảm tax
```python
# Tìm: tax = int(winnings * 0.05)
# Thành
tax = int(winnings * 0.01)  # 1% instead of 5%
```

### Tăng hệ số game
```python
# Tìm: winnings = int(bet * 2 * multiplier)
# Thành
winnings = int(bet * 3 * multiplier)  # 3x instead of 2x
```

### Thêm lệnh mới
```python
@bot.command(name='newcmd')
async def new_command(ctx):
    await ctx.send("Response!")
```

---

## 🆘 Troubleshooting Files

- **Bot không online?** → Check DISCORD_TOKEN trong .env
- **Lệnh không chạy?** → Check prefix trong bot_updated.py
- **Database error?** → Check gambling_data.json permissions
- **Import error?** → Chạy: `pip install -r requirements.txt`

---

## 📞 Next Steps

1. **Mới?** → Đọc QUICKSTART.md
2. **Muốn chơi?** → Đọc COMMANDS.md
3. **Muốn custom?** → Đọc ADVANCED.md
4. **Có bug?** → Check CHANGELOG.md

---

**Happy coding! 🚀**
