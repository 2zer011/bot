# 📝 Changelog - 2zer011 Bot

## [v1.0.0] - 2024-07-24

### ✨ Features
- ✅ **Kiếm tiền**: `!w <job>` với cooldown 2 phút (1-2k/lần)
- ✅ **6 Game cờ bạc**:
  - Tung đồng xu (`!flip`) - 2x
  - Xúc xắc (`!dice`) - 6x
  - Tài/Xỉu (`!taixiu`) - 2x
  - Máy bay (`!plane`) - 1-10x
  - Máy jackpot (`!jackpot`) - 3-20x
  - Dò mìn (`!domin`) - 1.15-4.6x

- ✅ **Shop System**: 4 item buff may mắn
  - 🍀 Bùa may mắn - 1.2x (500M)
  - 🪙 Đồng xu vàng - 1.5x (1B)
  - 🐉 Vảy rồng - 2.0x (2B)
  - 🥚 Quả trứng may mắn - special (3B)

- ✅ **Economy System**:
  - Database JSON persistent
  - 5% tax trên tiền thắng → admin
  - Item buff stacking (3.6x max)

- ✅ **Admin Commands**:
  - `!add <user> <amount>` - Cộng tiền
  - `!set <user> <amount>` - Set tiền
  - `!init <user>` - Khởi tạo
  - `!admin <user>` - Set admin mới
  - `!info <user>` - Xem thông tin
  - `!stats` - Thống kê server

- ✅ **User Commands**:
  - `!vi` - Xem ví
  - `!shop` - Xem shop
  - `!buy <item>` - Mua item

### 📚 Documentation
- README.md - Hướng dẫn setup đầy đủ
- QUICKSTART.md - Setup nhanh 5 phút
- COMMANDS.md - Danh sách tất cả lệnh
- ADVANCED.md - Hướng dẫn custom

### 🔧 Technical
- discord.py 2.3.2
- JSON database
- .env environment variables
- Error handling & validation

---

## [v1.1.0] - Coming Soon 🚧

### 🎯 Planned Features
- [ ] Leaderboard (`!lb`, `!top10`)
- [ ] User stats tracking (wins/losses)
- [ ] Daily reward system
- [ ] Weekly lottery
- [ ] Guild economy (team betting)
- [ ] Custom game odds editor
- [ ] Transaction history (`!history`)
- [ ] Blacklist system
- [ ] Cooldown per game type
- [ ] Multi-language support (EN, VN, CN)

### 🎮 New Games
- [ ] Rock-Paper-Scissors
- [ ] Higher/Lower
- [ ] Roulette
- [ ] Blackjack
- [ ] Poker
- [ ] Crash game v2

### 💎 Premium Features
- [ ] VIP role perks
- [ ] Double rewards
- [ ] Reduced tax
- [ ] Priority support

### 🗄️ Database
- [ ] Migrate to SQLite
- [ ] Cloud backup
- [ ] Auto-save intervals
- [ ] Data import/export

---

## [v1.2.0] - Future 🔮

### Major Updates
- [ ] Web dashboard
- [ ] API endpoints
- [ ] Mobile app companion
- [ ] Trading system (user-to-user)
- [ ] Auction house
- [ ] Battle pass system

### Performance
- [ ] Caching layer
- [ ] Async database
- [ ] Rate limiting
- [ ] Load balancing

---

## Bug Fixes & Improvements

### v1.0.1 (Hotfixes)
- Fixed: Admin commands error handling
- Improved: Tax calculation precision
- Added: Command help messages
- Better: Error messages clarity

### v1.0.2
- Fixed: Database file creation
- Improved: Item effect stacking
- Added: Multiplier display in embeds
- Better: Cooldown messaging

---

## Known Issues

### Current (v1.0.0)
- ⚠️ Database not auto-backup (manual backup recommended)
- ⚠️ No transaction history yet
- ⚠️ Single-threaded (may slow on high traffic)
- ⚠️ JSON database not ideal for large servers

### Workarounds
- Backup `gambling_data.json` regularly
- Use `!stats` to track changes
- Deploy on stable host
- Monitor file size (if huge, migrate to SQLite)

---

## Deprecated

### v0.x (Original)
- `!gamble` (merged into specific game commands)
- Simple wallet (now has items)
- No admin commands

---

## Version Compatibility

| Version | Discord.py | Python | Status |
|---------|------------|--------|--------|
| v1.0.0 | 2.3.2 | 3.8+ | ✅ Active |
| v1.1.0 | 2.3.2+ | 3.8+ | 🚧 In Dev |
| v1.2.0 | 2.4.0+ | 3.9+ | 🔮 Planned |

---

## Migration Guide

### v0.x → v1.0.0
```bash
# Backup old database
cp gambling_data.json gambling_data.json.backup

# No migration needed - compatible!
# Just update bot_updated.py
```

---

## Contributors
- **2zer011** - Original concept & design
- **Claude** - Development & testing

---

## License
MIT License - Free to use and modify

---

## Feedback & Requests

Tính năng muốn thêm? Bug cần sửa?
- Gửi issue
- Gửi pull request
- Discord DM

---

**Latest Update: July 24, 2024**
