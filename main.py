import random
import copy
import time

list_dict_combination = [
    {'11': 'O', '12': 'O', '13': 'O', '14': 'O', '15': 'O', '16': 'O'},
    {'21': 'O', '22': 'O', '23': 'O', '24': 'O', '25': 'O', '26': 'O'},
    {'31': 'O', '32': 'O', '33': 'O', '34': 'O', '35': 'O', '36': 'O'},
    {'41': 'O', '42': 'O', '43': 'O', '44': 'O', '45': 'O', '46': 'O'},
    {'51': 'O', '52': 'O', '53': 'O', '54': 'O', '55': 'O', '56': 'O'},
    {'61': 'O', '62': 'O', '63': 'O', '64': 'O', '65': 'O', '66': 'O'}]

list_dict_combination_user = copy.deepcopy(list_dict_combination)
list_dict_combination_comp = copy.deepcopy(list_dict_combination)

def list_key_combination(ls_comb): # список всех ключей
    keys = []
    for i in ls_comb:
        for j in list(i.keys()):
            keys.append(j)
    return keys

list_key_check = list_key_combination(list_dict_combination) # список всех ключей user
list_key_user = copy.deepcopy(list_key_check) # не зависимые дубликаты списка всех ключей, будут удаляться использованные ключи
list_key_comp = copy.deepcopy(list_key_check)

class Board:

    def __init__(self, ls_comb, user_comp):
        self.ls_comb = ls_comb
        self.user_comp = user_comp
        list_screen = [[' ', '1', '2', '3', '4', '5', '6'], ]
        num_str = 1
        temp = []
        if self.user_comp == 'user':
            print('===========================')
            print('Ваше поле')
        if self.user_comp == 'comp':
            print('===========================')
            print('Поле компьютра')

        for i in ls_comb[:6]:
            temp = list(i.values()) # список значений словаря по строчно
            temp.insert(0, str(num_str)) #вставлем нумерацию на нулевую позицию в каждую строку
            list_screen.append(temp) # состовлем список из списков значений словаря
            num_str += 1 # увеличиваем нумерацию на каждую строку
        for i in list_screen: # каждый список выводим по символьно с интевалом и |
            print(*[f"{x + ' |':>2}" for x in i])  # 3 - размер отступов

def update_list_dict_combination(key, ls_comb, k_comb, symb):
    symbol = symb
    for i in ls_comb:
        for j in i.keys():
            if j == key:
                if symbol == '■':
                    i[j] = symbol
                if symbol == 'X':
                    i[j] = symbol
                if symbol == '◦':
                    i[j] = symbol
    k_comb.remove(key)

def shut_computer(ls_comb, k_comb, num_ship):
    global num_ship_user_chk
    ls_diff = [] # для раненых
    temp = []

    for i in range(0, 3): # проверяет есть ли раненые корабли
        for num in num_ship_user_chk[i]:
            if num not in num_ship[i] and (len(num_ship[i]) == 2 or len(num_ship[i]) == 1):
                ls_diff.append(num) # если есть раненые, то бить будет рядом с этими клетками

    if len(ls_diff) == 2: # если две клетки трехпалубного подбита, то следующий выбор только справа-слева или свехи-снизу
        if (int(ls_diff[1]) - int(ls_diff[0])) == 1:
            if str(int(ls_diff[0]) - 1) in k_comb:
                temp.append(str(int(ls_diff[0])-1))
            if str(int(ls_diff[1]) + 1) in k_comb:
                temp.append(str(int(ls_diff[1])+1))
        if (int(ls_diff[1]) - int(ls_diff[0])) == 10:
            if str(int(ls_diff[0]) - 10) in k_comb:
                temp.append(str(int(ls_diff[0])-10))
            if str(int(ls_diff[1]) + 10) in k_comb:
                temp.append(str(int(ls_diff[1])+10))
        return random.choice(temp)

    if len(ls_diff) == 1:   #  # если подбита одна клетка в каком-либо корабле  # то следующий ход только рядом рандом
        if str(int(ls_diff[0]) - 1) in k_comb:
            temp.append(str(int(ls_diff[0]) - 1))
        if str(int(ls_diff[0]) + 1) in k_comb:
            temp.append(str(int(ls_diff[0]) + 1))
        if str(int(ls_diff[0]) - 10) in k_comb:
            temp.append(str(int(ls_diff[0]) - 10))
        if str(int(ls_diff[0]) + 10) in k_comb:
            temp.append(str(int(ls_diff[0]) + 10))
        return random.choice(temp)

    for i in range(0, 7): # проверяет есть ли потопленные корабли
        if num_ship_user_chk[i] not in num_ship: # если есть
            area_around_ship(num_ship_user_chk[i], ls_comb, k_comb) # удаляем поля вокруг корабля

    return random.choice(k_comb)

def shut(n_key, ls_comb, k_comb, num_ship, user_comp):
    for i in num_ship:
        for j in i:
            if j == n_key:
                i.remove(n_key) # удалить из списка кораблей
                if len(i) == 0:
                    update_list_dict_combination(n_key, ls_comb, k_comb, 'X')
                    print('КОРАБЛЬ ПОТОПЛЕН')
                    # print(f'num_ship {num_ship}')
                    # print(f'num_ship {len(num_ship)}')
                    if not any(num_ship):
                        return 1, user_comp # 1 - закончились корабли, победа , (user_comp - чтоб что-то передать)
                    return 0, user_comp # 0 - корабли еще есть, (0 - повторный ход usera, 1 - повторный ход computera)
                else:
                    update_list_dict_combination(n_key, ls_comb, k_comb, 'X')
                    print('КОРАБЛЬ ПОДБИТ НЕМНОГО')
                    return 0, user_comp # 0 - корабли еще есть, (0 - повторный ход usera, 1 - повторный ход computera)
    update_list_dict_combination(n_key, ls_comb, k_comb, '◦')
    print('ПРОМАХ')
    if user_comp == 1:
        return 0, 0 # 0 - корабли еще есть, (1 - передать ход компьютеру, 0 - передать ход пользователю)
    return 0, 1

def set_ship_board(ls_comb, k_comb):
    ship = []
    num_ship = []
    ship_deck = [[1, 3], [2, 2], [4, 1]]
    horiz_or_vert = [1, 10]  # 1 - горизонтально, 10 - вертикально
    key_start_ship = ''
    key_temp = ''
    for i in ship_deck: # берем список
        for j in range(0, i[0]): #первое число количество кораблей
            while True: # ставим корабль пака не войдет
                try: # если k_comb пустой random выдает ошибку
                    key_start_ship = random.choice(k_comb)  # определяем нос корабля в списке оставшихся полей
                except:
                    # print('не возможно установить корабли')
                    return False

                horiz_or_vert_ship_set = random.choice(horiz_or_vert)  # вертикально или горозонтально располагается корабль - 1 или 10
                if k_comb.count(str(int(key_start_ship) + horiz_or_vert_ship_set * (i[1] - 1))) == 0: # проверяем войдет ли корабль в поле
                    continue # нет - продолжаем искать место
                break

            for k in range(0, i[1]): # второе число количество палуб
                key_temp = str(int(key_start_ship) + k * horiz_or_vert_ship_set) # прибавляем по одной клетке
                ship.append(key_temp) # добавлем клетку, собираем корабль
                update_list_dict_combination(key_temp, ls_comb, k_comb, '■')

            num_ship.append(ship)
            area_around_ship(ship, ls_comb, k_comb)
            ship = []

    return num_ship

def area_around_ship(ship, ls_comb, k_comb):
    for i in ship:
        area_around_ship = [int(i) - 1, int(i) + 1, int(i) - 10, int(i) + 10,
                            int(i) - 1 + 10, int(i) - 1 - 10, int(i) + 1 - 10, int(i) + 1 + 10]
        for j in area_around_ship:
            if k_comb.count(str(j)):
                k_comb.remove(str(j))
    return area_around_ship

while True: # пока все корабли не встанут
    list_dict_combination_user = copy.deepcopy(list_dict_combination)
    list_key_user = copy.deepcopy(list_key_check)
    num_ship_user = set_ship_board(list_dict_combination_user, list_key_user)
    num_ship_user_chk = copy.deepcopy(num_ship_user) # т.к. ключи удаляются нужно в функции shut_computer выяснять, что удалили
    if num_ship_user:
       break

while True: # пока все корабли не встанут
    list_dict_combination_comp = copy.deepcopy(list_dict_combination)
    list_key_comp = copy.deepcopy(list_key_check)
    num_ship_comp = set_ship_board(list_dict_combination_comp, list_key_comp)
    if num_ship_comp:
       break

class Game:
    global num_ship_user
    global num_ship_comp

    def __init__(self, ls_comb, ls_comb_user, ls_comb_comp, k_comb):
        self.ls_comb = ls_comb
        self.ls_comb_user = ls_comb_user
        self.ls_comb_comp = ls_comb_comp
        self.k_comb = k_comb

        win = 0
        key_shut_comp = '0'
        k_comb_user = copy.deepcopy(k_comb)
        k_comb_comp = copy.deepcopy(k_comb)

        self.greet()

        while True:
            print('==========================================================')
            сomputer_step = input('Кто будет ходить первым? Введите: 0 - Вы, 1 - компьютер  :  ', )
            if сomputer_step not in ['0', '1']:
                print('Нет такого варианта. Введите 0 или 1')
                continue
            else:
                break
        while True:
            print('Показать корабли противника в начале игры?')
            show_ship = input('Введите: 0 - Не показывать, 1 - Показать  :  ', )
            if show_ship not in ['0', '1']:
                print('Нет такого варианта. Введите 1 или 0')
                continue
            else:
                break

        Board(ls_comb_user, 'user')

        if int(show_ship):
            Board(ls_comb_comp, 'comp')
        else:
            Board(ls_comb, 'comp')

        while True:
            if int(сomputer_step):
                print('=================================================')
                print('Ход компьютера')
                key_shut_comp = shut_computer(ls_comb_user, k_comb_user, num_ship_user) # если комп ранил, то будед бить по соседним клеткам
                print(f'Ход на поле {key_shut_comp}. Строка {list(key_shut_comp)[0]}. Колонка {list(key_shut_comp)[1]}.')
                self.comp_timer_think(0.06)
                win, сomputer_step = shut(key_shut_comp, ls_comb_user, k_comb_user, num_ship_user, 1)
                self.comp_timer_think(0.11)
                if win:
                    Board(ls_comb_user, 'user')
                    print('=================================================')
                    print('=============  Компьютер выйграл!  ==============')
                    print('=================================================')
                    print('Корабли противника')
                    Board(ls_comb_comp, 'comp')
                    break

                Board(ls_comb_user, 'user')
                Board(ls_comb, 'comp')

            if not int(сomputer_step):
                while True:
                    print('=================================================')
                    num_key = input('Ваш ход. Введите номер поля: номер строки и номер колонки (например 21)  : ', )
                    if num_key not in k_comb:  # доступные ходы будем проверять по списку ключей
                        print('Нет такого поля, введите правильные номер строки и номер колонки (например 21)')
                        continue
                    if num_key not in k_comb_comp:
                        print('Уже был ход на это поле')
                        continue
                    break
                print(f'Ход на поле {num_key}. Строка {list(num_key)[0]}. Колонка {list(num_key)[1]}.')
                self.comp_timer_think(0.06)
                win, сomputer_step = shut(num_key, ls_comb, k_comb_comp, num_ship_comp, 0)
                self.comp_timer_think(0.11)

                if win:
                    Board(ls_comb, 'comp')
                    print('=================================================')
                    print('===============  Вы выйграли!  ==================')
                    print('=================================================')
                    break
                Board(ls_comb, 'comp')

    def comp_timer_think(self, tm):
        for i in range(4):
            print('\r\u002f', end='')
            time.sleep(tm)
            print('\r\u002d', end='')
            time.sleep(tm)
            print('\r\u005c', end='')
            time.sleep(tm)
            print('\r\u00a6', end='')
            time.sleep(tm)

    def greet(self):
        print('==================================================')
        print('============     Приветсвуем вас     =============')
        print('============         в игре          =============')
        print('============       морской бой       =============')
        print('==================================================')
        print('============     формат ввода: xy    =============')
        print('============    x - номер строки     =============')
        print('============    y - номер колонки    =============')

Game(list_dict_combination, list_dict_combination_user, list_dict_combination_comp, list_key_check)


