from django.db import models
import time
import json
import requests

API_KEY = "YOUR_API_KEY"

GAME_MODES = {
	0: 'Unknown',
	1: 'All Pick',
	2: 'Captains Mode',
	3: 'Random Draft',
	4: 'Single Draft',
	5: 'All Random',
	6: 'Intro',
	7: 'The Diretide',
	8: 'Reverse Captains Mode',
	9: 'Greeviling',
	10: 'Tutorial',
	11: 'Mid Only',
	12: 'Least Played',
	13: 'New Player Pool',
	14: 'Compendium Matchmaking',
	15: 'Custom',
	16: 'Captains Draft',
	17: 'Balanced Draft',
	18: 'Ability Draft',
	19: 'Event',
	20: 'All Random Death Match',
	21: '1 vs 1 Solo Mid',
	22: 'Ranked All Pick'
}

LOBBY_TYPES = {
	-1: 'Invalid',
	0: 'Public Matchmaking',
	1: 'Practise',
	2: 'Tournament',
	3: 'Tutorial',
	4: 'Co-op with bots',
	5: 'Team Match',
	6: 'Solo Queue',
	7: 'Ranked',
	8: '1v1 Mld'

}




def string_splitting(array):
	result = ''
	for x in array:
		result += str(x) + ','
	return result	

def time_converter(duration):
	result = str(int(duration/60)) +':'+ str(duration - int(duration/60)*60) 
	return result


class Match(models.Model):
	match_id = models.IntegerField(default=0)
	players = models.CharField(max_length=5000)
	result = models.CharField(default='Unknown',max_length=100)
	gamemode = models.CharField(default='Unknown',max_length=150)
	lobby = models.CharField(default='Unknown',max_length=100)
	duration = models.CharField(default='Unknown',max_length=100)
	start_time = models.CharField(default='Unknown',max_length=150)
	region = models.IntegerField(default=0)

	def initialize_match(self,match_id):
		data = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id='
		+str(match_id)+'&key='+API_KEY).json()['result']
		self.match_id = data['match_id']
		self.radiant_win = data['radiant_win']
		self.radiant_score = data['radiant_score']
		self.dire_score = data['dire_score']
		self.gamemode = GAME_MODES[data['game_mode']]
		self.lobby = LOBBY_TYPES[data['lobby_type']]
		self.duration = time_converter(data['duration'])
		self.start_time = time.ctime(data['start_time'])
		self.players = data['players']
		self.region = self.region_initialize(data)
		self.item_initialize()
		self.heroes_to_imgurl('json/heroes.json')
		self.items_to_imagepath('json/items.json')
		self.net_worth()
		self.get_players_summaries()

	def get_players_summaries(self):

		players_ids = []
		for player in self.players:
			player['account_id'] += 76561197960265728
			players_ids.append(player['account_id'])

		players_info = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?steamids='
		+str(players_ids)+'&key='+API_KEY).json()['response']['players']

		for player in self.players:
			player['name'] = 'Anonymous'
			for i in players_info:
				if(int(i['steamid']) == int(player['account_id'])):
					player['name'] = i['personaname']
					

	def net_worth(self):
		for player in self.players:
			player['net_worth'] = 0
			for i in player['items'].values():
				player['net_worth'] += i['cost']
			player['net_worth'] += player['gold']


	def item_initialize(self):
		for player in self.players:
			player['items'] = {}
			for i in range(6):
				x = 'item_' + str(i)
				player['items'][x] = {}

			player['backpack'] = {}
			for i in range(3):
				x = 'backpack_' + str(i)
				player['backpack'][x] = player[x]


	def region_initialize(self,data):
		json_data = open('json/regions.json')   
		reg_data = json.load(json_data)
		
		region = data['cluster']
		act_region = 'Unknown'
		cluster = reg_data['regions']

		for x in cluster:
			if x['id'] == region:
				act_region = x['name']

		json_data.close()

		return act_region


	def heroes_to_imgurl(self,path_to_json):
		heroes_data = json.load(open(path_to_json))

		for player in self.players:
			for hero in heroes_data:
				if(player['hero_id'] == hero['id']):
					player['hero_img_url'] = hero['url_small_portrait']


	def items_to_imagepath(self,path_to_json):
		items_data = json.load(open(path_to_json))
		
		for player in self.players:
			player['items'] = {}
			for i in range(6):
				x = 'item_' + str(i)
				for unit in items_data:
					if(player[x] == unit['id']):
						player['items'][x] = {}
						player['items'][x]['cost'] = unit['cost']
						player['items'][x]['img_path'] = str(unit['name'][5:]) + '.png'
				player.pop(x)

		for player in self.players:
			player['backpack'] = {}
			for i in range(3):
				x = 'backpack_' + str(i)
				for unit in items_data:
					if(player[x] == unit['id']):
						player['backpack'][x] = {}
						player['backpack'][x]['cost'] = unit['cost']
						player['backpack'][x]['img_path'] = str(unit['name'][5:]) + '.png'
				player.pop(x)		