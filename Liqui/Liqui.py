import urllib, http.client
import os
import time
import json
# эти модули нужны для генерации подписи API
import hmac, hashlib
import Exel

API_KEY = 'O0QLLYC7-HBSLNYZ4-250VL40D-YJA4OIL2-LYHE3SHX'# ключи API, которые предоставила liqui
API_SECRET = b'22d31445443cd255b370d194c3bdada5c056000176f929166ecdfbc7c643cb02' # обратите внимание, что добавлена 'b' перед строкой
# Тонкая настройка
CURRENCY_1 = 'myst' # на вторую валюту покупает первую. Потом перую продает, чтобы увеличить вторую. 
CURRENCY_2 = 'btc'  # Вторая валюта растет, а первая то обнуляется, то вырастает.
CURRENCY_1_DIGITS=8  
CURRENCY_1_MIN_QUANTITY = 0.1 # Это минимальная ставка, которая допускается на бирже. Для разных валют она разная, и, вообще, стоило бы получать её автоматически через API запрос. Но это усложнит код, поэтому я указал её как константу. Тем не менее, если вы планируете торговать другой валютой, вам следует поменять это значение, иначе торговля может затрудниться. 
CURRENT_PAIR = (CURRENCY_1 + '_' + CURRENCY_2).lower()
ORDER_LIFE_TIME = 3 # через сколько минут отменять неисполненный ордер на покупку CURRENCY_1
STOCK_FEE = 0.002 # Комиссия, которую берет биржа (0.002 = 0.2%)
AVG_PRICE_PERIOD = 90 # За какой период брать среднюю цену (по сделкам)
CAN_SPEND = 0.004 # Сколько тратить CURRENCY_2 при покупке CURRENCY_1. Бот будет пытаться создать ордера именно на эту сумму
PROFIT_MARKUP = 0.001 # Какой навар нужен с каждой сделки? (0.001 = 0.1%)
DEBUG = True# True - выводить отладочную информацию, False - писать как можно меньше
STOCK_TIME_OFFSET = 0 # Если расходится время биржи с текущим 
NONCE = 1   # (counter) Minimum nonce value - 1, maximum - 4294967294. To reset the nonce value you need to create a new key.
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
# базовые настройки
API_URL = 'api.liqui.io'  # All API requests are made from this address: https://api.liqui.io/api/3/<method_name>/<pair_listing>
API_VERSION = 'api/3'     # Currency pairs are hyphen-separated (-), e.g.: https://api.liqui.io/api/3/ticker/eth_btc-ltc_btc
# Свой класс исключений
class ScriptError(Exception):
    pass
class ScriptQuitCondition(Exception):
    pass


# все обращения к API проходят через эту функцию
def call_api(api_method, http_method="POST", public=True, **kwargs):
    payload = {}
    if not public:
        try:
            nonce_file = open(CURR_DIR + "/nonce", "r+")
        except FileNotFoundError:
            nonce_file = open(CURR_DIR + "/nonce", "w+")
        try:
            nonce = int(nonce_file.read())
        except ValueError:
            nonce = 0    
        nonce = (NONCE if not nonce else nonce)+1
        nonce_file.close()
        nonce_file = open(CURR_DIR + "/nonce", "w")
        nonce_file.write(str(nonce))
        nonce_file.close()
        payload = {'nonce': nonce}
    
    if kwargs:  # Если в ф-цию переданы параметры в формате ключ:значение
        payload.update(kwargs)# добавляем каждый параметр в словарь payload, получится {'nonce':123172368123, 'param1':'val1', 'param2':'val2'}    
    payload =  urllib.parse.urlencode(payload) # Переводим словарь payload в строку, в формат для отправки через GET/POST и т.п.
    H = hmac.new(key=API_SECRET, digestmod=hashlib.sha512) # Из строки payload получаем "подпись", хешируем с помощью секретного ключа API
    H.update(payload.encode('utf-8'))
    sign = H.hexdigest() # sing - получаемый ключ, который будет отправлен на биржу для проверки
    headers = {"Content-type": "application/x-www-form-urlencoded",   # Формируем заголовки request для отправки запроса на биржу.
           "Key":API_KEY,  # Передается публичный ключ API и подпись, полученная с помощью hmac
           "Sign":sign}
    conn = http.client.HTTPSConnection(API_URL, timeout=60) # Создаем подключение к бирже, если в течении 60 сек не удалось подключиться, обрыв соединения
    # запрашиваем переданный адрес, в заголовке запроса уходят headers, в теле - payload
    conn.request(http_method, ("" if public else '/tapi') + ("/"+API_VERSION if public else '')  + ("/"+ api_method  if public else ''), payload, headers)
    response = conn.getresponse().read()# Получаем ответ с биржи и читаем его в переменную response
    conn.close() # Закрываем подключение

    try:# Полученный ответ переводим в строку UTF, и пытаемся преобразовать из текста в объект Python
        obj = json.loads(response.decode('utf-8')) # JSON-формат обмена данными JavaScript, позволяет кодировать и декодировать данные в удобном формате.
        if 'error' in obj and obj['error']: # Смотрим, есть ли в полученном объекте ключ "error"
            raise ScriptError(obj['error']) # Если есть, выдать ошибку, код дальше выполняться не будет
        return obj # Вернуть полученный объект как результат работы ф-ции
    except json.decoder.JSONDecodeError:
        raise ScriptError('Ошибка анализа возвращаемых данных, получена строка', response)  # Если не удалось перевести полученный ответ (вернулся не JSON)

def CHECK():
    try:# Получаем список активных ордеров
        opened_orders_dict = call_api(api_method="", http_method="POST", public=False, method="ActiveOrders", pair=CURRENT_PAIR )['return']###
        opened_orders = []
        for order in opened_orders_dict:
            curr_order = opened_orders_dict[order]
            curr_order['order_id'] = order
            opened_orders.append(curr_order)
    except (KeyError, ScriptError):
        if DEBUG:
            print('Открытых ордеров нет') 

# Реализация алгоритма
def main_flow():
    try:
        try:# Получаем список активных ордеров
            opened_orders_dict = call_api(api_method="", http_method="POST", public=False, method="ActiveOrders", pair=CURRENT_PAIR )['return']###
            opened_orders = []
            for order in opened_orders_dict:
                curr_order = opened_orders_dict[order]
                curr_order['order_id'] = order
                opened_orders.append(curr_order)
        except (KeyError, ScriptError):
            if DEBUG:
                print('Открытых ордеров нет')
            opened_orders = []    
        sell_orders = []
        # Есть ли неисполненные ордера на продажу CURRENCY_1?
        for order in opened_orders:
            if order['type'] == 'sell':
                # Есть неисполненные ордера на продажу CURRENCY_1, выход
                raise ScriptQuitCondition('Выход, ждем пока не исполнятся/закроются все ордера на продажу (один ордер может быть разбит биржей на несколько и исполняться частями)')
            else:
                # Запоминаем ордера на покупку CURRENCY_1
                sell_orders.append(order)
                
        # Проверяем, есть ли открытые ордера на покупку CURRENCY_1
        if sell_orders: # открытые ордера есть
            for order in sell_orders:
                # Проверяем, есть ли частично исполненные
                if DEBUG:
                    print('Проверяем, что происходит с отложенным ордером', order['order_id'])

                order_history = call_api(api_method="", http_method="POST", public=False, method="OrderInfo", order_id=order['order_id'])['return'][order['order_id']]

                if order_history['status'] == 0 and order_history['start_amount'] != order_history['amount']:
                    
                    # по ордеру уже есть частичное выполнение, выход
                    raise ScriptQuitCondition('По ордеру уже есть частичное выполнение, выход, продолжаем надеяться докупить валюту по тому курсу, по которому уже купили часть')
                else:
                    if DEBUG:
                        print('Частично исполненных ордеров нет')
                    
                    time_passed = time.time() + STOCK_TIME_OFFSET*60*60 - int(order['timestamp_created'])

                    if time_passed > ORDER_LIFE_TIME * 60:
                        # Ордер уже давно висит, никому не нужен, отменяем
                        call_api(api_method="", http_method="POST", public=False, method="CancelOrder", order_id=order['order_id'])
                        raise ScriptQuitCondition('Отменяем ордер -за ' + str(ORDER_LIFE_TIME) + ' минут не удалось купить '+ str(CURRENCY_1))
                    else:
                        raise ScriptQuitCondition('Выход, продолжаем надеяться купить валюту по указанному ранее курсу')
                

        else: # Открытых ордеров нет
            balances = call_api(api_method="", http_method="POST", public=False, method="getInfo")['return']['funds']
            if float(balances[CURRENCY_1]) >= CURRENCY_1_MIN_QUANTITY: # Есть ли в наличии CURRENCY_1, которую можно продать?
                """
                    Высчитываем курс для продажи.
                    Нам надо продать всю валюту, которую купили, на сумму, за которую купили + немного навара и минус комиссия биржи
                    При этом важный момент, что валюты у нас меньше, чем купили - бирже ушла комиссия
                    0.00134345 1.5045
                """
                wanna_get =  "%.8f" % (CAN_SPEND + CAN_SPEND * (STOCK_FEE+PROFIT_MARKUP))  # сколько хотим получить за наше кол-во
                rate = "%.8f" % (float(wanna_get)/float(balances[CURRENCY_1]))
                print('sell', balances[CURRENCY_1], wanna_get, rate)
                
                new_order = call_api(api_method="", http_method="POST", public=False, method="Trade", pair=CURRENT_PAIR, type="sell", rate=rate, amount="%.8f" % (float(balances[CURRENCY_1]) - 0.0000001))['return']
            
                print(new_order)
                if DEBUG:
                    print('Создан ордер на продажу', CURRENCY_1, new_order['order_id'])
            else:
                # CURRENCY_1 нет, надо докупить
                # Достаточно ли денег на балансе в валюте CURRENCY_2 (Баланс >= CAN_SPEND)
                if float(balances[CURRENCY_2]) >= CAN_SPEND:
                    # Узнать среднюю цену за AVG_PRICE_PERIOD, по которой продают CURRENCY_1

                    deals =  call_api(api_method="trades/"+CURRENT_PAIR)
                    prices = []
                    for deal in deals[CURRENT_PAIR]:
                        time_passed = time.time() + STOCK_TIME_OFFSET*60*60 - int(deal['timestamp'])
                        if time_passed < AVG_PRICE_PERIOD*60:
                            prices.append(float(deal['price']))
                    try:        
                        avg_price = sum(prices)/len(prices)
                        """
                            Посчитать, сколько валюты CURRENCY_1 можно купить.
                            На сумму CAN_SPEND за минусом STOCK_FEE, и с учетом PROFIT_MARKUP
                            ( = ниже средней цены рынка, с учетом комиссии и желаемого профита)
                        """
                        # купить больше, потому что биржа потом заберет кусок
                        my_need_price = round(avg_price + avg_price * (STOCK_FEE+PROFIT_MARKUP), CURRENCY_1_DIGITS) 
                        my_amount = CAN_SPEND/my_need_price
                        
                        print('buy ',' amount=', my_amount, ' price=',my_need_price)
                        
                        # Допускается ли покупка такого кол-ва валюты (т.е. не нарушается минимальная сумма сделки)
                        if my_amount >= CURRENCY_1_MIN_QUANTITY:
                            print('send order, price=', my_need_price,' amount=',round(my_amount,CURRENCY_1_DIGITS))
                            new_order = call_api(api_method="", http_method="POST", public=False, method="Trade", pair=CURRENT_PAIR, type="buy", rate=my_need_price, amount=round(my_amount,8))['return']

                            print(new_order)
                            if DEBUG:
                                print('Создан ордер на покупку', new_order['order_id'])
                            
                        else: # мы можем купить слишком мало на нашу сумму
                            raise ScriptQuitCondition('Выход, не хватает денег на создание ордера')
                    except ZeroDivisionError:
                        print('Не удается вычислить среднюю цену', prices)
                else:
                    raise ScriptQuitCondition('Выход, не хватает денег')
        
    except ScriptError as e:
        print(e)
    except ScriptQuitCondition as e:
        if DEBUG:
            print(e)
        pass

while(True):
    CHECK()
    # main_flow()
    print('*'*80)
    time.sleep(1)

