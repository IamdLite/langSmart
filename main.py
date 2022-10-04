from tkinter import *
from matplotlib import image
from matplotlib.pyplot import text
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Lang Smart")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
current_card = {}
words_to_learn = {}

#data processing 
try:
    data = pandas.read_csv("data/words_to_learn.csv")
    pandas.DataFrame(data)
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    words_to_learn = original_data.to_dict(orient="records")
else:  
    words_to_learn = data.to_dict(orient = "records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_to_learn)
    canvas.itemconfig(card_title, text= "French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, flip_card)
    

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text = current_card["English"], fill="white")
    canvas.itemconfig(card_background, image = card_back_img)   

flip_timer = window.after(3000, flip_card)

def is_known():
    words_to_learn.remove(current_card) 
    data = pandas.DataFrame(words_to_learn)
    data.to_csv("data/words_to_learn.csv")       
    next_card() 
    
#flash card
canvas = Canvas(height=520, width = 800)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image = card_front_img)
card_title = canvas.create_text(400, 150, text= "Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text= "word", font=("Ariel", 60, "bold"))
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

#buttons
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command= next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file = "images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command = is_known)
known_button.grid(row=1, column=1)

next_card()

























window.mainloop()