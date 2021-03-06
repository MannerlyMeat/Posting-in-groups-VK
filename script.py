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
from random import randint

timer = 0
#global groups

def post_script():

    #выгрузка id групп
    global groups
    global vk_api
    global text
    global i
    global owner
    global photo_id
    global post_link
    
    groups = np.loadtxt("groups.txt", delimiter='\t', dtype=np.int)
    #print(groups)
    #подсчет элементов в массиве
    try:
        temp = len(groups)
    except TypeError:
        print("В файле с группами должно быть больше одной группы")
        input("Нажмите Enter для продолжения")
        exit()
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
                text_and_image()             
            elif img_yn == 0 and link_yn == 0:
                only_text()
            elif img_yn == 0 and link_yn == 1:
                text_and_link()
            elif img_yn == 1 and link_yn == 1:
                image_and_link()

            print('Успешно')

            p+=1
            if p == 50:
                break
        except vk.exceptions.VkAPIError as er:
            print('Стена закрыта или другая ошибка')
            print(er)
            time.sleep(5)
    print("Успешно сделаных записей - " + str(p))
    input("Нажмите Enter для продлжения")


def random_time():
    global timer
    timer = randint(20,40)

def delete_from_list():
    f = open("groups.txt")
    output = []
    for line in f:
        if not str(groups[i]) in line:
            output.append(line)
    f.close()
    f = open("groups.txt", "w")
    f.writelines(output)
    f.close()


def only_text():
    vk_api.wall.post(message=' '.join(map(str,text)), owner_id=groups[i])
    post_id = vk_api.wall.get(owner_id = groups[i], count = 1)
    post_id = post_id['items']
    post_id = post_id[0]
    post_id = post_id['id']
    with open("post_address.txt", "a") as file:
        file.write("vk.com/wall" + str(groups[i]) + "_" + str(post_id)+ "\n")
    delete_from_list()
    random_time()
    print(timer)
    time.sleep(int(timer))


def text_and_image():
    vk_api.wall.post(message=' '.join(map(str,text)), owner_id=groups[i], attachments="photo"+owner+"_"+photo_id)
    post_id = vk_api.wall.get(owner_id = groups[i], count = 1)
    post_id = post_id['items']
    post_id = post_id[0]
    post_id = post_id['id']
    with open("post_address.txt", "a") as file:
        file.write("vk.com/wall" + str(groups[i]) + "_" + str(post_id)+ "\n")
    delete_from_list()
    random_time()
    print(timer)
    time.sleep(int(timer)) 


def text_and_link():
    vk_api.wall.post(message=' '.join(map(str,text)) + "\n Ссылка - " + post_link, owner_id=groups[i])
    post_id = vk_api.wall.get(owner_id = groups[1], count = 1)
    post_id = post_id['items']
    post_id = post_id[0]
    post_id = post_id['id']
    with open("post_address.txt", "a") as file:
        file.write("vk.com/wall" + str(groups[i]) + "_" + str(post_id)+ "\n")
    delete_from_list()
    random_time()
    print(timer)
    time.sleep(int(timer))


def image_and_link():
    vk_api.wall.post(message=' '.join(map(str,text)) + "\n Ссылка - " + post_link, owner_id=groups[i], attachments="photo"+owner+"_" + photo_id)
    post_id = vk_api.wall.get(owner_id = groups[1], count = 1)
    post_id = post_id['items']
    post_id = post_id[0]
    post_id = post_id['id']
    with open("post_address.txt", "a") as file:
        file.write("vk.com/wall" + str(groups[i]) + "_" + str(post_id)+ "\n")
    delete_from_list()
    random_time()
    print(timer)
    time.sleep(int(timer))    
    
post_script()
#random_time()
