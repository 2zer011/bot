# 📚 Danh sách lệnh - 2zer011 Bot

## 💰 Kiếm tiền & Ví

### !w (Work)
Làm việc để kiếm tiền
```
!w                    # Mặc định (lập trình)
!w fishing            # Đánh cá
!w mining             # Khai thác
!w farming            # Nông nghiệp
!w chef               # Nấu ăn
!w design             # Thiết kế
!w gaming             # Chơi game
```
- ⏱️ Cooldown: 2 phút
- 💵 Kiếm: 1,000-2,000 coin mỗi lần

### !vi (Wallet)
Xem ví tiền của bạn
```
!vi
```
- Hiển thị số dư
- Hiển thị item sở hữu

---

## 🎲 Các trò chơi

### !flip (Coin Flip)
Tung đồng xu - 50/50 may rủi
```
!flip 1000
```
- Hệ số thắng: **2x**
- Tax: -5%

### !dice (Dice Roll)
Tung xúc xắc, đoán số 1-6
```
!dice 1000 6          # Cược 1000, đoán số 6
!dice 5000 1
```
- Hệ số thắng: **6x** (1:6 xác suất)
- Tax: -5%

### !taixiu (Tai/Xiu)
Tài = tổng > 7, Xỉu = tổng ≤ 7
```
!taixiu 1000 tai      # Đoán tài
!taixiu 5000 xiu      # Đoán xỉu
```
- Hệ số thắng: **2x**
- Tax: -5%

### !plane (Plane)
Máy bay - chọn lúc rút tiền trước khi crash
```
!plane 1000
!plane 50000
```
- Hệ số: **1x - 10x** (ngẫu nhiên)
- Tax: -5%
- Rủi ro cao, may rủi cao

### !jackpot (Slot Machine)
Máy slot 3 bánh xe
```
!jackpot 2000
!jackpot 10000
```
- 3 ô giống: **20x**
- 2 ô giống: **3x**
- Khác: THUA
- Tax: -5%

### !domin (Minesweeper)
Dò mìn - 25 ô, 1-24 bom
```
!domin 1000 5         # 1000 coin, 5 bom
!domin 5000 15        # Rủi ro cao, hệ số cao
```
**Công thức hệ số:**
- Hệ số = 1 + (số bom × 0.15)
- 5 bom = 1.75x
- 10 bom = 2.5x
- 15 bom = 3.25x
- 24 bom = 4.6x

- Reveal 5 ô, không trúng bom = thắng
- Trúng 1 bom = THUA
- Tax: -5%

---

## 🏪 Shop & Item

### !shop
Xem cửa hàng item
```
!shop
```

### !buy
Mua item buff may mắn
```
!buy lucky_charm      # 🍀 500M coin (1.2x)
!buy golden_coin      # 🪙 1B coin (1.5x)
!buy dragon_scale     # 🐉 2B coin (2.0x)
!buy fortune_egg      # 🥚 3B coin (premium)
```

**Item Effect:**
- 1 item: 1.2x - 2.0x tiền thắng
- 2 item: 1.2 × 1.5 = 1.8x
- 3 item: 1.2 × 1.5 × 2.0 = 3.6x
- Càng nhiều item = tiền thắng càng lớn

**Ví dụ:**
```
Thắng 1000 coin với 3 item = 1000 × 3.6 = 3600 coin
```

---

## 🛡️ Admin Commands

### !add
Cộng tiền cho user
```
!add @username 5000
!add @user 1000000
```

### !set
Set số dư cho user
```
!set @username 10000
!set @user 0
```

### !init
Khởi tạo tiền cho user (mặc định 10k)
```
!init @username
!init @username 50000
```

### !admin
Đặt admin mới
```
!admin @username
```

### !info
Xem thông tin user
```
!info @username      # Xem info user khác
!info                # Xem info bản thân
```

### !stats
Thống kê toàn server
```
!stats
```
- Tổng user
- Tổng tiền toàn server
- Tiền của admin

---

## 🎯 Chiến lược chơi

### Beginner (Bình thường)
```
!w                 # Kiếm 1-2k
!flip 1000         # Thắng 2k, thua 1k (50/50)
!dice 1000 6       # Thắng 6k (16% chance)
```

### Intermediate (Trung bình)
```
!taixiu 5000 tai   # Thắng 10k (50% chance)
!plane 10000       # Thắng 10-100k (risky)
```

### Advanced (Nâng cao)
```
!domin 50000 10    # Thắng 125k (cao hệ số)
!jackpot 100000    # Thắng 300k-2M (lottery)
```

### Pro (Item build)
```
!buy golden_coin          # 1B coin (1.5x)
!buy dragon_scale         # 2B coin (2.0x)
!domin 50000 15          # Thắng 50k × 3.25 × 2.0 = 325k
```

---

## 💡 Tips & Tricks

1. **Item Stacking**
   - Mua nhiều item khác nhau để stack effect
   - 3 item = 3.6x multiplier

2. **Work Farming**
   - Spam `!w` mỗi 2 phút → kiếm passive income
   - 1000-2000 × 30 lần/giờ = 30-60k/giờ

3. **Low Risk**
   - `!flip` + `!dice` + `!taixiu` = 50-50 hoặc 16%
   - Chọn game mình thoải mái với xác suất

4. **High Risk High Reward**
   - `!domin` 20+ bom = hệ số 4x+
   - Nhưng tỷ lệ trúng bomb cao

5. **Bankroll Management**
   - Đừng all-in 1 lần
   - Phân chia tiền thành 10-20 lần cược
   - Dừng khi thua, dừng khi thắng lớn

---

## 📊 Xác suất

| Game | Xác suất thắng | Hệ số | Expected Value |
|------|---|---|---|
| Flip | 50% | 2x | 0% |
| Dice (1-6) | 16.67% | 6x | 0% |
| TaiXiu | 50% | 2x | 0% |
| Plane | 50% (avg) | 5x (avg) | 0% |
| Jackpot | 3.8% | 20x | -4% |
| Domin 10 | 72% | 2.5x | -4% (approx) |

*Expected Value = Xác suất × Hệ số - 1*

---

## ⚠️ Lưu ý

- ✅ **Luôn có 5% tax** khi thắng
- ✅ **Cooldown 2 phút** mỗi work
- ✅ **Không thể âm tiền** - thua hết = stop
- ✅ **Item không mất** khi chơi, dùng để buff

---

**Chúc bạn chơi vui! 🎰💰**
