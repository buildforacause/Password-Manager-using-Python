from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project


def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    pass_letter = [random.choice(letters) for _ in range(nr_letters)]
    pass_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    pass_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list = pass_letter + pass_symbols + pass_numbers
    random.shuffle(password_list)
    password = "".join(password_list)

    pass_input.delete(0, END)
    pass_input.insert(END, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_entry():
    web = website_input.get().title()
    email = email_input.get()
    password_save = pass_input.get()
    new_data = {
        web: {
            "email": email,
            "password": password_save
        }
    }
    if not web or not email or not password_save:
        messagebox.showinfo(title=":(", message="One of the fields is empty!!")
    else:
        is_ok = messagebox.askokcancel(title=web, message=f"Are the details OK?\nEmail:{email} and "
                                                          f"Password:{password_save}")
        if is_ok:
            try:
                # using json files to save data
                with open("data.json", mode="r") as data:
                    # reading the data from the json file
                    data_file = json.load(data)
                    # adding the data in the existing file to maintain the json data structure
                    data_file.update(new_data)
            # we can catch more than one error like this
            except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
                with open("data.json", mode="w") as data:
                    json.dump(new_data, data, indent=4)
            # executes only when try block runs successfully
            else:
                with open("data.json", mode="w") as data:
                    # dump method is used to write in a json file and indent is used for spacing out the data
                    json.dump(data_file, data, indent=4)
            # executes everytime no matter what
            finally:
                website_input.delete(0, END)
                pass_input.delete(0, END)


# ---------------------------- SEARCH PASSWORDS ------------------------------- #


def search():
    web = website_input.get().title()
    try:
        with open("data.json", mode="r") as data:
            data_dict = json.load(data)
        messagebox.showinfo(title=f"{web}", message=f"Email: {data_dict[web]['email']}\n"
                                                    f"Password:{data_dict[web]['password']}")
    except KeyError:
        messagebox.showinfo(title=":(", message=f"Sorry, no information about {web}")
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        messagebox.showinfo(title="OOPS!", message="Data file does not exist!")

# ---------------------------- UI SETUP ------------------------------- #


# creating tkinter window
window = Tk()
window.title("Password Manager")
window.config(padx=100, pady=50)
# creating a canvas for GUI
canvas = Canvas(width=200, height=200)
# creating image for canvas
image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, column=1)
# creating labels
web_label = Label(text="Website:")
web_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

pass_label = Label(text="Password:")
pass_label.grid(row=3, column=0)
# creating input boxes
website_input = Entry(width=52)
website_input.grid(row=1, column=1, columnspan=2)
website_input.focus()

email_input = Entry(width=52)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(END, "bmovies52@gmail.com")

pass_input = Entry(width=52)
pass_input.grid(row=3, column=1, columnspan=2)
# creating buttons
generate_pass_button = Button(text="Generate Password", width=14, command=generate_pass)
generate_pass_button.grid(row=3, column=2)

add_button = Button(text="Add", width=44, command=add_entry)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=14, command=search)
search_button.grid(row=1, column=2)
window.mainloop()
