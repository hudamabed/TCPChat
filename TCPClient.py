import socket
import threading
import tkinter as tk
from tkinter import ttk
import sys
from datetime import datetime

global receive_thread
global stop_thread

# Define constants for the client
HOST = 'localhost'
PORT = 8000


# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Function to handle incoming messages
usernames_set = set()
client_socket.connect((HOST, PORT))

root = tk.Tk()
root.configure(bg="palevioletred")
root.title('Chat')
def receive_messages():
    while True:
        try:
            if stop_thread == True:
                sys.exit(0)
                break

            data = client_socket.recv(1024).decode()
            
            if not data:
                break

            msg_type = data[0]
            msg = data[1:]

            if msg_type == 'o':
                if msg in usernames_set:
                    add_message(f"{msg} has just left the room", 'system')
                    usernames_set.remove(msg)
                else:
                    add_message(f"{msg} has just joined the room", 'system')
                    usernames_set.add(msg)
            elif msg_type == 'O':
                curr_online_users = msg.split(',')
                usernames_set.update(curr_online_users)
                       

            elif msg_type in ['z', 'w']:
                add_message(msg, 'system')
            else:
                add_message(msg, 'others')
        except:
            client_socket.close()
            break

def send_message(event=None):
    message = input_field.get()
    if len(usernames_set) == 0:
        root.title(f'Chat - {message}') 
    input_field.delete(0, tk.END)
    client_socket.send(message.encode())
    add_message(message, 'me')

def clear_chat():
     chat_window.config(state=tk.NORMAL)
     chat_window.delete('1.0', tk.END)
     chat_window.config(state=tk.DISABLED)




def on_closing():
    client_socket.close()
    sys.exit(0)

def show_online_connected():
    update_online_clients(usernames_set)


chat_frame = tk.Frame(root)
chat_frame.pack(side=tk.TOP, padx=10, pady=10)
chat_frame.configure(bg="pink")

online_clients_frame = tk.Frame(chat_frame)
online_clients_frame.pack(side=tk.RIGHT, padx=10)
online_clients_frame.configure(bg="pink")

scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_window = tk.Text(chat_frame, height=20, width=50,
                      yscrollcommand=scrollbar.set, wrap="word")
chat_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar.config(command=chat_window.yview)

chat_window.tag_config('user', foreground='#88C0D0')
chat_window.tag_config('server', foreground='#8FBCBB')
chat_window.tag_config('small', font=("Helvetica", 7))
chat_window.tag_config('greycolour', foreground="#D8DEE9")
chat_window.tag_config("me", justify="right")
chat_window.tag_config("others", justify="left")
chat_window.tag_config("system", justify="center")
chat_window.tag_config("right", justify="right")
chat_window.tag_config("small", font=("Helvetica", 7))
chat_window.tag_config("colour", foreground="#D8DEE9")

chat_window.config(state=tk.DISABLED)

chat_window.configure(background='palevioletred')

root.option_add("*Font", "TkFixedFont")
root.option_add("*sent.Font", "TkFixedFont")
root.option_add("*received.Font", "TkFixedFont")

input_frame = tk.Frame(root)
input_frame.pack(side=tk.BOTTOM, padx=10, pady=10)
input_frame.configure(bg="pink")

input_field = tk.Entry(input_frame, width=40)
input_field.bind("<Return>", send_message)
input_field.pack(side=tk.LEFT)

send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)
send_button.configure(bg="pink", fg="#2E3440")

clear_chat_button = tk.Button(input_frame, text="Clear Chat", command=clear_chat)
clear_chat_button.pack(side=tk.LEFT)
clear_chat_button.configure(bg="pink", fg="#2E3440")

show_online_connected_button = tk.Button(input_frame, text="Show connected clients", command=show_online_connected)
show_online_connected_button.pack(side=tk.LEFT)
show_online_connected_button.configure(bg="pink", fg="#2E3440")

online_clients_label = tk.Label(online_clients_frame, text="Online Clients:")
online_clients_label.pack(side=tk.TOP)
online_clients_label.configure(bg="palevioletred", fg="#D8DEE9")

online_clients_listbox = tk.Listbox(online_clients_frame, height=20, width=20)
online_clients_listbox.pack(side=tk.BOTTOM, padx=10, pady=10)

online_clients_listbox.configure(bg="palevioletred", fg="#D8DEE9", highlightbackground="#81A1C1",
                                 highlightcolor="#81A1C1", selectbackground="#81A1C1", selectforeground="#D8DEE9")


def get_time_formatted():
    return datetime.now().strftime("%a %I-%M %p \n")


emoji_list = ['😀', '😂', '😍', '🤔', '😎','❤️','🤣','😉','😍']

def send_emoji(emoji_idx):
    emoji = emoji_list[emoji_idx]
    input_field.insert(0, emoji)  # set the emoji as the text of the input field
    # Send the emoji to the server



for i in range(len(emoji_list)):
    emoji_button = ttk.Button(root, text=emoji_list[i])
    emoji_button.pack(side=tk.LEFT, padx=5, pady=5)
    emoji_button.bind("<Button-1>", lambda event, idx=i: (send_emoji(idx), input_field.focus()))


def add_message(msg, sender):
    
    chat_window.config(state=tk.NORMAL)

    fa = "black"
    bg_color = "pink"
    text_position = ""
    tags = ""
    text_direction = tk.LEFT

    match sender:
        case 'others':
            text_position = "left"
            fa = "black"
            tags = 'others'
        case 'system':
            text_position = "center"
            fa = "black"
            tags = 'system'
            text_direction = tk.CENTER
        case 'me':
            text_position = "right"
            fa = "black"
            tags = 'me'
            
    
    chat_window.insert(tk.END, '\n ', text_position)
    chat_window.insert(tk.END, get_time_formatted(),('small', 'greycolour', text_position))
    chat_window.insert(tk.END, ' ', text_position)

    chat_window.config(state=tk.DISABLED)
    
    message = tk.Label(chat_window, fg=fa, text=msg, wraplength=200, font=("Arial", 10), bg=bg_color, bd=4, justify=text_direction, relief="flat", anchor="center")

    chat_window.window_create(tk.END, window=message)
    chat_window.insert(tk.END, '\n', "center")
    chat_window.tag_add(tags, "end-2l", "end-1c")
    chat_window.config(foreground="#0000CC", font=("Helvetica", 9))
    chat_window.yview(tk.END)



# Function to update the list of online clients
def update_online_clients(online_clients):
    # Clear the current list of online clients
    online_clients_listbox.delete(0, tk.END)

    # Add each online client to the listbox
    for client in online_clients:
        online_clients_listbox.insert(tk.END, client)


# Create a new thread to handle incoming messages
stop_thread = False
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main loop
tk.mainloop()






















# import socket
# import threading
# import tkinter as tk
# from tkinter import ttk
# import sys
# from datetime import datetime

# global receive_thread
# global stop_thread

# # Define constants for the client
# HOST = 'localhost'
# PORT = 8000


# # Create a socket object
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# # Function to handle incoming messages
# usernames_set = set()
# client_socket.connect((HOST, PORT))

# root = tk.Tk()
# root.configure(bg="steelblue")
# root.title('Chat')
# def receive_messages():
#     while True:
#         try:
#             if stop_thread == True:
#                 sys.exit(0)
#                 break

#             data = client_socket.recv(1024).decode()
#             if not data:
#                 break

#             msg_type = data[0]
#             msg = data[1:]
            

#             if msg_type == 'o':
#                 if msg in usernames_set:
#                     add_message(f"{msg} has just left the room", 'system')
#                     usernames_set.remove(msg)
#                 else:
#                     add_message(f"{msg} has just joined the room", 'system')
#                     usernames_set.add(msg)
#             elif msg_type == 'O':
#                 curr_online_users = msg.split(',')
#                 usernames_set.update(curr_online_users)
                       

#             elif msg_type in ['z', 'w']:
#                 add_message(msg, 'system')
#             else:
#                 add_message(msg, 'others')
#         except:
#             client_socket.close()
#             break

# def send_message(event=None):
#     message = input_field.get()
#     if len(usernames_set) == 0:
#         root.title(f'Chat - {message}') 
#     input_field.delete(0, tk.END)
#     client_socket.send(message.encode())
#     add_message(message, 'me')

# def clear_chat():
#      chat_window.config(state=tk.NORMAL)
#      chat_window.delete('1.0', tk.END)
#      chat_window.config(state=tk.DISABLED)




# def on_closing():
#     client_socket.close()
#     sys.exit(0)

# def show_online_connected():
#     update_online_clients(usernames_set)


# chat_frame = tk.Frame(root)
# chat_frame.pack(side=tk.TOP, padx=10, pady=10)
# chat_frame.configure(bg="steelblue")


# online_clients_frame = tk.Frame(chat_frame)
# online_clients_frame.pack(side=tk.RIGHT, padx=10)
# online_clients_frame.configure(bg="steelblue")

# scrollbar = tk.Scrollbar(chat_frame)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# chat_window = tk.Text(chat_frame, height=20, width=50,
#                       yscrollcommand=scrollbar.set, wrap="word")
# chat_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

# scrollbar.config(command=chat_window.yview)

# chat_window.tag_config('user', foreground='#88C0D0')
# chat_window.tag_config('server', foreground='#8FBCBB')
# chat_window.tag_config('small', font=("Helvetica", 7))
# chat_window.tag_config('greycolour', foreground="#D8DEE9")
# chat_window.tag_config("me", justify="right")
# chat_window.tag_config("others", justify="left")
# chat_window.tag_config("system", justify="center")
# chat_window.tag_config("right", justify="right")
# chat_window.tag_config("small", font=("Helvetica", 7))
# chat_window.tag_config("colour", foreground="#D8DEE9")

# chat_window.config(state=tk.DISABLED)

# chat_window.configure(background='slategray')

# root.option_add("*Font", "TkFixedFont")
# root.option_add("*sent.Font", "TkFixedFont")
# root.option_add("*received.Font", "TkFixedFont")

# input_frame = tk.Frame(root)
# input_frame.pack(side=tk.BOTTOM, padx=10, pady=10)
# input_frame.configure(bg="steelblue")


# input_field = tk.Entry(input_frame, width=40)
# input_field.bind("<Return>", send_message)
# input_field.pack(side=tk.LEFT)
# bold_font = ("Arial", 12, "bold")
# input_field['font'] = bold_font

# send_button = tk.Button(input_frame, text="Send", command=send_message)
# send_button.pack(side=tk.LEFT)
# send_button.configure(bg="white", fg="#2E3440")
# bold_font = ("Arial", 12, "bold")
# send_button['font'] = bold_font

# clear_chat_button = tk.Button(input_frame, text="Clear Chat", command=clear_chat)
# clear_chat_button.pack(side=tk.LEFT)
# clear_chat_button.configure(bg="white", fg="#2E3440")
# bold_font = ("Arial", 12, "bold")
# clear_chat_button['font'] = bold_font

# show_online_connected_button = tk.Button(input_frame, text="Show connected clients", command=show_online_connected)
# show_online_connected_button.pack(side=tk.LEFT)
# show_online_connected_button.configure(bg="white", fg="#2E3440")
# bold_font = ("Arial", 12, "bold")
# show_online_connected_button['font'] = bold_font

# online_clients_label = tk.Label(online_clients_frame, text="Online Clients:")
# bold_font = ("Arial", 14, "bold")
# online_clients_label['font'] = bold_font
# online_clients_label.pack(side=tk.TOP)
# online_clients_label.configure(bg="steelblue", fg="#D8DEE9")

# online_clients_listbox = tk.Listbox(online_clients_frame, height=20, width=20)
# online_clients_listbox.pack(side=tk.BOTTOM, padx=10, pady=10)

# online_clients_listbox.configure(bg="slategray", fg="#D8DEE9", highlightbackground="#81A1C1",
#                                  highlightcolor="#81A1C1", selectbackground="#81A1C1", selectforeground="#D8DEE9")
# bold_font = ("Arial", 14, "bold")
# online_clients_listbox['font'] = bold_font


# def get_time_formatted():
#     return datetime.now().strftime("%a %I-%M %p \n")


# emoji_list = ['😀', '😂', '😍', '🤔', '😎','❤️','🤣','😉','😍']

# def send_emoji(emoji_idx):
#     emoji = emoji_list[emoji_idx]
#     input_field.insert(0, emoji)  # set the emoji as the text of the input field
#     # Send the emoji to the server



# for i in range(len(emoji_list)):
#     emoji_button = ttk.Button(root, text=emoji_list[i])
#     emoji_button.pack(side=tk.LEFT, padx=5, pady=5)
#     emoji_button.bind("<Button-1>", lambda event, idx=i: (send_emoji(idx), input_field.focus()))
# def add_message(msg, sender):
    
#     chat_window.config(state=tk.NORMAL)


#     fa = "slategray"
#     bg_color = "slategray"
#     text_position = ""
#     tags = ""
#     text_direction = tk.LEFT

#     match sender:
#         case 'others':
#             text_position = "left"
#             fa = "indigo"
#             tags = 'others'
#         case 'system':
#             text_position = "center"
#             fa = "black"
#             tags = 'system'
#             text_direction = tk.CENTER
#         case 'me':
#             text_position = "right"
#             fa = "maroon"
#             tags = 'me'
            
    
#     chat_window.insert(tk.END, '\n ', text_position)
#     chat_window.insert(tk.END, get_time_formatted(),('small', 'greycolour', text_position))
#     chat_window.insert(tk.END, ' ', text_position)

#     chat_window.config(state=tk.DISABLED)
    
#     message = tk.Label(chat_window, fg=fa, text=msg, wraplength=200, font=("Arial", 12,"bold"), bg=bg_color, bd=4, justify=text_direction, relief="flat", anchor="center")

#     chat_window.window_create(tk.END, window=message)
#     chat_window.insert(tk.END, '\n', "center")
#     chat_window.tag_add(tags, "end-2l", "end-1c")
#     chat_window.config(foreground="#0000CC", font=("Helvetica", 9))
#     chat_window.yview(tk.END)



# # Function to update the list of online clients
# def update_online_clients(online_clients):
#     # Clear the current list of online clients
#     online_clients_listbox.delete(0, tk.END)

#     # Add each online client to the listbox
#     for client in online_clients:
#         online_clients_listbox.insert(tk.END, client)


# # Create a new thread to handle incoming messages
# stop_thread = False
# receive_thread = threading.Thread(target=receive_messages)
# receive_thread.start()

# root.protocol("WM_DELETE_WINDOW", on_closing)

# # Start the main loop
# tk.mainloop()








