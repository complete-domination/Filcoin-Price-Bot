import discord
import aiohttp
import asyncio
import os

# Use environment variables for security
TOKEN = os.environ['TOKEN']
GUILD_ID = int(os.environ['GUILD_ID'])

# CoinGecko ID for Filecoin
COIN = "filecoin"

# Discord intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)

# Function to get price and 24h change
async def get_price_data():
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={COIN}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            price = data[0]['current_price']
            change_24h = data[0]['price_change_percentage_24h']
            return price, change_24h

@client.event
async def on_ready():
    guild = client.get_guild(GUILD_ID)
    bot_member = guild.get_member(client.user.id)
    print(f"Logged in as {client.user}")

    while True:
        price, change_24h = await get_price_data()

        # Choose emoji based on 24
