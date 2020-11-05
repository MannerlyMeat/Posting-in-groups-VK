import vk_api
from typing import Any
from vk_api import VkUpload
from requests import get as request
import vk
import datetime
import time
import requests
import json
import numpy as np
import getpass


def parse_script():
    login = input('Введите логин: ')
    password = getpass.getpass('Введите пароль: ')
    app_id = open('app_id.txt')
    
    try:
        scope =  'photos, wall, groups'
        session = vk.AuthSession(app_id, login, password, scope)
        vk_api = vk.API(session, v='5.124')
    except vk.exceptions.VkAuthError as er:
        input("Логин или пароль введены неверно. Нажмите Enter, чтобы продолжить")
        exit()

    
    search_text = input('Введите ключевое слово: ') 


    groups = vk_api.groups.search(q=search_text,type='group',count = 1000, fields = 'wall')
    #c = groups.get('count')
    #print(c)
    #c = 10
    i=0
    o=0
    try:
        while i<1000:
            temp = groups.get('items')
            temp2 = temp[i]
            temp_cls = temp2['is_closed']
            temp3 = temp2['id']
            wall_info = temp2['wall']
            i+=1
            if temp_cls == 0 and wall_info == 1:
                with open("groups_id.txt", "r") as f:
                    if str(temp3) not in f.read():
                        with open("groups_id.txt", "a") as file:
                            file.write("-"+str(temp3)+'\n')
                o+=1
            #print(o)
    except IndexError:
        print()
    print('Получено групп - ' + str(o))
    input("Нажмите Enter для продлжения")


parse_script()
