from tkinter import *
from tkinter import messagebox


class Players:
    # This was my first ever class btw xD
    p1 = ''
    p2 = ''

    def __init__(self, username):
        if Players.p1 == '':
            Players.p1 = username
        elif Players.p2 == '':
            Players.p2 = username


def __read_file(filename):
    line = filename.readline()
    return line.rstrip('\n').split(',') if line else ['', '']


def __user_validation(username, password, username_only):
    """
    opens users.csv and checks if the received info matches the info in the file
    (if username_only is True checks only the username else, checks the whole info),
    returns a bool.
    """
    with open("used_files/users.csv") as users_file:
        read_username, read_password = __read_file(users_file)
        while read_username and username != read_username:
            read_username, read_password = __read_file(users_file)

    return (username == read_username if username_only
            else username == read_username and password == read_password and Players.p1 != username)


def __emergentwindow(username, password):
    """
    if user_validation returns True invokes successwindow else invokes errorwindow.
    """
    if __user_validation(username, password, False) and username != Players.p1:
        Players(username)
        __successwindow()
    elif username == Players.p1:
        __errorwindow('already logged')
    else:
        __errorwindow('wrong info')


def __successwindow():
    if Players.p2 == '':
        messagebox.showinfo('Success', 'Player 1 successfully logged!\n(Player 2, please log-in)')
    else:
        messagebox.showinfo('Success', 'Player 2 successfully logged!\n'
                                       '(Close the log-in window to start playing!)')


def __errorwindow(msg_type):
    possible_cases = {'already logged': 'Error, Username is already logged.',
                      'wrong info': 'Error, Username or password is not correct.'}
    messagebox.showerror('Error', possible_cases[msg_type])


def __apply_login(username, password, username_entry, password_entry):
    """
    is invoked by the login button, and invokes emergentwindow.
    also cleans the username and password entries.
    """
    __emergentwindow(username, password)
    username_entry.delete(0, END)
    password_entry.delete(0, END)


def __apply_signin(username, password, password2, RootSignup, file_name):
    """
    is invoked by the signup button, invokes register_new_user(), and closes the signup window.
    """
    __register_new_user(username, password, password2, file_name)
    RootSignup.destroy()


def __emergentwindow_signup(msg_type, username, msg):
    possible_msg = {'invalid_username': f'Username {username} is invalid. '
                                        'It should have between 4 and 15 chars and be formed '
                                        'solely by letters, numbers, and _',
                    'diff_passwords': 'Both passwords should be the same',
                    'invalid_passwords': 'Invalid password. '
                                      'Password should have between 8 and 15 chars, '
                                      'and be formed by at least 1 lowercase 1 uppercase and _ or -',
                    'user_created': f'User {username} has been successfully created.',
                    'already_registered': f'User {username} is already registered'}
    if msg_type == 'error':
        messagebox.showerror('error', possible_msg[msg])
    elif msg_type == 'info':
        messagebox.showinfo('success', possible_msg[msg])
    elif msg_type == 'warning':
        messagebox.showwarning('warning', possible_msg[msg])


def __register_new_user(username, password, password2, file_name):
    """
    saves new user in users.csv, in case of error invokes emergentwindow_signup
    giving it the corresponding info.
    """
    if not __validate_username(username):
        __emergentwindow_signup('error', username, 'invalid_username')
    elif password != password2:
        __emergentwindow_signup('error', username, 'diff_passwords')
    elif not __validate_password(password):
        __emergentwindow_signup('error', username, 'invalid_passwords')
    elif not __user_validation(username, password, True):
        with open(file_name, 'a', encoding="utf8") as users_file:
            users_file.write(f'{username},{password}\n')
        __emergentwindow_signup('info', username, 'user_created')
    else:
        __emergentwindow_signup('warning', username, 'already_registered')


def __validate_username(username):
    """
    validates that the username has an adequate length and that is formed only by
    letters, numbers, and _ .
    """
    valid_name = False
    min_length = 4
    max_length = 15
    only_letters = username.replace('_', '')
    if ((min_length <= len(username) <= max_length) and
            (only_letters.isalnum() and not only_letters.isalpha() and not
             only_letters.isnumeric()) and '_' in username):
        valid_name = True

    return valid_name


def __validate_password(password):
    """
    validates that the password has an adequate length and that is formed by
    at least one lowercase, uppercase, number and _ or -, also makes sure it doesn't have
    sp characters or accents.
    """
    valid_pw = False
    num = 0
    upper = 0
    lower = 0
    chars = 0
    accents = 0
    min_length = 8
    max_length = 12
    pw_without_underscore = password.replace('_', '')
    pw_without_underscore = pw_without_underscore.replace('-', '')
    if (min_length <= len(password) <= max_length) and ('_' in password or '-' in password):
        i = 0
        while i < len(pw_without_underscore) and not valid_pw:
            if pw_without_underscore[i].isupper():
                upper += 1
            elif pw_without_underscore[i].islower():
                lower += 1
            elif pw_without_underscore[i].isnumeric():
                num += 1
            elif not pw_without_underscore[i].isalnum():
                chars += 1
            elif pw_without_underscore[i] in 'áéíóú':
                accents += 1

            i += 1

            if num > 0 and upper > 0 and lower > 0 and chars == 0 and accents == 0:
                valid_pw = True

    return valid_pw


def __gui_signup():
    """
    creates a gui for registering new players.
    """
    RootSignup = Toplevel()
    RootSignup.iconbitmap('used_files/pikachu.ico')
    RootSignup.title("Wordle Game | Sign-up")
    RootSignup.resizable(0, 0)
    RootSignup.geometry("350x150")
    RootSignup.config(bg='sky blue')

    FrameSignup = Frame(RootSignup)
    FrameSignup.pack()
    FrameSignup.config(bg='black')
    FrameSignup.config(relief='groove')
    FrameSignup.config(bd=5)
    FrameSignup.grid(rowspan=5, columnspan=5, padx=50, pady=20)

    UsernameSignup = StringVar()
    PasswordSignup = StringVar()
    PasswordReentered = StringVar()

    LabelUsername = Label(FrameSignup, text='Username')
    LabelUsername.grid(row=0, column=0, sticky='w')
    LabelUsername.config(bg='black')
    LabelUsername.config(fg='white')
    TextboxUsername = Entry(FrameSignup, textvariable=UsernameSignup)
    TextboxUsername.grid(row=0, column=1, sticky='w')
    TextboxUsername.config(bg='black')
    TextboxUsername.config(fg='white')

    LabelPassword = Label(FrameSignup, text='Password')
    LabelPassword.grid(row=1, column=0, sticky='w')
    LabelPassword.config(bg='black')
    LabelPassword.config(fg='white')
    TextboxPassword = Entry(FrameSignup, textvariable=PasswordSignup)
    TextboxPassword.grid(row=1, column=1, sticky='w')
    TextboxPassword.config(show='*')
    TextboxPassword.config(bg='black')
    TextboxPassword.config(fg='white')

    LabelPasswordReentered = Label(FrameSignup, text='Reenter password')
    LabelPasswordReentered.grid(row=2, column=0, sticky='w')
    LabelPasswordReentered.config(bg='black')
    LabelPasswordReentered.config(fg='white')
    TextboxPasswordReentered = Entry(FrameSignup, textvariable=PasswordReentered)
    TextboxPasswordReentered.grid(row=2, column=1, sticky='w')
    TextboxPasswordReentered.config(show='*')
    TextboxPasswordReentered.config(bg='black')
    TextboxPasswordReentered.config(fg='white')

    ButtonSignup = Button(RootSignup,
                          text="Enter",
                          command=lambda: __apply_signin(UsernameSignup.get(),
                                                         PasswordSignup.get(),
                                                         PasswordReentered.get(),
                                                         RootSignup, 'used_files/users.csv'))
    ButtonSignup.grid(row=5, column=2)


def __gui():
    """
    log-in gui.
    has a button to invoke gui_signup.
    """
    # Root of GUI
    root = Tk()
    root.iconbitmap('used_files/pikachu.ico')
    root.title('Wordle Game | Log-in')
    root.resizable(False, False)
    root.geometry('350x200')
    root.config(bg='hot pink')

    # Frame of GUI
    frame = Frame(root)
    frame.config(bg='black')
    frame.config(relief='groove')
    frame.config(bd=5)
    frame.grid(rowspan=5, columnspan=5, padx=70, pady=20)

    # All the labels below
    LabelUser = Label(frame, text='Username:')
    LabelUser.config(bg='black')
    LabelUser.config(fg='white')
    LabelUser.grid(row=0, column=0, padx=5, pady=10)

    LabelPassword = Label(frame, text='Password:')
    LabelPassword.config(bg='black')
    LabelPassword.config(fg='white')
    LabelPassword.grid(row=1, column=0, padx=5, pady=5)

    # All the entries below
    UsernameEntry = Entry(frame)
    UsernameEntry.config(bg='black')
    UsernameEntry.config(fg='white')
    UsernameEntry.grid(row=0, column=1, padx=5, pady=10)

    PasswordEntry = Entry(frame)
    PasswordEntry.config(bg='black')
    PasswordEntry.config(fg='white')
    PasswordEntry.config(show='*')
    PasswordEntry.grid(row=1, column=1, padx=5, pady=5)

    # Buttons
    ButtonEnter = Button(root, text='Enter',
                         command=lambda: __apply_login(UsernameEntry.get(),
                                                       PasswordEntry.get(),
                                                       UsernameEntry,
                                                       PasswordEntry))
    ButtonEnter.grid(row=5, column=1, padx=5, pady=5)

    ButtonRegister = Button(root, text='Register',
                            command=__gui_signup)
    ButtonRegister.grid(row=5, column=3, padx=5, pady=5)

    ButtonOut = Button(root, text='Exit login',
                       command=lambda: root.destroy())
    ButtonOut.grid(row=6, column=2, padx=5, pady=5)

    root.mainloop()


def main_login():
    """
    main function that runs the whole module, and returns a list with the name of the players [p1, p2]
    """
    __gui()
    list_players = [Players.p1, Players.p2]
    return list_players
