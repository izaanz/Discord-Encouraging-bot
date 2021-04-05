import discord
import os
import requests
import json
import random
from replit import db

# List of user defined sad words (we can use data of sad words to increase flexibility)
sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'depressing', 'tensed']

# List of user defined encouraging words
starter_encouragements = [
  'You can do this!',
  'Hang in there.',
  "Remember! Everything is a part of life, it will pass sooner than you think :)",
  "Go Kill yourself!"
]   

if 'responding' not in db.keys():
  db['responding'] = True

# To fetch quotes from an api (random quotes api added)
def get_quote():
  response = requests.get("https://api.quotesnewtab.com/v1/quotes/random")
  # Converting response into json
  json_data = json.loads(response.text)
  # Fetching quote and author from JSon data
  quote = json_data['quote'] + " - " + json_data['author']
  return quote

# To add/update the list of ecnouraging messages
def update_encouragements(encouraging_message):
  if 'encouragements' in db.keys():
    encouragements = db['encouragements']
    encouragements.append(encouraging_message)
    db['encouragements'] = encouragements
  else:
    db['encouragements'] = [encouraging_message]

# To delete an encouragment message by IndexError
def delete_encouragement(index):
  encouragements = db['encouragements']
  if len(encouragements) >= index:
    del encouragements[index]
    db['encouragements'] = encouragements

client = discord.Client()

@client.event # if below event happens
async def on_ready(): # aysnc functions activates when 'something' happens
  print(f"We have logged in as {client.user}") # Client.user fetches the username of bot

@client.event # If a message event is recieved
async def on_message(message):
  # If the author of the message is bot itself
  if message.author == client.user:
    return

  msg = message.content

  # If the message startswith a specific keyword (command)
  if message.content.startswith('!hello'):
    await message.channel.send('Hello!')
    print("Greeted an user\n")
  if message.content.startswith('!bye'):
    print("Wished goodbye to an user\n")
    await message.channel.send('See you later!')
  if message.content.startswith('!inspire'):
    print("Inspired an user with a random quote\n")
    await message.channel.send(get_quote())

  # If db['responding'] is true (Respond trigger block)
  if db['responding']:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options.extend(db["encouragements"])
    # If message contains sad words from the list of sad words
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))
  

  # Invokes update_encouragements function to add user provided message
  if msg.startswith('!new'):
    encouraging_message = msg.split('!new ',1)[1]
    await message.channel.send('Encouraging message added successfully!')
    update_encouragements(encouraging_message)

  # Deletes user-added message
  if msg.startswith('!del'):
    encouragements = []
    if 'encouragements' in db.keys():
      index = int(msg.split('!del', 1)[1])
      await message.channel.send(f"{db['encouragements'][index]} -> Deleting...")   
      delete_encouragement(index)
      encouragements = db['encouragements']

  # Prints the list of user added words along with index
  if msg.startswith('!list'):
    encouragements = []
    if 'encouragements' in db.keys():
      encouragements = db['encouragements']
    await message.channel.send("User submitted word's index:\n")  
    for i, item in enumerate(encouragements, start=0): 
      await message.channel.send(f"{i}: {item}")

  # Respond trigger to switch on/off replies on sad_words
  if msg.startswith('!respond'):
    value = msg.split('!respond ', 1)[1]
    if value.lower() == 'true':
      db['responding'] = True
      await message.channel.send('Responding is on.')
    else:
      db['responding'] = False
      await message.channel.send('Responding is off.')


# To run the bot (Token)
# .env file hides the info from public in repl.it free tier
client.run(os.getenv('TOKEN'))