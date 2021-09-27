import discord
import sqlite3
import random
import string

class player:

    def __init__(self, username, code, status):
        self.username= username
        self.code = code
        self.status = status

conn = sqlite3.connect('player.db')

c = conn.cursor()

TOKEN = "ODg5MjIzNTU2OTcyNTc2Nzc4.YUeH-A.JKTAzH9VOOD2RQDYrk56GtDdQJM"

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Hello There')

@client.event
async def on_message(message):
    username = str(message.author)
    user_message = str(message.content)

    if message.author == client.user:
        return

    if "!code" == user_message[0:5]:
        user_code = user_message[6:11]
        print(user_code)
        c.execute("SELECT * FROM players WHERE code=?", (user_code,))
        users_codes = c.fetchall()
        if len(users_codes) == 0:
            print("no user with code {}".format(user_code))
            await message.channel.send("No user with that code")
            return
        print(users_codes)
        user_name = users_codes[0][0]
        print(user_name)
        c.execute("UPDATE players SET status = 'zombie' WHERE username = ?",(user_name,))
        conn.commit()
        print("player updated")
        g = client.get_guild(889205819156074558)
        for ur in g.members:
            print()
            print(str(ur))
            print(user_name)
            if str(ur) == user_name:
                zrole = discord.utils.get(g.roles, name="Zombie")
                await ur.add_roles(zrole)
                hrole = discord.utils.get(g.roles, name="Human")
                await ur.remove_roles(hrole)
                await message.channel.send("zombified {}".format(user_name))
                return
        await message.channel.send("{} no longer on the server".format(user_name))
        return
    
    elif "!create" == user_message[0:7]:
        print("creating user...")
        c.execute("SELECT * FROM players WHERE username=?", (username,))
        for u in c.fetchall():
            if u[0] == username:
                print("{} is already a user")
                await message.channel.send("already a user")
                await message.author.send("Remeber your code is ")
                await message.author.send(u[1])
                return

        code = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        c.execute("SELECT * FROM players WHERE code=?", (code,))
        codes = []
        for u in c.fetchall():
                codes.append(u[1])
        print(codes)
        while(True):
            if code not in codes:
                break
            code = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
                
        c.execute("INSERT INTO players VALUES (?, ?, 'human')",(username, code))
        conn.commit()
        print("human {}".format(username))
        await message.channel.send("User created")
        await message.author.send("Your code is ")
        await message.author.send(code)

        g = client.get_guild(889205819156074558)
        for ur in g.members:
            if str(ur) == str(username):
                hrole = discord.utils.get(g.roles, name="Human")
                await ur.add_roles(hrole)
        return
        
    elif "!get" == user_message[0:4] and username in ["Byverone#5767","zeevoid#9498","valariarian#2462"]:
        user_name = user_message.split(' ')[1]

        c.execute("SELECT * FROM players WHERE username=?", (user_name,))
        for u in c.fetchall():
            if u[0] == user_name:
                await message.channel.send("{} code is {}".format(user_name,u[1]))
                return
        await message.channel.send("{} does not exist".format(user_name))
        return



client.run(TOKEN)