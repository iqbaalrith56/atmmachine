from tkinter import *
from tkmacosx import Button

# Default Settings
current_balance = 3500.70
correct_pin = "123"

# Function Intro - Nak start Program
def intro():
    print("[INFO] Displaying PIN Entry Page")  # Log action
    show_page("pin_entry") # Display function pin_entry
    entry_var.set("")  # Clear PIN input - Default Value
    result_label.config(text="", fg="black") # Condition Result Label

def validate_pin():
    entered_pin = entry_var.get() # Get Value from entry pin
    print(f"[ACTION] Entered PIN: {entered_pin}")  # Log action
    # Check Condition Pin Entry
    if entered_pin == correct_pin:
        print("[SUCCESS] PIN validated successfully") # Log action
        main_menu()  # Go to main menu
    else:
        print("[ERROR] Invalid PIN entered") # Log action
        result_label.config(text="Incorrect PIN number. Try again!", fg="red")
        entry_var.set("")  # Clear input and Try again

def main_menu():
    print("[INFO] Displaying Main Menu")  # Log action
    show_page("menu")
    balance_label.config(text=f"Current Balance: RM{current_balance:.2f}")
    exit_label.pack_forget()

def perform_function(choice):
    print(f"[ACTION] Selected Function: {choice}")  # Log action

    global exit_label
    exit_label = Label(text="Thank you for banking with Maybank", font=("Arial", 12), fg="red")
    result_label_func.config(text="")
    
    # Enable keypad and controls
    confirm_btn.config(state=NORMAL)
    clear_btn.config(state=NORMAL)
    for button in keypad_frame_func.winfo_children():
        button.config(state=NORMAL)

    # Do While Condition for Menu
    while True:
        if choice == 1:  # Deposit
            function_label.config(text="Deposit Funds")
            confirm_btn.config(command=lambda: process_transaction(1)) 
            
            # lambda: small anonymous function
            # lambda function can take any number of arguments, but can only have one expression.

        elif choice == 2:  # Withdraw
            function_label.config(text="Withdraw Funds")
            confirm_btn.config(command=lambda: process_transaction(2))

        elif choice == 3:  # Balance Inquiry
            print(f"[INFO] Displaying Current Balance: RM{current_balance:.2f}") # Log action
            function_label.config(text=f"Current Balance: RM{current_balance:.2f}")
            confirm_btn.config(state=DISABLED)
            clear_btn.config(state=DISABLED)
            for button in keypad_frame_func.winfo_children(): # Loop find button keypad to disable
                button.config(state=DISABLED)

        else: # Exit
            print("[INFO] Exiting application")
            exit_label.pack(pady=10)
            intro()
            break
        
        # Action do after choice selected
        entry_var.set("")  # Reset input for new function
        show_page("function")
        exit_label.config(text="")
        break

def process_transaction(choice):
    global current_balance
    try:
        amount = float(entry_var.get())
        if choice == 1:  # Deposit
            print(f"[ACTION] Depositing: RM{amount:.2f}") # Log action
            current_balance += amount
            result_label_func.config(text=f"Deposited RM{amount:.2f}. New Balance: RM{current_balance:.2f}", fg="green")
        elif choice == 2:  # Withdraw
            print(f"[ACTION] Attempting Withdrawal: RM{amount:.2f}") # Log action
            if amount <= current_balance:
                current_balance -= amount
                print(f"[SUCCESS] Withdrawal successful. New Balance: RM{current_balance:.2f}") # Log action
                result_label_func.config(text=f"Withdraw RM{amount:.2f}. New Balance: RM{current_balance:.2f}", fg="green")
            else:
                print("[ERROR] Insufficient Funds") # Log action
                result_label_func.config(text=f"Account balance insufficient to withdraw. \nCurrent Balance: RM{amount:.2f}", fg="red")
        entry_var.set("")
        
    except ValueError:
        print("[ERROR] Invalid amount entered") # Log action
        result_label_func.config(text="Invalid amount. Enter a number.", fg="red")

def keypad_input(digit):
    current = entry_var.get()
    print(f"[ACTION] Keypad Input: {digit}")  # Log action
    entry_var.set(current + digit)

def clear_input():
    print("[ACTION] Clearing input field")  # Log action
    entry_var.set("")

def show_page(page):
    print(f"[INFO] Navigating to page: {page}")  # Log action
    for p in pages:
        pages[p].pack_forget()
    pages[page].pack(fill="both", expand=True)
    root.update_idletasks() # Reload with cache

def disable_keyboard(event):
    return "break"  # Prevents keyboard input

# Initialize main window
root = Tk()
root.title("ATM Machine") # App Name
root.geometry("400x600") # Size Window

# Input variable
entry_var = StringVar()

# Pages dictionary
pages = {}

# PIN Entry Page
pin_page = Frame(root)
pages["pin_entry"] = pin_page

Label(pin_page, text="Welcome to ATM", font=("Arial", 20, "bold")).pack(pady=30)
Label(pin_page, text="Enter your PIN:", font=("Arial", 14)).pack(pady=10)

pin_input = Entry(pin_page, textvariable=entry_var, font=("Arial", 16), bd=2, justify="center", width=12)
pin_input.pack(pady=10)

pin_input.bind("<Key>", disable_keyboard) # Disable Keyboard Laptop/PC

result_label = Label(pin_page, text="", font=("Arial", 12), fg="red")
result_label.pack(pady=10)

# Keypad and Controls
keypad_frame = Frame(pin_page)
keypad_frame.pack(pady=10)

buttons = [
    ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
    ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
    ("", 3, 0), ("0", 3, 1), (".", 3, 2),
]
for (text, row, col) in buttons:
    Button(
        keypad_frame, text=text, width=70, bg='white', fg="black",
        font=("Arial", 12), command=lambda t=text: keypad_input(t)
    ).grid(row=row, column=col, padx=5, pady=5)

control_frame = Frame(pin_page)
control_frame.pack(pady=10)

clear_func_btn = Button(control_frame, text="Clear", bg="yellow", fg="black", font=("Arial", 12), width=70, command=clear_input)
destroy_btn = Button(control_frame, text="Cancel", bg="red", fg="black", font=("Arial", 12), width=70, command=root.destroy)
validate_btn = Button(control_frame, text="Enter", bg="green", font=("Arial", 12), command=validate_pin)

destroy_btn.grid(row=0, column=0, padx=10)
clear_func_btn.grid(row=0, column=1, padx=10)
validate_btn.grid(row=0, column=2, padx=10)

# Main Menu Page
menu_page = Frame(root)
pages["menu"] = menu_page

Label(menu_page, text="Main Menu", font=("Arial", 20)).pack(pady=20)
balance_label = Label(menu_page, text="", font=("Arial", 16))
balance_label.pack(pady=10)

menu_frame = Frame(menu_page)
menu_frame.pack(pady=20)

menu_buttons = [
    ("Deposit", lambda: perform_function(1)),
    ("Withdraw", lambda: perform_function(2)),
    ("Balance Inquiry", lambda: perform_function(3)),
    ("Exit", lambda: perform_function(4)),
]
for text, command in menu_buttons:
    Button(menu_frame, text=text, width=200, command=command).pack(pady=5)

# Function Page
function_page = Frame(root)
pages["function"] = function_page

function_label = Label(function_page, text="Function Page", font=("Arial", 20))
function_label.pack(pady=20)

Label(function_page, text="Enter Amount:", font=("Arial", 14)).pack(pady=10)

func_input = Entry(function_page, textvariable=entry_var, font=("Arial", 16), bd=2, justify="center", width=12)
func_input.pack(pady=10)

func_input.bind("<Key>", disable_keyboard)

result_label_func = Label(function_page, text="", font=("Arial", 12))
result_label_func.pack(pady=10)

# Keypad for Function Page
keypad_frame_func = Frame(function_page)
keypad_frame_func.pack(pady=10)

for (text, row, col) in buttons:
    Button(
        keypad_frame_func, text=text, width=100,
        font=("Arial", 12), command=lambda t=text: keypad_input(t)
    ).grid(row=row, column=col, padx=5, pady=5)

# Controls for Function Page
control_frame_func = Frame(function_page)
control_frame_func.pack(pady=10)

confirm_btn = Button(control_frame_func, text="Confirm", bg="green", fg="white", font=("Arial", 12), width=70)
back_btn = Button(control_frame_func, text="Back", bg="red", fg="white", font=("Arial", 12), width=70, command=main_menu)
clear_btn = Button(control_frame_func, text="Clear", bg="yellow", fg="black", font=("Arial", 12), width=70, command=clear_input)

clear_btn.grid(row=0, column=0, padx=10)
back_btn.grid(row=0, column=1, padx=10)
confirm_btn.grid(row=0, column=2, padx=10)

# Start application with PIN entry page
intro()

# Run the application
root.mainloop()