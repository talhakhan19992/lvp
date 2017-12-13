import urllib.request
import ssl
import re

def stats(id):
	#stat-desc.+?\>(.+?)\<\/.+?\n.+?stat-value.+?\>(.+?)\<
	
	url = "https://pacommunity.co.uk/server/15/profile/%s" % id;
	
	result = {};
	
	context = ssl._create_unverified_context()
	
	with urllib.request.urlopen(url, context = context) as response:
		
		html = response.read().decode("utf-8");
		
		stats = {};
		
		stats['name'] = re.search("profile\\/\\d+.\\>View\\s+(.+)\\'", html).group(1);
		stats['avatar'] = re.search("pac-avatar.+?\\n.+?img.+?src\\=\\\"(.+?)\\\"", html).group(1);
		stats['playtime'] = re.search("header\\\"\\>(Server\\splaytime).+?\\n.+?\\>(.+?)\\<", html).group(2);
		
		for match in re.finditer("stat-desc.+?\>(.+?)\\<\\/.+?\\n.+?stat-value.+?\\>(.+?)\\<", html, flags=0):
			stats[match.group(1)] = match.group(2);
		
		result = stats;
	
	url = "https://pacommunity.co.uk/profile/%s" % id;
	with urllib.request.urlopen(url, context = context) as response:
		
		html = response.read().decode("utf-8");
		
		for match in re.finditer("md-3.+xs-6\\sheader.\\>(.+?)\\<.+?\\n.+?md-4.+?info(?:\\sserver\\d+?)?\\\"\\>(.+)\\<\\/", html, flags=0):
			result[match.group(1)] = match.group(2);
		
	return result;

def search(name):
	
	url = "https://pacommunity.co.uk/search?pac_profile=%s" % name;
	
	context = ssl._create_unverified_context()
	
	class PACPlayer:
		def __init__(self, id, name):
			self.id = id;
			self.name = name;
		
		def __repr__(self):
			return self.name + ": %s" % self.id;
			
	class PACResults:
		def __init__(self, ids, names):
			self.ids = ids;
			self.names = names;
							
		def get_players(self):
			
			players = [];
			
			for i in range(0, len(self.ids)):
				players.append(PACPlayer(self.ids[i], self.names[i]));
				
			return players;
			
	with urllib.request.urlopen(url, context = context) as response:
		
		html = response.read().decode("utf-8");
		
		ids = [];
		names = [];
		
		for match in re.finditer("href=\"\\/profile\\/(\\d+)\"", html, flags=0):
			ids.append(match.group(1));
			
		for match in re.finditer("sm-9.+\\n.+header\">(.+)<\\/h5>", html, flags=0):
			names.append(match.group(1));
		
		return PACResults(ids, names);