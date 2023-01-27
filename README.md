# Python
my python programs

pip install requests
"python" или “pip” не является внутренней или внешней командой,
Проще всего найти файл pip.exe и скопировать его в корень диска С
Для того, чтобы решить эту проблему надо зайти в папку, куда у Вас установлен интерпретатор (папка в которой есть файл python.exe), скопировать полный путь добавить его в переменную окружения path.
Для того, чтобы добавить путь в переменную окружения path, щелкните правой кнопкой по иконке мой компьютер — свойства — дополнительные параметры системы — дополнительно — переменные среды. В открывшемся окне среди «Системных переменных» ищем переменную path и дописываем в конец уже существующих путей путь к интерпретатору на вашем компьютере (все пути разделяются точкой с запятой).  См.картинку:
C:\Program Files (x86)\Python36-32\Scripts
C:\Program Files (x86)\Python36-32
Добавить в обозревателе решение VS путь   C:\Program Files (x86)\Python36-32\Lib\site-packages\pip\_vendor

в директории с setup.py запускаешь cmd ком строку и в ней выполни код python setup.py install

hohla@yandex.ru
Hohla2010
Secret:  4ff25982c12a23b736e6bb078c5f4a866d52d53df92dfa204ef1fb86d891db62
Key:  BYH1BJEX-SL4HBJ0Q-5Z6FBG2I-ILU2OBDO-DEK9NNWR

Запуск нескольких скриптов. 
В командной строке (cmd): пишете python + путь к одному скрипту + Enter. Запускаете вторую командную строку, в ней python + путь к другому скрипту + Enter и т.п., будет одновременно работать несколько скриптов.
 
Устанавливаем Anaconda (Python+библиотеки) https://geektimes.ru/company/wirex/blog/292555/
Дистрибутив Anaconda https://www.anaconda.com/download/

Gekko - Open source bitcoin trading bot platform https://gekko.wizb.it/
Официальный сайт Python, где можно скачать интерпретатор (Python 3)  https://www.python.org/
Официальная документация по Python: https://docs.python.org/3/
Веб-сервис, позволяющий исполнять программы на Python прямо в вашем браузере: https://trinket.io/python/41462f0f16
Среда для написания программ PyCharm Educational Edition или PyCharm Community Edition:
https://www.jetbrains.com/pycharm-educational/
https://www.jetbrains.com/pycharm/
Текстовый редактор с подсветкой синтаксиса программ Sublime Text 3: http://www.sublimetext.com/3
Интерактивный учебник языка Python (на русском языке): http://pythontutor.ru/

s = 'ab12c59p7dq'
digits = []
for symbol in s:
    if '1234567890'.find(symbol) != -1:
        digits.append(int(symbol))
print(digits)

a = '192.168.0.1'.split('.')  # вернет список, полученный разрезанием исходной строки по символам '.'

