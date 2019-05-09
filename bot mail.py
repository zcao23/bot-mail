#-*- coding:UTF-8 -*-
import imaplib, email, smtplib, time

server = "imap.gmail.com"
fadd =  "botemail.sit@gmail.com"
mbody = ["""Hi"""]
   
def run():
    login_in_to_imaplib()
    login_in_to_smtplib()
    check_inbox()
    count_number()
    send_mail()
    ending_process()

def login_in_to_imaplib():
    global i
    i = imaplib.IMAP4_SSL('imap.gmail.com', '993')
    (retcode, capabilities) = i.login('botemail.sit@gmail.com', 'stevensemailbot1')
    if retcode == "OK":
        print ('imaplib connected')
    if retcode != "OK":
        print ('imaplib is not connected')

def login_in_to_smtplib():
    global s
    s = smtplib.SMTP('smtp.gmail.com','587')
    s.starttls()
    (retcode, capabilities) = s.login('botemail.sit@gmail.com', 'stevensemailbot1')
    if not (retcode == 235 or retcode == 250):
        print ('smtplib does not work')
    else:
        print ('smptlib works')

def check_inbox():
    (retcode, msg_count) = i.select('INBOX')
    if retcode == 'OK':
        print ('inbox works')
    if retcode != "OK":
        print ('inbox not find')

def count_number():
    global ids
    (retcode, message_indices) = i.search(None, "ALL")
    ids = message_indices[0]
    print (ids)

def send_mail():
    for n in ids.split():
        print (n)
        (retcode, data) = i.fetch(n,'(RFC822)')
            
        if retcode == 'OK':
            print ('fetched something')
            rmsg = email.message_from_string(data[0][1].decode('utf-8'))
            print (rmsg, 'you got the message')
            msub = "from bot email"
            print (msub)
            mfro = rmsg['from'].replace("<", '').replace(">", '').split()[-1]
            print (mfro)          
        else:
            print ("can't fetch")
            
        mhead = ['From:%s' % fadd, 'To:%s' % mfro ,'Subject:%s' % msub]
        print (mhead)
        smsg = "\r\n\r\n".join(['\r\n'.join(mhead), '\r\n'.join(mbody)])
        print (smsg)
               
        s.sendmail(fadd, mfro, smsg)
        print ("Send to %s success!" % mfro)
    
        i.store(n, '+FLAGS', '\\Deleted')
        time.sleep(5)

def ending_process():   
    i.expunge()
    i.close()
    i.logout()
    s.quit()


    

    
