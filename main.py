print('Для работы нужно ввести цифру от 1 до 3.')
print('1 - Постинг. Если будет прикреплена фотография - нужно ввести полное название файла с расширением. Для файла с текстом достаточно ввести названия текстового файла')
print('2 - Парсинг. Получение списка групп в отдельный файл')
print('3 - Выход')

exitApp = True


while exitApp == True:
    answer = int(input('Введите от 1 до 3: '))
    if answer == 1:
        from script import post_script
        #exitApp = False
    elif answer == 2:
        from parse import parse_script
        #exitApp = False
    elif answer == 3:
        exit()
    else:
        #print('Введите от 1 до 3: ')
        answer = int(input('Введите от 1 до 3: '))
