import urllib, http.client  # pip install requests
import os
import time
import json
# эти модули нужны для генерации подписи API
import hmac, hashlib

from openpyxl import Workbook  # pip install openpyxl    
from datetime import datetime, timezone

# ключи API, которые предоставила exmo
API_KEY = 'K-1841708dd388ddc4bbfddcb1dd0ef36d33dd22e7'
# обратите внимание, что добавлена 'b' перед строкой
API_SECRET = b'S-d29d11c6eb5a5f465e342649b97cfbf6850fa6f0'

# базовые настройки
API_URL = 'api.exmo.com'
API_VERSION = 'v1'

# Свой класс исключений
class ScriptError(Exception):
    pass
class ScriptQuitCondition(Exception):
    pass

# все обращения к API проходят через эту функцию
def call_api(**kwargs):
    payload = {'nonce': int(round(time.time()*1000))}

    if kwargs:
        payload.update(kwargs)
    payload =  urllib.parse.urlencode(payload)

    H = hmac.new(key=API_SECRET, digestmod=hashlib.sha512)
    H.update(payload.encode('utf-8'))
    sign = H.hexdigest()
    
    headers = {"Content-type": "application/x-www-form-urlencoded",
           "Key":API_KEY,
           "Sign":sign}
    conn = http.client.HTTPSConnection(API_URL, timeout=60)
    conn.request("POST", "/"+API_VERSION + "/" + kwargs['method'], payload, headers)
    response = conn.getresponse().read()
    
    conn.close()

    try:
        obj = json.loads(response.decode('utf-8'))

        if 'error' in obj and obj['error']:
            raise ScriptError(obj['error'])
        return obj
    except json.decoder.JSONDecodeError:
        raise ScriptError('Ошибка анализа возвращаемых данных, получена строка', response)

# Получим список всех пар, по которым торгует биржа
pairs_list = []
pairs = call_api(method='pair_settings')
for pair in pairs:
    pairs_list.append(pair) # сложим их в словарь
pairs_str = ','.join(pairs_list) # из словаря создадим строку, с парами, разделенными запятыми

# Создадим Excel файл
wb = Workbook()
ws = wb.active
# Вставим заголовки
ws.append(["Дата сделки", "Пара сделки", "ID ордера", "ID сделки", "Тип сделки", "Кол-во по сделке", "Цена сделки", "Сумма сделки"])

# Получим историю торгов по всем парам
trades = call_api(method='user_trades', pair=pairs_str, limit=10000)
for pair in trades: # пройдемся по каждой паре
    if not trades[pair]: #пропускаем пары, по которым не было торгов
        continue
    # Теперь проходим по всем торгам этой пары
    for trade in trades[pair]:
        # Мы бы могли использовать метод dict.values(), но нам нужны данные в определенном порядке, причем каждый раз для каждого массива, так что немного усложним код
        # Форматируем и вставляем строку с данными в Excel
        ws.append([
            datetime.fromtimestamp(trade['date'], timezone.utc), # дата сделки
            pair, # Пара сделки
            trade['order_id'], # ID ордера
            trade['trade_id'], # ID сделки
            'Покупка' if trade['type'] == 'buy' else 'Продажа',
            float(trade['quantity']), # Кол-во по сделке
            float(trade['price']), # Цена сделки
            float(trade['amount']) * (-1 if trade['type'] == 'buy' else 0.998), # сумма сделки, если buy то отрицательная - так удобнее считать потом
        ])
    
# Сохраняем файл
wb.save(os.path.dirname(os.path.abspath(__file__)) + "/exmo_excel.xlsx")
print('Работу закончил')
