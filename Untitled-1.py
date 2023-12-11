from tkinter import *
import random

Hangman = ['''
   +---+
       |
       |
       |
      ===''', '''
    +---+
    O   |
        |
        |
       ===''', '''
    +---+
    O   |
    |   |
        |
       ===''', '''
    +---+
    O   |
   /|   |
        |
       ===''', '''
    +---+
    O   |
   /|\  |
        |
       ===''', '''
    +---+
    O   |
   /|\  |
   /    |
       ===''', '''
    +---+
    O   |
   /|\  |
   / \  |
       ===''']

list = ["provide","illustrious","encouraging","fantastic","squealing","unbecoming","nutritious","unwieldy","disapprove","lamentable","astonishing","british","quizzical"]

randomWord = random.choice(list)
print(randomWord)

hiddenWord = ""
hiddenText = ""

points = 0

form = Tk()
form.title("Game GUI")
form.geometry('650x450')

draw = Canvas(form, width=650, height=450, bg='ivory')
draw.pack()
draw.create_text(325,20,text="Live Score: "+ str(points))

for wordToGuess in randomWord:              
    if wordToGuess in hiddenWord:        
        draw.create_text(325,420,text=wordToGuess)
    else:
        hiddenText += " _ "
        hide = draw.create_text(325,200,text=hiddenText)

def getAlpha():
    alpha = entry.get()
    return alpha

def main():
    global hiddenWord
    
    if len(getAlpha()) > 1:      
        hiddenWord += getAlpha()
    else: 
        draw.itemconfig(hide,text=hiddenText.replace(" _ ",getAlpha()))
        hiddenText.replace(" _ ", getAlpha())

if __name__ == '__main__':

    entry = Entry(form)
    draw.create_window(325,270,window=entry)

    confirmButton = Button(text='Confirmer ',command=main)
    draw.create_window(325,300,window=confirmButton)
        
    print(hiddenText)

    form.mainloop()