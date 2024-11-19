"""THE OPEN SOURCE CODE FOR THE LEMON CURRENCY BOT."""

"""
LAST UPDATED: 19TH OF NOVEMBER 2024.
IF YOU WOULD LIKE TO SUGGEST ANY FEATURES, PLEASE USE THE OFFICIAL DISCORD SERVER.
IF YOU WOULD LIKE TO 'MAKE' A FEATURE, PLEASE MAKE A PULL REQUEST.
    ㄴ PLEASE REFER TO THE 'CONTRIBUTING' FILE BEFORE MAKING A PR.
IF YOU HAVE FOUND A CRUCIAL BUG THAT COULD RUIN THE (VIRTUAL) ECONOMY, PLEASE SHOOT ME A DM, OR EMAIL US.

ANY QUESTIONS? PLEASE DM, EMAIL US, OR USE THE OFFICIAL DISCORD SERVER.
"""


import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import json
import os
import random
from threading import Thread
from dotenv import load_dotenv
from discord.ui import Button, View
import platform

intents = discord.Intents.default()
intents.members = True # ENSURE THIS IS SET TO 'TRUE' TO GRANT THE BOT MEMBER INTENTS.
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
# THE ! PREFIX DOES NOT WORK. THE AI TOLD ME TO DO IT, SO..
def load_jobs():
    with open("jobs.json", "r") as f:
        return json.load(f)
# THE JOBS COMMAND IS ARCHIVED AS OF NOW.

def get_user_balance(user_id):
    return

def update_user_balance(user_id, amount):
    pass

def load_balances():
    if os.path.exists("balances.json"):
        try:
            with open("balances.json", "r") as f:
                return json.load(f)
            # LOADS THE BALANCE.JSON FILE, IF IT DOESN'T EXIST, OR ERROR, IT MAKES A NEW ONE, OR PRINTS AN ERROR OUTPUT.
        except json.JSONDecodeError:
            print("Error decoding JSON from balances.json")
            return {}
    return {}

balances = load_balances() or {}
# LOAD_BALANCES() LOADS THE BALANCE FROM THE BALANCES.JSON FILE.

def save_balances():
    with open("balances.json", "w") as f:
        json.dump(balances, f)
# SAVE_BALANCES() SAVES THE CURRENT BALANCE TO THE BALANCES.JSON FILE.
# WITHOUT THIS, THE PROGRAM WILL NOT SAVE YOUR BALANCE TO THE JSON FILE.

def get_timestamp(interaction, command_name):
    return f"\n{command_name} executed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
# GETS TIMESTAMP OF THE USER.

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Running on: {platform.system()} {platform.release()} ({platform.machine()})")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="v0.0.6")) # SETS THE STATUS MESSAGE FOR THE BOT.
    await bot.tree.sync()
# PRINTS THE LOGIN MESSAGE TO THE CONSOLE BEFORE ACTIVATING THE BOT.

for user_id in balances.keys():
    if 'bank' not in balances[user_id]:
        balances[user_id]['bank'] = 0
# THIS LOADS THE USER'S BALANCE FROM THE BALANCES.JSON FILE. IF USER DOESN'T EXIST IN THE FILE, RETURNS TO 0 LEMONS.

def create_jobs_file():
    jobs = {
        "Lemonade Stand Part-time Worker": {
            "price": 500,
            "role": "Lemonade Stand Part-time Worker Role",
            "lemons_per_hour": 10
        },
        "Lemon Picker": {
            "price": 700,
            "role": "Lemon Picker Role",
            "lemons_per_hour": 20
        },
        "Scammer": {
            "price": 6969,
            "role": "Scammer Role",
            "lemons_per_hour": 100
        },
        "Lemon Planter": {
            "price": 200,
            "role": "Lemon Planter Role",
            "lemons_per_hour": 2
        }
    }

    with open("jobs.json", "w") as f:
        json.dump(jobs, f, indent=4)

create_jobs_file()
# THIS WILL CREATE A JOBS.JSON FILE, EVEN THOUGH THIS WILL NOT BE USED ANYWHERE.
# AGAIN, THIS COMMAND IS ARCHIVED AS OF NOW, AND WILL BE UPDATED LATER ON.

@bot.tree.command(name="balance", description="Check your or another user's balance.")
async def balance(interaction: discord.Interaction, user: discord.User = None):
    if user is None:
        user = interaction.user
    user_id = str(user.id)
    if user_id not in balances:
        balances[user_id] = {"balance": 0, "last_claimed": None, "consecutive_days": 0, "bank": 0}
        # THIS MAKES THE USER INPUT OPTIONAL
        # IF YOU WANT TO SEE OTHER USER'S BALANCE, THE SECOND INPUT IS NECESSARY.
    balance = balances[user_id]["balance"]
    bank_balance = balances[user_id]["bank"]
    vitamins_available = balance // 10000
        # IF YOU ARE WONDERING WHAT THIS IS, THIS IS ONLY FOR MY IRL FRIENDS.
    embed = discord.Embed(color=0xf2ed58)
    embed.title = f"{user.name}'s Balance"
    embed.description = f"{interaction.user.mention}\n🍋 Wallet: {balance}\n🏦 Bank: {bank_balance}\n\nAvailable Vitamins: {vitamins_available}"
        # THIS DISPLAYS THE USER'S WALLET BALANCE, AND THEIR BANK BALANCE, AFTER LOADING IT FROM THE BALANCES.JSON FILE.
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    embed.set_footer(text=f"\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | balance")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="beg", description="Beg for lemons.")
async def beg(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    randomlemon = random.randint(1, 15)
    # DECLARED 'RANDOMLEMON' AS A VARIABLE HOLDING THE RANDOM OUTPUT OF THE /BEG LEMON COMMAND.
    if user_id not in balances:
        balances[user_id] = {"balance": 0, "last_claimed": None, "consecutive_days": 0, "bank": 0}
    if random.randint(1, 3) == 1:
        # THERE IS A 33.33% CHANCE THAT YOU WILL SUCCEED A BEG.
        # CHANGE THE DENOMINATOR (3) TO EDIT PROBABILITIES.
        balances[user_id]["balance"] += randomlemon
        save_balances()
        embed = discord.Embed(color=0xf2ed58)
        embed.title = "You Got Lemons!"
        embed.description = f"{interaction.user.mention}, you received {randomlemon} 🍋 lemons!"
    else:
        embed = discord.Embed(color=0xf25858)
        embed.title = "No Lemons!"
        embed.description = f"Person: No, {interaction.user.mention}. You'll just use it to buy Genshin characters."
            # YOU CAN EDIT THE 'NO U STINKY' TO CHANGE THE BEG FAIL MESSAGE.
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | beg")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="harvest", description="Harvest your lemons.")
    # USED TO BE CALLED /DAILY.
async def harvest(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    current_time = datetime.now()
    if user_id not in balances:
        balances[user_id] = {"balance": 0, "last_claimed": None, "consecutive_days": 0, "bank": 0}
    last_claimed = balances[user_id]["last_claimed"]
    consecutive_days = balances[user_id]["consecutive_days"]
    if last_claimed is None or (current_time - datetime.fromisoformat(last_claimed)) >= timedelta(days=1):
        if last_claimed is None:
            earned_lemons = 10
            consecutive_days = 1
                # RETURNS THE CONSECUTIVE_DAYS VARIABLE TO 1, IF STREAK LOST, OR DOESN'T EXIST.
        else:
            if (current_time - datetime.fromisoformat(last_claimed)) < timedelta(days=1):
                consecutive_days = 1
            else:
                consecutive_days += 1
            earned_lemons = 10 + (consecutive_days - 1) * 2
                # YOU WILL GET +2 LEMONS PER DAY, WHEN YOU USE /HARVEST.
        balances[user_id]["balance"] += earned_lemons
        balances[user_id]["last_claimed"] = current_time.isoformat()
        balances[user_id]["consecutive_days"] = consecutive_days
        save_balances()
        embed = discord.Embed(color=0xf2ed58)
        embed.title = "Harvest successful!"
        embed.description = f"{interaction.user.mention}, you have received {earned_lemons} 🍋 lemons! Total balance: {balances[user_id]['balance']}. Your current streak: {consecutive_days} day(s).{get_timestamp(interaction, 'harvest')}"
    else:
        embed = discord.Embed(color=0xf25858)
        embed.title = "Already Harvested"
            # SAYS "NUH UH" WHEN IT HASN'T BEEN 24 HOURS. SINCE THE LAST TIME HARVESTED
        time_left = timedelta(days=1) - (current_time - datetime.fromisoformat(last_claimed))
        embed.description = f"You can harvest again in {time_left.days} day(s) and {time_left.seconds // 3600} hour(s). Your current streak: {consecutive_days} day(s).{get_timestamp(interaction, 'harvest')}"
            # YOU CAN MODIFY THE 3600 ABOVE, TO CHANGE THE DAILY COLLECT TIME.
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | harvest")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="modify", description="Modify a user's balance by adding or subtracting lemons.")
async def modify(interaction: discord.Interaction, user: discord.User, amount: int):
    try:
        banker_role_id = 1302118831342354473
            # REQUIRES THE ROLE ID OF THE BANKER ROLE IN THE OFFICIAL LEMON SERVER.
        if not any(role.id == banker_role_id for role in interaction.user.roles):
            await interaction.response.send_message("Ni meiyou permissions.", ephemeral=True)
            return
                # YOU CANNOT RUN THIS COMMAND IF YOU DO NOT HAVE THE RIGHT PERMISSIONS.

        user_id = str(user.id)
        if user_id not in balances:
            balances[user_id] = {"balance": 0, "last_claimed": None, "consecutive_days": 0, "bank": 0}
        new_balance = balances[user_id]["balance"] + amount
        balances[user_id]["balance"] = max(new_balance, 0)
        save_balances()
        embed = discord.Embed(color=0xf2ed58)
        embed.title = "Balance Modified!"
        embed.description = f"{amount} 🍋 lemons have been {'added to' if amount > 0 else 'subtracted from'} {user.mention}'s balance.{get_timestamp(interaction, 'modify')}"
            # "ADDED" IF IT IS A POSITIVE INTEGER, "SUBTRACTED" IF IT IS A NEGATIVE INTEGER.
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | modify")
        await interaction.response.send_message(embed=embed)
    except discord.errors.NotFound as e:
        print(f"Error: {e}")
        await interaction.response.send_message("There was an issue processing your request. Please try again later.", ephemeral=True)

@bot.tree.command(name="bet", description="Bet lemons on the spin of the wheel!")
async def bet(interaction: discord.Interaction, amount: int):
    user_id = str(interaction.user.id)
    if user_id not in balances:
        balances[user_id] = {"balance": 0, "last_claimed": None, "consecutive_days": 0, "bank": 0}
    current_balance = balances[user_id]["balance"]
    if amount <= 0:
        await interaction.response.send_message("You need to bet a positive amount of lemons.", ephemeral=True)
            # BLOCKS NEGATIVE VALUE INPUTS.
        return
    elif amount > current_balance:
        await interaction.response.send_message("You don't have enough lemons to place that bet.", ephemeral=True)
        return
            # MAKES IT SO THAT YOU CANNOT BET MORE THAN YOU HAVEI IN YOUR BALANCE.

    outcomes = [
                (0, "You lost all the lemons you bet."),
        (round(1.3 * amount), "You gained 130% of your bet!"),
        (round(2.0 * amount), "You gained 200% of your bet!"),
        (round(100 * amount), "Jackpot! You gained 1000% of your bet!"),
        (round(1000 * amount), "MEGA JACKPOT! You gained 99000% of your bet!")
    ]
    probabilities = [50, 30, 19, 0.9, 0.1]

    # 50% CHANCE YOU LOSE EVERYTHING,
    # 30% CHANCE YOU GAIN 130% OF YOUR BET
    # 19% CHANCE YOU GAIN 200% OF YOUR BET (WHICH IS DOUBLE)
    # 0.9% CHANCE YOU GAIN 1000% OF YOUR BET
    # 0.1% CHANCE YOU GAIN 99000% OF YOUR BET

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

@bot.tree.command(name="leaderboard", description="View the top balances.")
async def leaderboard(interaction: discord.Interaction):
    sorted_users = sorted(balances.items(), key=lambda x: x[1]["balance"], reverse=True)[:10]
    embed = discord.Embed(title="Leaderboard", color=0xf2ed58)

    for idx, (user_id, data) in enumerate(sorted_users):
        # SORTS THE USERS TOP TO BOTTOM IN TERMS OF BALANCE
        try:
            member = await interaction.guild.fetch_member(int(user_id))
            embed.add_field(name=f"{idx + 1}. {member.name} (ID: {member.id})", value=f"🍋 {data['balance']}", inline=False)
        except discord.NotFound:
            embed.add_field(name=f"{idx + 1}. Unknown User", value=f"🍋 {data['balance']}", inline=False)

    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | ledaerboard")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="deposit", description="Deposit lemons into the bank.")
async def deposit(interaction: discord.Interaction, amount: str):
    user_id = str(interaction.user.id)
    if user_id not in balances:
        balances[user_id] = {"balance": 0, "last_claimed": None, "consecutive_days": 0, "bank": 0}

    if amount.lower() == "all":
        amount = balances[user_id]["balance"]
    else:
        amount = int(amount)

    if amount <= 0:
        await interaction.response.send_message("You need to deposit a positive amount of lemons.", ephemeral=True)
        return
    elif amount > balances[user_id]["balance"]:
        await interaction.response.send_message("You don't have enough lemons to deposit.", ephemeral=True)
        return

    balances[user_id]["balance"] -= amount
    balances[user_id]["bank"] += amount
    save_balances()
    embed = discord.Embed(color=0xf2ed58)
    embed.title = "Deposit Successful"
    embed.description = f"{amount} 🍋 lemons have been deposited into your bank.\nNew Balance: 🍋 {balances[user_id]['balance']}\nBank Balance: 🍋 {balances[user_id]['bank']}"
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | deposit")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="withdraw", description="Withdraw lemons from the bank.")
async def withdraw(interaction: discord.Interaction, amount: str):
    user_id = str(interaction.user.id)
    if user_id not in balances:
        balances[user_id] = {"balance": 0, "last_claimed": None, "consecutive_days": 0, "bank": 0}

    if amount.lower() == "all":
        amount = balances[user_id]["bank"]
    else:
        amount = int(amount)

    if amount <= 0:
        await interaction.response.send_message("You need to withdraw a positive amount of lemons.", ephemeral=True)
        return
    elif amount > balances[user_id]["bank"]:
        await interaction.response.send_message("You don't have enough lemons in the bank to withdraw.", ephemeral=True)
        return

    balances[user_id]["bank"] -= amount
    balances[user_id]["balance"] += amount
    save_balances()
    embed = discord.Embed(color=0xf2ed58)
    embed.title = "Withdrawal Successful"
    embed.description = f"{amount} 🍋 lemons have been withdrawn from your bank.\nNew Balance: 🍋 {balances[user_id]['balance']}\nBank Balance: 🍋 {balances[user_id]['bank']}"
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | withdraw")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="pickpocket", description="Pickpocket lemons from another user.")
@commands.cooldown(1, 300, commands.BucketType.user)
async def pickpocket(interaction: discord.Interaction, user: discord.User):
    if user.id == interaction.user.id:
        await interaction.response.send_message("You cannot pickpocket yourself!", ephemeral=True)
        return
            # MAKES IT SO THAT YOU CANNOT STEAL FROM YOURSELF, AND DUPLICATE LEMONS.

    user_id = str(user.id)

    if user_id not in balances:
        await interaction.response.send_message(f"{user.name} has no lemons to steal.", ephemeral=True)
        return
            # CANNOT STEAL IF SOMEONE HAS NO LEMONS IN THEIR WALLET (BALANCE).

    user_balance = balances[user_id]["balance"]

    if user_balance <= 0:
        await interaction.response.send_message(f"{user.name} has no lemons to steal.", ephemeral=True)
        return
        # CANNOT STEAL IF SOMEONE HAS NO LEMONS IN THEIR WALLET (BALANCE).

    success = random.randint(1, 10) == 1
        # 10% CHANCE SUCCEEDING A PICKPOCKET. CAN EDIT DENOMINATOR & NUMERATOR TO EDIT THE PROBABILITIES

    if success:
        stolen_amount = random.randint(int(0.7 * user_balance), user_balance)
            # STEALS 70% ~ 100% OF SOMEONE'S LEMONS.
        balances[user_id]["balance"] -= stolen_amount
        balances[str(interaction.user.id)]["balance"] += stolen_amount
        save_balances()
        embed = discord.Embed(color=0xf2ed58)
        embed.title = "Pickpocket Success!"
        embed.description = f"{interaction.user.mention} stole {stolen_amount} 🍋 lemons from {user.mention}!"
    else:
        if balances[str(interaction.user.id)]["balance"] <= 0:
            await interaction.response.send_message("You have no lemons to lose!", ephemeral=True)
            return
        lost_amount = random.randint(int(0.5 * balances[str(interaction.user.id)]["balance"]), int(0.8 * balances[str(interaction.user.id)]["balance"]))
            # IF FAILED TO PICKPOCKET, THE USER WILL LOSE 50%~80% OF THEIR OWN LEMONS.
        balances[str(interaction.user.id)]["balance"] -= lost_amount
        save_balances()
        embed = discord.Embed(color=0xf25858)
        embed.title = "Pickpocket Failed!"
        embed.description = f"{interaction.user.mention} was caught and lost {lost_amount} 🍋 lemons!"

    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | pickpocket")
    await interaction.response.send_message(embed=embed)

@pickpocket.error
async def pickpocket_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(color=0xf25858)
        embed.title = "Cooldown Active"
        embed.description = f"You need to wait {round(error.retry_after)} seconds before using this command again."
        await interaction.response.send_message(embed=embed, ephemeral=True)
            # THIS REQUIRES A FIX; NO COOLDOWNS ARE IN PLACE.

@bot.tree.command(name="donate", description="Donate lemons to another user.")
async def donate(interaction: discord.Interaction, user: discord.User, amount: int):
    donor_id = str(interaction.user.id)
    recipient_id = str(user.id)

    if donor_id not in balances:
        balances[donor_id] = {"balance": 0, "last_claimed": None, "consecutive_days": 0, "bank": 0}

    if recipient_id not in balances:
        balances[recipient_id] = {"balance": 0, "last_claimed": None, "consecutive_days": 0, "bank": 0}

    donor_balance = balances[donor_id]["balance"]

    if amount <= 0:
        await interaction.response.send_message("You need to donate a positive amount of lemons.", ephemeral=True)
        return
    elif amount > donor_balance:
        await interaction.response.send_message("You don't have enough lemons to donate.", ephemeral=True)
        return

    balances[donor_id]["balance"] -= amount
    balances[recipient_id]["balance"] += amount
    save_balances()

    embed = discord.Embed(color=0xf2ed58)
    embed.title = "Donation Successful!"
    embed.description = f"{interaction.user.mention} donated {amount} 🍋 lemons to {user.mention}!"
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
    embed.set_footer(text=f"\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | donate")
    await interaction.response.send_message(embed=embed)

##########################################################

# embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
# embed.set_footer(text=f"\n{interaction.user.name} | {datetime.now().strftime('%H:%M:%S')} | COMMAND NAME")

bot.run("TOKEN")
# CHANGE TOKEN BEFORE RUNNING/UPLOADING CODE TO REPOSITORY.
