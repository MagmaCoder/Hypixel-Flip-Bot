import requests
import discord
import os
import server
from discord.ext import commands
#Oak Wood: "LOG"
#Spruce Wood: "LOG:1"
#Birch Wood: "LOG:2"
#Dark Oak Wood: "LOG_2:1"
#Acacia Wood: "LOG_2"
#Jungle Wood: "LOG:3"
#Gunpowder: "SULPHUR"
#Lapis Lazuli: "INK_SACK:4"
#Cocoa Beans: "INK_SACK:3"
#Red Mushroom Block: "HUGE_MUSHROOM_2"
#Brown Mushroom Block: "HUGE_MUSHROOM_1"
#LOG_2:1 = Dark Oak
#LOG_2 = Acacia
#

bot = commands.Bot(command_prefix=".")
TOKEN = os.getenv("DISCORD_TOKEN")

def get_name(name):
    if name in TRANSLATED_NAMES:
        return TRANSLATED_NAMES[name]
    else:
        lower = name.lower().replace("_"," ")
        return lower.title()



TRANSLATED_NAMES = {
    "LOG":"Oak Log",
    "LOG:1":"Spruce Wood",
    "LOG:2":"Birch Wood",
    "LOG_2:1":"Dark Oak Wood",
    "LOG_2":"Acacia Wood",
    "LOG:3":"Jungle Wood",
    "RAW_FISH":"Raw Cod",
    "RAW_FISH:1":"Raw Salmon",
    "RAW_FISH:2":"Raw Clownfish",
    "RAW_FISH:3":"Pufferfish",
    "SULPHUR":"Gunpowder",
    "CARROT_ITEM":"Carrot",
    "POTATO_ITEM":"Potato",
    }

NPC_PRICES = {
    "ROTTEN_FLESH":[1,8,"Adventurer"],
    "BONE":[1,8,"Adventurer"],
    "STRING":[1,10,"Adventurer"],
    "SLIMEBALL":[1,10,"Adventurer"],
    "SULPHUR":[1,10,"Adventurer"],
    "LOG":[5,25,"Lumber Merchant"],
    "LOG_2:1":[5,25,"Lumber Merchant"],
    "LOG_2":[5,25,"Lumber Merchant"],
    "LOG:1":[5,25,"Lumber Merchant"],
    "LOG:2":[5,25,"Lumber Merchant"],
    "LOG:3":[5,25,"Lumber Merchant"],
    "RAW_FISH":[1,20,"Fish Merchant"],
    "RAW_FISH:1":[1,30,"Fish Merchant"],
    "RAW_FISH:2":[1,100,"Fish Merchant"],
    "RAW_FISH:3":[1,40,"Fish Merchant"],
    "COAL":[2,8,"Mine Merchant"],
    "COBBLESTONE":[1,2,"Builder"],
    "ICE":[1,1,"Builder or Sherry"],
    "PACKED_ICE":[1,9,"Builder or Sherry"],
    "SPIDER_EYE":[1,12,"Alchemist"],
    "GHAST_TEAR":[1,200,"Alchemist"],
    "MAGMA_CREAM":[1,20,"Alchemist"],
    "FLINT":[1,6,"Pat"],
    "GRAVEL":[1,4,"Pat"],
    "GOLD_INGOT":[1,5.5,"Gold Forger"],
    "IRON_INGOT":[1,5,"Iron Forger"],
    "WHEAT":[64,149,"Farm Merchant"],
    "CARROT_ITEM":[64,149,"Farm Merchant"],
    "POTATO_ITEM":[64,149,"Farm Merchant"],
    "MELON":[64,128,"Farm Merchant"],
    "PUMPKIN":[64,512,"Farm Merchant"],
    "INK_SACK:3":[64,320,"Farm Merchant"],
    "RED_MUSHROOM":[64,768,"Farm Merchant"],
    "BROWN_MUSHROOM":[64,768,"Farm Merchant"],
    "SUGAR_CANE":[64,320,"Farm Merchant"],
    "CACTUS":[64,640,"Farm Merchant"],
    "SAND":[64,256,"Farm Merchant"],
    }

PLAYER_API_KEY = os.getenv("HYPIXEL_TOKEN")
DATA = {"key":PLAYER_API_KEY}
HYPIXEL_URL = "https://api.hypixel.net/skyblock/bazaar"

async def get_bazaar(ctx):
    Current_Bazaar_Data = requests.get(HYPIXEL_URL,DATA).json()
    products = Current_Bazaar_Data["products"]
    flipped_items = []
    for product in products:
        current_product = products[product]

        pr_name = current_product["product_id"]
        pr_status = current_product["quick_status"]
        pr_avg_buy = pr_status["buyPrice"]
        pr_avg_sell = pr_status["sellPrice"]
        #CHECK FLIP
        try:
            current_npc_price = NPC_PRICES[pr_name]
            if current_npc_price[0] > 1:
                npc_single_cost = current_npc_price[1] / current_npc_price[0]
            else:
                npc_single_cost = current_npc_price[1]
            if pr_avg_sell > npc_single_cost:
                translated_name = get_name(pr_name)
                flipped_items.append([translated_name,current_npc_price[2],npc_single_cost,pr_avg_sell,int((pr_avg_sell*640))-(int(npc_single_cost)*640)])
        except Exception as e:
            pass
    string = ""
    counter = 0
    title = ""
    value_n = "."
    total_profit = 0
    embedVar = discord.Embed(title="Current Flips:", description="The current NPC -> Bazaar flips.", color=0x00ff00)
    for flipped_item in flipped_items:
        if counter == 0:
            title = flipped_item[0] + " : :shopping_cart: "+flipped_item[1]+". :arrow_down: " +str(flipped_item[2])+", :arrow_up: "+str(round(flipped_item[3],3))+". :chart_with_upwards_trend: "+str(round(flipped_item[4],3))
            total_profit += round(flipped_item[4],3)
            counter += 1
        elif counter == 1:
            value_n = "**"+flipped_item[0] + " : :shopping_cart: "+flipped_item[1]+". :arrow_down: " +str(flipped_item[2])+", :arrow_up: "+str(round(flipped_item[3],3))+". :chart_with_upwards_trend: "+str(round(flipped_item[4],3))+"**"
            total_profit += round(flipped_item[4],3)
            embedVar.add_field(name=title, value=value_n, inline=False)
            title = ""
            value_n = "."
            counter = 0
    embedVar.add_field(name="Total Profit: :chart_with_upwards_trend: "+str(total_profit),value="⠀", inline=False)
          
    await ctx.send(embed=embedVar)
    #string += flipped_item[0]+" from the "+flipped_item[1]+". Buy for " +str(flipped_item[2])+" sell for "+str(round(flipped_item[3],3))+". Profit is "+str(round(flipped_item[4],3))+".\n"
    
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")

@bot.command()
async def chkflps(ctx):
    '''Check the current NPC -> Bazaar flips.'''
    await get_bazaar(ctx)

server.server()
bot.run(TOKEN)
