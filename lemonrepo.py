import discord
from discord.ext import commands
from datetime import datetime, timedelta
import json
import os
import random

# Load JSON Balance File
def load_balances():
    if os.path.exists("balances.json"):
        with open("balances.json", "r") as f:
            return json.load(f)
    return {}

def save_balances():
    with open("balances.json", "w") as f:
        json.dump(balances, f)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
balances = load_balances()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="v.0.0.1"))

    await bot.tree.sync()

def get_timestamp(interaction, command_name):
    return f"\n\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | {command_name}"

@bot.tree.command(name="balance", description="Check your or another user's balance.")
async def balance(interaction: discord.Interaction, user: discord.User = None):
    if user is None:
        user = interaction.user

    user_id = str(user.id)
    if user_id not in balances:
        balances[user_id] = {"balance": 0, "last_claimed": None, "consecutive_days": 0}

    balance = balances[user_id]["balance"]
    vitamins_available = balance // 10000  # Available Vitamins
    embed = discord.Embed(color=0xf2ed58)
    embed.title = f"{user.name}'s Balance"
    embed.description = f"@{interaction.user.mention}\n🍋: {balance}\n\nAvailable Vitamins: {vitamins_available}"

    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | balance")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="beg", description="Beg for lemons.")
async def beg(interaction: discord.Interaction):
    user_id = str(interaction.user.id)

    if user_id not in balances:
        balances[user_id] = {"balance": 0, "last_claimed": None, "consecutive_days": 0}

    if random.randint(1, 5) == 1:
        balances[user_id]["balance"] += 1
        save_balances()
        embed = discord.Embed(color=0xf2ed58)
        embed.title = "You Got Lemons!"
        embed.description = f"{interaction.user.mention}, you received 1 🍋 lemon!"
    else:
        embed = discord.Embed(color=0xf25858)
        embed.title = "No Lemons!"
        embed.description = f"{interaction.user.mention}, no u stinky."

    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | beg")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="daily", description="Claim your daily lemons.")
async def daily(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    current_time = datetime.now()

    if user_id not in balances:
        balances[user_id] = {"balance": 0, "last_claimed": None, "consecutive_days": 0}

    last_claimed = balances[user_id]["last_claimed"]
    consecutive_days = balances[user_id]["consecutive_days"]

    if last_claimed is None or (current_time - datetime.fromisoformat(last_claimed)) >= timedelta(days=1):
        if last_claimed is None:
            earned_lemons = 10
            consecutive_days = 1
        else:
            if (current_time - datetime.fromisoformat(last_claimed)) < timedelta(days=1):
                consecutive_days = 1
            else:
                consecutive_days += 1

            earned_lemons = 10 + (consecutive_days - 1) * 2

        balances[user_id]["balance"] += earned_lemons
        balances[user_id]["last_claimed"] = current_time.isoformat()
        balances[user_id]["consecutive_days"] = consecutive_days
        save_balances()

        embed = discord.Embed(color=0xf2ed58)
        embed.title = "Daily Reward Claimed!"
        embed.description = f"{interaction.user.mention}, you have received {earned_lemons} 🍋 lemons! Total balance: {balances[user_id]['balance']}. Your current streak: {consecutive_days} day(s).{get_timestamp(interaction, 'daily')}"
    else:
        embed = discord.Embed(color=0xf25858)
        embed.title = "Daily Reward Already Claimed"
        time_left = timedelta(days=1) - (current_time - datetime.fromisoformat(last_claimed))
        embed.description = f"You can claim your daily reward again in {time_left.days} day(s) and {time_left.seconds // 3600} hour(s). Your current streak: {consecutive_days} day(s).{get_timestamp(interaction, 'daily')}"

    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="modify", description="Modify a user's balance by adding or subtracting lemons.")
async def modify(interaction: discord.Interaction, user: discord.User, amount: int):
    if discord.utils.get(interaction.user.roles, name="Bank") is None:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    user_id = str(user.id)
    if user_id not in balances:
        balances[user_id] = {"balance": 0, "last_claimed": None, "consecutive_days": 0}

    new_balance = balances[user_id]["balance"] + amount
    balances[user_id]["balance"] = max(new_balance, 0)
    save_balances()

    embed = discord.Embed(color=0xf2ed58)
    embed.title = "Balance Modified!"
    embed.description = f"{amount} 🍋 lemons have been {'added to' if amount > 0 else 'subtracted from'} {user.mention}'s balance.{get_timestamp(interaction, 'modify')}"
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="bet", description="Bet lemons on the spin of the wheel!")
async def bet(interaction: discord.Interaction, amount: int):
    user_id = str(interaction.user.id)

    if user_id not in balances:
        balances[user_id] = {"balance": 0, "last_claimed": None, "consecutive_days": 0}

    current_balance = balances[user_id]["balance"]

    if amount <= 0:
        await interaction.response.send_message("You need to bet a positive amount of lemons.", ephemeral=True)
        return
    elif amount > current_balance:
        await interaction.response.send_message("You don't have enough lemons to place that bet.", ephemeral=True)
        return

# BETTING OUTCOMES:
    outcomes = [
        (0, "You lost all the lemons you bet."),                                    # Lose all
        (round(1.25 * amount), "You gained 125% of your betting!"),                 # Gain 125%
        (round(1.3 * amount), "You gained 130% of your betting!"),                  # Gain 130%
        (round(100 * amount), "Jackpot! You gained 1000% of your betting!"),        # Gain 1000%
        (round(1000 * amount), "MEGA JACKPOT! You gained 99000% of your betting!")  # Gain 99000%
    ]

    probabilities = [50, 25, 24, 0.9, 0.1]

    spin_result = random.choices(outcomes, weights=probabilities, k=1)[0]
    lemons_won = spin_result[0]
    message = spin_result[1]

    new_balance = balances[user_id]["balance"] + lemons_won - amount
    balances[user_id]["balance"] = max(new_balance, 0)
    save_balances()

    embed = discord.Embed(color=0xf2ed58)
    embed.title = "Spin the Wheel Result"
    embed.description = f"{interaction.user.mention}, {message}\nYour new balance: 🍋 {balances[user_id]['balance']}"

    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | bet")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="leaderboard", description="Show the leaderboard of lemon balances.")
async def leaderboard(interaction: discord.Interaction):
    sorted_balances = sorted(balances.items(), key=lambda item: item[1]['balance'], reverse=True)

    embed = discord.Embed(title="Leaderboard", color=0xf2ed58)

    embed.description = "Top Richest People:\n"
    for i, (user_id, user_data) in enumerate(sorted_balances[:10]):
        user = await bot.fetch_user(user_id)
        embed.description += f"{i + 1}. {user.name} - 🍋 {user_data['balance']}\n"

    if not sorted_balances:
        embed.description = "No users found."

    embed.set_footer(text=f"{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | leaderboard")
    await interaction.response.send_message(embed=embed)

###########################################

# bot.run('TOKEN GOES HERE')