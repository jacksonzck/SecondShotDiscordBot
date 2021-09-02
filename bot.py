import discord
import os
from dotenv import load_dotenv
import sqlite3
import datetime


con = sqlite3.connect('database.db')

load_dotenv()

client = discord.Client()
con.execute('''CREATE TABLE IF NOT EXISTS currency
                (name text, id bigint, amount bigint, tmsp timestamp)''')
con.execute('''CREATE TABLE IF NOT EXISTS transactions
                (orgin text, orginId bigInt, recipient text, recipientId bigint, amount bigint, tmsp timestamp)''')


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    cur = con.cursor()
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        return
    if message.content.startswith('$ping'):
        print()
        return
    if message.content.startswith('$createAccount'):
        cur.execute(f'''SELECT * FROM currency WHERE id = {message.author.id}''')
        row = cur.fetchone()
        if row is None:
            cur.execute("INSERT INTO currency VALUES (?, ?, ?, ?)", (message.author.name, message.author.id, 250, message.created_at))
            con.commit()
            await message.reply("Account Created.")
        else:
            await message.reply("You already have an account.")
        return
    if message.content.startswith('$bal'):
        cur.execute(f"SELECT * FROM currency WHERE id = {message.author.id}")
        row = cur.fetchone()
        if row is not None:
            await message.reply(f"Your balance is ${row[2]}")
        else:
            await message.reply(f"No balance found. Please create an account first.")
        return
    if message.content.startswith('$tra'):
        _, amount, recipient = message.content.split



client.run(os.environ['DISCORD_TOKEN'])