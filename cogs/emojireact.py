import discord
from discord.ext import commands
from .utils.dataIO import dataIO
import os
import re
from random import choice
try:
    from emoji import UNICODE_EMOJI
except:
    raise RuntimeError("Can't load emojis. Do 'pip3 install emoji'.")

class ServerEmojiReact():
    def __init__(self, bot):
        self.bot = bot
        self.settings_file = "data/emojireact/settings.json"
        self.settings = dataIO.load_json(self.settings_file)

    @commands.group(pass_context=True)
    async def emojireact(self, ctx):
        if ctx.invoked_subcommand is None:
             await self.bot.send_cmd_help(ctx)

    @emojireact.group(pass_context=True, name="unicode")
    async def _unicode(self, ctx):
        """Add or remove unicode emoji reactions"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @emojireact.group(pass_context=True, name="server")
    async def _server(self, ctx):
        """Add or remove server emoji reactions"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @emojireact.group(pass_context=True, name="all")
    async def _all(self, ctx):
        """Add or remove all emoji reactions"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @emojireact.group(pass_context=True, name="random")
    async def _random(self, ctx):
        """Add or remove all emoji reactions"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @_all.command(pass_context=True, name="add", aliases=["on"])        
    async def add_all(self,ctx):
        """Adds all emoji reactions to the server"""
        self.settings[ctx.message.server.id] = {"unicode":True, "server": True}
        dataIO.save_json(self.settings_file, self.settings)
        await self.bot.send_message(ctx.message.channel, "Okay, I will react to messages containing emojis!")

    @_all.command(pass_context=True, name="remove", aliases=["off"])        
    async def rem_all(self,ctx):
        """Removes all emoji reactions to the server"""
        self.settings[ctx.message.server.id] = {"unicode":False, "server": False}
        dataIO.save_json(self.settings_file, self.settings)
        await self.bot.send_message(ctx.message.channel, "Okay, I will not react to messages containing emojis!")

    @_random.command(pass_context=True, name="add", aliases=["on"])        
    async def add_rand(self,ctx):
        """Adds all emoji reactions to the server"""
        self.settings[ctx.message.server.id] = {"unicode":True, "server": True, "random":True}
        dataIO.save_json(self.settings_file, self.settings)
        await self.bot.send_message(ctx.message.channel, "Okay, I will react to messages containing emojis!")

    @_random.command(pass_context=True, name="remove", aliases=["off"])        
    async def rem_rand(self,ctx):
        """Removes all emoji reactions to the server"""
        self.settings[ctx.message.server.id] = {"unicode":False, "server": False, "random":False}
        dataIO.save_json(self.settings_file, self.settings)
        await self.bot.send_message(ctx.message.channel, "Okay, I will not react to messages containing emojis!")

    @_unicode.command(pass_context=True, name="add", aliases=["on"])        
    async def add_unicode(self,ctx):
        """Adds unicode emoji reactions to the server"""
        if ctx.message.server.id not in self.settings:
            self.settings[ctx.message.server.id] = {"unicode":True, "server": False}
        else:
            self.settings[ctx.message.server.id]["unicode"] = True
        dataIO.save_json(self.settings_file, self.settings)
        await self.bot.send_message(ctx.message.channel, "Okay, I will react to messages containing unicode emojis!")

    @_unicode.command(pass_context=True, name="remove", aliases=["off"])        
    async def rem_unicode(self,ctx):
        """Removes unicode emoji reactions to the server"""
        if ctx.message.server.id not in self.settings:
            self.settings[ctx.message.server.id] = {"unicode":False, "server": False}
        else:
            self.settings[ctx.message.server.id]["unicode"] = False
        dataIO.save_json(self.settings_file, self.settings)
        await self.bot.send_message(ctx.message.channel, "Okay, I will not react to messages containing unicode emojis!")

    @_server.command(pass_context=True, name="add", aliases=["on"])        
    async def add_server(self,ctx):
        """Adds server emoji reactions to the server"""
        if ctx.message.server.id not in self.settings:
            self.settings[ctx.message.server.id] = {"unicode":True, "server": True}
        else:
            self.settings[ctx.message.server.id]["server"] = True
        dataIO.save_json(self.settings_file, self.settings)
        await self.bot.send_message(ctx.message.channel, "Okay, I will react to messages containing server emojis!")

    @_server.command(pass_context=True, name="remove", aliases=["off"])        
    async def rem_server(self,ctx):
        """Removes server emoji reactions to the server"""
        if ctx.message.server.id not in self.settings:
            self.settings[ctx.message.server.id] = {"unicode":False, "server": False}
        else:
            self.settings[ctx.message.server.id]["server"] = False
        dataIO.save_json(self.settings_file, self.settings)
        await self.bot.send_message(ctx.message.channel, "Okay, I will not react to messages containing server emojis!")

    async def on_message(self, message):
        channel = message.channel
        server = message.server
        if channel.is_private:
            return
        if server.id not in self.settings:
            return
        emoji_list = []
        for word in re.split(r"[<> ]+", message.content):
            if word.startswith(":") and self.settings[server.id]["server"]:
                emoji_list.append(word)
            if word in UNICODE_EMOJI and self.settings[server.id]["unicode"]:
                emoji_list.append(word)
        if "random" in self.settings[server.id]:
            if self.settings[server.id]["random"]:
                emoji = choice(list(UNICODE_EMOJI))
                try:
                    await self.bot.add_reaction(message, emoji)
                except:
                    await self.bot.add_reaction(message, "😘")
        if emoji_list == []:
            return
        for emoji in emoji_list:
            try:
                await self.bot.add_reaction(message, emoji)
            except:
                pass



def check_folders():
    if not os.path.exists("data/emojireact"):
        print("Creating data/emojireact folder...")
        os.makedirs("data/emojireact")


def check_files():
    f = "data/emojireact/settings.json"
    data = {}
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, data)



def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(ServerEmojiReact(bot))
