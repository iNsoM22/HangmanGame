# Importing the needed Libraries
import random
import time
from tkinter import *
import tkinter.messagebox
from string import ascii_uppercase


def secret_word():
    """Takes no Argument and return a str:word from a text file containing different words."""
    # Opening the file in read mode.
    file1 = open("words.txt")
    # Reading and Splitting the Words with space separation.
    f = (file1.read()).split()
    # Now clossing the file.
    file1.close()
    # Using random function, returning a random word from the list of words.
    return random.choice(f).upper()


def congrats():
    """Function takes no argument and is responsible for creating the Congrulatory Screen when the user WINS."""
    global play_button, Highscore_l, Score_l, frame
    # Destroying the game window, as the player had already guessed the correct word.
    game_window.destroy()
    # Now defining an inner-function that will allow the User to play again.

    def play_again(inner_frame):
        """This Functin is created to allow the user to play again and destroy the congratulatory window to start the
        game again."""
        inner_frame.destroy()
        hangman_game()

    # Now Calculating the Player's score.
    player_score = guesses_left * len(set(word))  # --> Word is converted into a SET to remove the redundant letters.
    # Now Creating a Frame that will contain the Congratulatory Message.
    congrats_frame = Frame(root, padx=10, pady=20)
    congrat_label = Label(congrats_frame, text=f"Hurray!!!!! You have correctly guessed the word {word}", padx=110,
                          pady=20, font=["Bold Italic"])
    play_abutton = Button(congrats_frame, text="Play Again", padx=110, pady=20, relief=GROOVE,
                          command=lambda: play_again(congrats_frame))
    Score_l = Label(congrats_frame, text=f"Your Score is {player_score}", padx=120, pady=20, font=["Bold Italic"])
    Button(congrats_frame, text="Quit", padx=110, pady=20, relief=GROOVE,
           command=root.destroy).grid(row=0, column=0, columnspan=10, sticky="e")
    # This Condition is added to check if the player had acheived a new highscore for the game.
    if player_score > player_highscore:
        Highscore_l = Label(congrats_frame, text="New HIGHSCORE", padx=110, pady=20, font=["Bold Italic"])
        Highscore_l.grid(row=6, column=0, columnspan=10)

    # Now placing the Widget on the screen.
    Score_l.grid(row=4, column=0, columnspan=10)
    play_abutton.grid(row=0, column=0, columnspan=10, sticky="w")
    congrat_label.grid(row=1, column=0, columnspan=10)
    congrats_frame.grid()

    # Now Appending the Score of the Player into Score FIle.
    file1 = open("score.txt", "a")
    file1.write(name_entry.get() + "=" + str(player_score) + "\n")
    file1.close()


def highscores(operation="GAME"):
    """This Function takes no argument and is responsibe for checking the Highscore of the game."""
    global player_highscore
    # A condition that checks if the admin wants to delete the highscores.
    if operation == "reset":
        open("score.txt", "w").close()
    # Opening a text file of highscores in append mode to assure the file's existence.
    file1 = open("score.txt", "a+")
    file1.seek(0)    # --> Incase if the file already exist then it will take the pointer to the start.
    read = file1.read().split("\n")
    # This statement is added to remove the null string from the list.
    # The null string is created due to splitting through line separation.
    read.remove("")
    score_list = []   # --> This Variable:list is created to store all the scores.
    for i in read:
        if "=" in i[-2:]:  # --> This statement will check the index of the "=" sign, to slice the string accordingly.
            score_list.append(int(i[-1:]))
        else:
            score_list.append(int(i[-2:]))

    # If the file is empty then the max function will return an error.
    # So in order to tackle it, using the exception handling.
    try:
        player_highscore = max(score_list)
    except ValueError:
        player_highscore = 0
    
    file1.close()
    

def rem_words(lst):
    """Takes ONE argument that is a list containg all the remaining words and Creates Buttons for the Elements."""
    temp = list(ascii_uppercase)  # --> A list containing all the Alphabets for the reference.
    # Now creating a GUI Keyboard.

    r = c = 0  # --> These are the variables, set for displaying the buttons in rows and columns.
    # Now iterating over the reference list.
    for i in temp:
        # This Statement is added to check if the word is already guessed or not. Then its color will be changed.
        if i in lst:
            Button(rem_frame, text=i, padx=30, pady=15,  bg="#f0f8ff", command=lambda x=i: check(x)).grid(row=r, column=c)
        else:
            Button(rem_frame, text=i, padx=30, pady=15, bg="Light Pink", command=lambda x=i: check(x)).grid(row=r, column=c)

        # This statement is created to change the color of the correct guesses.
        if i in word and i in words_left:  # --> Words_left is a list, containing all the already guessed letters.
            Button(rem_frame, text=i, padx=30, pady=15, bg="Light Green",
                   command=lambda x=i: check(x)).grid(row=r, column=c)

        # After Displaying a button, changing the column variable by incrementing it.
        c += 1
        if c == 10:  # --> If the column'value reaches 10, changing the row and resetting the column's value to 0.
            r += 1
            c = 0


# Creating a Function that checks if the entered character is in the scret word or not.
def check(player_guess):
    """This Function Checks if the guessed word is in the word or not and generate warnings and decrement guesses."""
    global guesses_left, L1, guesses_bar, words_left, charac_p, warnings

    # Using For loop to replace the underscores with the characters of secret word.
    for i, char in enumerate(word):
        if char in player_guess:
            words_left[i] = char
        if "".join(words_left) == word:
            return congrats()

    # This statement checks if the letter is in the remaining letters list and also not in the secret word.
    if player_guess not in word and player_guess in rem:

        if player_guess in ('A', 'E', 'I', 'O', 'U'):  # --> If the letter is a vowel; 2 guesses will be subtracted
            charac_p += 2
            guesses_left -= 2
        else:
            charac_p += 1

        # if the warnings are available and the guessed letter was in the remaining letters list.
            # 1 guess will be subtracted.
            if warnings > 0:
                guesses_left -= 1

    # Using Exception handling to tackle the issue of removing the same letter again, and subtracting the warning.
    try:
        rem.remove(player_guess)
    except ValueError:
        warnings -= 1

        # This condition is added to show the Lost Warning Label untill all the warnings are used.
        if warnings >= 0:
            # Creating and destroying the Warning Lost Label.
            warn_lost_label = Label(game_window, text="YOU LOST A WARNING", bg="#ffffff", padx=20, pady=15,
                                    font=["Times New Roman", 15])
            warn_lost_label.grid(row=2, column=10, sticky="e")
            warn_lost_label.after(2000, warn_lost_label.destroy)

    # This condition is added to set the value of warning to 0, when warning becomes negative.
    if warnings <= 0:
        warnings = 0
        guesses_left -= 1
        charac_p += 1

    # Now Displaying the updated widgets.
    secret_word_label.config(text=" ".join(words_left))
    rem_words(rem)  # --> Calling the rem_word function to display the remaining and correct letters.

    # Now Updating the Labels using config.
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
                                               message=f"   All your guesses are used.  \n  The WORD was {word}.    \n  Do You Want to Play Again   ")
        # If the user clicks on yes, the game will restart.
        if reply == 'yes':
            game_window.destroy()
            hangman_game()
        else:
            root.destroy()


# Now Creating the Actual Logic and Interface for the game.
def hangman_game():
    """Function takes no argument and is responsible for Creating, and displaying Interface and layout of the GAME."""
    # Assigning some values to global namespace for their usage in game.
    global game_window, guesses_bar, secret_word_label, word, words_left
    global guesses_left, warnings, player_highscore, rem_frame
    global rem, photo, photo_label, charac_p, warning_label

    charac_p = 0  # --> This variable is for the picture containg the HANGMAN.
    warnings = 3  # --> This variable is for the warnings.
    guesses_left = 6  # --> This variable is for the guesses left.
    word = secret_word()  # --> This variable calls the secret_word function and stores the word returned by the function.
    words_left = [i for i in "_" * len(word)]  # --> This list is for the dashes('_') that will be displayed for the length of the word.
    # Now Clearing all the previous Frames for Creating the GAME's Layout.
    Interf_Frame.grid_forget()
    # Creating an Interface for the game.
    game_window = Frame(root, padx=30, pady=10, bg="#ffffff")  # --> A Frame that will contain all the widgets for the GAME.
    # Now Creating Labels as well as a QUIT Button for the GAME.
    secret_word_label = Label(game_window, text=" ".join(words_left), padx=120, bg="#ffffff",  pady=45, font=["Times New Roman", 50])
    Button(game_window, text="Quit", padx=30, pady=20, bg="#ffffff", command=root.destroy).grid(row=0, column=0, sticky="w")
    warning_label = Label(game_window, text=f"{warnings} warnings are left", padx=20, pady=15, bg="#ffffff",
                          font=["Times New Roman", 15])
    # Now Opening all the PHOTOS of HANGMAN, using tkinter's PhotoImage. and Also Storing them in a Variable:tuple.
    photo = tkinter.PhotoImage(file="HM\\0.png"), tkinter.PhotoImage(file="HM\\1.png"), \
        tkinter.PhotoImage(file="HM\\2.png"), tkinter.PhotoImage(file="HM\\3.png"), \
        tkinter.PhotoImage(file="HM\\4.png"), tkinter.PhotoImage(file="HM\\5.png"), \
        tkinter.PhotoImage(file="HM\\6.png"), tkinter.PhotoImage(file="HM\\7.png"), \
        tkinter.PhotoImage(file="HM\\8.png")
    # A Label that will display the photos.
    photo_label = Label(game_window, image=photo[charac_p])

    # Calling the Highscore function to get the highscore value .
    highscores()

    # Now displaying the highscore and remaining guesses on the screen.
    game_score = Label(game_window, text=f"The HighScore is {player_highscore}", bg="#ffffff", padx=60, pady=35,
                       font=["Times New Roman", 15])
    guesses_bar = Label(game_window, text=f"{guesses_left} guesses are left", bg="#ffffff",  padx=30, pady=35,
                        font=["Times New Roman", 15])

    # rem is the variable containing all the aplhabets that are yet to be selected.
    rem = list(ascii_uppercase)  # --> # From String Library, Converting the UPPERCASE ALPHABETS into a List due to its flexibility.
    # A frame created to store the Buttons for the Alphabets, this frame is created inside the Frame for the game_window.
    rem_frame = Frame(game_window, padx=10, pady=10, border=5, bg="#ffffff")
    rem_words(rem)

    # Now Displaying ALL the widgets on the screen.
    secret_word_label.grid(row=7, column=9, columnspan=10, sticky="e")
    guesses_bar.grid(row=0, column=10, sticky="e", pady=10)
    warning_label.grid(row=1, column=10, padx=2, sticky="e")
    photo_label.grid(row=2, rowspan=10, sticky="w")
    game_score.grid(row=0, column=1, columnspan=9, padx=2)
    rem_frame.grid(row=8, column=1, columnspan=10, sticky="w")
    game_window.pack()


# Now creating a Function for player's interface
def player_interface(playername):
    """Takes one Argument that is the user's inputted name, and displays the PLAY button."""
    global play_button  # --> This button is made global to use it instead of creating a new one everytime.
    # Checks if the user had entered a name or not. If not an error message will appear.
    if playername != "":
        # Now the previous widgets asking for information will be removed and a play button will appear.
        user_frame.grid_forget()
        play_button = Button(Interf_Frame, text="Play", padx=40, pady=25, command=hangman_game)
        play_button.grid(row=8, column=0, columnspan=10)
    else:
        tkinter.messagebox.showinfo(title="Login Error", message="Please Enter a valid USERNAME.")


# Now making a function that adds the inputted words into the file
def word_add_function(entry, frame):
    """This function takes two argument which are FRAME's name and entry wigdet;the words entered by the admin in entry
    widget. This Function writes the words in the file."""

    # This will get the words from the entry box and creates a list of them.
    inputted_word = entry.get().split(",")

    # Now opening the file and converting all the existing words into a list.
    file1 = open("words.txt", "r+")
    f = file1.read()
    f = f.split()

    # Now checking if the yet to be added word is already in the file-list or not. Only those words which are not in
    # the file-list are addded.
    for i in inputted_word:
        if i not in f:  # --> Writing the word in the file if it doesn't exist in the file already.
            file1.write(" "+i)

    # Now closing the file and showing a message.
    file1.close()
    Label(frame, text="The Words are added Successfully").grid(row=3, column=0, columnspan=10)
    frame.after(5000, frame.destroy)  # This will destroy the Frame after some specific time.
    # Now Re-Activating the Buttons after some time.
    time.sleep(2)
    addwords_button["state"] = NORMAL
    score_reset_button["state"] = NORMAL


# Now defining a function that will append the new word in the word's file
def add_words():
    """Function takes NO argument and creates an entry widget for the user to add more words."""
    global admin_main_scr_frame, OK_button
    # Disabling the Buttons to Lock the admin from the re-clicking the same button.
    addwords_button["state"] = DISABLED
    score_reset_button["state"] = DISABLED
    # Now Creating the Layout for the Word addition screen.
    admin_main_scr_frame = Frame(root, padx=20, pady=20, bg="Light pink", highlightbackground="Light Green",
                                 highlightthickness=5, highlightcolor="Blue")
    admin_entry = Entry(admin_main_scr_frame, width=50)
    admin_main_scr_frame.grid(row=6, column=0, columnspan=10)
    OK_button = Button(admin_main_scr_frame, text="OK", relief=GROOVE, padx=10, pady=5,
                       command=lambda: word_add_function(admin_entry, admin_main_scr_frame))
    # Now displaying the Widgets on the screen.
    admin_entry.grid(row=1, column=0, columnspan=10)
    OK_button.grid(row=2, column=0, columnspan=10)


# Now defining a Function that calls the Main Screen of the Admin Menu
def admin_menu():
    """Function takes and return no argument and Creates a Layout for the Administrator mode."""
    global admin_root, addwords_button, score_reset_button
    # This statement will check if the admin access will be authorized or not.
    if name_entry.get() == "admin" and pass_entry.get() == "12345":
        # Removing previous frames to display the new ones.
        user_frame.destroy()
        Interf_Frame.destroy()
        admin_label = Label(root, text="WELCOME TO THE ADMIN INTERFACE", bg="#aaddbb", font=["Italic", 20], padx=20, pady=10)
        admin_frame = Frame(root, padx=20, pady=20)
        addwords_button = Button(root, text="Add More Words",bg="#deedee", command=add_words, font=["Italic", 20], padx=20, pady=10)
        score_reset_button = Button(root, text="Reset the Highscores", bg="#deedee", command=lambda: highscores('reset'),
                                    font=["Italic", 20], padx=20, pady=10)
        # Now displaying the widgets on the screen.
        admin_label.grid(row=0, column=0, columnspan=10)
        admin_frame.grid(row=1, column=0, columnspan=10)
        addwords_button.grid(row=2, column=0, columnspan=10)
        score_reset_button.grid(row=3, column=0, columnspan=10)
    else:
        # If the user inputs wrong USERNAME/PASSWORD, error message will appear.
        tkinter.messagebox.showinfo(title="Login Error", message="Please Enter a Valid Username/Password")


# Defining a function that enables the user to change its interface.
def switch():
    """This FUnction takes and returns no argument, and is used to destroy the Information-Login layout."""
    # These will destroy the existing labels to create the new ones.
    user_frame.destroy()
    # This will change the status of continue button.
    continue_button["state"] = NORMAL


# Defining a User Interface for the Player
def user_info(value):
    """Function takes one argument:int and is responsible for displaying the Information asking widgets."""
    # Setting Local variables as the global ones.
    global user_frame, name_entry, pass_label, pass_entry, name_label, Back_button, Login_button
    continue_button["state"] = DISABLED

    # Creating a new frame for the information entering field.
    user_frame = Frame(root, padx=10, pady=5, border=5, borderwidth=15, bg="LightGreen")
    # Now creating some basic Labels and buttons.
    name_label = Label(user_frame, font=["Bold"], bg='#f1c27d')
    name_entry = Entry(user_frame, width=30)
    Back_button = Button(user_frame, text="Back", padx=15, pady=10, relief=GROOVE, command=switch)
    Login_button = Button(user_frame, text="Login", padx=15, pady=10, relief=GROOVE)

    # Checking, the user's chosen interface, and configuring the Labels and Button's command to the chosen interface.
    if value == 1:
        name_label.config(text="Player's Interface")
        Login_button.config(command=lambda: player_interface(name_entry.get()))
    else:
        name_label.config(text="Admin's Interface")
        Login_button.config(command=admin_menu)
        pass_label = Label(user_frame, text="Password", font=["Bold"], bg='#f1c27d')
        pass_entry = Entry(user_frame, show="*", width=30)
        pass_label.grid(row=9, column=0)
        pass_entry.grid(row=10, column=0)

    # Now Displaying the Widgets on the screen.
    name_label.grid(row=7, column=0)
    name_entry.grid(row=8, column=0)
    Back_button.grid(row=11, column=0, sticky="e", pady=2)
    Login_button.grid(row=11, column=0, sticky="w", pady=2)
    user_frame.grid()


# This is the Main Starting Point for the Program.
# Now Creating an Interface for Player and Administrator
root = Tk()  # --> This will create a window.
root.title("Hangman Game") # --> Setting the name of the window to HANGMAN GAME.
icon_photo = tkinter.PhotoImage(file="HM/index.png")
root.iconphoto(FALSE, icon_photo)
# Creating a base Frame, which displays the Player or Admin Choice.
Interf_Frame = Frame(root, padx=20, pady=20, bg="Light pink", highlightbackground="Light Green", highlightthickness=5,
                     highlightcolor="Blue")
Label(Interf_Frame, text="Welcome to the Hangman Game", padx=10, pady=20, font=["Italic", 25]).grid(row=0, column=0
                                                                                                    , padx=50)
# Creating a Variable that can store the user's choice of interface
access = IntVar()
access.set(1)
INTERFchoice_label = Label(Interf_Frame, text="Please Choose an Interface", padx=20, pady=5, font=["Bold Italic", 10])
Radiobutton(Interf_Frame, text="Player Access", variable=access, value=1, background="Light Blue", padx=30,
            pady=20).grid(row=3, column=0)
Radiobutton(Interf_Frame, text="Administrator Access", variable=access, value=0, background="#a52a2a",
            padx=30, pady=20).grid(row=4, column=0)

# Now a button is created that can call the concerned function on the basis of stored value in the variable.
continue_button = Button(Interf_Frame, text="Continue", padx=10, pady=7, relief=GROOVE,
                         command=lambda: user_info(access.get()))

# Now displaying the widgets on the screen.
root.configure(bg='#f1c27d')
INTERFchoice_label.grid(row=1, column=0)
Interf_Frame.grid(row=3, column=0)
continue_button.grid(row=5, column=0)

root.mainloop()
