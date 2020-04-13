import sqlite3
import pandas as pd

DB_FILEPATH = '/home/jack/Downloads/rpg_db.sqlite3'
connection = sqlite3.connect(DB_FILEPATH)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR", cursor)
print()


#Total characters:
query = '''SELECT COUNT(name) FROM charactercreator_character '''
result = cursor.execute(query).fetchone()

print("Total number of characters:")
print(f'{result[0]} \n')

#Total characters per subclass:
query = '''SELECT * FROM
    (SELECT COUNT(DISTINCT character_ptr_id) as cleric FROM charactercreator_cleric), 
    (SELECT COUNT(DISTINCT character_ptr_id) as fighter FROM charactercreator_fighter),
    (SELECT COUNT(DISTINCT character_ptr_id) as mage FROM charactercreator_mage),
    (SELECT COUNT(DISTINCT mage_ptr_id) as necromancer FROM charactercreator_necromancer),
    (SELECT COUNT(DISTINCT character_ptr_id) as thief FROM charactercreator_thief)
	'''

result2 = cursor.execute(query).fetchone()
print(f'''Clerics: {result2[0]}  
Fighters: {result2[1]}   
Mages: {result2[2]}  
Necromancers: {result2[3]}
Theives: {result2[4]} \n''')

# How many total Items?
query = ''' SELECT COUNT(item_id) FROM armory_item '''
result3 = cursor.execute(query).fetchone()
print('Total items: ')
print(f'{result3[0]} \n')

# Items that are weapons and items that are not
query = ''' SELECT * FROM
(SELECT COUNT(item_ptr_id) AS weapons FROM armory_weapon),
(SELECT COUNT(item_id) - 37 AS nonweapons FROM armory_item) '''
result4 = cursor.execute(query).fetchone()
print('Items that are weapons: ')
print(f'{result[0]} \n')
print('Items that are not weapons: ')
print(f'{result4[1]} \n')

# How many items does each character have? (first 20 rows)
query = ''' SELECT character_id AS characters, COUNT(*) AS items FROM  charactercreator_character_inventory
GROUP BY character_id LIMIT 20 '''
result5 = cursor.execute(query).fetchall()
print('How many items each character has: (character_id, # of items)')
print(f'{result5} \n')

# How many weapons does each character have?
query = ''' SELECT character_id AS char_id, COUNT(*) AS weapons FROM charactercreator_character_inventory AS characters, armory_weapon as armory
WHERE characters.item_id = armory.item_ptr_id
GROUP BY character_id LIMIT 20 '''
result6 = cursor.execute(query).fetchall()
print('How many weapons each character has: (character_id, # of weapons)')
print(f'{result6} \n')

# Average items per character
query = ''' SELECT AVG(items.count) FROM (
SELECT COUNT(*) AS count FROM charactercreator_character_inventory
GROUP BY character_id) AS items '''
result7 = cursor.execute(query).fetchone()
print('Average number of items per character: ')
print(f'{result7[0]} \n')

# Average weapons per character
query = ''' SELECT AVG(weapons.count) FROM (
SELECT COUNT(*) AS count FROM charactercreator_character_inventory AS character_inv, armory_weapon AS armory
WHERE character_inv.item_id = armory.item_ptr_id
GROUP BY character_id) AS weapons '''
result8 = cursor.execute(query).fetchone()
print('Average number of weapons per character: ')
print(f'{result8[0]} \n')