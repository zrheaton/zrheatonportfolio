import cowsay
import random

def cowsay_message(message):
    # List of selected animals
    animals = ['dog', 'cow', 'tux']

    # Select a random animal
    selected_animal = random.choice(animals)

    # Check if the selected animal is available in cowsay
    if selected_animal in cowsay.char_names:
        getattr(cowsay, selected_animal)(message)
    else:
        cowsay.cow(message)

if __name__ == "__main__":
    jokes = [
        "Why did the data scientist go broke? Because he couldn't find any relationships!",
        "Why don't data scientists trust their gut? Because they prefer to use analytics!",
        "Why was the computer cold? It left its Windows open after collecting data!",
        "Why did the data analyst stay calm? Because he knew how to keep his pivot points!",
        "How does a data scientist organize a party? They invite all the data and let it mingle!",
        "Why was the data sad? It had too many outliers and felt excluded!",
        "What do you call a data collection robot? A gatherer bot!",
        "Why did the database administrator go to therapy? It had too many issues to index!",
        "Why did the spreadsheet break up with the database? It found it too formula-ic!",
        "Why did the data cross the road? To get to the other slide of the presentation!"
    ]

    # Select a random joke
    random_joke = random.choice(jokes)

    cowsay_message(random_joke)
