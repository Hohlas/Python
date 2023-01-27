
"""     КЛЮЧИ ОТКРЫТИЯ ФАЙЛОВ
r (Read)    - чтение. Если файла нет, генерится исключение FileNotFoundError
w (Write)   - запись. Если файла нет, он создается. Если он есть, старые данные в нем стираются.
a (Append)  - дозапись. файла нет, он создается. Если он есть, то данные дописываются в конец.
b (Binary)  - работа с бинарными файлами. Применяется вместе с другими режимами - w или r.
"""
""" КЛЮЧИ СЧИТЫВАНИЯ ФАЙЛОВ
readline()  - читает одну строку из файла
read()      - читает все содержимое файла в одну строку
readlines() - читает все строки файла в список
"""
filename="notes.txt"
#   ЗАПИСЬ ФАЙЛА  ################################################################
try:
    myfile = open("notes.txt", "w")
    try:
        myfile.write("Name, Phone, Address")
    except Exception as e:
        print(e)
    finally:
        myfile.close()
except Exception as ex:    print(ex)

# после выполнения инструкций файл закроется автоматом, даже если в них возникнут ошибки
print("WRITE")
with open(filename, "w") as myfile:
    myfile.write("name, phone, addr")   # перезапись с начала
# запись с помощью ф. print
with open(filename, "a") as myfile: # 
    print("\nAlex, 92046, Street", file=myfile)
    print("Mike, 14617, Broadw", file=myfile)

#   ЧТЕНИЕ ФАЙЛА  ####################################################################
print("READ")
with open(filename, "r") as myfile:
    lines = myfile.readlines() # Читает все строки из файла в список

with open(filename, "r") as myfile:
    line = myfile.readline()  # читает первую строку из файла
    while line:
        print(line, end="")
        line = myfile.readline() # читает поочереди строки из файла

FileList=[]
for line in open(filename):
    line = line.split(",") # разбивает  строку  по  указанному  символу "," и  создает  список  значений
    FileList.append(line)
    print ("0:",line[0],"1:",line[1],"2:",line[2])
print("FileList[1]=",FileList[1],"\nFileList[1][2]=",FileList[1][2])
print("read lines: ",lines)


