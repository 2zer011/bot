# 🎰 2zer011 Gambling Bot - Discord

Một bot Discord hoàn chỉnh với hệ thống cờ bạc bằng tiền ảo **2zer011 Coin**.

## ✨ Tính năng

### 💰 Kiếm tiền
- `!w <công việc>` - Làm việc mỗi 2 phút kiếm 1-2k coin
- Công việc có sẵn: `default`, `fishing`, `mining`, `farming`, `chef`, `design`, `gaming`

### 🎲 Các trò chơi cờ bạc

| Lệnh | Mô tả | Hệ số thắng |
|------|-------|-----------|
| `!flip <tiền cược>` | Tung đồng xu | 2x |
| `!dice <tiền> <1-6>` | Xúc xắc | 6x |
| `!taixiu <tiền> <tai\|xiu>` | Tài/Xỉu | 2x |
| `!plane <tiền cược>` | Máy bay | 1-10x |
| `!jackpot <tiền cược>` | Máy jackpot | 3-20x |
| `!domin <tiền> <bom>` | Dò mìn | 1.15x-3.6x |

### 🏪 Shop
- `!shop` - Xem các item buff may mắn
- `!buy <item_id>` - Mua item
- Item giúp tăng tiền thắng từ 1.2x đến 2.0x

**Item có sẵn:**
- 🍀 Bùa may mắn - 500M coin (1.2x)
- 🪙 Đồng xu vàng - 1B coin (1.5x)
- 🐉 Vảy rồng - 2B coin (2.0x)
- 🥚 Quả trứng may mắn - 3B coin

### 👤 Ví & Quản lý
- `!vi` - Xem ví của bạn

### 🛡️ Lệnh Admin
- `!add <user> <tiền>` - Cộng tiền
- `!set <user> <tiền>` - Set tiền
- `!init <user> [tiền=10000]` - Khởi tạo tiền
- `!admin <user>` - Đặt admin mới
- `!info [user]` - Xem thông tin user
- `!stats` - Thống kê toàn server

## 🔧 Cài đặt

### 1. Clone/Download Bot
```bash
git clone <repo-url>
cd gambling_bot
```

### 2. Cài đặt Dependencies
```bash
pip install -r requirements.txt
```

### 3. Tạo Discord Bot
1. Vào [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Đặt tên bot (VD: "2zer011 Bot")
4. Vào tab "Bot" → Click "Add Bot"
5. Copy token dưới "TOKEN"

### 4. Cấu hình Bot
1. Tạo file `.env`:
```bash
cp .env.example .env
```

2. Mở `.env` và thêm token:
```
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
```

### 5. Cấp quyền cho Bot
Trong Developer Portal:
- Bot Permissions:
  - `Send Messages`
  - `Embed Links`
  - `Read Message History`
  - `Add Reactions`
  - `Use Slash Commands`

OAuth2 URL: Chọn scopes `bot`, permissions trên, copy URL để mời bot vào server

### 6. Chạy Bot
```bash
python bot_updated.py
```

## 📊 Cách chơi

### Tài/Xỉu
```
!taixiu 1000 tai
```
- Tung 2 xúc xắc, tính tổng
- Tài = > 7, Xỉu = <= 7
- Thắng x2 tiền cược

### Dò mìn
```
!domin 1000 10
```
- 25 ô tổng, 10 ô có bom
- Hệ số = 1 + (số bom × 0.15)
- Càng nhiều bom → càng lớn hệ số (nhưng rủi ro cao)
- Reveal 5 ô, không trúng bom = thắng

### Máy bay
```
!plane 5000
```
- Máy bay bay với hệ số ngẫu nhiên
- Bạn chọn lúc nào rút tiền
- Nếu rút trước crash = thắng, nếu crash trước = thua

## 💡 Hệ thống Item

Mỗi item có thể stack:
- 1 item = 1.2x
- 2 item khác nhau = 1.2 × 1.5 = 1.8x
- 3 item khác nhau = 1.2 × 1.5 × 2.0 = 3.6x

Ví dụ: Thắng 1000 coin với đủ item = 3600 coin

## 💸 Tax System

- Mỗi lần thắng bị trừ **5%** gửi vào ví Admin
- Admin có quyền cộng/trừ tiền người dùng
- Dữ liệu lưu trong `gambling_data.json`

## 📁 Cấu trúc Files

```
gambling_bot/
├── bot_updated.py          # Bot chính
├── gambling_bot.py          # Version cũ (không dùng token .env)
├── requirements.txt         # Dependencies
├── .env                     # Token (KHÔNG share)
├── .env.example            # Template .env
├── gambling_data.json      # Database (tự tạo)
└── README.md               # File này
```

## 🛡️ Bảo mật

- **Không share token** trong commit
- File `.env` đã được thêm vào `.gitignore`
- Database `gambling_data.json` lưu trên local

## 🚀 Hosting (Optional)

Để bot chạy 24/7:

### Replit
1. Upload code lên Replit
2. Tạo `.env` với token
3. Run `python bot_updated.py`
4. Bật "Always on" (Pro)

### Heroku
```bash
heroku create your-bot-name
git push heroku main
```

Cần tạo file `Procfile`:
```
worker: python bot_updated.py
```

## ❓ Troubleshooting

### Bot offline
- Check token trong `.env` đúng chưa
- Bot có online permission chưa

### Lệnh không chạy
- Check prefix (hiện tại là `!`)
- Bot có role để send message không

### Lỗi import
```bash
pip install -r requirements.txt --upgrade
```

## 📝 Thêm tính năng

Muốn thêm game mới? Copy template:
```python
@bot.command(name='tenmoi')
async def game_moi(ctx, bet: int):
    user_money = gambling.get_user_money(ctx.author.id)
    if user_money < bet:
        await ctx.send(f"❌ Không đủ tiền!")
        return
    
    gambling.set_user_money(ctx.author.id, user_money - bet)
    
    # Logic game ở đây
    result = random.random() > 0.5
    
    if result:
        winnings = int(bet * 2 * gambling.get_multiplier(ctx.author.id))
        tax = int(winnings * 0.05)
        actual_win = winnings - tax
        gambling.add_user_money(ctx.author.id, actual_win)
        if ADMIN_ID:
            gambling.add_user_money(ADMIN_ID, tax)
        await ctx.send(f"✅ Thắng {actual_win:,}!")
    else:
        await ctx.send(f"❌ Thua!")
```

## 📞 Support

Lỗi? Hãy check:
1. Token đúng không?
2. Bot có permisison không?
3. Database file tồn tại không?

---

**Made with ❤️ for 2zer011**

v1.0 | 2024
