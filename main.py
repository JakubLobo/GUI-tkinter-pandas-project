from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flashcard Project")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

# Flashcard image
canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 263, image=card_front)
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# Creating texts
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text='', font=('Ariel', 60, 'bold'))


# Taking random word from a word list
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
finally:
    to_learn = data.to_dict(orient='records')
current_card = {}


def generate_word():
    global current_card, flip_timer
    try:
        window.after_cancel(flip_timer)
    except:
        pass
    # Generate random French word
    current_card = {}
    canvas.itemconfig(card, image=card_front)
    current_card = choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill='black')
    canvas.itemconfig(card_word, text=current_card['French'], fill='black')

    # Change the card on English after 3s
    flip_timer = window.after(3000, flip_card)


# Change card function
def flip_card():
    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_word, text=current_card['English'])
    canvas.itemconfig(card_title, fill='white')
    canvas.itemconfig(card_word, fill='white')


def learned_it():
    global to_learn, current_card
    to_learn.remove(current_card)
    df_words_to_learn = pandas.DataFrame(to_learn)
    df_words_to_learn.to_csv('data/words_to_learn.csv', index=False)
    generate_word()


# Buttons
wrong_button_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=generate_word)
wrong_button.grid(row=1, column=0)
right_button_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_image, highlightthickness=0, command=learned_it)
right_button.grid(row=1, column=1)

# Generation of the first random word
generate_word()



window.mainloop()