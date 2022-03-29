import discord
from discord.ext import commands
import dotenv
import os
import sqlite3
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


client = commands.Bot("!")

dotenv.load_dotenv()

conn = sqlite3.connect("orders.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS orders(txid string)")
conn.commit()
conn.close()

def gettx(txid):
    try:
        rpc_connection = AuthServiceProxy("http://user:pw@127.0.0.1:22555")

        for i in range(0, 9):
            transaction = rpc_connection.gettxout(txid, i)

            if transaction == None:
                continue

            bal = transaction["value"]

            print(bal)

            if 11 > bal > 9:
                if transaction["addresses"][0] == "BKTjvyDMEMrJDQPTnEyJLTYVkrrBWsuqHj":
                    return 10
                else:
                    return True

            elif 16 > bal > 14:
                if transaction["addresses"][0] == "BKTjvyDMEMrJDQPTnEyJLTYVkrrBWsuqHj":
                    return 15
                else:
                    return True

            else:
                return True

    except JSONRPCException:
        return False



@client.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="you buying cheese | !menu")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print(f"Successfully logged in as {client.user}. Online on {len(client.guilds)} Servers.")


@client.command()
async def menu(ctx):
    embed = discord.Embed(
        title = "TODAY'S MENU",
        description = "**Here is your menu, sir. :sunglasses:**\nYou can buy cheese buy sending the amount for \nthe cheese to BKTjvyDMEMrJDQPTnEyJLTYVkrrBWsuqHj and then redeem your\n cheese by using the command on the menu + the txid. \nNo guarantees for any lost funds!",
        colour = discord.colour.Color.from_rgb(255,172,50),
    )
    embed.set_image(url="https://cdn.discordapp.com/attachments/857288120650694689/954780173503434773/menu.png")
    await ctx.send(embed=embed)

@client.command()
async def gouda(ctx, txid):
    tx = gettx(txid)
    if tx == True:
        await ctx.send("You didn't send enough moni, now your moni is gone, sir... (or something went wrong, dm Pichi)")
    elif tx == False:
        await ctx.send("An unknown error occured, sir. Try again, sir.")
    elif tx == None:
        await ctx.send("txid invalid, sir.")
    else:
        print(tx)
        conn = sqlite3.connect("orders.db")
        cur = conn.cursor()
        new = cur.execute("SELECT * FROM orders WHERE txid = (?)", (txid,))
        new = new.fetchone()
        if not new == None:
            await ctx.send("You have already claimed your cheese, sir. You can get some more by paying more money.")
            conn.close()
        else:
            cur.execute("INSERT INTO orders VALUES (?)", (txid,))
            conn.commit()
            conn.close()
            embed = discord.Embed(
                title = "GOUDA",
                description = "Here is your gouda, sir.",
                colour = discord.colour.Color.from_rgb(255,172,50),
            )
            embed.set_image(url="https://cdn.discordapp.com/nottelling.jpg")
            await ctx.send(embed=embed)


@gouda.error
async def hello_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("You need to specify your txid, sir.")
    else:
        await ctx.send("An unknown error occured. Try again, sir. (hmmmmmm)")


@client.command()
async def emmental(ctx, txid):
    tx = gettx(txid)
    if tx == True:
        await ctx.send("You didn't send enough moni, now your moni is gone, sir... (or something went wrong, dm Pichi)")
    elif tx == False:
        await ctx.send("An unknown error occured, sir. Try again, sir.")
    elif tx == None:
        await ctx.send("txid invalid, sir.")
    else:
        conn = sqlite3.connect("orders.db")
        cur = conn.cursor()
        new = cur.execute("SELECT * FROM orders WHERE txid = (?)", (txid,))
        new = new.fetchone()
        if not new == None:
            await ctx.send("You have already claimed your cheese, sir. You can get some more by paying more money.")
            conn.close()
        else:
            cur.execute("INSERT INTO orders VALUES (?)", (txid,))
            conn.commit()
            conn.close()
            embed = discord.Embed(
                title = "GOUDA",
                description = "Here is your emmental, sir.",
                colour = discord.colour.Color.from_rgb(255,172,50),
            )
            embed.set_image(url="https://cdn.discordapp.com/nottelling.jpg")
            await ctx.send(embed=embed)


@emmental.error
async def hello_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("You need to specify your txid, sir.")
    else:
        await ctx.send("An unknown error occured. Try again, sir. (hmmmmmm)")


@client.command()
async def mix(ctx, txid):
    tx = gettx(txid)
    if tx == True:
        await ctx.send("You didn't send enough moni, now your moni is gone, sir... (or something went wrong, dm Pichi)")
    elif tx == False:
        await ctx.send("An unknown error occured, sir. Try again, sir.")
    elif tx == 10:
        await ctx.send("You only sent 10BKC. You can only buy gouda or emmental with that.")
    elif tx == None:
        await ctx.send("txid invalid, sir.")
    else:
        conn = sqlite3.connect("orders.db")
        cur = conn.cursor()
        new = cur.execute("SELECT * FROM orders WHERE txid = (?)", (txid,))
        new = new.fetchone()
        if not new == None:
            await ctx.send("You have already claimed your cheese, sir. You can get some more by paying more money.")
            conn.close()
        else:
            cur.execute("INSERT INTO orders VALUES (?)", (txid,))
            conn.commit()
            conn.close()
            embed = discord.Embed(
                title = "GOUDA",
                description = "Here is your super duper exotic mix, sir.",
                colour = discord.colour.Color.from_rgb(255,172,50),
            )
            embed.set_image(url="https://cdn.discordapp.com/nottelling.jpg")
            await ctx.send(embed=embed)


@mix.error
async def hello_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("You need to specify your txid, sir.")
    else:
        await ctx.send("An unknown error occured. Try again, sir. (hmmmmmm)")

client.run(os.getenv("TOKEN"))
