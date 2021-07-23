from pprint import pprint
import requests
from tqdm import tqdm
from time import sleep
from tqdm import trange
import json

class Add_VK_foto_in_YaDi:

    def __init__(self, token_VK, token_YaDi):
        self.token_VK = token_VK
        self.token_YaDi = token_YaDi

    def token_vk(self):
        with open(self.token_VK, encoding='utf-8') as f:
            token_vk = f.read().strip()
            return token_vk

    def VK_photo(self):
        URL = 'https://api.vk.com/method/photos.get'
        token = self.token_vk()
        params = {
            'access_token': token,
            'v': '5.131',
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': '5',
            'rev': '1'
        }
        res = requests.get(URL, params).json()['response']['items']
        photo_album = []
        likes_list = []
        for photo in res:
            photo_dict = {}
            if photo['likes']['count'] not in likes_list:
                name = str(photo['likes']['count'])
                likes_list.append(photo['likes']['count'])
            else:
                name = str(photo['likes']['count']) + str(photo['date'])
            photo_dict['file_name'] = name
            for i in photo['sizes']:
                s_max = 0
                s = int(i['height']) * int(i['width'])
                if s > s_max:
                    photo_dict['sizes'] = i['type']
                    photo_dict['link'] = i['url']
                    s_max = s
            photo_album.append(photo_dict)
        pprint(photo_album)
        return photo_album

    def token_yadi(self):
        with open(self.token_YaDi, encoding='utf-8') as f:
            token_yadi = f.read().strip()
            return token_yadi

    def upload(self):
        folder_name = input('Bведите имя папки для скачивания:')
        token = self.token_yadi()
        url = 'https://cloud-api.yandex.net/v1/disk/resources?path=' + folder_name
        headers = {'Accept': 'application/json', 'Authorization': 'OAuth ' + token}
        r = requests.put(url, headers=headers)
        if r.status_code == 201:
            pprint(f'Создана папка {folder_name}')
        else:
            folder_name = input(f'Папка {folder_name} уже существует, введите имя новой папки:')
            token = self.token_yadi()
            url = 'https://cloud-api.yandex.net/v1/disk/resources?path=' + folder_name
            headers = {'Accept': 'application/json', 'Authorization': 'OAuth ' + token}
            r = requests.put(url, headers=headers)
            pprint(f'Создана папка {folder_name}')
        file_list = self.VK_photo()
        for file in file_list:
            params = {
                'path': f"{folder_name}/{file['file_name']}",
                'url': f"{file['link']}"
            }
            url = "https://cloud-api.yandex.net/v1/disk/resources/upload/"
            req = requests.post(url=url, params=params, headers=headers)
            if req.status_code == 202:
                pprint(f"Фотография {file['file_name']} загружена успешно")

for it in trange(5):
    sleep(.01)

if __name__ == '__main__':
    uploader = Add_VK_foto_in_YaDi('D:\\Study_Pyton\\dip_par\\token_VK.txt', 'D:\\Study_Pyton\\dip_par\\token_YaDi.txt')
    uploader.VK_photo()
    uploader.upload()


