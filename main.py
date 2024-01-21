import json
import re
import tkinter as tk
import webbrowser

import modules
import threading

with open('data.json', 'r+') as file:
    url = json.load(file)['url']

root = tk.Tk()
root.configure(background='grey')
root.geometry('750x500')
root.title('image generator')
titlelabel = tk.Label(root, text="Générateur d'image", font='arial', background='grey', wraplength=250)
titlelabel.grid(row=0, column=1)
textscript = tk.Text(root, background='grey', font='white', width=40, height=10)

style_frame = tk.Frame(root)
style_frame.grid(column=0, row=2, sticky='nw')
label_style = tk.Label(style_frame, text="Style des images:")
label_style.pack(side="left")
var_list = []

real_var = tk.BooleanVar(name='real-var')
real_cb = tk.Checkbutton(style_frame, text='réel', variable=real_var)
real_cb.pack(side='left')
var_list.append(real_var)

fantasy_var = tk.BooleanVar()
fantasy_cb = tk.Checkbutton(style_frame, text='imaginaire', variable=fantasy_var)

fantasy_cb.pack(side='left')
var_list.append(fantasy_var)
order = ['FILM', 'FANTASY']


def start():
    var_True = []
    value = [var.get() for var in var_list]
    for i, b in enumerate(value):
        if b:
            var_True.append(order[i])
    if len(var_True) > 1:
        return
    else:
        text = textscript.get("1.0", "end-1c")
        number = number_entry.get()
        if number.isdigit() is False or number == 0:
            number = 1
        modules.main(number=number, text=text, style=var_True[0] if len(var_True) == 1 else 'FILM',
                     root=root)


def set_data(t):
    with open('data.json', 'r+') as file:
        data = json.loads(file.read())
        file.close()
    if t == 'cookies':
        text = cookies_set.get("1.0", "end-1c")
        with open('data.json', 'w+') as file:
            bm = re.findall(r'cf_bm=(.*?);', text)
            cid = re.findall(r'CID=(.*?);', text)
            brand = re.findall(r"X-Canva-Brand: (.*?)'", text)
            data['cookies']['__cf_bm'] = bm[0] if len(bm) == 1 else print('pas set-bm')
            data['cookies']['CID'] = cid[0] if len(cid) == 1 else print('pas set-cid')
            data['headers']['X-Canva-brand'] = brand[0] if len(brand) == 1 else print('pas canva brand')
            json.dump(data, file, indent=2)
            file.close()

    if t == 'url':
        text = set_url.get("1.0", "end-1c")
        with open('data.json', 'w+') as file:
            if t == 'url':
                data['url'] = text
            json.dump(data, file, indent=2)
            file.close()

    return


def open_url():
    with open('data.json', 'r+') as file:
        u = json.load(file)['url']
    webbrowser.open_new(u)

number_entry = tk.Entry(root)
number_entry.grid(column=0, row=3, sticky='w')
start_btn = tk.Button(root, command=start, text='transformer le script en images')
start_btn.grid(column=0, row=4, sticky='w')
root.columnconfigure(2, minsize=850)
textscript.grid(column=0, row=1)

set_frame = tk.Frame(root, background='grey')
set_frame.grid(column=2, row=1, sticky='nsew')
cookie_title = tk.Label(set_frame, text='set les cookies', background='grey')
cookie_title.grid(row=0, column=0, sticky='nsew')
cookies_set = tk.Text(set_frame, background='grey', width=40, height=10)
cookies_set.grid(row=1, column=0)
set_button = tk.Button(set_frame, text='set les cookies', command=lambda e='cookies': set_data(e))
set_button.grid(sticky='w')

seturl_title = tk.Label(set_frame, text="set l'url", background='grey')
seturl_title.grid(row=3, column=0, sticky='nsew')
set_url = tk.Text(set_frame, background='grey', width=40, height=1)
set_url.grid(row=4, column=0)
seturl_button = tk.Button(set_frame, text="set l'url", command=lambda e='url': set_data(e))
seturl_button.grid(sticky='w')
openurl_btn = tk.Button(set_frame, text="ouvrir canva", command=open_url)
openurl_btn.grid()
root.mainloop()
