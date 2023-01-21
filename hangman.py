# Importing the needed Libraries
import random
from tkinter import *
import tkinter.messagebox
from string import ascii_uppercase



def secret_word():
    '''Takes no Argument and return a str:word from a word file containing different words.'''
    file1 = open("words.txt")
    f = (file1.read()).split()
    file1.close()
    return random.choice(f).upper()


def congrats():
    global play_button, Highscore_l, Score_l, frame
    game_window.destroy()

    def play_again(frame):
        frame.destroy()
        Hangman_game()

    player_score = guesses_left * len(set(word))
    congrats_frame = Frame(root, padx=10, pady=20)
    congrat_label = Label(congrats_frame, text=f"Hurray!!!!! You have correctly guessed the word {word}", padx=110, pady=20,
                          font=["Bold Italic"])

    congrat_label.grid(row=1, column=0, columnspan=10)
    play_abutton = Button(congrats_frame, text="Play Again", padx=110, pady=20, relief=GROOVE, command=lambda : play_again(congrats_frame))
    play_abutton.grid(row=0, column=0, columnspan=10)
    if player_score > player_highscore:
        Highscore_l = Label(congrats_frame, text="New HIGHSCORE", padx=110, pady=20, font=["Bold Italic"])
        Highscore_l.grid(row=6, column=0, columnspan=10)
    Score_l = Label(congrats_frame, text=f"Your Score is {player_score}", padx=120, pady=20, font=["Bold Italic"])
    Score_l.grid(row=4, column=0, columnspan=10)
    congrats_frame.grid()
    file1 = open("score.txt", "a")
    file1.write(name_entry.get() + "=" + str(player_score) + "\n")
    file1.close()


def highscores(operation="GAME"):
    global player_highscore
    # A condition that checks if the admin wants to delete the highscores.
    if operation == "reset":
        open("score.txt", "w").close()
    
    # Opening a csv file of highscores in append mode to assure the file's existence.
    file1 = open("score.txt", "a+")
    file1.seek(0)    # --> Incase if the file already exist then it will take the pointer to the start.
    read = file1.read().split()
    print(read)
    score_list = []
    for i in read:
        if "=" in i[-2:]:
            score_list.append(int(i[-1:]))
        else:
            score_list.append(int(i[-2:]))
    score_list = [int(i) for i in score_list]

    # If the file is empty then the max function will return an error.
    # So in order to tackle it, using the exception handling.
    try:
        player_highscore = max(score_list)
    except ValueError:
        player_highscore = 0
    
    file1.close()
    


def rem_words(lst):
    '''Takes a list as argument and Creates Buttons for the Elements'''
    temp = list(ascii_uppercase)
    # Now creating a GUI Keyboard.
    r = c = 0
    for i in temp:
    # This statment is created to change the color of the correct guesses. 
        if i in word and i in words_left:
            Button(rem_frame, text=i, padx=30, pady=15, bg="Light Green",
                   command=lambda x=i: check(x)).grid(row=r, column=c)
        else:
            Button(rem_frame, text=i, padx=30, pady=15, command=lambda x=i: check(x)).grid(row=r, column=c)
        c += 1
        if c == 10:
            r += 1
            c = 0

# Creating a Function that checks if the entered character is in the scret word or not.
def check(player_guess):
    '''This Function Checks if the guessed word is in the word or not and generate warnings and decreement guesses.'''
    global guesses_left, L1, guesses_bar, words_left, charac_p, warnings, guesses_made

    guesses_made = [] # --> This list is created to store the already guessed letters.
    # Using For loop to replace the underscores with the characters of secret word.
    for i, char in enumerate(word):
        if char in player_guess:
            words_left[i] = char
        if "".join(words_left) == word:
            return congrats()

    # This statement checks if the letter is in the remaining letters list and also not in the secret word.
    if player_guess not in word and player_guess in rem:

        if player_guess in ('A', 'E', 'I', 'O', 'U'): # --> If the letter is a vowel; 2 guesses will be subtracted
            charac_p += 2
            guesses_left -= 2
        else:
            charac_p += 1
            if warnings > 0: # --> This statement is added to subtract the guesses after all warnings are used.
                guesses_left -= 1

    # Using Exception handling to tackle the issue of removing the same letter again, and subtracting the warning.
    try:
        rem.remove(player_guess)
    except ValueError:
        warnings -= 1

    # This condition is added to set the value of warning to 0, when warning becomes negative.
    if warnings <= 0:
        warnings = 0
        guesses_left -= 1
        charac_p += 1

    # Now Displaying the updated widgets.
    game_L1.config(text="  ".join(words_left))
    rem_words(rem)
    guesses_made.append(player_guess)
    photo_label.config(image=photo[charac_p])
    warning_label.config(text=f"{warnings} warnings are left")
    guesses_bar.config(text=f"{guesses_left} guesses are left")

    # Now adding a condition that will appear if the user runs out of his guesses.
    if guesses_left <= 0:
        guesses_left = 0
        guesses_bar.config(text=f"{guesses_left} guesses are left")
        photo_label.config(image=photo[charac_p + 1])
        # A popup will appear that asks the user, if He wants to play again or quit.
        reply = tkinter.messagebox.askquestion(title="GAME OVER",
                                               message="All your guesses are used.\nDo You Want to Play Again")
        # If the user clicks on yes, the game will restart.
        if reply == 'yes':
            game_window.destroy()
            Hangman_game()
        else:
            root.destroy()


# Now Creating the Actual Logic and Interface for the game.
def Hangman_game():
    # Assigning some values for their usage in game.
    global game_window, guesses_bar, game_L1, word, words_left
    global guesses_left, warnings, player_highscore, rem_frame
    global rem, photo, photo_label, charac_p, warning_label
    charac_p = 0
    warnings = 3
    guesses_left = 6
    word = secret_word()
    words_left = [i for i in "_" * len(word)]
    print(word)
    main_scr_frame.grid_forget()
    play_button.grid_forget()
    # Creating an Interface for the game.
    game_window = Frame(root, padx=50, pady=50)
    game_L1 = Label(game_window, text="  ".join(words_left), padx=120, pady=45, font=["Times New Roman", 50])
    Button(game_window, text="Quit", padx=30, pady=20, command=root.destroy).grid(row=0, column=0, sticky="w", pady=10)
    warning_label = Label(game_window, text=f"{warnings} warnings are left", padx=20, pady=15,
                          font=["Times New Roman", 15])
    photo = tkinter.PhotoImage(file="HM\\0.png"), tkinter.PhotoImage(file="HM\\1.png"), \
        tkinter.PhotoImage(file="HM\\2.png"), tkinter.PhotoImage(file="HM\\3.png"), \
        tkinter.PhotoImage(file="HM\\4.png"), tkinter.PhotoImage(file="HM\\5.png"), \
        tkinter.PhotoImage(file="HM\\6.png"), tkinter.PhotoImage(file="HM\\7.png"), \
        tkinter.PhotoImage(file="HM\\8.png")
    photo_label = Label(game_window, image=photo[charac_p])
    photo_label.grid(row=2, rowspan=10, sticky="w")

    # Calling the Highscore function to get the highscore value .
    highscores()

    # Now displaying the highscore and remaining guesses on the screen.
    game_score = Label(game_window, text=f"The HighScore is {player_highscore}", padx=60, pady=35,
                       font=["Times New Roman", 15])
    guesses_bar = Label(game_window, text=f"{guesses_left} guesses are left", padx=30, pady=35,
                        font=["Times New Roman", 15])

    # This is the logic to display all the characters that are left to be guessed
    rem = list(ascii_uppercase)
    rem_frame = Frame(game_window, padx=10, pady=10, border=5)
    rem_frame.grid(row=15, column=0, columnspan=10)
    rem_words(rem)

    game_L1.grid(row=9, column=9, columnspan=10, sticky="SW")
    guesses_bar.grid(row=0, column=10, sticky="e", pady=10)
    warning_label.grid(row=1, column=10, padx=2, sticky="e")
    game_score.grid(row=0, column=1, columnspan=9, padx=2)
    game_window.pack()


# Now creating a Function for player's interface
def player_interface(playername):
    '''Takes one Argument that is the user's inputted name, and displays the PLAY button.'''
    global play_button
    # Checks if the user had entered a name or not. If not an error message will appear.
    if playername != "":

        # Now all the previous widgets will be removed and a play button will appear.
        user_frame.grid_forget()
        Interf_Frame.grid_forget()
        play_button = Button(root, text="Play", padx=40, pady=25, command=Hangman_game)
        play_button.grid(row=4, column=0, columnspan=10)
    else:
        tkinter.messagebox.showinfo(title="Login Error", message="Please Enter a valid USERNAME.")


# Now making a function that adds the inputted words into the file
def word_add_function(entry):
    '''This function takes one argument which are the words entered by the admin in entry widget.
    This Function writes the words in the file.'''

    # This will get the words from the entry box and creates a list of them.
    inputted_word = entry.get().split(",")

    # Now opening the file and converting all the existing words into a list.
    file1 = open("words.txt", "r+")
    f = file1.read()
    f = f.split()

    # Now checking if the yet to be added word is already in the file-list or not. Only those words which are not in
    # the file-list are addded.
    for i in inputted_word:
        if i in f:
            continue
        else:
            file1.write(i + " ")

    # Now closing the file and showing a message.
    file1.close()
    Label(admin_main_scr_frame, text="The Words are added Successfully").grid(row=3, column=0, columnspan=10)
    admin_main_scr_frame.after(5000, admin_main_scr_frame.destroy)
    # Now Re-Activating the Buttons.
    addwords_button["state"] = NORMAL
    score_reset_button["state"] = NORMAL
    entry.destroy()
    OK_button.destroy()


# Now defining a function that will append the new word in the word's file
def add_words():
    '''Function takes NO argument and creates an entry widget for the user to add more words.'''
    global admin_main_scr_frame, OK_button
    # Disabling the Buttons to Lock the admin from the re-clicking the same button.
    addwords_button["state"] = DISABLED
    score_reset_button["state"] = DISABLED
    # Now Creating the Layout for the WOrd addition screen.
    admin_main_scr_frame = Frame(root, padx=20, pady=20, bg="Light pink", highlightbackground="Light Green",
                         highlightthickness=5, highlightcolor="Blue")
    admin_entry = Entry(admin_main_scr_frame, width=50)
    admin_main_scr_frame.grid(row=6, column=0, columnspan=10)
    OK_button = Button(admin_main_scr_frame, text="OK", relief=GROOVE, padx=10, pady=5,
                       command = lambda : word_add_function(admin_entry))
    admin_entry.grid(row=1, column=0, columnspan=10)
    OK_button.grid(row=2, column=0, columnspan=10)


# Now defining a Function that calls the Main Screen of the Admin Menu
def admin_menu():
    '''Function takes and return no argument and Creates a Layout for the Administrator mode.'''
    global admin_root, addwords_button, score_reset_button
    # This statement will check if the admin access will be authorized or not.
    if name_entry.get() == "admin" and pass_entry.get() == "12345":
        user_frame.grid_forget()
        main_scr_frame.grid_forget()
        Interf_Frame.grid_forget()
        admin_label = Label(root, text="WELCOME TO THE ADMIN INTERFACE", font=["Italic", 20], padx=20, pady=10)
        admin_frame = Frame(root, padx=20, pady=20, bg="Light pink", highlightbackground="Light Green",
                            highlightcolor="Blue")
        addwords_button = Button(root, text="Add More Words", command=add_words, font=["Italic", 20], padx=20, pady=10)
        score_reset_button = Button(root, text="Reset the Highscores", command=lambda: highscores('reset'), font=["Italic", 20],
                                    padx=20, pady=10)
        admin_label.grid(row=0, column=0, columnspan=10)
        admin_frame.grid(row=1, column=0, columnspan=10)
        addwords_button.grid(row=2, column=0, columnspan=10)
        score_reset_button.grid(row=3, column=0, columnspan=10)
    else:
        # If the user inputs wrong USERNAME/PASSWORD, error message will appear.
        tkinter.messagebox.showinfo(title="Login Error", message="Please Enter a Valid Username/Password")


# Defining a function that enables the user to change its interface.
def switch():
    # These will destroy the existing labels to create the new ones.
    user_frame.destroy()
    # This will change the status of continue button.
    continue_button["state"] = NORMAL


# Defining a User Interface for the Player
def user_info(value):
    # Setting Local variables as the global ones.
    global user_frame, name_entry, pass_label, pass_entry, name_label, Back_button, Login_button
    continue_button["state"] = DISABLED

    # Creating a new frame for the information entering field.
    user_frame = Frame(root, padx=10, pady=5, border=5, borderwidth=15, bg="LightGreen")
    user_frame.grid()

    name_label = Label(user_frame, font=["Bold"], bg='#f1c27d')
    name_entry = Entry(user_frame, width=30)

    Back_button = Button(user_frame, text="Back", padx=15, pady=10, relief=GROOVE, command=switch)
    Login_button = Button(user_frame, text="Login", padx=15, pady=10, relief=GROOVE)

    # Checking, the user's chosen interface.
    if value == 1:
        name_label.config(text="Player's Interface")
        Login_button.config(command=lambda: player_interface(name_entry.get()))
    else:
        name_label.config(text="Admin's Interface")
        pass_label = Label(user_frame, text="Password", font=["Bold"], bg='#f1c27d')
        pass_entry = Entry(user_frame, show="*", width=30)
        pass_label.grid(row=9, column=0)
        pass_entry.grid(row=10, column=0)
        Login_button.config(command=admin_menu)

    name_label.grid(row=7, column=0)
    name_entry.grid(row=8, column=0)
    Back_button.grid(row=11, column=0, sticky="e")
    Login_button.grid(row=11, column=0, sticky="w")


# Now Creating a Interface for Player and Administrator
root = Tk()
root.title("Hangman Game")
main_scr_frame = Frame(root, padx=20, pady=20)
MyLabel_General = Label(main_scr_frame, text="Welcome to the Hangman Game", padx=10, pady=20, font=["Italic", 25])

# Creating a base Frame, which displays the Player or Admin Choice.
Interf_Frame = Frame(root, padx=20, pady=20, bg="Light pink", highlightbackground="Light Green", highlightthickness=5,
                     highlightcolor="Blue")


# Creating a Variable that can store the user's choice of interface

access = IntVar()
access.set(1)
INTERFACEchoice_label = Label(Interf_Frame, text="Please Choose an Interface", padx=20, pady=5, font=["Bold Italic", 10])
Radiobutton(Interf_Frame, text="Player Access", variable=access, value=1, background="Light Blue", padx=30,
            pady=20).grid(row=2, column=1)
Radiobutton(Interf_Frame, text="Administrator Access", variable=access, value=0, background="#a52a2a",
            padx=30, pady=20).grid(row=3, column=1)
continue_button = Button(Interf_Frame, text="Continue", padx=10, pady=7, relief=GROOVE, command=lambda: user_info(access.get()))

# Now a button is created that can call the concerned function on the basis of stored value in the variable.
MyLabel_General.grid(row=1, column=0, padx=50)
root.configure(bg='#f1c27d')

main_scr_frame.grid(row=0, column=0)
INTERFACEchoice_label.grid(row=0, column=1)
Interf_Frame.grid(row=3, column=0)
continue_button.grid(row=4, column=1)

root.mainloop()
