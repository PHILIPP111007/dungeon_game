import json
import time
import random
import re

import change_pathname
import welcome


def print_game_map():
	if not tavern_flag:
		print(f'\n\nMAP {map_id}:\n')
	else:
		print('\n\nTAVERN:\n')

	game_map[hero_coordinates[0]][hero_coordinates[1]] = 'H'

	print('   ', end=' ')
	for i in range(1, len(game_map[0]) + 1):
		print(chr(i + 64), end=' ')
	print()
	print('   ', end=' ')

	for _ in range(1, len(game_map[0]) + 1):
		print('-', end=' ')
	print()

	for i in range(len(game_map)):
		print(chr(i + 65), end=' | ')
		for j in range(len(game_map[0])):
			print(game_map[i][j], end=' ')
		print('|')

	print('   ', end=' ')
	for _ in range(len(game_map[0])):
		print('-', end=' ')
	print()



def change_H_into_none():
	game_map[hero_coordinates[0]][hero_coordinates[1]] = ' '



def its_a_stone_print():
	print('It is impossible to climb a rock\n')



def print_time_sleep():
	for _ in range(3):
		print('.')
		time.sleep(.7)
	print('\n')



# __________________________________



# move using WASD
def hero_movement_wasd():
	global map_id
	global tavern_flag


	if word == 'w' and hero_coordinates[0] - 1 >= 0:
		a = -1
		b = 0
	elif word == 's' and hero_coordinates[0] + 1 <= len(game_map) - 1:
		a = 1
		b = 0
	elif word == 'a' and hero_coordinates[1] - 1 >= 0:
		a = 0
		b = -1
	elif word == 'd' and hero_coordinates[1] + 1 <= len(game_map[0]) - 1:
		a = 0
		b = 1
	else:
		return
	
	x = hero_coordinates[0] + a
	y = hero_coordinates[1] + b

	if game_map[x][y] == stone_picture:
		return its_a_stone_print()
	elif game_map[x][y] == monster_picture:
		monster_coordinates = [x, y]
		return monster(monster_coordinates)
	elif game_map[x][y] == shop_picture:
		return shop_print()
	else:
		change_H_into_none()
		if game_map[x][y] == portal_picture_forward:
			if not tavern_flag:
				map_id = str(int(map_id) + 1)
			else:
				tavern_flag = False
			load_map_plus()
		elif game_map[x][y] == portal_picture_backward:
			if not tavern_flag:
				map_id = str(int(map_id) - 1)
			else:
				tavern_flag = False
			load_map_minus()
		else:
			if game_map[x][y] == chest_picture:
				chest()
			elif game_map[x][y] == heart_picture:
				heart()

			if x:
				hero_coordinates[0] += a
			elif y:
				hero_coordinates[1] += b
		print_game_map()




# move using chess coding
def hero_movement_chess():
	global map_id
	global tavern_flag


	x = ord(word.split()[0]) - 65
	y = ord(word.split()[1]) - 65


	if 0 <= x < len(game_map) and 0 <= y < len(game_map[0]):
		if game_map[x][y] == stone_picture:
			return its_a_stone_print()
		elif game_map[x][y] == monster_picture:
			monster_coordinates = [x, y]
			return monster(monster_coordinates)
		elif game_map[x][y] == shop_picture:
			return shop_print()
		else:
			change_H_into_none()
			if game_map[x][y] == portal_picture_forward:
				if not tavern_flag:
					map_id = str(int(map_id) + 1)
				else:
					tavern_flag = False
				load_map_plus()
			elif game_map[x][y] == portal_picture_backward:
				if not tavern_flag:
					map_id = str(int(map_id) - 1)
				else:
					tavern_flag = False
				load_map_minus()
			else:
				hero_coordinates[0] = x
				hero_coordinates[1] = y

				if game_map[x][y] == chest_picture:
					chest()
				elif game_map[x][y] == heart_picture:
					heart()

			print_game_map()



# __________________________________



def load_map_plus():
	global data_json
	global hero_coordinates
	global game_map


	with open(f'{change_pathname.path}/maps/{map_id}.json', 'r', encoding='UTF-8') as file:
		data_json = json.load(file)
		hero_coordinates = data_json['+']
		game_map = data_json['map']



def load_map_minus():
	global data_json
	global hero_coordinates
	global game_map


	with open(f'{change_pathname.path}/maps/{map_id}.json', 'r', encoding='UTF-8') as file:
		data_json = json.load(file)
		hero_coordinates = data_json['-']
		game_map = data_json['map']



def load_inventory():
	global inventory


	with open(f'{change_pathname.path}/items/save.json', 'r', encoding='UTF-8') as file:
		inventory = json.load(file)



# __________________________________



def chest():
	with open(f'{change_pathname.path}/items/resourses.json', 'r') as file:
		data = json.load(file)
		if 'wooden_sword' in inventory:
			inventory['wooden_sword'][2] += 1
		else:
			inventory['wooden_sword'] = data['weapons']['wooden_sword']
		inventory['$'] += 5

	print('\nYou got wooden_sword and $5')
	print_time_sleep()



def heart():
	if inventory['HP'] + 5 >= max_hp:
		inventory['HP'] = max_hp
	else:
		inventory['HP'] += 5

	print(f'\nYou have increased your health by 5 units! You have {inventory["HP"]} HP')
	print_time_sleep()



# __________________________________



def monster(monster_coordinates):
	with open(f'{change_pathname.path}/items/monsters.json', 'r', encoding='UTF-8') as file:
		monsters_data_json = json.load(file)
		monster_data = random.choice(list(monsters_data_json))
		monster_data = [monster_data, monsters_data_json[monster_data]]
	
	print(f'\nYou got {monster_data[0]}: {monster_data[1][0]} HP | damage {monster_data[1][1]}')
	choice = input('Get into a fight? (1 / 0)\n')
	if choice == '1':
		print(f'Get ready!\nYou will fight {favorite_weapon}')
		print_time_sleep()
		return fight(monster_data, monster_coordinates)
	else:
		print('You passed unnoticed...\n')



def fight(monster_data, monster_coordinates):
	global lose_flag
	global inventory


	while True:
		if monster_data[1][0] - inventory[favorite_weapon][1] <= 0:
			print(f'Congratulations! You won, and you also got $5\nYour health is {inventory["HP"]} HP\n')
			inventory['$'] += 5
			change_H_into_none()
			hero_coordinates[0] = monster_coordinates[0]
			hero_coordinates[1] = monster_coordinates[1]
			print_time_sleep()
			print_game_map()
			break
		else:
			monster_data[1][0] -= inventory[favorite_weapon][1]

		if inventory['HP'] - monster_data[1][1] <= 0:
			if inventory['$'] - 5 <= 0:
				inventory['$'] = 0
			else:
				inventory['$'] -= 5
			print(f'You lost...\nYou also lost some coins, your balance: ${inventory["$"]}')
			lose_flag = True
			print_time_sleep()
			break
		else:
			inventory['HP'] -= monster_data[1][1]



# __________________________________



def menu():

	choice = input('\nMENU:\n"enter" - exit the menu\n2 - backpack\n3 - tavern\nq - save and quit the game\n9 - quit the game and reset progress\n')
	if choice == '2':
		inventory_print()
		print()
	elif choice == '3':
		tavern_load_map()
		print()
	elif choice == 'q':
		print()
		save_game()
		return 'q'
	elif choice == '9':
		print()
		reset_progress()
		return 'q'



def save_game():
	inventory['HP'] = max_hp
	with open(f'{change_pathname.path}/items/save.json', 'w', encoding='UTF-8') as file:
		json.dump(inventory, file)



def reset_progress():
	with open(f'{change_pathname.path}/items/save.json', 'w', encoding='UTF-8') as file:
		json.dump(inventory_reset, file)



def inventory_print():
	global favorite_weapon


	print('\nINVENTORY:')
	print(f'{"health".ljust(len(max(inventory, key=len)) + 1)}: {inventory["HP"]} HP')
	print(f'{"coins".ljust(len(max(inventory, key=len)) + 1)}: ${inventory["$"]}')
	print(f'{"hand".ljust(len(max(inventory, key=len)) + 1)}: damage {inventory["hand"][1]}')

	for key in inventory:
		if key != 'HP' and key != '$' and key != 'hand':
			print(f'{key.ljust(len(max(inventory, key=len)) + 1)}: cost ${inventory[key][0]} | damage {inventory[key][1]} | in stock {inventory[key][2]}')
	print()
	choice = input('Do you want to choose a primary weapon? (1 / 0):\n')
	if choice == '1':
		wish = input('Which weapon will you choose from your backpack?\n')
		if wish in inventory and wish != 'HP' and wish != '$':
			favorite_weapon = wish
			print(f'You have selected {favorite_weapon}\n')
		else:
			print('You entered incorrect data\n')



def tavern_load_map():
	global data_json
	global hero_coordinates
	global game_map
	global tavern_flag


	print('\nYou go to the tavern')
	print_time_sleep()
	tavern_flag = True
	with open(f'{change_pathname.path}/maps/tavern.json', 'r', encoding='UTF-8') as file:
		data_json = json.load(file)
		hero_coordinates = data_json['+']
		game_map = data_json['map']
	print_game_map()



def shop_print():
	print('\nSHOP:\n')
	print(f'Total coins: ${inventory["$"]}')

	choice = input('Do you want to buy or sell a weapon? (1 - buy, 2 - sell, "enter" - exit)\n')

	if choice == '1':
		print()
		buy_weapon()
	elif choice == '2':
		print()
		sell_weapon()



def buy_weapon():
	with open(f'{change_pathname.path}/items/resourses.json', 'r') as file:
		data = json.load(file)
		for key, value in data['weapons'].items():
			print(f'{key.ljust(len(max(data["weapons"], key=len)) + 1)}: cost ${value[0]} | damage {value[1]}')
	print()
	choice = input('What would you like to buy? Enter the name of the weapon:\n')
	if choice in data['weapons']:
		if inventory['$'] >= data['weapons'][choice][0]:
			if choice in inventory:
				inventory[choice][2] += 1
			else:
				inventory[choice] = data['weapons'][choice]
			inventory['$'] -= data['weapons'][choice][0]
			print(f'\nYou have purchased {choice}!\n')
		else:
			print('\nYou don\'t have enough coins...\n')
	else:
		print('\nWe do not have such weapons...\n')



def sell_weapon():
	for key in inventory:
		if key != 'HP' and key != '$' and key != 'hand':
			print(f'{key.ljust(len(max(inventory, key=len)) + 1)}: can be sold for ${inventory[key][0]} | in stock {inventory[key][2]}')
	print()
	choice = input('What would you like to sell? Enter the name of the weapon:\n')
	if choice in inventory and choice != 'HP' and choice != '$' and choice != 'hand':
		if inventory[choice][2] > 1:
			inventory[choice][2] -= 1
			inventory['$'] += inventory[choice][0]
		else:
			inventory['$'] += inventory[choice][0]
			del inventory[choice]
		print(f'\nYou sold {choice}!\n')
	else:
		print('\nYou don\'t have that kind of weapon...\n')



# __________________________________



# global variables
word = input('Start the game "Dungeon_v2.2"? (1 / 0):\n')
files_path = change_pathname.path
map_id = '1'
max_hp = 30
inventory_reset = {"HP": max_hp, "$": 0, "hand": [0, 1, 1]}

stone_picture = '@'
chest_picture = '?'
heart_picture = '♡'
monster_picture = 'M'
shop_picture = 'S'
portal_picture_forward = '+'
portal_picture_backward = '-'

tavern_flag = False
game_map = []
hero_coordinates = []
data_json = {}
inventory = {}

favorite_weapon = 'hand'
lose_flag = False



# __________________________________




# game cycle
if word == '1':

	print(welcome.rules)
	load_map_plus()
	load_inventory()
	print_game_map()
	
	while True:

		if lose_flag is True:
			word = input('Rebirth? (1 / 0)\n')
			if word == '0':
				save_game()
				print('See you later!')
				break
			else:
				print('You have been reborn!\n')
				print_game_map()
				inventory['HP'] = max_hp
				lose_flag = False

		word = input('("enter" - skip), (m - menu):\n').strip()
		if word == 'm':

			word = menu()
			if word == 'q':
				print('See you later!')
				break

		elif word in ('w', 'a', 's', 'd'):
			hero_movement_wasd()

		elif re.fullmatch(r'^[A-Z] [A-Z]$', word):
			hero_movement_chess()

else:
	print('See you later!')

