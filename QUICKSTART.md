# 🚀 Quick Start - 2zer011 Bot

Chạy bot trong 5 phút!

## 1️⃣ Tạo Bot trên Discord

1. Vào https://discord.com/developers/applications
2. Click **New Application** → Đặt tên → **Create**
3. Vào tab **Bot** → Click **Add Bot**
4. Dưới **TOKEN** → Click **Copy** (lưu lại)
5. Tìm **MESSAGE CONTENT INTENT** → Bật nó
6. **Save Changes**

## 2️⃣ Mời Bot vào Server

1. Vào tab **OAuth2** → **URL Generator**
2. Scopes: Chọn `bot`
3. Permissions: Chọn:
   - `Send Messages`
   - `Embed Links`
   - `Read Messages/View Channels`
   - `Read Message History`
4. Copy URL ở dưới → Mở link → Chọn server → **Authorize**

## 3️⃣ Setup Code

### Windows
```bash
# Tải Python (nếu chưa)
# https://www.python.org/

# Mở Command Prompt ở folder bot
pip install discord.py python-dotenv

# Tạo .env
echo DISCORD_TOKEN=PASTE_YOUR_TOKEN_HERE > .env

# Chạy bot
python bot_updated.py
```

### Mac/Linux
```bash
pip3 install discord.py python-dotenv

# Tạo .env
echo "DISCORD_TOKEN=PASTE_YOUR_TOKEN_HERE" > .env

# Chạy bot
python3 bot_updated.py
```

## 4️⃣ Test Bot

Vào Discord server, gõ:
```
!vi
```

Nếu bot reply → ✅ Thành công!

---

## 📝 Khởi tạo tiền cho user

```
!init @username 50000
```

## 🎮 Thử chơi game đầu tiên

```
!flip 1000
```

## 🆘 Lỗi?

### Bot không online
- Check token trong `.env` đúng chưa
- Bot có MESSAGE_CONTENT_INTENT chưa
- Click "Save Changes" nếu chỉnh bot settings

### Lỗi `ModuleNotFoundError`
```bash
# Windows
pip install discord.py python-dotenv

# Mac/Linux
pip3 install discord.py python-dotenv
```

### Lệnh không chạy
- Check prefix (mặc định là `!`)
- Bot có permission Send Messages không?

---

**OK xong! Chúc chơi vui! 🎰**
