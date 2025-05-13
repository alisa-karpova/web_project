import sqlite3


def check(form):
    level = form.level.data
    style = form.style.data

    message = ''

    # проверяем, есть ли ошибки
    if level == 'beginner':
        if style != 'base':
            message = 'Измените уровень катания, если Вы уже освоили базовую технику'
        elif form.high_tramps.data:
            message = 'Для выполнения трюков с больших трамплинов необходим уровень катания "Профи"'
        else:
            message = 'Все данные заполнены корректно'

    elif style == 'base':
        message = 'Измените уровень катания, если Вы ещё не освоили базовую технику'

    elif level == 'experienced' and form.high_tramps.data:
        message = 'Для выполнения трюков с больших трамплинов необходим уровень катания "Профи"'

    elif ('freestyle' not in style) and form.high_tramps.data:
        message = 'Выберите "Фристайл" / "Карвинг и фристайл", если будете прыгать с больших трамплинов'

    else:
        message = 'Все данные заполнены корректно'

    return message


def find_snowboard(form):
    con = sqlite3.connect('db/snb.db')
    cur = con.cursor()

    level = form.level.data
    style = form.style.data
    high_tramps = form.high_tramps.data

    # определяем характеристики сноуборда
    if level == 'beginner':
        stiffness = '1'      # жесткость: низкая
        shape = '1'          # форма: Twin Tip
        deflection = '4678'  # прогиб: Flying V (C2BTX), Flat, Flat Top, Rocker
        height = '2'         # ростовка: средняя

    elif level == 'experienced':
        if style == 'carving':
            stiffness = '2'       # жесткость: средняя
            shape = '123'         # форма: любая
            deflection = '12345'  # прогиб: все разновидности Camber
            height = '2'          # ростовка: средняя

        elif style == 'freestyle':
            stiffness = '12'        # жесткость: низкая, либо средняя
            shape = '1'             # форма: Twin Tip
            deflection = '1245678'  # прогиб: все, кроме Directional Camber
            height = '12'           # ростовка: низкая, либо средняя

        elif style == 'freeride':
            stiffness = '2'       # жесткость: средняя
            shape = '2'           # форма: Directional
            deflection = '23457'  # прогиб: все, кроме Camber, Flat и Rocker
            height = '2'          # ростовка: средняя

        elif style == 'carving_freestyle':
            stiffness = '2'      # жесткость: средняя
            shape = '1'          # форма: Twin Tip
            deflection = '1245'  # прогиб: Camber, Camrock, Flying V (C2BTX), Pure Pop Camber
            height = '2'         # ростовка: средняя

        elif style == 'carving_freeride':
            stiffness = '2'      # жесткость: средняя
            shape = '2'          # форма: Directional
            deflection = '2345'  # прогиб: Camrock, Directional Camber, Flying V (C2BTX), Pure Pop Camber
            height = '2'         # ростовка: средняя

    else:
        if style == 'carving':
            stiffness = '23'  # жесткость: средняя, либо высокая
            shape = '123'     # форма: любая
            deflection = '1'  # прогиб: Camber
            height = '23'     # ростовка: средняя, либо высокая

        elif style == 'freestyle':
            stiffness = '12'       # жесткость: низкая, либо средняя
            shape = '13'           # форма: Twin Tip, либо Directional Twin
            deflection = '124678'  # прогиб: все, кроме Directional Camber (Directional Rocker)
            height = '12'          # ростовка: низкая, либо средняя
            if form.high_tramps.data:
                stiffness = '3'     # жесткость: высокая
                deflection = '125'  # прогиб: Camber, Camrock, Pure Pop Camber
                height = '2'        # ростовка: средняя

        elif style == 'freeride':
            stiffness = '23'     # жесткость: средняя, либо высокая
            shape = '2'          # форма: Directional
            deflection = '2347'  # прогиб: Camrock, Directional Camber, Flying V (C2BTX), Flat Top
            height = '23'        # ростовка: средняя, либо высокая

        elif style == 'carving_freestyle':
            stiffness = '2'     # жесткость: средняя
            shape = '1'         # форма: Twin Tip, либо Directional Twin
            deflection = '125'  # прогиб: Camber, Camrock, Pure Pop Camber
            height = '2'        # ростовка: средняя
            if high_tramps:
                stiffness = '3'   # жесткость: высокая
                deflection = '1'  # прогиб: Camber

        elif style == 'carving_freeride':
            stiffness = '23'  # жесткость: средняя, либо высокая
            shape = '23'      # форма: Directional, либо Directional Twin
            deflection = '3'  # прогиб: Directional Camber (Directional Rocker)
            height = '23'     # ростовка: средняя, либо высокая

    # изменение типа данных для SQL-запросов
    params = [stiffness, shape, deflection, height]
    params = [int(par) if len(par) == 1 else tuple([int(el) for el in list(par)]) for par in params]

    # операторы для SQL-запросов (зависят от количества элементов в кортеже)
    qs = ['=' if type(par) is int else 'in' for par in params]

    # рост и вес пользователя
    height = form.height.data
    weight = form.weight.data

    # поиск соответствующего роста и веса в БД
    wts = [el[0] for el in cur.execute("""SELECT DISTINCT вес FROM heights""").fetchall()]
    if weight not in wts:
        min_w = 100
        for i in range(len(wts)):
            if abs(wts[i] - weight) < min_w:
                min_w = abs(wts[i] - weight)
                ind_w = i
        db_w = wts[ind_w]
    else:
        db_w = weight

    hts = [el[0] for el in cur.execute(f'SELECT рост from heights WHERE вес = {db_w}').fetchall()]
    if height not in hts:
        min_h = 100
        for i in range(len(hts)):
            if abs(hts[i] - height) < min_h:
                min_h = abs(hts[i] - height)
                ind_h = i
        db_h = hts[ind_h]
    else:
        db_h = height

    # список результатов запросов на получение характеристик сноуборда
    res = [cur.execute(f"SELECT жесткость FROM types_of_stiffness WHERE id {qs[0]} {params[0]}").fetchall(),
           cur.execute(f"SELECT форма FROM shapes WHERE id {qs[1]} {params[1]}").fetchall(),
           cur.execute(f"SELECT прогиб FROM deflections WHERE id {qs[2]} {params[2]}").fetchall(),
           cur.execute(f"SELECT ростовка FROM heights WHERE (вес = {db_w}) and (рост = {db_h})").fetchall()]

    # результаты с названиями характеристик
    # создание поля необходимо для записи результатов в БД
    res = [', '.join([str(el[0]) for el in res[i]]) for i in range(len(res))]

    return res