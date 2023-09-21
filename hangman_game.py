from tkinter import *
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import random, os

class App(ctk.CTk):
    chances = 7
    chosenWord = ""
    guessedLetters = []
    usersGuesses = ""
    score = 0
    
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        self.title("hangman")
        self.geometry("300x500")
        
        self.labelScore = ctk.CTkLabel(self, text=f"SCORE {self.score}")
        self.labelScore.grid(row = 0, column = 1, padx=(5, 10), pady=10)

        self.label = ctk.CTkLabel(self, text="Answer: ")
        self.label.grid(row = 1, column = 0, padx=(5, 10), pady=10)

        self.EntryAnswer = ctk.CTkEntry(self)
        self.EntryAnswer.grid(row = 1, column = 1, padx=(5, 10), pady=10)

        self.button = ctk.CTkButton(self, text ="Enter", width = 50, command = self.main)
        self.button.grid(row = 1, column = 2, padx=(5, 10), pady=10)
        
        self.labelGuessWord = ctk.CTkLabel(self, text="WORD GOING TO BE HERE")
        self.labelGuessWord.grid(row = 2, column = 1, padx=(5, 10), pady=10)
        
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        """ image = ctk.CTkImage(light_image=Image.open(f'{self.dir_path}\\health_bar\\full_health_bar.jpg'),
                                  dark_image=Image.open(f'{self.dir_path}\\health_bar\\full_health_bar.jpg'),
                                  size=(30, 30))
        self.health = ctk.CTkLabel(self, image=image)
        self.health.grid(row = 3, column = 0) """
        
        """ self.iconphoto(False, f'logo') """
        
        self.randomWord()
        self.display()
        print(self.chosenWord)
        
    def main(self):
        if self.button.cget("text") == 'Reset':
            self.resetGame()
            
        else:
            userAnswer = (self.EntryAnswer.get()).lower()
            self.EntryAnswer.delete(0, END)
            
            try:
                if userAnswer.isalpha():
                    self.logic(userAnswer)
                else:
                    raise Exception("Type a word or letter")
            except Exception:
                CTkMessagebox(message = "Type letters or a word",
                            icon = "warning", option_1 = "Ok")
            
    def logic(self, userAnswer):
        if len(userAnswer) > 1:
            if userAnswer == self.chosenWord.lower():
                for i in range(len(self.chosenWord)):
                    self.guessedLetters[i] = self.chosenWord[i]
                self.display()
                self.checkWin(True)
            else:
                self.chances -= 1
        else:
            letterGuessed = 0
            
            for i in range(len(self.chosenWord)):
                if self.guessedLetters[i].lower() == userAnswer or self.usersGuesses.find(userAnswer) >= 0:
                    print('already guessed')
                    return
                               
                elif self.chosenWord[i].lower() == userAnswer:
                    self.guessedLetters[i] = self.chosenWord[i]
                    letterGuessed += 1
                    
            if letterGuessed != 0:
                print('found letter')
                self.display()
            else:
                print('letter not found')
                self.usersGuesses += userAnswer
                self.chances -= 1
        
        if self.chances == 0:
            self.checkWin(False)
    
    def checkWin(self, isWin):
        if isWin is False:
            print('You lost')
            self.score = 0
        else:
            print('you guessed the word correctly')
            self.score += 1
            
        self.button.configure(text = 'Reset')
        self.labelScore.configure(text=f"SCORE {self.score}")

    def display(self):
        displayText = ""
        
        for letter in self.guessedLetters:
            displayText += letter + " "
        
        self.labelGuessWord.configure(text = displayText)
            
    def randomWord(self):
        numberOfWords = 0
        
        try:
            file = open(f"{self.dir_path}\\word_list.txt", 'r')
            with file as fp:
                numberOfWords = len(fp.readlines())
            
            file = open(f"{self.dir_path}\\word_list.txt", 'r')    
            lines = file.readlines()
            
            file.close()
        
            self.chosenWord = lines[random.randint(0, numberOfWords)].replace('\n', '')
            
            for letter in self.chosenWord:
                if letter.isalpha():
                    self.guessedLetters.append('_')
                else:
                    self.guessedLetters.append(letter)
        except:
            CTkMessagebox(title="Error", message = "File doesn't exist",
                          icon = "cancel", option_1 = "Ok")

    def resetGame(self):
        self.usersGuesses = ""
        self.guessedLetters.clear()        
        self.randomWord()
        self.display()
        self.button.configure(text = 'Enter')
        
      
if __name__ == '__main__':
    app = App()
    app.mainloop()