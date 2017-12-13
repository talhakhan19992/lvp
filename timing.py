## @file   timing.py
##
## @author Benjamin Williams <bwilliams@lincoln.ac.uk>
## @brief  Contains classes and functions for the timing loop, such as randomly updating statuses.
##

import discord
import asyncio
import random
import schedule
from threading import Timer
import threading
import time
import math
import text

from multiprocessing import Queue
import queue

class TimerLoop(object):
	
	callback_queue = None;
	
	@staticmethod
	async def update_status(client):
		await client.change_presence(game=discord.Game(name=random.choice(text.statuses)));

	@staticmethod
	async def start(client):
		
		await TimerLoop.update_status(client);
		
		while True:
			await asyncio.sleep(0.1);
						
			roundedTime = round(time.time(), 1); 
		
			if roundedTime % 120 == 0:
				await TimerLoop.update_status(client);

			try:
				callback = TimerLoop.callback_queue.get(False) #doesn't block
				
				func = callback[0];
				channel = callback[1];
				user = callback[2];
				message = callback[3];
				
				await func(channel, user, message);
				
				#loop = asyncio.get_event_loop();
				#task = asyncio.ensure_future(func(channel, user, message));
				#loop.run_until_complete(task);
				
			except queue.Empty: #raised when queue is empty
				continue;
				
			
