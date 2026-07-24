# ❓ FAQ - 2zer011 Bot

## Setup & Installation

### ❓ Bot không online
**Giải pháp:**
1. Check token trong `.env` đúng không?
2. Bot có permission `Send Messages` không?
3. Bot có role trong server không?
4. Restart bot: `Ctrl+C` → chạy lại

### ❓ Lỗi: `Token is invalid`
**Giải pháp:**
1. Vào Discord Developer Portal
2. Copy token mới từ Bot tab
3. Paste vào `.env`
4. Restart bot

### ❓ Lỗi: `ModuleNotFoundError: No module named 'discord'`
**Giải pháp:**
```bash
# Windows
pip install discord.py python-dotenv

# Mac/Linux
pip3 install discord.py python-dotenv
```

### ❓ Lỗi: `FileNotFoundError: .env`
**Giải pháp:**
1. Tạo file `.env` trong thư mục bot
2. Copy từ `.env.example`
3. Thêm DISCORD_TOKEN

### ❓ Bot không có permission gửi message
**Giải pháp:**
1. Vào Server Settings → Roles
2. Tìm bot role
3. Thêm permission:
   - Send Messages
   - Embed Links
   - Read Messages/View Channels

---

## Gameplay & Economy

### ❓ Làm sao kiếm tiền nhanh nhất?
**Trả lời:**
```
Option 1: Spam !w (mỗi 2 phút 1-2k)
- 30 lần/giờ = 30-60k/giờ (passive)

Option 2: Chơi game tỉ lệ cao
- !dice 10k → 60k (16% chance)
- !domin 10k 15 → 48.75k (cao hệ số)

Option 3: Combo
- !w liên tục + đầu tư item → thắng lớn
```

### ❓ Chiến lược chơi tốt nhất?
**Trả lời:**
```
Beginner:
- Chỉ play !flip, !dice, !taixiu
- Cược nhỏ (1-5k)
- Không all-in

Intermediate:
- Mix game theo thích hợp
- Cược 10-20k
- Mua 1-2 item

Advanced:
- Stack 3 item (3.6x buff)
- Play high-risk games (!domin 20+ bom)
- Bankroll management
```

### ❓ Mấy % để thắng?
**Trả lời:**

| Game | Win % | Hệ số | EV |
|------|-------|-------|-----|
| Flip | 50% | 2x | 0% |
| Dice | 16.7% | 6x | 0% |
| TaiXiu | 50% | 2x | 0% |
| Plane | 50% (avg) | 5x | -5% |
| Jackpot | 3.8% | 20x | -5% |
| Domin | 70% (10 bomb) | 2.5x | -5% |

*Expected Value âm vì có 5% tax*

### ❓ Tại sao lúc nào cũng thua?
**Trả lời:**
- Mỗi game -5% tax trên thắng
- Chỉ 50% chance trên many game
- Xác suất dài hạn = âm lợi
- **Giải pháp:** Play for fun, không for profit

### ❓ Làm sao reset tiền?
**Trả lời (Admin):**
```
!set @user 0           # Set 0
!set @user 100000      # Reset với 100k mới
```

---

## Shop & Items

### ❓ Nên mua item nào?
**Trả lời:**
```
Beginner (100M tiền):
- Không mua (quá đắt)

Intermediate (1B+ tiền):
- Mua golden_coin (1.5x)
- Lợi nhất về giá/hiệu năng

Advanced (5B+):
- Mua cả 3: lucky_charm + golden_coin + dragon_scale
- 1.2 × 1.5 × 2.0 = 3.6x multiplier!
```

### ❓ Item có hết không?
**Trả lời:**
- Không hết
- Item không bị mất khi chơi
- Có thể dùng mãi mãi
- Giá trị là permanent buff

### ❓ Chênh lệch item lớn lắm, sao vậy?
**Trả lời:**
- Item đắt = effect mạnh
- Dragon scale 2B, effect 2x
- = 1 lần thắng × 2 = lợi nhuận cao
- Đầu tư 2B, kiếm lại trong 2-3 game thắng

### ❓ Mua item có cách nào rẻ hơn?
**Trả lời:**
- Hiện tại không
- Giá cố định
- Đội một là chơi để kiếm tiền trước

---

## Admin & Management

### ❓ Làm sao set admin?
**Trả lời:**
```
Người admin đầu tiên gõ: !admin @newadmin
```

### ❓ Admin làm gì được?
**Trả lời:**
```
!add @user 5000        # Cộng tiền
!set @user 10000       # Set tiền
!init @user 50000      # Khởi tạo tiền
!info @user            # Xem thông tin
!stats                 # Thống kê server
!admin @user           # Đặt admin mới
```

### ❓ Nên cho user bao nhiêu tiền?
**Trả lời:**
- Beginner: 10-50k
- Regular: 50-100k
- VIP: 100-500k

### ❓ Làm sao xem tiền admin kiếm được?
**Trả lời:**
```
!stats              # Xem tiền admin
!info @joker.real   # (nếu admin là @joker.real)
```

### ❓ Tax 5% đó, lợi gì?
**Trả lời:**
- Admin kiếm từ người chơi thắng
- Tạo incentive cho admin
- Balance economy

---

## Bugs & Issues

### ❓ Bot reply rất chậm
**Giải pháp:**
- Bot bạn hosting ở đâu?
- Internet tốt không?
- Server Discord overload?

### ❓ Lệnh bị duplicate?
**Giải pháp:**
- Có 2 alias cho lệnh?
- Kiểm tra `@bot.command(aliases=...)`

### ❓ Database bị corrupt
**Giải pháp:**
```bash
# Backup trước
cp gambling_data.json gambling_data.json.backup

# Delete
rm gambling_data.json

# Bot sẽ tạo mới khi restart
```

### ❓ Tiền user bị mất
**Giải pháp:**
```
Restore backup: cp gambling_data.json.backup gambling_data.json
Hoặc: !add @user <tiền>
```

### ❓ User spam lệnh
**Giải pháp (Admin):**
```
!set @spammer 0        # Reset tiền
Hoặc: Remove user role
```

---

## Customization

### ❓ Có cách nào thay đổi prefix?
**Trả lời:**
```python
# bot_updated.py, line ~11
bot = commands.Bot(command_prefix='!')

# Thành
bot = commands.Bot(command_prefix='>')
```
Giờ dùng `>vi` thay vì `!vi`

### ❓ Làm sao thêm game mới?
**Trả lời:**
Xem ADVANCED.md → "Thêm Game Mới" section

### ❓ Có cách nào giảm tax?
**Trả lời:**
```python
# Tìm
tax = int(winnings * 0.05)

# Thành (1% tax)
tax = int(winnings * 0.01)
```

### ❓ Có thể tăng hệ số game?
**Trả lời:**
```python
# Ví dụ: Flip
# Cũ: winnings = int(bet * 2 * multiplier)
# Mới: winnings = int(bet * 3 * multiplier)  # 3x thay vì 2x
```

### ❓ Có cách nào backup database?
**Trả lời:**
```bash
# Lệnh bash
cp gambling_data.json gambling_data.json.backup.$(date +%Y%m%d)

# Hoặc dùng admin command
!export               # (nếu có)
```

---

## Hosting & Deployment

### ❓ Hosting ở đâu tốt nhất?
**Trả lời:**
- **Local:** Miễn phí, nhưng phải bật máy 24/7
- **Replit:** Miễn phí, tích hợp tốt, có "Always On"
- **Heroku:** Miễn phí (tiếp), reliable
- **VPS:** $5-20/tháng, full control

### ❓ Bot chạy 24/7 trên Heroku?
**Trả lời:**
- Có thể, nhưng phải có Pro account
- Hoặc dùng Replit (easy hơn)

### ❓ Có cách nào host miễn phí vĩnh viễn?
**Trả lời:**
- Replit 24/7 (free)
- Local machine (nếu chịu bật máy)

---

## Performance & Optimization

### ❓ Database sẽ không tăng quá lớn không?
**Trả lời:**
- v1.0.0: JSON file, có thể tăng
- v1.1.0: Migrate to SQLite (plan)
- Cách này lưu 1 user/100 byte ≈ 100MB per 1M users

### ❓ Bot sẽ lag khi có nhiều user?
**Trả lời:**
- Không nhiều, JSON load/save nhanh
- Nếu 10k+ users → nên migrate SQLite
- Hoặc dùng advanced database

### ❓ Có cách tối ưu không?
**Trả lời:**
- Xem ADVANCED.md → Caching section
- Hoặc dùng SQLite thay JSON

---

## Discord Features

### ❓ Bot có thể post embed không?
**Trả lời:**
- Có! Bot đã dùng embeds
- Colorful, professional looking

### ❓ Bot có thể tạo reaction menu không?
**Trả lời:**
- Có thể, nhưng v1.0 không có
- Có thể thêm ở v1.1

### ❓ Bot có thể kết nối database cloud không?
**Trả lời:**
- Có (MongoDB, PostgreSQL, etc)
- Có thể code thêm ở ADVANCED.md

---

## Moneytization & Support

### ❓ Có thể charge user tiền thật không?
**Trả lời:**
- **Không nên!** (Discord ToS violation)
- Chỉ dùng tiền ảo (2zer011 Coin)
- Không kết nối payment system

### ❓ Có thể kiếm tiền từ bot?
**Trả lời:**
- Gián tiếp: Ads, Patreon, Ko-fi
- Trực tiếp: Không allowed
- Tập trung vào mình vui

---

## Community & Support

### ❓ Có server Discord official không?
**Trả lời:**
- Hiện không
- Có thể tạo

### ❓ Có documentation không?
**Trả lời:**
- Có, 6 file:
  - README.md
  - QUICKSTART.md
  - COMMANDS.md
  - ADVANCED.md
  - CHANGELOG.md
  - FAQ.md (file này)

### ❓ Có preview/demo không?
**Trả lời:**
- Hiện không
- Có thể yêu cầu

---

## Miscellaneous

### ❓ Bot tên gì?
**Trả lời:**
- 2zer011 Bot
- Hoặc custom name khi setup

### ❓ Có Easter egg không?
**Trả lời:**
- Không (v1.0)
- Hãy suggest!

### ❓ Có theme song không?
**Trả lời:**
- Không :(
- Nhưng có emoji! 🎰🎲💰

### ❓ Support tiếng gì?
**Trả lời:**
- Tiếng Việt (hiện tại)
- Plan: English, Chinese (v1.1+)

---

## Chưa tìm thấy câu hỏi?

**Tùy chọn:**
1. Xem documentation files
2. Check source code comments
3. Discord community (soon)

---

**Last Update: July 24, 2024**
