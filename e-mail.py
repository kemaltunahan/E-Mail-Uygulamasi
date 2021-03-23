from tkinter import *                                  #for root
import tkinter.messagebox as mb                        #for message box in the roots
from tkinter.scrolledtext import ScrolledText          #for scroll text
import sqlite3 as sql                                  #for database
import numpy as np                                     #for numpy array
import warnings                                        #for future warnings
import smtplib                                         #for send to e-mail
from cryptography.fernet import Fernet                 #to hide the password

key = Fernet.generate_key()
f = Fernet(key)

"""
Created on 29 October 2020
@author : Kemal Tunahan Bingöl
"""

#for ignore to future warnings in 71th line
warnings.simplefilter(action='ignore', category=FutureWarning)

#database class
class Database():
    def __init__(self,cursor):
        self.cursor = cursor
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tablo (Name TEXT,Surname TEXT,Info TEXT,E_Mail TEXT,Password TEXT)")

    #for add data to database (sign up)
    def addData(self):
        self.cursor = cursor

        #to write password in the form of star
        """
        length =len(self.take_pasw_sign)
        self.take_pasw_sign_actual = length * "*"
        """

        self.encry = f.encrypt(self.take_pasw_sign.encode())

        self.cursor.execute("INSERT INTO tablo VALUES (?,?,?,?,?)",(self.take_name_sign.capitalize(),self.take_surname_sign.capitalize(),self.take_secques_sign.capitalize(),self.take_e_mail_sign,self.take_pasw_sign))
        con.commit()

    #data extraction (returning value)
    def dataExtraction(self):
        self.cursor = cursor
        self.cursor.execute("SELECT * FROM tablo")
        self.datas = self.cursor.fetchall()
        con.commit()
        return self.datas

    #for change to data (password)
    def dataChange(self):
        self.cursor = cursor
        con.commit()

    #for contrast login
    def contrastLogin(self):
        self.cursor = cursor
        self.take_e_mail = self.e_mail_entry.get()
        self.take_pasw = self.pasw_entry.get()

        self.extracted2 = self.dataExtraction()
        self.arr2 = np.array(self.extracted2)

        if(self.arr2.size != 0):
            self.take_e_mail_and_pasw_login = self.arr2[:,3:5]
        else:
            self.take_e_mail_and_pasw_login = self.arr2

        length = len(self.take_e_mail)
        if(self.take_e_mail == "" or "@gmail.com" not in self.take_e_mail[length-10:]):
            mb.showerror("HATA","Lütfen geçerli bir e-mail giriniz!")
        else:
            if(self.take_pasw == ""):
                mb.showerror("HATA","Lütfen bir şifre giriniz!")
            else:
                if(self.take_e_mail in self.take_e_mail_and_pasw_login):
                    if(self.take_pasw in self.take_e_mail_and_pasw_login):
                        for i in self.take_e_mail_and_pasw_login:
                            if(i[0] == self.take_e_mail):
                                if(i[1] == self.take_pasw):
                                    self.e_mail_entry.delete(0,"end")
                                    self.pasw_entry.delete(0,"end")
                                    self.loginpage()
                    else:
                        mb.showerror("HATA","Yanlış şifre!")
                else:
                    mb.showerror("HATA","Kullanıcı bulunamadı!")

    #for contrast sign up
    def contrastSignup(self):
        self.cursor = cursor
        self.take_name_sign = self.name_entry.get()
        self.take_surname_sign = self.surname_entry.get()
        self.take_secques_sign = self.secques_entry.get()
        self.take_e_mail_sign = self.sign_e_mail_entry.get()
        self.take_pasw_sign = self.sign_pasw_entry.get()
        self.take_pasw_sign_again = self.sign_pasw_again_entry.get()

        #make a array from datas of extracted
        self.extracted = self.dataExtraction()
        self.arr = np.array(self.extracted)

        #check of e-mail in databases
        if(self.arr.size != 0):
            self.e_mails = self.arr[:,3:4]
        else:
            self.e_mails = self.arr

        if (self.take_name_sign == "" or self.take_surname_sign == "" or self.take_secques_sign == "" or self.take_e_mail_sign == "" or self.take_pasw_sign == ""):
            mb.showerror("HATA", "Eksik parametre alındı!")
        else:
            if (self.take_pasw_sign != self.take_pasw_sign_again):
                mb.showerror("ŞİFRE HATASI","Şifreler uyuşmuyor!")
            else:
                if(self.take_e_mail_sign in self.e_mails):
                    mb.showerror("KULLANICI HATASI", "Kullanıcı zaten var!")
                else:
                    if (len(self.take_pasw_sign) < 6):
                        mb.showerror("GÜVENSİZ ŞİFRE", "Şifreniz 6 haneden küçük olamaz!")
                    else:
                        length = len(self.take_e_mail_sign)
                        if("@gmail.com" not in self.take_e_mail_sign[length-10:]):
                            mb.showerror("GEÇERSİZ E-MAİL","Lütfen geçerli bir e-mail giriniz!")
                        else:
                            mb._show("BİLGİ VER", "Kaydınız başarıyla oluşturuldu!")
                            self.addData()
                            self.root2.destroy()

    def contrastforget(self):
        self.cursor = cursor

        self.take_e_mail_forget = self.ques_e_mail_entry.get()
        self.take_ques = self.ques_entry.get()

        self.extracted3 = self.dataExtraction()
        self.arr3 = np.array(self.extracted3)
        self.take_e_mail_and_ques_forget = self.arr3[:,2:4]

        for i in self.take_e_mail_and_ques_forget:
            if("@gmail.com" in self.take_e_mail_forget):
                if(i[1] == self.take_e_mail_forget):
                    if(i[0] == self.take_ques.capitalize()):
                        self.newpassword()
            else:
                mb.showerror("HATA","Lütfen bir e-mail giriniz!")
                break

    def contrastNewPassword(self):
        self.take_newpass = self.newpass_entry.get()
        self.take_newpass_again = self.newpass_entry_again.get()

        self.extracted4 = self.dataExtraction()
        self.arr4 = np.array(self.extracted4)
        self.take_e_mail_and_take_e_mail_again = self.arr4[:,:]

        if(len(self.take_newpass) < 6  or len(self.take_newpass_again) < 6):
            mb.showerror("HATA","Kısa şifre! En az 6 karakter giriniz!")
        else:
            if(self.take_newpass == self.take_newpass_again):
                for i in self.take_e_mail_and_take_e_mail_again:
                    if(self.take_e_mail_forget == i[3]):
                        self.cursor.execute("UPDATE tablo SET Password = {} WHERE Password = {}".format(self.take_newpass,i[-1]))
                        mb.showinfo("BİLGİ","Şifre başarıyla güncellendi!")
            else:
                mb.showerror("HATA","Şifreler eşleşmiyor!")

#send to e-mail class
class SMTP():
    pass
"""
    def send_E_mail(self,mail,e_mail,pasw,whom,content):
        self.mail = mail
        self.mail.ehlo()
        self.mail.starttls()
        self.mail.login(e_mail,pasw)
        self.whom = whom.get()
        self.content = content.get('1.0',END)
        print(self.whom,self.content)
"""
#root's class
class Root(Database,SMTP):
    def __init__(self,root):
        self.root = root
        self.createroot()

    #main root
    def createroot(self):
        self.root.geometry("402x402")
        self.root.title("E-MAİL GİRİŞ EKRANI")
        self.img = PhotoImage(file="e-mail-giriş.png")
        self.pict = Label(self.root,image=self.img)
        self.pict.grid(row=0,column=0)

        self.e_mail = Label(self.root, text="E-POSTA ADRESİ:", font=("NEW TIMES ROMAN", 10), bg="black",fg="white").place(x=45, y=150)
        self.e_mail_entry = Entry(self.root, insertbackground="white", bg="black", fg="white", width=20,font=("NEW TIMES ROMAN", 13))
        self.e_mail_entry.place(x=167, y=150)
        self.pasw = Label(self.root, text="ŞİFRE:", width=14, font=("NEW TIMES ROMAN", 10), bg="black",fg="white").place(x=45, y=190)
        self.pasw_entry = Entry(self.root, insertbackground="white", bg="black", fg="white", width=20,font=("NEW TIMES ROMAN", 13), show="*")
        self.pasw_entry.place(x=167, y=190)

        self.variable = IntVar()
        self.check = Checkbutton(self.root, variable=self.variable, activebackground="cyan4",selectcolor="black", text="Şifreyi Göster",bg="black", fg="white", font=("NEW TIMES ROMAN", 10),command=self.viewpassword).place(x=100, y=235)

        self.forget = Button(self.root, text="Şifremi Unuttum!", activebackground="cyan4",width=12, font=("NEW TIMES ROMAN", 10), bg="black",fg="white",command=self.forgetpassword).place(x=220, y=233)

        self.login = Button(self.root,text="Giriş Yap",fg="white",bg="black",activebackground="SpringGreen4",font=("NEW TIMES ROMAN",10),width=12,command=self.contrastLogin).place(x=145,y=285)

        self.sign = Button(self.root, text="Kayıt Ol", width=37, font=("NEW TIMES ROMAN", 10), activebackground="orange4",bg="black",fg="white",command=self.signup).place(x=45, y=330)

    #for view to password
    def viewpassword(self):
        if (self.variable.get() == 1):
            self.pasw_entry.config(show="")
        else:
            self.pasw_entry.config(show="*")

    #root of remember to password
    def forgetpassword(self):
        self.root4 = Tk()
        self.root4.title("GÜVENLİK SORUSU EKRANI")
        self.root4.geometry("500x200")
        self.root4.config(bg="spring green2")
        self.ques_e_mail = Label(self.root4, bg="skyblue1", width=20, text="E-Mail Adresi:",font=("NEW TIMES ROMAN", 12))
        self.ques_e_mail.place(x=10, y=40)
        self.ques_e_mail_entry = Entry(self.root4, width=30, font=("NEW TIMES ROMAN", 12))
        self.ques_e_mail_entry.place(x=210, y=40)
        self.ques = Label(self.root4,bg="skyblue1",width=20,text="En Sevdiğiniz Öğretmen:",font=("NEW TIMES ROMAN",12))
        self.ques.place(x=10,y=75)
        self.ques_entry = Entry(self.root4,width=30,font=("NEW TIMES ROMAN",12),show="*")
        self.ques_entry.place(x=210,y=75)
        self.control = Button(self.root4,text="Doğrula",bg="dark orange1",activebackground="forest green",fg="black",activeforeground="white",font=("NEW TIMES ROMAN",12),width=15,command=self.contrastforget)
        self.control.place(x=275,y=145)
        self.back3 = Button(self.root4, text="Geri Dön", font=("NEW TIMES ROMAN", 12), width=15, bg="red3", fg="white",activebackground="dark red", activeforeground="white",command=self.root4.destroy)
        self.back3.place(x=75, y=145)
        self.variable3 = 1
        self.check2 = Checkbutton(self.root4, width=12, selectcolor="white", activeforeground="white",activebackground="deepskyblue4",text="İsmi Göster", bg="purple2",fg="black", font=("NEW TIMES ROMAN", 12),command=self.viewpassword3)
        self.check2.place(x=210, y=105)
        self.root4.mainloop()

    #root for a new password
    def newpassword(self):
        self.root4.destroy()
        self.root5 = Tk()
        self.root5.title("ŞİFRE OLUŞTURMA EKRANI")
        self.root5.geometry("450x180")
        self.root5.config(bg="SlateBlue1")
        self.newpass = Label(self.root5,text="Yeni Şifre:",font=("NEW TIMES ROMAN",12),width=15,bg="gold4",fg="white")
        self.newpass.place(x=15,y=25)
        self.newpass_entry = Entry(self.root5,font=("NEW TIMES ROMAN",12),width=30)
        self.newpass_entry.place(x=165,y=25)
        self.newpass_again = Label(self.root5, text="Yeni Şifre Tekrar:", font=("NEW TIMES ROMAN", 12), width=15, bg="gold4",fg="white")
        self.newpass_again.place(x=15, y=65)
        self.newpass_entry_again = Entry(self.root5, font=("NEW TIMES ROMAN", 12), width=30)
        self.newpass_entry_again.place(x=165, y=65)
        self.back4 = Button(self.root5, text="Geri Dön", font=("NEW TIMES ROMAN", 12), width=15,activeforeground="white",activebackground="dark red",bg="brown4",fg="white",command=self.root5.destroy)
        self.back4.place(x=65, y=120)
        self.register = Button(self.root5, text="Kaydet", font=("NEW TIMES ROMAN", 12), width=15,bg="seagreen2",activeforeground="white",activebackground="dark green",command=self.contrastNewPassword)
        self.register.place(x=235,y=120)
        self.root5.mainloop()

    #sign up root
    def signup(self):
        self.e_mail_entry.delete(0,"end")
        self.pasw_entry.delete(0,"end")
        self.root2 = Tk()
        self.root2.title("KAYIT OLMA EKRANI")
        self.root2.geometry("1000x275")
        self.root2.config(bg="royal blue")

        self.name = Label(self.root2, text="İsim:", width=20, font=("NEW TIMES ROMAN", 10), bg="tomato",fg="black")
        self.name.place(x=20, y=45)
        self.surname = Label(self.root2, text="Soyisim:", width=20, font=("NEW TIMES ROMAN", 10), bg="tomato",fg="black")
        self.surname.place(x=20, y=85)
        self.secques = Label(self.root2, text="En sevdiğiniz öğretmen:", width=20, font=("NEW TIMES ROMAN", 10), bg="tomato",fg="black")
        self.secques.place(x=20, y=125)

        self.name_entry = Entry(self.root2, insertbackground="black", bg="white", fg="black", width=30,font=("NEW TIMES ROMAN", 12))
        self.name_entry.place(x=200, y=45)

        self.surname_entry = Entry(self.root2, insertbackground="black", bg="white", fg="black", width=30,font=("NEW TIMES ROMAN", 12))
        self.surname_entry.place(x=200, y=85)

        self.secques_entry = Entry(self.root2, insertbackground="black", bg="white", fg="black", width=30,font=("NEW TIMES ROMAN", 12))
        self.secques_entry.place(x=200, y=125)

        self.sign_e_mail = Label(self.root2, text="E Mail:", width=20, font=("NEW TIMES ROMAN", 10), bg="tomato",fg="black")
        self.sign_e_mail.place(x=520, y=45)
        self.sign_pasw = Label(self.root2, text="Şifre:", width=20, font=("NEW TIMES ROMAN", 10), bg="tomato",fg="black")
        self.sign_pasw.place(x=520, y=85)
        self.sign_pasw_again = Label(self.root2, text="Şifre Tekrar:", width=20, font=("NEW TIMES ROMAN", 10), bg="tomato",fg="black")
        self.sign_pasw_again.place(x=520, y=125)

        self.sign_e_mail_entry = Entry(self.root2, insertbackground="black", bg="white", fg="black", width=30,font=("NEW TIMES ROMAN", 12))
        self.sign_e_mail_entry.place(x=700, y=45)

        self.sign_pasw_entry = Entry(self.root2, insertbackground="black", bg="white", fg="black", width=30,font=("NEW TIMES ROMAN", 12), show="*")
        self.sign_pasw_entry.place(x=700, y=85)

        self.sign_pasw_again_entry = Entry(self.root2, insertbackground="black", bg="white", fg="black", width=30,font=("NEW TIMES ROMAN", 12), show="*")
        self.sign_pasw_again_entry.place(x=700, y=125)

        self.sign_in = Button(self.root2, text="Kayıt Ol", font=("NEW TIMES ROMAN", 12),activeforeground="white", activebackground="green",width=15, bg="medium spring green",fg="black",command=self.contrastSignup)
        self.sign_in.place(x=425, y=200)

        self.back = Button(self.root2,text="Geri Dön",font=("NEW TIMES ROMAN",12),width=15,bg="red3",fg="white",activebackground="dark red",activeforeground="white",command=self.root2.destroy)
        self.back.place(x=30,y=200)

        self.variable2 = 1
        self.check2 = Checkbutton(self.root2, width=15,selectcolor="white", text="Şifreyi Göster", bg="yellow4", fg="black",font=("NEW TIMES ROMAN", 12),command=self.viewpassword2)
        self.check2.place(x=700, y=160)

        self.root2.mainloop()

    #for view to password 2
    def viewpassword2(self):
        if(self.variable2 == 1):
            self.sign_pasw_entry.config(show="")
            self.sign_pasw_again_entry.config(show="")
            self.variable2 = 0
        else:
            self.variable2 = 1
            self.sign_pasw_entry.config(show="*")
            self.sign_pasw_again_entry.config(show="*"),

    #for view to password 3
    def viewpassword3(self):
        if(self.variable3 == 1):
            self.ques_entry.config(show="")
            self.variable3 = 0
        else:
            self.variable3 = 1
            self.ques_entry.config(show="*")

    #root of send to e-mail
    def loginpage(self):

        self.root3 = Tk()
        self.root3.geometry("500x500")
        self.root3.title("E-MAİL GÖNDERME EKRANI")
        self.root3.config(bg="goldenrod2")

        self.whom = Label(self.root3,text="KİME:",font=("NEW TIMES ROMAN",12),width=10,bg="deepskyblue",fg="black")
        self.whom.place(x=50,y=50)

        self.whom_entry = Entry(self.root3,font=("NEW TIMES ROMAN",13),width=30)
        self.whom_entry.place(x=175,y=50)

        self.message = Label(self.root3,text="MESAJ:",font=("NEW TIMES ROMAN",13),width=10,bg="deepskyblue")
        self.message.place(x=50,y=100)

        self.message_entry = ScrolledText(self.root3,font=("NEW TIMES ROMAN",13),width=28,height=15)
        self.message_entry.place(x=175,y=100)
        self.message_entry.vbar.config(cursor = "target")

        self.back2 = Button(self.root3,text="Geri Dön",font=("NEW TIMES ROMAN",12),width=15,bg="red2",fg="white",activebackground="red4",activeforeground="white",command=self.root3.destroy)
        self.back2.place(x=50,y=425)

        self.send = Button(self.root3,text="Gönder",font=("NEW TIMES ROMAN",12),width=15,bg="green3",fg="white",activebackground="dark green",activeforeground="white",command=self.send_E_mail)
        self.send.place(x=300, y=425)

        self.root3.mainloop()

    def send_E_mail(self):

        with smtplib.SMTP('smtp.gmail.com', 587) as self.mail:
            self.whom = self.whom_entry.get()
            self.content = self.message_entry.get('1.0', END)
            #print(self.whom, self.content, self.take_e_mail , self.take_pasw)
            self.mail.ehlo()
            self.mail.starttls()
            self.mail.login(self.take_e_mail, self.take_pasw)

            self.mail.sendmail(self.take_e_mail,self.whom,self.content)

#create database object
con = sql.connect("E-Mail.db")
cursor =con.cursor()
Database(cursor)

#create root object
root=Tk()
Root(root)
root.mainloop()
con.commit()
con.close()
