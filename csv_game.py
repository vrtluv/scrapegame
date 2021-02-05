import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictReader



BASE_URL = "http://quotes.toscrape.com/"

def read_quotes(filename):
	with open(filename, "r") as file:
		csv_reader = DictReader(file)
		return list(csv_reader)

def start_game(quotes):
	quote = choice(quotes)
	rem_guesses = 4
	print("Here's a quote: ")
	print(quote["text"])
	print(quote["author"])
	guess = ''
	while guess.lower() != quote['author'].lower() and rem_guesses > 0:
		guess = input(f"Guesses remaining: {rem_guesses} \nWho said this quote?")
		if guess.lower() == quote['author'].lower():
			print(f"Nice, you got it, the author was {quote['author']}")
			break
		rem_guesses -= 1
		if  rem_guesses == 3:
			res = requests.get(f"{BASE_URL}{quote['bio-link']}")
			soup = BeautifulSoup(res.text, "html.parser")
			birth_date = soup.find(class_="author-born-date").text
			birth_loc = soup.find(class_="author-born-location").text
			print (f"Clue 1: This author was born {birth_loc} on {birth_date}")
		elif rem_guesses == 2:
			print(f"Clue 2: This authors first initial is {quote['author'][0]}")
		elif rem_guesses == 1:
			last_initial = quote['author'].split(" ")[1][0]
			print(f'Clue 3: This authors last initial is {last_initial}')
		else:
			print(f"Sorry you ran out of guesses. The answer was {quote['author']}")

	again = ''
	while again.lower() not in ('y', 'yes', 'n', 'no'):
		again = input('Would you like to play again (y/n)?')
	if again.lower() in ('yes', 'y'):
		print("Ok!, Let's Play")
		return start_game(quotes)
	else:
		print("Thanks, until next time")	


quotes = read_quotes("quotes.csv")
start_game(quotes)



	