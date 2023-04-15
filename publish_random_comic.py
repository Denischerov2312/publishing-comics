import os
import random
from os.path import split, splitext
from urllib.parse import unquote, urlsplit

import requests
from dotenv import load_dotenv


def get_upload_url(token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': token,
        'v': 5.131,
        'group_id': group_id,
        }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def get_file_extension(url):
    filepath = unquote(urlsplit(url).path)
    file_extension = splitext(split(filepath)[1])[1]
    return file_extension


def download_picture(url, filepath):
    response = requests.get(url)
    response.raise_for_status()
    with open(filepath, "wb") as file:
        file.write(response.content)
    return filepath


def download_comic(comic_id):
    url = f'https://xkcd.com/{comic_id}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic = response.json()
    image_url = comic['img']
    extension = get_file_extension(image_url)
    filepath = f"{comic['safe_title']}{extension}"
    download_picture(image_url, filepath)
    return comic, filepath


def upload_photo_to_server(filepath, upload_url):
    with open(filepath, 'rb') as file:
        files = {
            'photo': file
            }
        response = requests.post(upload_url, files=files)
    response.raise_for_status()
    args = response.json()
    return args['photo'], args['hash'], args['server']


def add_photo_to_album(photo, hash, server, token, group_id):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'photo': photo,
        'access_token': token,
        'hash': hash,
        'server': server,
        'v': '5.131',
        'group_id': group_id,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def add_photo_to_wall(message, attachments, token):
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


def publish_comic(photo, hash, server, token, group_id, comic):
    album_response = add_photo_to_album(photo, hash, server, token, group_id)
    attachments = get_attachments(album_response)
    message = comic['alt']
    post_response = add_photo_to_wall(message, attachments, token)
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
    token = os.environ['ACCESS_TOKEN']
    group_id = os.environ['GROUP_ID']
    comic_id = get_random_comic_id()
    try:
        comic, filepath = download_comic(comic_id)
        upload_url = get_upload_url(token, group_id)
        photo, hash, server = upload_photo_to_server(filepath, upload_url)
        post_response = publish_comic(photo, hash, server, token, group_id, comic)
    finally:
        os.remove(filepath)
    print(post_response)


if __name__ == '__main__':
    main()
