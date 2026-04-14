"""
2zer011 Discord Bot
Tác giả: joker.real
Phiên bản: 2.0 (Mở rộng)
Mô tả: Bot tiền ảo với nhiều trò chơi và hệ thống nghề nghiệp.
"""

import discord
from discord.ext import commands
from discord.ui import View, Button
import random
import json
import asyncio
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple

# ==================== CONFIG ====================
TOKEN = 'YOUR_BOT_TOKEN_HERE'  # <-- THAY TOKEN CỦA BẠN VÀO ĐÂY
DATA_FILE = 'data.json'

# ==================== INTENTS ====================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# ==================== DATA MANAGEMENT ====================
_data_lock = asyncio.Lock()

def load_data() -> Dict[str, Any]:
    """Tải dữ liệu từ file JSON."""
    if not os.path.exists(DATA_FILE):
        return {"users": {}, "daily": {}, "work_cooldown": {}, "investments": {}}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Đảm bảo các trường mới tồn tại
            if "work_cooldown" not in data:
                data["work_cooldown"] = {}
            if "investments" not in data:
                data["investments"] = {}
            if "users" in data:
                for uid in data["users"]:
                    if "job" not in data["users"][uid]:
                        data["users"][uid]["job"] = None
                        data["users"][uid]["job_level"] = 1
                        data["users"][uid]["job_exp"] = 0
                    if "last_work" not in data["users"][uid]:
                        data["users"][uid]["last_work"] = None
            return data
    except (json.JSONDecodeError, IOError):
        return {"users": {}, "daily": {}, "work_cooldown": {}, "investments": {}}

async def save_data(data: Dict[str, Any]) -> None:
    """Lưu dữ liệu bất đồng bộ."""
    async with _data_lock:
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Lỗi ghi file: {e}")

def get_user_data(user_id: int) -> Dict[str, Any]:
    """Lấy dữ liệu user, tự động tạo mới nếu chưa có."""
    data = load_data()
    uid = str(user_id)
    if uid not in data["users"]:
        data["users"][uid] = {
            "balance": 100,
            "last_daily": None,
            "job": None,
            "job_level": 1,
            "job_exp": 0,
            "last_work": None
        }
        asyncio.create_task(save_data(data))
    return data["users"][uid]

async def update_balance(user_id: int, amount: int, operation: str = "set") -> int:
    """Cập nhật số dư."""
    data = load_data()
    uid = str(user_id)
    if uid not in data["users"]:
        data["users"][uid] = {
            "balance": 100,
            "last_daily": None,
            "job": None,
            "job_level": 1,
            "job_exp": 0,
            "last_work": None
        }

    if operation == "add":
        data["users"][uid]["balance"] += amount
    elif operation == "subtract":
        data["users"][uid]["balance"] -= amount
    elif operation == "set":
        data["users"][uid]["balance"] = amount

    if data["users"][uid]["balance"] < 0:
        data["users"][uid]["balance"] = 0

    await save_data(data)
    return data["users"][uid]["balance"]

async def get_balance(user_id: int) -> int:
    data = load_data()
    uid = str(user_id)
    return data["users"].get(uid, {}).get("balance", 100)

def create_embed(title: str, description: str, color: discord.Color = discord.Color.blue()) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="2zer011 Bot • Tiền ảo 2zer011 coin")
    return embed

# ==================== JOBS DEFINITIONS ====================
JOBS = {
    "lập trình viên": {"base_salary": 80, "emoji": "💻", "description": "Code ngày đêm, lương cao nhưng áp lực."},
    "nông dân": {"base_salary": 40, "emoji": "🌾", "description": "Trồng trọt, chăn nuôi, thu nhập ổn định."},
    "thợ mỏ": {"base_salary": 60, "emoji": "⛏️", "description": "Đào vàng, đá quý, nhưng mệt."},
    "nhân viên văn phòng": {"base_salary": 50, "emoji": "📋", "description": "Công việc nhẹ nhàng, lương vừa phải."},
    "tài xế": {"base_salary": 70, "emoji": "🚗", "description": "Lái xe đường dài, thu nhập khá."},
    "bác sĩ": {"base_salary": 100, "emoji": "🩺", "description": "Cứu người, lương cao nhưng đòi hỏi trình độ."},
    "đầu bếp": {"base_salary": 55, "emoji": "🍳", "description": "Nấu ăn ngon, có tips."},
    "cảnh sát": {"base_salary": 65, "emoji": "👮", "description": "Giữ trật tự, lương ổn."}
}

# ==================== UTILS ====================
def is_admin(ctx: commands.Context) -> bool:
    """Kiểm tra admin đặc biệt."""
    return ctx.author.name == "joker.real"

def validate_bet(ctx: commands.Context, bet: int, balance: int) -> bool:
    return bet > 0 and bet <= balance

# ==================== VIEWS & INTERACTIONS ====================
class MathView(View):
    def __init__(self, user_id: int, correct_answer: int):
        super().__init__(timeout=30.0)
        self.user_id = user_id
        self.correct_answer = correct_answer
        self.answered = False
        choices = [correct_answer]
        while len(choices) < 4:
            offset = random.randint(-10, 10)
            fake = correct_answer + offset
            if fake < 0:
                fake = correct_answer + random.randint(1, 10)
            if fake not in choices and fake >= 0:
                choices.append(fake)
        random.shuffle(choices)
        for i, ans in enumerate(choices):
            button = Button(label=str(ans), style=discord.ButtonStyle.primary, row=i//2)
            button.callback = self.create_callback(ans)
            self.add_item(button)

    def create_callback(self, answer: int):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("❌ Bạn không phải người dùng lệnh này!", ephemeral=True)
                return
            if self.answered:
                await interaction.response.send_message("⏰ Câu hỏi đã được trả lời hoặc hết thời gian.", ephemeral=True)
                return
            self.answered = True
            if answer == self.correct_answer:
                reward = 15
                await update_balance(self.user_id, reward, "add")
                embed = create_embed("✅ Chính xác!", f"Bạn nhận được **{reward}** coin.\nSố dư: **{await get_balance(self.user_id)}**", discord.Color.green())
            else:
                embed = create_embed("❌ Sai rồi!", f"Đáp án đúng là **{self.correct_answer}**.\nBạn không nhận được coin.", discord.Color.red())
            for item in self.children:
                item.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)
        return callback

    async def on_timeout(self):
        if not self.answered:
            for item in self.children:
                item.disabled = True
            if self.message:
                embed = create_embed("⏰ Hết giờ!", "Bạn đã không trả lời kịp.", discord.Color.orange())
                await self.message.edit(embed=embed, view=self)

class SpinView(View):
    def __init__(self, user_id: int):
        super().__init__(timeout=60.0)
        self.user_id = user_id
        self.spun = False

    @discord.ui.button(label="🎡 Quay", style=discord.ButtonStyle.success)
    async def spin_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Bạn không phải người dùng lệnh này!", ephemeral=True)
            return
        if self.spun:
            await interaction.response.send_message("⏰ Bạn đã quay rồi!", ephemeral=True)
            return
        self.spun = True
        rewards = [0, 10, 20, 50, 100]
        prize = random.choice(rewards)
        await update_balance(self.user_id, prize, "add")
        embed = create_embed("🎡 Vòng quay may mắn", f"Bạn nhận được **{prize}** coin!\nSố dư: **{await get_balance(self.user_id)}**", discord.Color.gold())
        button.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)

class BlackjackGame:
    # (Giữ nguyên từ code cũ)
    def __init__(self, bet: int):
        self.bet = bet
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False
        self.player_hand.append(self.draw_card())
        self.dealer_hand.append(self.draw_card())
        self.player_hand.append(self.draw_card())
        self.dealer_hand.append(self.draw_card())

    def create_deck(self):
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def draw_card(self):
        return self.deck.pop()

    def hand_value(self, hand):
        value = 0
        aces = 0
        for card in hand:
            rank = card[:-1]
            if rank in ['J', 'Q', 'K']:
                value += 10
            elif rank == 'A':
                aces += 1
                value += 11
            else:
                value += int(rank)
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        return value

    def player_total(self):
        return self.hand_value(self.player_hand)

    def dealer_total(self):
        return self.hand_value(self.dealer_hand)

    def dealer_visible_card(self):
        return self.dealer_hand[0]

    def player_hand_str(self):
        return ' '.join(self.player_hand)

    def dealer_hand_str(self, hide_second=True):
        if hide_second and not self.game_over:
            return f"{self.dealer_hand[0]} ??"
        return ' '.join(self.dealer_hand)

bj_games: Dict[int, BlackjackGame] = {}

# ==================== HORSE RACE VIEW ====================
class HorseRace:
    def __init__(self, ctx: commands.Context):
        self.ctx = ctx
        self.horses = [
            {"name": "Ngựa Ô", "emoji": "🐎", "speed": random.uniform(0.8, 1.2)},
            {"name": "Bạch Mã", "emoji": "🦄", "speed": random.uniform(0.8, 1.2)},
            {"name": "Hỏa Mã", "emoji": "🔥🐴", "speed": random.uniform(0.8, 1.2)},
            {"name": "Phong Mã", "emoji": "💨🐴", "speed": random.uniform(0.8, 1.2)},
            {"name": "Lôi Mã", "emoji": "⚡🐴", "speed": random.uniform(0.8, 1.2)},
        ]
        self.bets: Dict[int, Tuple[int, int]] = {}  # user_id -> (horse_index, amount)
        self.race_started = False
        self.race_finished = False
        self.winner_index = -1
        self.odds = [round(1 / (h["speed"] / 1.0), 2) for h in self.horses]  # tỷ lệ cược đơn giản

    def place_bet(self, user_id: int, horse_idx: int, amount: int):
        if user_id in self.bets:
            return False, "Bạn đã đặt cược rồi!"
        if horse_idx < 0 or horse_idx >= len(self.horses):
            return False, "Ngựa không tồn tại!"
        if amount <= 0:
            return False, "Số tiền cược không hợp lệ!"
        self.bets[user_id] = (horse_idx, amount)
        return True, f"Đặt {amount} coin vào {self.horses[horse_idx]['name']} {self.horses[horse_idx]['emoji']}"

    def get_race_status_embed(self) -> discord.Embed:
        embed = discord.Embed(title="🏇 ĐUA NGỰA - Đặt cược ngay!", color=discord.Color.gold())
        desc = "**Danh sách ngựa:**\n"
        for i, h in enumerate(self.horses):
            desc += f"{i+1}. {h['emoji']} **{h['name']}** - Tỷ lệ thắng: x{self.odds[i]}\n"
        desc += "\n⏳ **Thời gian đặt cược: 30 giây**\n"
        if self.bets:
            desc += "**Người đã đặt:**\n"
            for uid, (hidx, amt) in self.bets.items():
                user = self.ctx.guild.get_member(uid)
                name = user.display_name if user else f"User {uid}"
                desc += f"- {name}: {amt} coin vào {self.horses[hidx]['name']}\n"
        else:
            desc += "Chưa có ai đặt cược.\n"
        embed.description = desc
        embed.set_footer(text="Nhấn nút bên dưới để chọn ngựa.")
        return embed

class HorseRaceView(View):
    def __init__(self, race: HorseRace):
        super().__init__(timeout=30.0)
        self.race = race
        for i, h in enumerate(race.horses):
            button = Button(label=f"{i+1}. {h['name']}", emoji=h['emoji'], style=discord.ButtonStyle.primary, row=i//3)
            button.callback = self.create_callback(i)
            self.add_item(button)

    def create_callback(self, horse_idx: int):
        async def callback(interaction: discord.Interaction):
            if self.race.race_started:
                await interaction.response.send_message("⏳ Đua đã bắt đầu, không thể đặt cược nữa!", ephemeral=True)
                return
            # Mở modal nhập số tiền
            modal = BetAmountModal(self.race, horse_idx)
            await interaction.response.send_modal(modal)
        return callback

    async def on_timeout(self):
        if not self.race.race_started:
            await self.start_race()

    async def start_race(self):
        self.race.race_started = True
        # Vô hiệu hóa tất cả nút
        for item in self.children:
            item.disabled = True
        if hasattr(self, 'message'):
            await self.message.edit(view=self)

        # Thông báo bắt đầu đua
        embed = discord.Embed(title="🏁 ĐUA NGỰA BẮT ĐẦU!", description="Các chú ngựa đang vào vị trí...", color=discord.Color.green())
        await self.message.channel.send(embed=embed)

        # Mô phỏng đường đua (animation đơn giản)
        track_length = 20
        positions = [0] * len(self.race.horses)
        track_msg = await self.message.channel.send("Chuẩn bị...")
        await asyncio.sleep(1)

        while max(positions) < track_length:
            # Cập nhật vị trí
            for i, h in enumerate(self.race.horses):
                step = random.uniform(0.5, 1.5) * h["speed"]
                positions[i] = min(positions[i] + step, track_length)

            # Tạo thanh tiến độ
            lines = []
            for i, h in enumerate(self.race.horses):
                progress = int(positions[i])
                bar = "🟩" * progress + "⬜" * (track_length - progress)
                lines.append(f"{h['emoji']} **{h['name']}**: {bar} ({progress}/{track_length})")
            race_status = "\n".join(lines)
            embed = discord.Embed(title="🏇 Đang đua...", description=race_status, color=discord.Color.blue())
            await track_msg.edit(embed=embed)
            await asyncio.sleep(0.8)

        # Xác định người thắng
        max_pos = max(positions)
        winners = [i for i, p in enumerate(positions) if p == max_pos]
        self.race.winner_index = random.choice(winners)  # Nếu có nhiều, chọn ngẫu nhiên
        winner_horse = self.race.horses[self.race.winner_index]

        # Trả thưởng
        results = []
        for uid, (hidx, amt) in self.race.bets.items():
            if hidx == self.race.winner_index:
                win_amount = int(amt * self.race.odds[hidx])
                await update_balance(uid, win_amount, "add")
                results.append(f"<@{uid}> thắng **{win_amount}** coin!")
            else:
                await update_balance(uid, amt, "subtract")
                results.append(f"<@{uid}> thua **{amt}** coin.")

        # Embed kết quả
        embed = discord.Embed(title="🏆 KẾT QUẢ ĐUA NGỰA", color=discord.Color.gold())
        embed.add_field(name="Ngựa chiến thắng", value=f"{winner_horse['emoji']} **{winner_horse['name']}**", inline=False)
        embed.add_field(name="Kết quả cược", value="\n".join(results) if results else "Không có ai đặt cược.", inline=False)
        await self.message.channel.send(embed=embed)

class BetAmountModal(discord.ui.Modal, title="Nhập số tiền cược"):
    def __init__(self, race: HorseRace, horse_idx: int):
        super().__init__()
        self.race = race
        self.horse_idx = horse_idx
        self.amount = discord.ui.TextInput(
            label="Số tiền muốn cược",
            placeholder="Nhập số nguyên dương",
            required=True,
            min_length=1,
            max_length=10
        )
        self.add_item(self.amount)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            amount = int(self.amount.value)
        except ValueError:
            await interaction.response.send_message("❌ Số tiền không hợp lệ!", ephemeral=True)
            return
        balance = await get_balance(interaction.user.id)
        if amount > balance:
            await interaction.response.send_message(f"❌ Bạn chỉ có {balance} coin!", ephemeral=True)
            return
        if amount <= 0:
            await interaction.response.send_message("❌ Số tiền phải lớn hơn 0!", ephemeral=True)
            return

        success, msg = self.race.place_bet(interaction.user.id, self.horse_idx, amount)
        if success:
            # Trừ tiền tạm thời? Thực tế ta trừ khi kết thúc đua. Nhưng để an toàn, ta trừ luôn.
            await update_balance(interaction.user.id, amount, "subtract")
            embed = discord.Embed(title="✅ Đặt cược thành công!", description=msg, color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            # Cập nhật embed chính (nếu có)
            # Tìm view gốc để refresh? Không cần thiết lắm.
        else:
            await interaction.response.send_message(f"❌ {msg}", ephemeral=True)

# ==================== ECONOMY COG ====================
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='coin', aliases=['bal', 'balance'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coin(self, ctx):
        balance = await get_balance(ctx.author.id)
        embed = create_embed(f"💰 Ví của {ctx.author.display_name}", f"Số dư: **{balance}** 2zer011 coin", discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name='daily')
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        data = load_data()
        uid = str(ctx.author.id)
        now = datetime.utcnow().isoformat()
        last = data["daily"].get(uid)
        if last:
            last_time = datetime.fromisoformat(last)
            if datetime.utcnow() - last_time < timedelta(hours=24):
                remaining = timedelta(hours=24) - (datetime.utcnow() - last_time)
                hours, remainder = divmod(remaining.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                await ctx.send(f"⏳ Bạn đã nhận daily rồi. Hãy quay lại sau **{hours}h {minutes}m**.")
                return
        reward = random.randint(20, 50)
        await update_balance(ctx.author.id, reward, "add")
        data["daily"][uid] = now
        await save_data(data)
        embed = create_embed("🎁 Điểm danh hàng ngày", f"Bạn nhận được **{reward}** coin!\nSố dư: **{await get_balance(ctx.author.id)}**", discord.Color.gold())
        await ctx.send(embed=embed)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Bạn cần chờ {error.retry_after:.0f} giây nữa.")

    @commands.command(name='top')
    async def top(self, ctx):
        data = load_data()
        users = data["users"]
        sorted_users = sorted(users.items(), key=lambda x: x[1]["balance"], reverse=True)[:10]
        if not sorted_users:
            await ctx.send("Chưa có dữ liệu.")
            return
        description = ""
        for i, (uid, udata) in enumerate(sorted_users, 1):
            user = self.bot.get_user(int(uid))
            name = user.name if user else f"User {uid}"
            description += f"**{i}.** {name}: **{udata['balance']}** coin\n"
        embed = create_embed("🏆 Bảng xếp hạng giàu có", description, discord.Color.gold())
        await ctx.send(embed=embed)

    @commands.command(name='toan')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def toan(self, ctx):
        op = random.choice(['+', '-', '*'])
        if op == '+':
            a, b = random.randint(1, 50), random.randint(1, 50)
            correct = a + b
        elif op == '-':
            a, b = random.randint(20, 100), random.randint(1, 20)
            correct = a - b
        else:
            a, b = random.randint(1, 12), random.randint(1, 12)
            correct = a * b
        question = f"{a} {op} {b} = ?"
        embed = create_embed("🧮 Giải toán nhận coin", f"**{question}**\nChọn đáp án đúng:", discord.Color.blue())
        view = MathView(ctx.author.id, correct)
        msg = await ctx.send(embed=embed, view=view)
        view.message = msg

# ==================== GAMES COG (Tài Xỉu, Slot, Tung xu, Lucky, Dice, Blackjack) ====================
class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='taixiu')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def taixiu(self, ctx, choice: str, amount: int):
        choice = choice.lower()
        if choice not in ['tai', 'xiu']:
            await ctx.send("❌ Lựa chọn không hợp lệ. Dùng `tai` hoặc `xiu`.")
            return
        balance = await get_balance(ctx.author.id)
        if not validate_bet(ctx, amount, balance):
            await ctx.send("❌ Số tiền cược không hợp lệ hoặc vượt quá số dư.")
            return
        dice = [random.randint(1, 6) for _ in range(3)]
        total = sum(dice)
        result = "tai" if total >= 11 else "xiu"
        win = (choice == result)
        if win:
            await update_balance(ctx.author.id, amount, "add")
            new_bal = await get_balance(ctx.author.id)
            embed = create_embed("🎲 Tài Xỉu - Thắng!", f"Xúc xắc: {' '.join(map(str, dice))} (Tổng: {total})\nKết quả: **{result.upper()}**\nBạn thắng **{amount}** coin!\nSố dư: **{new_bal}**", discord.Color.green())
        else:
            await update_balance(ctx.author.id, amount, "subtract")
            new_bal = await get_balance(ctx.author.id)
            embed = create_embed("🎲 Tài Xỉu - Thua!", f"Xúc xắc: {' '.join(map(str, dice))} (Tổng: {total})\nKết quả: **{result.upper()}**\nBạn thua **{amount}** coin.\nSố dư: **{new_bal}**", discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name='slot')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slot(self, ctx, amount: int):
        balance = await get_balance(ctx.author.id)
        if not validate_bet(ctx, amount, balance):
            await ctx.send("❌ Số tiền cược không hợp lệ.")
            return
        symbols = ['🍒', '🍋', '💎', '7️⃣']
        result = [random.choice(symbols) for _ in range(3)]
        win_multiplier = 0
        if result[0] == result[1] == result[2]:
            if result[0] == '7️⃣':
                win_multiplier = 5
            elif result[0] == '💎':
                win_multiplier = 4
            else:
                win_multiplier = 3
        win_amount = amount * win_multiplier
        if win_multiplier > 0:
            await update_balance(ctx.author.id, win_amount, "add")
            new_bal = await get_balance(ctx.author.id)
            embed = create_embed("🎰 Slot Machine - JACKPOT!", f"{' | '.join(result)}\nBạn thắng **{win_amount}** coin! (x{win_multiplier})\nSố dư: **{new_bal}**", discord.Color.gold())
        else:
            await update_balance(ctx.author.id, amount, "subtract")
            new_bal = await get_balance(ctx.author.id)
            embed = create_embed("🎰 Slot Machine - Thua", f"{' | '.join(result)}\nBạn mất **{amount}** coin.\nSố dư: **{new_bal}**", discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name='quay')
    async def quay(self, ctx):
        embed = create_embed("🎡 Vòng quay may mắn", "Nhấn nút **Quay** bên dưới để nhận phần thưởng ngẫu nhiên!", discord.Color.gold())
        view = SpinView(ctx.author.id)
        await ctx.send(embed=embed, view=view)

    @commands.command(name='tungxu')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def tungxu(self, ctx, choice: str, amount: int):
        choice = choice.lower()
        if choice not in ['ngua', 'sap']:
            await ctx.send("❌ Chọn `ngua` hoặc `sap`.")
            return
        balance = await get_balance(ctx.author.id)
        if not validate_bet(ctx, amount, balance):
            await ctx.send("❌ Số tiền cược không hợp lệ.")
            return
        coin = random.choice(['ngua', 'sap'])
        win = (choice == coin)
        if win:
            await update_balance(ctx.author.id, amount, "add")
            new_bal = await get_balance(ctx.author.id)
            embed = create_embed("🪙 Tung xu - Thắng!", f"Kết quả: **{coin.upper()}**\nBạn thắng **{amount}** coin!\nSố dư: **{new_bal}**", discord.Color.green())
        else:
            await update_balance(ctx.author.id, amount, "subtract")
            new_bal = await get_balance(ctx.author.id)
            embed = create_embed("🪙 Tung xu - Thua", f"Kết quả: **{coin.upper()}**\nBạn thua **{amount}** coin.\nSố dư: **{new_bal}**", discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name='lucky')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lucky(self, ctx, number: int):
        if number < 1 or number > 10:
            await ctx.send("❌ Số phải từ 1 đến 10.")
            return
        secret = random.randint(1, 10)
        if number == secret:
            reward = 100
            await update_balance(ctx.author.id, reward, "add")
            new_bal = await get_balance(ctx.author.id)
            embed = create_embed("🎯 Trúng số!", f"Số bí mật: **{secret}**\nBạn nhận được **{reward}** coin!\nSố dư: **{new_bal}**", discord.Color.green())
        else:
            embed = create_embed("🎯 Chúc may mắn lần sau", f"Số bí mật: **{secret}**\nBạn đoán: **{number}**", discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(name='dice')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dice(self, ctx, amount: int):
        balance = await get_balance(ctx.author.id)
        if not validate_bet(ctx, amount, balance):
            await ctx.send("❌ Số tiền cược không hợp lệ.")
            return
        player_roll = random.randint(1, 6)
        bot_roll = random.randint(1, 6)
        if player_roll > bot_roll:
            await update_balance(ctx.author.id, amount, "add")
            new_bal = await get_balance(ctx.author.id)
            embed = create_embed("🎲 Dice Duel - Thắng!", f"Bạn: **{player_roll}** | Bot: **{bot_roll}**\nBạn thắng **{amount}** coin!\nSố dư: **{new_bal}**", discord.Color.green())
        elif player_roll < bot_roll:
            await update_balance(ctx.author.id, amount, "subtract")
            new_bal = await get_balance(ctx.author.id)
            embed = create_embed("🎲 Dice Duel - Thua", f"Bạn: **{player_roll}** | Bot: **{bot_roll}**\nBạn thua **{amount}** coin.\nSố dư: **{new_bal}**", discord.Color.red())
        else:
            embed = create_embed("🎲 Dice Duel - Hòa", f"Bạn: **{player_roll}** | Bot: **{bot_roll}**\nHòa, không mất tiền.", discord.Color.blue())
        await ctx.send(embed=embed)

    # Blackjack commands
    @commands.command(name='bj')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blackjack_start(self, ctx, amount: int):
        if ctx.author.id in bj_games:
            await ctx.send("❌ Bạn đang có ván Blackjack đang chơi. Dùng `!hit` hoặc `!stand`.")
            return
        balance = await get_balance(ctx.author.id)
        if not validate_bet(ctx, amount, balance):
            await ctx.send("❌ Số tiền cược không hợp lệ.")
            return
        game = BlackjackGame(amount)
        bj_games[ctx.author.id] = game
        embed = create_embed("🃏 Blackjack", f"**Bài của bạn:** {game.player_hand_str()} (Tổng: {game.player_total()})\n"
                           f"**Bài của nhà cái:** {game.dealer_hand_str()}\n"
                           f"Cược: **{amount}** coin\n"
                           f"Dùng `!hit` để rút thêm, `!stand` để dừng.", discord.Color.dark_red())
        await ctx.send(embed=embed)

    @commands.command(name='hit')
    async def blackjack_hit(self, ctx):
        game = bj_games.get(ctx.author.id)
        if not game:
            await ctx.send("❌ Bạn không có ván Blackjack nào.")
            return
        if game.game_over:
            await ctx.send("Ván đã kết thúc. Dùng `!bj` để chơi mới.")
            return
        game.player_hand.append(game.draw_card())
        player_total = game.player_total()
        if player_total > 21:
            await update_balance(ctx.author.id, game.bet, "subtract")
            new_bal = await get_balance(ctx.author.id)
            embed = create_embed("🃏 Blackjack - Quắc!", f"**Bài của bạn:** {game.player_hand_str()} (Tổng: {player_total})\nBạn bị quắc và thua **{game.bet}** coin.\nSố dư: **{new_bal}**", discord.Color.red())
            game.game_over = True
            del bj_games[ctx.author.id]
            await ctx.send(embed=embed)
            return
        embed = create_embed("🃏 Blackjack - Rút bài", f"**Bài của bạn:** {game.player_hand_str()} (Tổng: {player_total})\n"
                           f"**Bài của nhà cái:** {game.dealer_hand_str()}\n"
                           f"Gõ `!hit` để rút tiếp hoặc `!stand` để dừng.", discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command(name='stand')
    async def blackjack_stand(self, ctx):
        game = bj_games.get(ctx.author.id)
        if not game:
            await ctx.send("❌ Bạn không có ván Blackjack nào.")
            return
        if game.game_over:
            await ctx.send("Ván đã kết thúc.")
            return
        game.game_over = True
        while game.dealer_total() < 17:
            game.dealer_hand.append(game.draw_card())
        player_total = game.player_total()
        dealer_total = game.dealer_total()
        result_msg = ""
        win = False
        push = False
        if dealer_total > 21:
            result_msg = "Nhà cái quắc! Bạn thắng."
            win = True
        elif player_total > dealer_total:
            result_msg = "Bạn thắng!"
            win = True
        elif player_total < dealer_total:
            result_msg = "Nhà cái thắng."
            win = False
        else:
            result_msg = "Hòa."
            push = True

        if win:
            await update_balance(ctx.author.id, game.bet, "add")
            new_bal = await get_balance(ctx.author.id)
        elif not push:
            await update_balance(ctx.author.id, game.bet, "subtract")
            new_bal = await get_balance(ctx.author.id)
        else:
            new_bal = await get_balance(ctx.author.id)

        embed = create_embed("🃏 Blackjack - Kết quả", f"**Bài của bạn:** {game.player_hand_str()} (Tổng: {player_total})\n"
                           f"**Bài của nhà cái:** {game.dealer_hand_str(hide_second=False)} (Tổng: {dealer_total})\n"
                           f"**{result_msg}**\n"
                           f"{'Thắng' if win else 'Thua' if not push else 'Hòa'} **{game.bet}** coin.\n"
                           f"Số dư: **{new_bal}**", discord.Color.green() if win else discord.Color.red() if not push else discord.Color.blue())
        await ctx.send(embed=embed)
        del bj_games[ctx.author.id]

# ==================== JOB SYSTEM COG ====================
class JobSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='job', invoke_without_command=True)
    async def job(self, ctx):
        """Xem thông tin nghề nghiệp hiện tại."""
        data = load_data()
        uid = str(ctx.author.id)
        user = data["users"].get(uid, {})
        job_name = user.get("job")
        if not job_name:
            embed = create_embed("💼 Nghề nghiệp", "Bạn chưa có nghề! Dùng `!job list` để xem danh sách nghề và `!job join <tên nghề>` để chọn.", discord.Color.orange())
            await ctx.send(embed=embed)
            return
        job_info = JOBS.get(job_name, {})
        level = user.get("job_level", 1)
        exp = user.get("job_exp", 0)
        next_exp = level * 100
        salary = int(job_info["base_salary"] * (1 + 0.1 * (level - 1)))
        embed = create_embed(f"💼 Nghề nghiệp: {job_info['emoji']} {job_name.title()}", 
                             f"**Cấp độ:** {level}\n**Kinh nghiệm:** {exp}/{next_exp}\n**Lương mỗi lần làm:** {salary} coin\n\nDùng `!work` để làm việc (mỗi 24h).",
                             discord.Color.green())
        await ctx.send(embed=embed)

    @job.command(name='list')
    async def job_list(self, ctx):
        """Danh sách các nghề có thể chọn."""
        desc = ""
        for name, info in JOBS.items():
            desc += f"{info['emoji']} **{name.title()}** - Lương cơ bản: {info['base_salary']} coin\n"
        embed = create_embed("📋 Danh sách nghề nghiệp", desc + "\nDùng `!job join <tên nghề>` để chọn.", discord.Color.blue())
        await ctx.send(embed=embed)

    @job.command(name='join')
    async def job_join(self, ctx, *, job_name: str):
        """Tham gia một nghề."""
        job_name = job_name.lower()
        if job_name not in JOBS:
            await ctx.send("❌ Nghề không tồn tại! Xem danh sách: `!job list`")
            return
        data = load_data()
        uid = str(ctx.author.id)
        if uid not in data["users"]:
            data["users"][uid] = {"balance": 100, "last_daily": None}
        data["users"][uid]["job"] = job_name
        data["users"][uid]["job_level"] = 1
        data["users"][uid]["job_exp"] = 0
        data["users"][uid]["last_work"] = None
        await save_data(data)
        embed = create_embed("✅ Đã chọn nghề", f"Bạn hiện là **{job_name.title()}** {JOBS[job_name]['emoji']}. Dùng `!work` để làm việc.", discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name='work')
    @commands.cooldown(1, 86400, commands.BucketType.user)  # 24h cooldown, nhưng ta sẽ kiểm tra thêm trong hàm
    async def work(self, ctx):
        """Làm việc để nhận lương và kinh nghiệm."""
        data = load_data()
        uid = str(ctx.author.id)
        user = data["users"].get(uid)
        if not user or not user.get("job"):
            await ctx.send("❌ Bạn chưa có nghề! Dùng `!job join <tên nghề>` trước.")
            return

        # Kiểm tra thời gian làm việc lần cuối
        last_work_str = user.get("last_work")
        now = datetime.utcnow()
        if last_work_str:
            last_work = datetime.fromisoformat(last_work_str)
            if now - last_work < timedelta(hours=24):
                remaining = timedelta(hours=24) - (now - last_work)
                hours, remainder = divmod(remaining.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                await ctx.send(f"⏳ Bạn đã làm việc rồi. Hãy quay lại sau **{hours}h {minutes}m**.")
                return

        job_name = user["job"]
        job_info = JOBS[job_name]
        level = user.get("job_level", 1)
        exp = user.get("job_exp", 0)
        base_salary = job_info["base_salary"]
        salary = int(base_salary * (1 + 0.1 * (level - 1)))

        # Thêm kinh nghiệm
        exp_gain = random.randint(20, 40)
        exp += exp_gain
        level_up = False
        next_exp = level * 100
        while exp >= next_exp:
            exp -= next_exp
            level += 1
            next_exp = level * 100
            level_up = True

        user["job_level"] = level
        user["job_exp"] = exp
        user["last_work"] = now.isoformat()

        await update_balance(ctx.author.id, salary, "add")
        await save_data(data)

        new_bal = await get_balance(ctx.author.id)
        msg = f"Bạn đã làm việc và nhận **{salary}** coin!\n+{exp_gain} EXP nghề."
        if level_up:
            msg += f"\n🎉 **Chúc mừng! Bạn đã thăng cấp lên cấp {level}!**"
        embed = create_embed(f"💼 Làm việc - {job_name.title()} {job_info['emoji']}", msg + f"\nSố dư: **{new_bal}** coin", discord.Color.green())
        await ctx.send(embed=embed)

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            # Không làm gì vì ta đã tự kiểm tra
            pass

# ==================== ADDITIONAL EARNING COG (Mine, Fish, Hunt, Invest, Rob, HorseRace) ====================
class ExtraEarning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mine')
    @commands.cooldown(1, 300, commands.BucketType.user)  # 5 phút
    async def mine(self, ctx):
        """Đào coin."""
        found = random.choices(
            [0, 10, 20, 30, 50, 100],
            weights=[30, 30, 20, 10, 7, 3]
        )[0]
        if found > 0:
            await update_balance(ctx.author.id, found, "add")
            embed = create_embed("⛏️ Đào coin", f"Bạn đào được **{found}** coin!\nSố dư: **{await get_balance(ctx.author.id)}**", discord.Color.green())
        else:
            embed = create_embed("⛏️ Đào coin", "Bạn không tìm thấy gì cả. 😢", discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name='fish')
    @commands.cooldown(1, 240, commands.BucketType.user)  # 4 phút
    async def fish(self, ctx):
        """Câu cá."""
        catch = random.choices(
            ["cá nhỏ", "cá vừa", "cá lớn", "cá hiếm", "rác"],
            weights=[40, 30, 15, 5, 10]
        )[0]
        rewards = {"cá nhỏ": 15, "cá vừa": 30, "cá lớn": 60, "cá hiếm": 150, "rác": 0}
        coin = rewards[catch]
        if coin > 0:
            await update_balance(ctx.author.id, coin, "add")
            embed = create_embed("🎣 Câu cá", f"Bạn câu được **{catch}** và bán được **{coin}** coin!\nSố dư: **{await get_balance(ctx.author.id)}**", discord.Color.green())
        else:
            embed = create_embed("🎣 Câu cá", "Bạn chỉ câu được rác... 😞", discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name='hunt')
    @commands.cooldown(1, 360, commands.BucketType.user)  # 6 phút
    async def hunt(self, ctx):
        """Săn bắn."""
        prey = random.choices(
            ["thỏ", "hươu", "lợn rừng", "gấu", "hổ", "không có gì"],
            weights=[30, 25, 20, 15, 5, 5]
        )[0]
        rewards = {"thỏ": 20, "hươu": 40, "lợn rừng": 70, "gấu": 150, "hổ": 300, "không có gì": 0}
        coin = rewards[prey]
        if coin > 0:
            await update_balance(ctx.author.id, coin, "add")
            embed = create_embed("🏹 Săn bắn", f"Bạn săn được **{prey}** và bán được **{coin}** coin!\nSố dư: **{await get_balance(ctx.author.id)}**", discord.Color.green())
        else:
            embed = create_embed("🏹 Săn bắn", "Bạn không săn được gì. 😢", discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name='invest')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invest(self, ctx, amount: int):
        """Đầu tư sinh lời sau 2-4 giờ."""
        balance = await get_balance(ctx.author.id)
        if amount <= 0 or amount > balance:
            await ctx.send("❌ Số tiền không hợp lệ.")
            return
        if amount < 100:
            await ctx.send("❌ Số tiền đầu tư tối thiểu là 100 coin.")
            return
        data = load_data()
        uid = str(ctx.author.id)
        now = datetime.utcnow()
        # Kiểm tra đầu tư đang chờ
        if uid in data["investments"]:
            inv = data["investments"][uid]
            end_time = datetime.fromisoformat(inv["end_time"])
            if now < end_time:
                remaining = end_time - now
                await ctx.send(f"⏳ Bạn đã có một khoản đầu tư đang chờ, kết thúc sau {remaining.seconds//3600}h {(remaining.seconds%3600)//60}m.")
                return
            else:
                # Đã đến hạn, xử lý kết quả cũ trước khi tạo mới? Ta sẽ xử lý tự động khi claim hoặc ở đây có thể tự claim.
                # Tạm thời tự động claim khi đến hạn khi gọi invest mới.
                pass

        # Trừ tiền
        await update_balance(ctx.author.id, amount, "subtract")
        duration_hours = random.randint(2, 4)
        end_time = now + timedelta(hours=duration_hours)
        profit_rate = random.uniform(0.05, 0.25)  # 5% đến 25%
        data["investments"][uid] = {
            "amount": amount,
            "end_time": end_time.isoformat(),
            "profit_rate": profit_rate,
            "claimed": False
        }
        await save_data(data)
        embed = create_embed("📈 Đầu tư", f"Bạn đã đầu tư **{amount}** coin.\nThời gian: {duration_hours} giờ.\nLợi nhuận dự kiến: {int(profit_rate*100)}%.\nDùng `!claim` sau khi hết thời gian để nhận.", discord.Color.gold())
        await ctx.send(embed=embed)

    @commands.command(name='claim')
    async def claim(self, ctx):
        """Nhận tiền từ đầu tư đã đến hạn."""
        data = load_data()
        uid = str(ctx.author.id)
        inv = data["investments"].get(uid)
        if not inv:
            await ctx.send("❌ Bạn không có khoản đầu tư nào.")
            return
        now = datetime.utcnow()
        end_time = datetime.fromisoformat(inv["end_time"])
        if now < end_time:
            remaining = end_time - now
            await ctx.send(f"⏳ Chưa đến hạn! Còn {remaining.seconds//3600}h {(remaining.seconds%3600)//60}m.")
            return
        if inv.get("claimed", False):
            await ctx.send("❌ Bạn đã nhận khoản đầu tư này rồi.")
            return

        amount = inv["amount"]
        profit = int(amount * inv["profit_rate"])
        total = amount + profit
        await update_balance(ctx.author.id, total, "add")
        inv["claimed"] = True
        await save_data(data)
        embed = create_embed("💰 Nhận đầu tư", f"Bạn nhận được **{total}** coin (gốc {amount} + lãi {profit}).\nSố dư: **{await get_balance(ctx.author.id)}**", discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name='rob')
    @commands.cooldown(1, 3600, commands.BucketType.user)  # 1 giờ
    async def rob(self, ctx, target: discord.Member):
        """Cướp tiền người khác (rủi ro cao)."""
        if target.id == ctx.author.id:
            await ctx.send("❌ Bạn không thể tự cướp chính mình.")
            return
        if target.bot:
            await ctx.send("❌ Không thể cướp bot.")
            return
        target_bal = await get_balance(target.id)
        if target_bal < 50:
            await ctx.send("❌ Nạn nhân quá nghèo, không đáng để cướp.")
            return
        # Xác suất thành công 30%
        success = random.random() < 0.3
        if success:
            steal = random.randint(int(target_bal*0.1), int(target_bal*0.3))
            steal = min(steal, target_bal)  # không vượt quá số dư
            await update_balance(target.id, steal, "subtract")
            await update_balance(ctx.author.id, steal, "add")
            embed = create_embed("🦹 Cướp thành công!", f"Bạn đã cướp được **{steal}** coin từ {target.mention}.\nSố dư của bạn: **{await get_balance(ctx.author.id)}**", discord.Color.green())
        else:
            fine = random.randint(50, 200)
            await update_balance(ctx.author.id, fine, "subtract")
            embed = create_embed("🚨 Cướp thất bại!", f"Bạn bị bắt và bị phạt **{fine}** coin.\nSố dư còn: **{await get_balance(ctx.author.id)}**", discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(name='horserace', aliases=['duangua'])
    @commands.cooldown(1, 60, commands.BucketType.guild)  # tránh spam nhiều cuộc đua cùng lúc
    async def horse_race(self, ctx):
        """Tổ chức cuộc đua ngựa."""
        race = HorseRace(ctx)
        view = HorseRaceView(race)
        embed = race.get_race_status_embed()
        msg = await ctx.send(embed=embed, view=view)
        view.message = msg
        # Lưu race vào view để timeout gọi start
        # Timeout sẽ tự start race

# ==================== ADMIN COG ====================
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addcoin')
    async def addcoin(self, ctx, member: discord.Member, amount: int):
        if not is_admin(ctx):
            await ctx.send("❌ Bạn không có quyền sử dụng lệnh này.")
            return
        if amount <= 0:
            await ctx.send("❌ Số coin phải lớn hơn 0.")
            return
        new_bal = await update_balance(member.id, amount, "add")
        embed = create_embed("👑 Admin", f"Đã thêm **{amount}** coin cho {member.mention}.\nSố dư mới: **{new_bal}**", discord.Color.purple())
        await ctx.send(embed=embed)

    @commands.command(name='setcoin')
    async def setcoin(self, ctx, member: discord.Member, amount: int):
        if not is_admin(ctx):
            await ctx.send("❌ Bạn không có quyền.")
            return
        if amount < 0:
            await ctx.send("❌ Số coin không được âm.")
            return
        new_bal = await update_balance(member.id, amount, "set")
        embed = create_embed("👑 Admin", f"Đã đặt số dư của {member.mention} thành **{amount}** coin.", discord.Color.purple())
        await ctx.send(embed=embed)

    @commands.command(name='resetcoin')
    async def resetcoin(self, ctx, member: discord.Member):
        if not is_admin(ctx):
            await ctx.send("❌ Bạn không có quyền.")
            return
        await update_balance(member.id, 0, "set")
        embed = create_embed("👑 Admin", f"Đã reset số dư của {member.mention} về 0.", discord.Color.purple())
        await ctx.send(embed=embed)

# ==================== HELP COG ====================
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help_command(self, ctx):
        embed = discord.Embed(title="🤖 2zer011 Bot - Hướng dẫn toàn tập", color=discord.Color.blue())
        embed.add_field(name="💰 Kinh tế", value="`!coin`, `!daily`, `!top`", inline=False)
        embed.add_field(name="🧮 Kiếm coin", value="`!toan` - Giải toán", inline=False)
        embed.add_field(name="🎮 Mini Games", value="`!taixiu`, `!slot`, `!quay`, `!tungxu`, `!lucky`, `!dice`, `!bj`, `!hit`, `!stand`", inline=False)
        embed.add_field(name="💼 Nghề nghiệp", value="`!job`, `!job list`, `!job join <nghề>`, `!work`", inline=False)
        embed.add_field(name="🛠️ Hoạt động khác", value="`!mine`, `!fish`, `!hunt`, `!invest`, `!claim`, `!rob @user`", inline=False)
        embed.add_field(name="🏇 Đua ngựa", value="`!horserace` hoặc `!duangua`", inline=False)
        embed.add_field(name="👑 Admin (joker.real)", value="`!addcoin`, `!setcoin`, `!resetcoin`", inline=False)
        embed.set_footer(text="Tiền ảo 2zer011 coin • Bot by joker.real")
        await ctx.send(embed=embed)

# ==================== EVENTS ====================
@bot.event
async def on_ready():
    print(f'Bot {bot.user} đã sẵn sàng!')
    await bot.change_presence(activity=discord.Game(name="!help | 2zer011 coin"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # Random drop (1%)
    if random.random() < 0.01:
        reward = random.randint(5, 15)
        await update_balance(message.author.id, reward, "add")
        embed = create_embed("🎁 Quà tặng bất ngờ!", f"{message.author.mention} vừa nhận được **{reward}** coin khi chat!", discord.Color.purple())
        await message.channel.send(embed=embed, delete_after=10.0)
    await bot.process_commands(message)

# ==================== LOAD COGS ====================
async def main():
    await bot.add_cog(Economy(bot))
    await bot.add_cog(Games(bot))
    await bot.add_cog(JobSystem(bot))
    await bot.add_cog(ExtraEarning(bot))
    await bot.add_cog(Admin(bot))
    await bot.add_cog(Help(bot))
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())