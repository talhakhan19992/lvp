## @file   util/client.py
##
## @author Benjamin Williams <bwilliams@lincoln.ac.uk>
## @brief  Contains functions for checking management only commands.
##

import discord
import random
import text
import util

async def usage(bot, string):
	await client.send_message(message.channel, "**Usage:* `%s`" % string);
	await client.send_message(message.channel, random.choice(text.usageMessages));

async def processing(bot):
	return await bot.say(random.choice(text.processingMessages));
	
async def exit(bot, channel=None):
	if channel == None:
		return await bot.say(random.choice(text.exitMessages) + ":wave:");
	else:
		return await bot.send_message(channel, random.choice(text.exitMessages) + ":wave:");
		