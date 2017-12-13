## @file   bot.py
##
## @author Benjamin Williams <bwilliams@lincoln.ac.uk>
## @brief  Main file for littlewhitey's discord bot, LWBot.
##

#Import system modules (required)
from discord.ext import commands
import discord
import random
import time
import asyncio

#Bot modules
from timing import TimerLoop
import text
import util.debug as debug
import pydle
import threading
from multiprocessing import Queue
import re;

from commands.regular import RegularCommands

#somewhere accessible to both:
callback_queue = Queue()
TimerLoop.callback_queue = callback_queue;

#Global info
token = "Mjg0NzYwNTkxNDg1MTA4MjM0.C5Jvrg.imJkhntgU6lKZ3eKGQPNc0316Y4";

echo_channel = '285755874276933632';
bot = commands.Bot(command_prefix='!', description="LWBot: littlewhitey's Discord bot")	

async def on_player_leave(groups):
	id     = groups[0];
	name   = groups[1];
	reason = groups[2];
	
	await bot.send_message(bot.get_channel(echo_channel), ':red_circle:     **%s** has left the server. (%s, id %s)' % (name, reason.lower(), id));
	
async def on_player_join(groups):
	id   = groups[0];
	name = groups[1];
	
	await bot.send_message(bot.get_channel(echo_channel), ':large_blue_circle:     **%s** has joined the server. (id %s)' % (name, id));

async def on_player_text(groups):
	id   = groups[0];
	name = groups[1];
	text = groups[2];
	
	await bot.send_message(bot.get_channel(echo_channel), ':speech_left:     **%s** (%s): %s' % (name, id, text));
	
async def on_player_death(groups):
	killer = groups[0];
	killed = groups[1];
	weapon = groups[2];
	health = groups[3];
		
	armour = 0;
	armourStr = "";
	
	if groups[4] != None:
		armour = groups[4];
		armourStr = ", %s armor" % armour;
		
	weaponEmojis = {
		"Sawn-off Shotgun" : "sawn",
		"Desert Eagle"     : "deagle",	
		"Unarmed"          : "fist",
		"Brass Knuckles"   : "fist",
		"Shovel"           : "shovel",
		"MAC-10"           : "uzi",
		"Sniper Rifle"     : "sniper"
	};
		
	if weapon in weaponEmojis:
		
		emojis = bot.get_all_emojis();
		
		for emoji in emojis:
			if emoji.name == weaponEmojis[weapon]:
				weapon = str(emoji);
				break;
		
	else:
		weapon = "`(%s)`" % weapon;
	
	await bot.send_message(bot.get_channel(echo_channel), ':punch:     %s %s %s `(%s hp%s)`' % (killer, weapon, killed, health, armourStr));

async def on_irc_message(channel, user, message):
	
	global bot
	
	pattern = r'[\x02\x0F\x16\x1D\x1F]|\x03(\d{,2}(,\d{,2})?)?';
	stripped = re.sub(pattern, '', message);

	#print(user + " said *" + message + "* on IRC. (" + threading.current_thread().name + ")");
	#await bot.send_message(bot.get_channel(echo_channel), '`%s`' % (stripped));
	
	#Kills
	match = re.search(r"\*\*\*\s(.+?)(?:\(\d{1,3}\)\s)killed\s(.+?)(?:\(\d{1,3}\)\s)\((.+?);\s(.+?)\shealth(?:\,\s(.+?)\s)?", stripped)

	if match != None:
		await on_player_death(match.groups());
		
	#Text
	match = re.search(r"\[(\d{1,3})\]\s(\S+?)\:\s(.+)", stripped);
	
	if match != None:
		await on_player_text(match.groups());
		
	#Joins (:large_blue_circle:)
	match = re.search(r"\[(\d{1,3})\]\s\*\*\*\s(.+?)\shas\sjoined\sthe\sgame\.", stripped);
	
	if match != None:
		await on_player_join(match.groups());
		
	#Parts (:red_circle:)
	match = re.search(r"\[(\d{1,3})\]\s\*\*\*\s(.+?)\shas\sleft\sthe\sgame\.\s\((.+?)\,", stripped);

	if match != None:
		await on_player_leave(match.groups());

client = None;

class MyClient(pydle.Client):
	""" This is a simple bot that will greet people as they join the channel. """

	global join, callback_queue

	def on_connect(self):
		super().on_connect();
		self.join('#lw.samp.echo');

	def on_channel_message(self, channel, user, message):
	
		super().on_channel_message(channel, user, message);
	
		#Call on_irc_message for main thread
		callback_queue.put([ on_irc_message, channel, user, message ]);

def botThread():
	
	global client
	
	client = MyClient('LWBotDiscord')
	
	RegularCommands.irc_bot = client;
	
	client.connect('pool.irc.tl', tls=True)
	client.handle_forever()

thread = threading.Thread(target=botThread);
thread.start();









extensions = [
	"commands.management",
	"commands.regular"
];
	
		  
#Print out init message
print("");
print("    THE CAKE");
print("               IS A LIE");
print("");
print("          *  *  *            ");
print("         *|_*|_*|*_         ");
print("     .-'`|* |* |*| `'-.     ");
print("     |`-............-'|     ");
print("     |                |     ");
print("     \\   _  .-.   _   /     ");
print("   ,-|'-' '-'  '-' '-'|-,   ");
print(" /`  \\._            _./  `\\ ");
print(" '._    `\"\"\"\"\"\"\"\"\"\"`    _.' ");
print("    `''--..........--''`    ");

print("\nLWBot: littlewhitey's discord server bot");
print("[bot token] " + token + "\n");

#Send status messages initially before connection + log in
debug.log_status("Creating discord client, connecting & logging in...");

@bot.event
async def on_message(message):
	if message.author.bot:
		return

	await bot.process_commands(message)
	
@bot.event
async def on_ready():

	global callback_queue
	
	#Show that we've logged in
	print("");
	debug.log_status("Successfully logged in. User details:");
	debug.log_info("\tusername: %s" % bot.user.name);
	debug.log_info("\tid:       %s" % bot.user.id);
	
	#List servers that LWBot is on
	for server in bot.servers:
	
		#Show server info
		print("");
		debug.log_status("Connected to %s (id: %s, owner: %s)" % (server.name, server.id, server.owner.nick));
		
		#Show channels
		debug.log_info("Channels for this server:");
		
		#List channels
		for channel in server.channels:
			debug.log_info("\t#%-30s - %s" % (channel.name, channel.topic));
	
	#Get loop
	loop = asyncio.get_event_loop();
	future = asyncio.Future();
	asyncio.ensure_future(TimerLoop.start(bot))
	
	#Log that we're all okay
	debug.log_status("All good in the hood! (" + threading.current_thread().name + ")");
	

for extension in extensions:
	try:
		bot.load_extension(extension)
		
	except Exception as e:
		print('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
			
#Start client
bot.run(token);


client.quit("#freefahadi2017");