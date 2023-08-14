import pandas
import random
from tkinter import *


def read_data_from_csv():
    try:
        return pandas.read_csv("words_to_learn.csv")
    except FileNotFoundError:
        return pandas.read_csv("data/jp.csv")


BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Courier"
after_call = ""
data = read_data_from_csv()

words = data.to_dict(orient="records")
random.shuffle(words)
index = 0
stage = 0


def set_after_call():
    global after_call
    after_call = window.after(3000, change_word)


def update_canvas(front_state, back_state):
    canvas.itemconfigure(canvas_lang1_text, state=front_state)
    canvas.itemconfigure(canvas_lang2_text, state=back_state)
    canvas.itemconfigure(canvas_front_image, state=front_state)
    canvas.itemconfigure(canvas_back_image, state=back_state)


def change_word(force_change=False, known_word=False):
    global index, stage, words, after_call
    stage += 1
    if force_change:
        stage = 0

    if known_word:
        words.remove(words[index])
        save_know_word_to_csv(words)

    if stage % 2 == 0:
        index += 1
        if index == len(words):
            random.shuffle(words)
            index = 0
        front_state = "normal"
        back_state = "hidden"
        canvas.itemconfigure(canvas_text, text=f"{words[index]['Japanese']}")
    else:
        front_state = "hidden"
        back_state = "normal"
        canvas.itemconfigure(canvas_text, text=f"{words[index]['English']}")

    update_canvas(front_state, back_state)
    window.after_cancel(after_call)
    set_after_call()


def save_know_word_to_csv(data_list):
    data = pandas.DataFrame(data_list)
    data.to_csv("words_to_learn.csv", index=False)


def rigt_button_call():
    change_word(force_change=True, known_word=True)


def wrong_button_call():
    change_word(force_change=True)


window = Tk()
window.title("Flash cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_back_image = PhotoImage(file="images/card_back.png")
card_front_image = PhotoImage(file="images/card_front.png")
right_button_image = PhotoImage(file="images/right.png")
wrong_button_image = PhotoImage(file="images/wrong.png")

canvas = Canvas(
    width=800,
    height=530,
    bg=BACKGROUND_COLOR,
    highlightthickness=0
)
canvas_front_image = canvas.create_image(400,
                                         265,
                                         image=card_front_image,
                                         state="normal")
canvas_back_image = canvas.create_image(400,
                                        265,
                                        image=card_back_image,
                                        state="hidden")

canvas_text = canvas.create_text(400,
                                 265,
                                 text=f"{words[index]['Japanese']}",
                                 fill="black",
                                 font=(FONT_NAME, 35, "bold"))
canvas_lang1_text = canvas.create_text(400,
                                       180,
                                       text="Japanese",
                                       fill="black",
                                       font=(FONT_NAME, 25, "bold"),
                                       state="normal")

canvas_lang2_text = canvas.create_text(400,
                                       180,
                                       text="English",
                                       fill="black",
                                       font=(FONT_NAME, 25, "bold"),
                                       state="hidden")

canvas.grid(row=0, column=0, columnspan=2, pady=50)

right_button = Button(image=right_button_image, command=rigt_button_call)
right_button.grid(row=1, column=0)

wrong_button = Button(image=wrong_button_image, command=wrong_button_call)
wrong_button.grid(row=1, column=1)

set_after_call()

window.mainloop()
