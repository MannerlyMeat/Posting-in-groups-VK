import vk_api
from typing import Any
from vk_api import VkUpload
import requests
import vk
import datetime
import time
import json
import numpy as np
import getpass
import os.path


def post_script():

    #выгрузка id групп
    groups = np.loadtxt("groups_id.txt", delimiter='\t', dtype=np.int)
    #подсчет элементов в массиве
    temp = len(groups)
    app_id = open('app_id.txt')
    
    
    login = input('Введите логин: ')
    password = getpass.getpass('Введите пароль: ')
    
    
    p=0
    
    try:
       #данные авторизации
        scope = 'photos, wall, groups'
        #авторизация в ВК
        session = vk.AuthSession(app_id, login, password, scope)
        vk_api = vk.API(session, v='5.124')
    except vk.exceptions.VkAuthError as er:
        input("Логин или пароль введены неверно. Нажмите Enter, чтобы продолжить")
        exit()
    
    img_yn = input("Прикрепить фотографию к записи? [Y/N] ")
    if img_yn == 'Y' or img_yn == 'y':
        img_yn = 1
        image = input("Введите название фотографии с расширением: ")
        while os.path.exists(image) == False:
            print('Такого файла не существует')
            image = input("Введите название фотографии с расширением: ")
    else:
        img_yn = 0

        
    textf = input("Введите название фалйа с текстом: ")
    while os.path.exists(textf + '.txt') == False:
        print('Такого файла не существует')
        textf = input("Введите название фалйа с текстом: ")

    link_yn = input("Прикрепить ссылку [Y/N] ")
    if link_yn == 'Y' or link_yn == 'y':
        link_yn = 1
        post_link = str(input('Вставьте ссылку: '))
    else:
        link_yn = 0
        
    #цикл постинга    
    for i in range(temp):
        text = open(textf + '.txt')
        #постинг в группу по порядковому номеру в массиве + получение данных о сервре для загрузки фото и её загрузка
        pos_group_id = groups[i]
        tempid = abs(pos_group_id)
        if img_yn == 1:
            upl_server = vk_api.photos.getWallUploadServer(group_id=tempid)
            upl_url = upl_server['upload_url']
            img = {'photo':(open(image, 'rb'))}
            upl_request = requests.post(upl_url, files = img)
            temp_server = upl_request.json()
            temp_hash = temp_server['hash']
            temp_photo = temp_server['photo']
            temp_server = temp_server['server']
            upl_done = vk_api.photos.saveWallPhoto(group_id = tempid, server = temp_server, photo = temp_photo, hash = temp_hash)
            temp = upl_done[0]
            owner = str(temp['owner_id'])
            photo_id = str(temp['id'])
            
        #постинг в группу
        gr_pos = abs(groups[i])
        try:
            if img_yn == 1 and link_yn == 0:
                vk_api.wall.post(message=' '.join(map(str,text)), owner_id=groups[i], attachments="photo"+owner+"_"+photo_id)
                time.sleep(5)
            elif img_yn == 0 and link_yn == 0:
                vk_api.wall.post(message=' '.join(map(str,text)), owner_id=groups[i])
                time.sleep(5)
            elif img_yn == 0 and link_yn == 1:
                vk_api.wall.post(message=' '.join(map(str,text)) + "\n Ссылка - " + post_link, owner_id=groups[i])
                time.sleep(5)
            elif img_yn == 1 and link_yn == 1:
                vk_api.wall.post(message=' '.join(map(str,text)) + "\n Ссылка - " + post_link, owner_id=groups[i], attachments="photo"+owner+"_"+photo_id)
                time.sleep(5)
            print('Успешно')
            
            p+=1
        except vk.exceptions.VkAPIError as er:
            print('Стена закрыта или другая ошибка')
            print(er)
            time.sleep(5)
    print("Успешно сделаных записей - " + str(p))
    input("Нажмите Enter для продлжения")

post_script()
