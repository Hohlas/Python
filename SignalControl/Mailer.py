# MAIL SEND #########################################################################################
import smtplib
LOGIN   = 'fx@hohla.ru'
PASSWORD= 'K.,fijyjr2004'
HOST    = "smtp.gmail.com"
FROM    = "fx@hohla.ru"
TO      = "mail@hohla.ru"
SUBJ    = "Mail from Python"
#BODY = "Python 3.4 rules them all!"
def SEND(BODY='some test'):
    msg = "From: %s\nTo: %s\nSubject: %s\n\n%s"  % ( FROM, TO, SUBJ, BODY)
    server = smtplib.SMTP(HOST, 587)
    server.starttls()
    server.login(LOGIN, PASSWORD)
    server.sendmail(FROM, TO, msg)
    server.quit()

# MAIL RECEIVE #######################################################################################
import imaplib, poplib, email
def RECEIVE():
    mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    mail.login(LOGIN, PASSWORD)
    mail.list()
    mail.select("inbox") # Подключаемся к папке "входящие".

    # последнее письмо
    result, data = mail.search(None, "ALL")
    ids = data[0] # Получаем сроку номеров писем
    id_list = ids.split() # Разделяем ID писем
    latest_email_id = id_list[-1] # Берем последний ID
    result, data = mail.fetch(latest_email_id, "(RFC822)") # Получаем тело письма (RFC822) для данного ID
    msg = email.message_from_bytes(data[0][1])
    #decode(‘utf-8’)
    print ("1 ############################################################")
    print ("To: ",  msg['To'])
    print ("Subj: ",msg['Subject'])
    print ("Date: ",msg['Date'])
    print ("From: ",email.utils.parseaddr(msg['From'])) # получаем имя отправителя "Yuji Tomita" 
    print ('MESSAGE:  ' , msg) 

    # предпоследнее письмо через вычисленный нами ID
    result, data = mail.uid('search', None, "ALL") # Выполняет поиск и возвращает UID писем. “UNSEEN”, "ALL"
    latest_email_uid = data[0].split()[-2]  # предпоследний 
    result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    print ("2 ############################################################")
    print ("To: ",  msg['To'])
    print ("Subj: ",msg['Subject'])
    print ("Date: ",msg['Date'])
    print ("From: ",email.utils.parseaddr(msg['From'])) # получаем имя отправителя "Yuji Tomita" 
    #print ("Items: ",mail_txt.items()) # Выводит все заголовки.
    print ('MESSAGE:  ' , msg); 
    print("\n END   #######################################")

    # несколько последних писем
    result, data = mail.search(None, 'ALL')  # change variable name, and use new name in for loop
    id_list = data[0].split() # Разделяем ID писем
    for i in range(-1, -10, -1) :
        num = id_list[i] # Берем последний ID
        result, data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        print (i,': Message  #######################################\n', msg) 

    mail.close()
    mail.logout()
    return msg
