import requests
import re
import time
import ui
import json
import g4f
import os

if os.path.isfile('cookie.json') is False:
    with open('cookies.json', 'w+') as file:
        data = {
            "cookies": {
                "CID": "",
                "__cf_bm": ""
            },
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
            }
        }
        json.dump(data, file, indent=2)
        file.close()

with open('cookies.json', 'r+') as c:
    t = json.load(c)
    cookies = t['cookies']
    headers = t['headers']


def text_to_prompts(text=None, number=5):
    g4f.debug.logging = True
    print(number)
    prompt = "Please follow these instructions carefully. Your Midjourney prompts must be extremely detailed, with captivating details, specific, and imaginative to generate the most unique and creative images possible. The only valid input for the first step of the 'Midjourney Prompt Generator' is a prompt with its title in the following format.{prompt's title in french} -> ==prompt==Never forgot braces and equeal symbols.Keep in mind that Midjourney has no memory. Make sure to replace prompt by your image description.  In the prompts, be careful to only include what Midjourney can describe, so no names or surnames of people it doesn't know. Each prompt must be independent of the others. Describe each prompt as if there is no context. ChatGPT will generate the number of prompts the user specifies. These prompts should be imaginative and descriptive, covering subjects, image support, composition, environment, lighting, colors, mood and tone, and likeness. Your response should be in the format with braces and equals sylbols. never forgot the format. I repeat, your response should have braces for titles which represent the sentance illustrated by the prompt and equals symbols before and after the prompt to midjourney. Here is an example of the format: {Elara observait les montagnes} ==Amidst the majestic mountains, visualize Elara standing on the edge of the quaint village, a cascade of curious stars reflecting in her wide, mesmerized eyes. Craft an image that captures the clandestine moments as Elara escapes her room every night, with the moonlight gently illuminating her path, creating an ethereal atmosphere of curiosity and wonder.== So I will give you a text and i would like that you make ", number, "prompts to illustrate all the text and not only on the beginning. Prompt have to be in the same order than the text. Make ", number, " prompts for the following script on all the script and not only on a part. so make sure that the ", number, "prompts can illustrate all the script. make sure to do the number of prompt that i just say you, so", number, "I insist,", number
    if text is None:
        text = "Il était une fois, dans un petit village enclavé entre les montagnes majestueuses, une jeune fille nommée Elara. Elle était connue pour sa curiosité débordante et son amour pour les étoiles. Chaque nuit, Elara s'évadait secrètement de sa chambre pour contempler le ciel étoilé, rêvant de voyages interstellaires. Un soir, alors qu'elle fixait une étoile particulièrement brillante, une étrange lueur enveloppa soudainement le village. Les habitants, inquiets, se rassemblèrent sur la place centrale, où Elara les rejoignit avec son regard émerveillé. L'étoile se révéla être une entité magique, un guide vers un royaume céleste. Audacieuse et intrépide, Elara décida de suivre cette lueur mystique. Elle fut transportée dans un monde éblouissant, où des constellations prenaient vie. Avec détermination, elle entreprit un voyage épique à travers les cieux, rencontrant des créatures magiques et surmontant des épreuves cosmiques. Finalement, Elara atteignit le sommet des étoiles, où elle découvrit le secret de la lumière éternelle. De retour dans son village, elle partagea sa merveilleuse aventure, inspirant les autres à rêver grand et à embrasser la magie qui réside au-delà de l'ordinaire. Et ainsi, le village, éclairé par la sagesse d'Elara, prospéra sous la lueur éternelle des étoiles."
    len_response = 0
    while len_response != number:
        response = g4f.ChatCompletion.create(model=g4f.models.gpt_35_long,
                                             messages=[{"role": "user", "content": f"{prompt} \n {text}"}],
                                             stream=False)
        len_response = len(re.findall(r"==(.*?)==", response))

        print(response)
        print(len(re.findall(r"==(.*?)==", response)))
        print(len(re.findall(r"[{\[](.*?)[}\]]", response)))
    return [re.findall(r"==(.*?)==", response), re.findall(r"[{\[](.*?)[}\]]", response)]


def gen_token():
    xcfr = re.findall(r'A":"(.*?)"',
                      requests.get('https://www.canva.com/_ajax/csrf3/ingredientgeneration', cookies=cookies,
                                   headers=headers).text)
    return xcfr[0] if len(xcfr) > 0 else 0


def start_image_gen(inp, style):
    json_data = {
        'A?': 'A',
        'A': {
            'A': inp,
        },
        'B': 4,
        'C': 'C',
        'D': style,
    }
    response = requests.post('https://www.canva.com/_ajax/ingredientgeneration', cookies=cookies, headers=headers,
                             json=json_data)
    return response.status_code if response.status_code != 200 else re.findall(r'"A":"(.*?)"', response.text)


def check_if_finish(u, result):
    for i, uid in enumerate(u):
        if result[i] == uid:
            return True
    return False


def get_links(u):
    t = time.time()
    time.sleep(8)
    print("image en cour de génération")
    link_list = u
    for i, uid in enumerate(u):
        p = []
        params = {
            'jobId': uid,
        }
        while len(p) != 5:
            time.sleep(2)
            response = requests.get('https://www.canva.com/_ajax/ingredientgeneration', params=params,
                                    cookies=cookies,
                                    headers=headers)
            p = re.findall(r'B":"(.*?)"', response.text)
            print(response.status_code)
            print(p)
            if len(p) > 0:
                if p[0] == 'D':
                    p = [0, 0, 0, 0, 0]

        if p == [0, 0, 0, 0, 0]:
            link_list[i] = False
        else:
            p.pop(0)
            link_list[i] = p

    """    while len(p) != 5:
        response = requests.get('https://www.canva.com/_ajax/ingredientgeneration', params=params, cookies=cookies,
                                headers=headersjobId)
        p = re.findall(r'B":"(.*?)"', response.text)
        print(response)
        if len(p) > 0:
            if p[0] == 'D':
                return 'Erreur D'
        time.sleep(2)
    p.pop(0)"""
    print(f"images générées en {t - time.time()}")
    print(link_list)
    return link_list


def create_image(inp, style):
    """
    :param inp:
    :return: retourne un code d'erreur si erreur
    """
    token = gen_token()
    if token != 0:
        headers["X-Csrf-Token"] = token
    else:
        print('erreur cookie')
        return
    uid = start_image_gen(inp, style)
    link = get_links([uid])[0]
    return link


def download_images(links, output_folder='images'):
    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_folder, exist_ok=True)

    for i, link in enumerate(links):
        try:
            # Obtenir le contenu de l'image
            response = requests.get(link)
            response.raise_for_status()

            # Enregistrer l'image dans le dossier de sortie
            image_path = os.path.join(output_folder, f'image_{i + 1}.jpg')
            with open(image_path, 'wb') as file:
                file.write(response.content)

            print(f"Image {i + 1} téléchargée avec succès: {image_path}")

        except requests.exceptions.RequestException as e:
            print(f"Échec du téléchargement de l'image {i + 1}. Erreur : {e}")


def main(number=None, text=None, style='FANTASY', root=None):
    if number is None:
        number = int(input("combien d'images?"))
    if text is None:
        text = input('script à illustrer:')
    token = gen_token()
    if token == 0:
        print('cookies invalide')
        exit()
    else:
        headers['X-Csrf-Token'] = token

    prompts = text_to_prompts(number=number, text=text)
    print("génération des images chargement...")
    uidlist = []
    for prompt in prompts[0]:
        uid = start_image_gen(prompt, style)
        if isinstance(uid, int):
            error_code = uid
            if error_code == 418:
                print("génération d'image impossible. \n    erreur probable: XCFR_TOKEN invalide")
            else:
                print(f"Erreur. Code d'erreur{error_code}")
                print('cookies: ', cookies, '\nheaders:', headers)
        else:
            uidlist.append(uid)
    links = get_links(uidlist)
    print(links)
    for j, l in enumerate(links):
        if l is False:
            print('prompt non conforme', prompts[0][j], '\n', prompts[1][j])
            new = False
            while new is False:
                print("prompt non conforme")
                new = create_image(input('modifier: '), style)
            links[j] = new
            print(links)
    ui.main(links, prompts[1], root)


if __name__ == '__main__':
    token = gen_token()
    if token != 0:
        headers["X-Csrf-Token"] = token
    else:
        print('erreur cookie')
    uid = start_image_gen('test', 'FILM')
    print(uid)
    print(get_links(uid))
