import requests
import re
import time
import ui
import json
import g4f
import os


if os.path.isfile('data.json') is False:
    with open('data.json', 'w+') as file:
        print("set data")
        data = {
            "cookies": {
                "CID": "",
                "__cf_bm": ""
            },
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
                'X-Canva-Brand': "BAF5w_DLWm4",
            },
            "url": ""
        }
        json.dump(data, file, indent=2)
        file.close()

headers = {}
cookies = {}


def text_to_prompts(text=None, number=5):
    g4f.debug.logging = True
    print(number)
    with open("prompt.txt", "r+") as p:
        prompt = p.read().replace('__number__', str(number))
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


def create_cookies():
    global headers
    global cookies

    with open('data.json', 'r+') as c:
        t = json.load(c)
        cookies = t['cookies']
        headers = t['headers']
    response = re.findall(r'A":"(.*?)"',
                      requests.get('https://www.canva.com/_ajax/csrf3/ingredientgeneration', cookies=cookies,
                                   headers=headers).text)
    xcfr = response[0] if len(response) == 1 else 0
    if xcfr == 0:
        return 0
    else:
        headers['X-Csrf-Token'] = response[0]
        return



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
    print(response)
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
                    link_list[i] = False
                    break

        p.pop(0)
        link_list[i] = p

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
    token = create_cookies()
    if token == 0:
        print('cookies invalide')
        exit()

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
    with open("prompt.txt", "r+") as p:
        pass
    token = create_cookies()
    uid = start_image_gen('test', 'FILM')
    print(uid)
    print(get_links(uid))
