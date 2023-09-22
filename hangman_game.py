from tkinter import *
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
from datetime import datetime
import random, os

class Menu(ctk.CTk):
    difficulty = ""
    
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")
        
        self.title("Menu Hangman")
        self.geometry("300x300")
        
        self.easyButton = ctk.CTkButton(self, text ="Easy", command = self.easy)
        self.easyButton.grid(row = 0, column = 2, padx=(80, 10), pady=(80, 10))
        
        self.mediumButton = ctk.CTkButton(self, text ="Medium", command = self.medium)
        self.mediumButton.grid(row = 1, column = 2, padx=(80, 10), pady=10)
        
        self.hardButton = ctk.CTkButton(self, text ="Hard", command = self.hard)
        self.hardButton.grid(row = 2, column = 2, padx=(80, 10), pady=10)
        
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.after(201, lambda: self.iconbitmap(f'{self.dir_path}\\logo.ico'))
    
    def easy(self):
        self.difficulty = 'easy'
        self.destroy()

    def medium(self):
        self.difficulty = 'medium'
        self.destroy()

    def hard(self):
        self.difficulty = 'hard'
        self.destroy()

class App(ctk.CTk):
    chances = 7
    chosenWord = ""
    guessedLetters = []
    usersGuesses = ""
    score = 0
    difficulty = ""
    
    def __init__(self, difficulty):
        super().__init__()

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        self.title("hangman")
        self.geometry("280x500")
        
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
        image = ctk.CTkImage(dark_image=Image.open(f"{self.dir_path}\\health_bar\\{self.chances}_health_bar.png"),
                             size=(228 - 57 - 57, 18))
        self.health = ctk.CTkLabel(self, image=image, text="")
        self.health.grid(row = 3, column = 1, padx=(5, 10), pady=10)
        
        self.quitButton = ctk.CTkButton(self, text='Close', command = self.closeApp)
        self.quitButton.grid(row = 4, column = 1, padx=(5, 10), pady=10)
        
        self.after(201, lambda: self.iconbitmap(f'{self.dir_path}\\logo.ico'))
        self.difficulty = difficulty

        self.randomWord()
        self.display()
        
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
                    raise Exception
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
            
            if sum([1 for i in range(len(self.chosenWord)) if self.guessedLetters[i] == self.chosenWord[i]]) == len(self.chosenWord):
                self.display()
                self.checkWin(True)
        
        self.healthBar(self.chances)
        if self.chances == 0:
            self.checkWin(False)
    
    def checkWin(self, isWin):
        displayText = ""
        
        if isWin is False:
            print('You lost')
            displayText += ''.join([letter + ' ' for letter in self.chosenWord])
            self.labelGuessWord.configure(text = displayText)
            
            if self.score > self.getFormatedText('best_score'):
                self.setBestScore(self.score)
            
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
            file = open(f"{self.dir_path}\\difficulty\\word_list\\{self.difficulty}_word_list.txt", 'r')
            with file as fp:
                numberOfWords = len(fp.readlines())
            
            file = open(f"{self.dir_path}\\difficulty\\word_list\\{self.difficulty}_word_list.txt", 'r')    
            lines = file.readlines()
            
            file.close()
        
            self.chosenWord = lines[random.randint(0, numberOfWords)].replace('\n', '')
            print(self.chosenWord)
            
            for letter in self.chosenWord:
                if letter.isalpha():
                    self.guessedLetters.append('_')
                else:
                    self.guessedLetters.append(letter)
        except:
            CTkMessagebox(title="Error", message = "File doesn't exist",
                          icon = "cancel", option_1 = "Ok")

    def resetGame(self):
        if self.chances == 0:
            self.chances = 7
            
        self.usersGuesses = ""
        self.guessedLetters.clear()        
        self.randomWord()
        self.display()
        self.healthBar(self.chances)
        self.button.configure(text = 'Enter')
     
    def healthBar(self, chances):
        image = ctk.CTkImage(dark_image=Image.open(f"{self.dir_path}\\health_bar\\{chances}_health_bar.png"),
                        size=(228 - 57 - 57, 18))
        self.health.configure(image=image)
        
    def setBestScore(self, score):
        currentDateTime = str(datetime.now())
        currentDateTime = f"{currentDateTime[8:10]}-{currentDateTime[5:7]}-{currentDateTime[0:4]} {currentDateTime[11:13]}:{currentDateTime[14:16]}:{currentDateTime[17:19]}"
        
        try:
            file = open(f"{self.dir_path}\\difficulty\\score\\{self.difficulty}_score_card.txt", 'w')
            
            file.write(f"{score}\n{currentDateTime}")
            file.close()
        except IOError as e:
            print(e)
    
    def getFormatedText(self, format):
        text = ""

        try:
            file = open(f"{self.dir_path}\\difficulty\\score\\{self.difficulty}_score_card.txt", 'r')
            with file as fp:
                text = (fp.readlines())
            
            match format:
                case 'best_score':
                    return int(text[0].replace('\n', ''))
                case 'date':
                    return text[1][0:10]
                case 'time':
                    return text[1][11:19]

        except IOError as e:
            print(e)

    def closeApp(self):
        self.checkWin(False)
        self.destroy()
    
if __name__ == '__main__':
    menu = Menu()
    menu.mainloop()
    
    difficulty = menu.difficulty
    
    app = App(difficulty)
    app.mainloop()