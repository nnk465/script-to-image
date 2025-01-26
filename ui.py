import os
import time
import tkinter as tk
from io import BytesIO
import requests
from PIL import Image, ImageTk, ImageDraw
from tkinter import ttk

liste_liens = []

image_lists = [[
                   'https:///92da2fb8-e988-4dd5-8e06-0d79911db95d?X-113%2Fus-east-1%2Fs3%2Faws4_-Amz-Expires=155182&X-Amz-Signature=89bd31b5259440370af8b412f171577a4820e9a24cbadee1f3f4efec3be77d53&X-18%3A44%20GMT',
                   'https:///dc5bd5ac-e84b-44a4-9143-1eebad0ffabe?X-T143927Z&X-Amz-Expires=101585&X-Amz-Signature=1ef37d99343b66b680c9e4fc3734f6cc9fa37da68ae60cef3683be44b5f532c5&X-52%3A32%20GMT',
                   'https:///71c17119-768b-4f1b-98d9-2e67c917d05a?X-T004601Z&X-Amz-Expires=150760&X-Amz-Signature=6d7e392d8cec362903538caf00527a52e62f0e45f25f4ba125aef835650cc622&X-38%3A41%20GMT',
                   'https:///710ffa52-61f1-4b57-a44b-8df987db38a1?X-T051708Z&X-Amz-Expires=132585&X-Amz-Signature=0c250eade809d31eebcf161a73996cfb4193a020a94d6cf535e820580f62ba33&X-06%3A53%20GMT'],
               'https:///4accfd81-e1f4-4910-8d0a-781eaa661a75?X-T072529Z&X-Amz-Expires=128033&X-Amz-Signature=06b073f606e63387fc30ff7e2e0e0d149edf161adb044a8f464b6eebb248e043&X-59%3A22%20GMT',
               [
                   'https:///ff167031-ddb0-4819-92e5-2467981cd52e?X-T073921Z&X-Amz-Expires=124835&X-Amz-Signature=9b345223700b23b0dca038904d5a69881836557dca55b35fd52ffc74d16729d9&X-19%3A56%20GMT',
                   'https:///6aadc405-0fb2-4f05-accf-48106ca149a7?X-T033733Z&X-Amz-Expires=139645&X-Amz-Signature=22d117c33327253ab3ba8cb83f7770a59f0e4bacdd671bffd0af42c163a2dfc1&X-24%3A58%20GMT',
                   'https:///db709605-91db-4a4b-a6ca-b93229aadb08?X-T141815Z&X-Amz-Expires=101914&X-Amz-Signature=398647b284c8b692559b456eaa77b2fb210a9b507d99b9e0a892cc3603b8d4a1&X-36%3A49%20GMT',
                   'https:///ba7adccb-1631-45b4-ae25-f9cfaf9d5cbf?X-T152310Z&X-Amz-Expires=99145&X-Amz-Signature=2b02ebdbb44a468eede257b5e1ee1772043f532fdd2dcc6e867e57d5481b778e&X-55%3A35%20GMT'],
               [
                   'https:///38e939e3-d086-4469-ae9b-fcfe9af6d661?X-T162448Z&X-Amz-Expires=92386&X-Amz-Signature=f338337c7aa95bac58437db1aed62f9b96b7deaadd8179f51ba02c3d0b24903b&X-04%3A34%20GMT',
                   'https:///be822da5-07a6-4eb2-8404-0298b2163b72?X-T102624Z&X-Amz-Expires=115765&X-Amz-Signature=2e0532dbe35b4faf5201e8b4514fe81abd1547bf5704c1e447e940b086ddfea1&X-35%3A49%20GMT',
                   'https:///a13a259d-9fac-41fe-8db4-30bdb9f0889b?X-113%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240113T202221Z&X-Amz-Expires=165244&X-Amz-Signature=a866a7c95ef3c679f1d7b7543916fa5e2045c3cd44c5cb12baa53d097836d47b&X-16%3A25%20GMT',
                   'https:///007f8965-7274-464e-bfc0-cd8d3d72907f?X-113%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240113T214704Z&X-Amz-Expires=162331&X-Amz-Signature=478754124b866fcdaab5f4de0288f57598a3dd82ed166d7db48fd3313a07053a&X-52%3A35%20GMT'],
               'https:///4e94d4d0-6721-4d2a-8451-c84061ffa3b7?X-T090324Z&X-Amz-Expires=118627&X-Amz-Signature=6125d678d6ff233926ce7c3711d9590d05032430468fb3d9fcebf96db1864015&X-00%3A31%20GMT']
titles = ['titre1', 'titre2', 'titre3', '4', '5']


def list_to_dict(image_list):
    """
    tkimage, la sortie  est un dict de ce style
    {lien: (photo, photo barrée, (x, y))
    lien2...}                      |--> position de l'image dans la grid
            """
    print('chargement des images...')
    tkimage = {}
    for i, l in enumerate(image_list):
        for j, lien in enumerate(l):
            if lien == 'Erreur D':
                pass
            photo = Image.open(BytesIO(requests.get(lien).content)).resize((108, 192))
            draw = ImageDraw.Draw(photo)
            draw.line((0, 0, photo.width, photo.height), fill="red", width=2)
            draw.line((0, photo.height, photo.width, 0), fill="red", width=2)
            tkimage[lien] = (ImageTk.PhotoImage(Image.open(BytesIO(requests.get(lien).content)).resize((108, 192))),
                             ImageTk.PhotoImage(photo), (i, j))
    return tkimage


def download_images():
    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists('image generator'):
        os.makedirs('image generator')
    for i, link in enumerate(liste_liens):
        try:
            response = requests.get(link, stream=True)
            filename = os.path.join('image generator', f"image{time.time(), i}.jpg")
            # Écrire les données binaires de l'image dans un fichier local
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

            print(f"Image {i + 1} téléchargée avec succès.")

        except Exception as e:
            print(f"Erreur lors du téléchargement de l'image {i + 1}: {e}")


def on_vertical_scroll(*args):
    canvas.yview(*args)


def afficher_images(tkimage, titles, root):
    print('affichage des images')
    canvas = tk.Canvas(master=root)
    canvas.grid(column=0, row=0, sticky='nsew')
    scroll = tk.Scrollbar(root, orient='vertical', command=canvas.yview)
    scroll.grid(column=1, row=0, sticky='ns')
    canvas.configure(yscrollcommand=scroll.set)
    frame = tk.Frame(master=canvas)
    canvas.create_window((0, 0), window=frame, anchor='nw')
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    # add images label
    for row, title in enumerate(titles):
        label = tk.Label(frame, text=titles[row], wraplength=100, anchor='w')
        label.grid(row=row, column=0, padx=5, pady=5, sticky='new')
    # add images button
    for k, i in enumerate(tkimage.items()):
        row = i[1][2][0]
        column = i[1][2][1]
        print(i[0])
        print(i[1])
        button = tk.Button(master=frame, image=i[1][0])
        button.configure(command=lambda link=i[0], btn=button: ajouter_lien(link, btn, tkimage))
        button.grid(row=row, column=column + 1, padx=5, pady=5)
    downbtn = tk.Button(root, command=download_images, text='télécharger les images')
    downbtn.grid(row=1)
    canvas.grid_columnconfigure(0, minsize=100)
    root.grid_columnconfigure(0, minsize=650)
    root.rowconfigure(0, minsize=500)
    root.geometry("668x531")


def ajouter_lien(lien, bouton, tkimage):
    if lien in liste_liens:
        liste_liens.remove(lien)
        bouton.configure(image=tkimage[lien][0])
    else:
        liste_liens.append(lien)
        bouton.configure(image=tkimage[lien][1])
    print("liste mise a jour:", liste_liens)


# Liste de listes de liens d'images (remplacez les liens par les vôtres)
liens_images = [
    ['lien_image1', 'lien_image2', 'lien_image3', 'lien_image4'],
    ['lien_image5', 'lien_image6', 'lien_image7', 'lien_image8'],
]


def main(images_list, titles, root):
    # Liste pour stocker les liens des images cliquées
    root = tk.Toplevel(root)
    root.geometry("750x500")
    im = list_to_dict(images_list)
    root.title("Affichage d'images")
    afficher_images(im, titles, root)
    # Lancer la boucle principale
    root.mainloop()


if __name__ == '__main__':
    main(image_lists, titles=titles)
