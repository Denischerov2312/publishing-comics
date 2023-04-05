import os
import random
from pathlib import Path, PurePosixPath
from os.path import split, splitext
from urllib.parse import unquote, urlsplit

import requests
from dotenv import load_dotenv


def get_upload_url_on_server(token):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': token,
        'v': 5.131,
        'group_id': 218983997,
        }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


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
    return filepath


def make_directory(filepath):
    path = PurePosixPath(filepath)
    directory_path = list(path.parents)[0]
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def download_comic(id):
    url = f'https://xkcd.com/{id}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    image_url = comic['img']
    extension = determine_file_extension(image_url)
    filepath = f"{comic['safe_title']}{extension}"
    download_picture(image_url, filepath)
    return comic, filepath


def upload_photo(photo_path, upload_url):
    with open(photo_path, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
    return response.json()


def upload_photo_to_server(filepath, token):
    upload_url = get_upload_url_on_server(token)
    with open(filepath, 'rb') as file:
        files = {
            'photo': file
            }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
    return response.json()


def upload_photo_to_album(args, token):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'photo': args['photo'],
        'access_token': token,
        'hash': args['hash'],
        'server': args['server'],
        'v': '5.131',
        'group_id': 218983997,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def upload_photo_to_wall(message, attachments, token):
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'v': '5.131',
        'access_token': token,
        'owner_id': -218983997,
        'from_group': 0,
        'message': message,
        'attachments': attachments,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def get_attachments(response):
    owner_id = response['response'][0]['owner_id']
    media_id = response['response'][0]['id']
    attachments = [f'photo{owner_id}_{media_id}']
    return attachments


def publicate_comic(id, token):
    comic, filepath = download_comic(id)
    server_response = upload_photo_to_server(filepath, token)
    album_response = upload_photo_to_album(server_response, token)
    attachments = get_attachments(album_response)
    message = comic['alt']
    post_response = upload_photo_to_wall(message, attachments, token)
    os.remove(filepath)
    return post_response


def get_random_comic_id():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    total_comics = response.json()['num']
    random_id = random.randrange(1, total_comics + 1)
    return random_id


def main():
    load_dotenv()
    token = os.getenv('ACCESS_TOKEN')
    id = get_random_comic_id()
    response = publicate_comic(id, token)
    print(response)


if __name__ == '__main__':
    main()
