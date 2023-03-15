import os
from pathlib import Path, PurePosixPath
from pprint import pprint
from os.path import split, splitext
from urllib.parse import unquote, urlsplit

import requests
from dotenv import load_dotenv


def get_upload_url_on_server(token):
    url = f'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': token,
        'v': 5.131,
        'group_id': 40498005,
        }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def get_upload_url_wall(token):
    url = f'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': token,
        'v': 5.131,
        'group_id': 40498005,
        }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response


def determine_file_extension(url):
    filepath = unquote(urlsplit(url).path)
    file_extension = splitext(split(filepath)[1])[1]
    return file_extension


def download_picture(url, filepath):
    response = requests.get(url)
    response.raise_for_status()
    make_directory(filepath)
    with open(filepath, "wb") as file:
        file.write(response.content)


def make_directory(filepath):
    path = PurePosixPath(filepath)
    directory_path = list(path.parents)[0]
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def download_comics():
    url = 'https://xkcd.com/614/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics = response.json()
    image_url = comics['img']
    download_picture(image_url, f'comics{determine_file_extension(image_url)}')
    return comics
    


def upload_photo(photo_path, upload_url):
    with open(photo_path, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
    return response.json()


def upload_photo_to_server(path ,token):
    upload_url = get_upload_url_on_server(token)
    with open(path, 'rb') as file:
        files = {
            'photo': file
            }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
    return response.json()


def upload_photo_to_album(args):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'photo': args['photo'],
        'access_token': token,
        'hash': args['hash'],
        'server': args['server'],
        'v': '5.131',
        'group_id': 40498005,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def main(token):
    comics = download_comics()
    response_server = upload_photo_to_server('comics.png', token)
    response_album = upload_photo_to_album(response_server)
    
    owner_id = response_album['response'][0]['owner_id']
    media_id = response_album['response'][0]['id']
    attachments = [f'photo{owner_id}_{media_id}']

    url = 'https://api.vk.com/method/wall.post'

    params = {
        'v': '5.131',
        'access_token': token,
        'owner_id': -218983997,
        'from_group': 0,
        'message': comics['alt'],
        'attachments': attachments,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    pprint(response.json())

    

if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('ACCESS_TOKEN')
    main(token)
