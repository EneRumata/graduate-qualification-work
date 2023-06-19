import tkinter
import tkinter.filedialog as fd
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import babel
import babel.numbers
from babel import *
from tkcalendar import Calendar
from tkcalendar import *
import os.path

import shutil

import sqlite3

numbers=('0','1','2','3','4','5','6','7','8','9')
pointers=('.',',','/','-')

user_id_for_combobox_number=[]
current_filepath=""
current_day=int(1)
current_month=int(1)
current_year=int(2023)
current_user_id=int(0)
current_selection_cell=''
current_selection_text=''
con=None
cur=None
max_user_id=int(0)
max_day_id=int(0)

def coords():
    stake_label.place_forget()
    stake_text.place_forget()
    hours_stake_label.place_forget()
    hours_stake_text.place_forget()
    hours_work_text.place_forget()
    hours_work_label.place_forget()
    hours_days_label.place_forget()
    hours_days_text.place_forget()
    items_cost_label.place_forget()
    items_cost_text.place_forget()
    items_count_label.place_forget()
    items_count_text.place_forget()

    day_items_text.place_forget()
    day_items_label.place_forget()
    day_hours_text.place_forget()
    day_hours_label.place_forget()

    stake_label.place(x=15,y=80)
    stake_text.place(x=120,y=80)
    hours_stake_label.place(x=15,y=110)
    hours_stake_text.place(x=120,y=115)
    hours_work_label.place(x=15,y=145)
    hours_work_text.place(x=120,y=150)
    hours_days_label.place(x=120,y=180)
    hours_days_text.place(x=120,y=185)
    items_cost_label.place(x=15,y=80)
    items_cost_text.place(x=120,y=80)
    items_count_label.place(x=15,y=115)
    items_count_text.place(x=120,y=115)
    
    day_items_text.place(x=390,y=470)
    day_items_label.place(x=285,y=470)
    day_hours_text.place(x=390,y=400)
    day_hours_label.place(x=285,y=400)
    
def make_invisible(widget):
    print("hyi")
    widget.place_forget()
   
def update_locked_cells():
    global stake_label
    global stake_text
    global hours_stake_label
    global hours_stake_text
    global hours_work_label
    global hours_work_text
    global hours_days_label
    global hours_days_text
    global items_cost_label
    global items_cost_text
    global items_count_label
    global items_count_text
    
    global day_hours_label
    global day_hours_text
    global day_items_label
    global day_items_text
    
    global day_weekend_btn
    global new_user_btn
    global change_name_btn
    global save_sql_btn
    global change_name_text
    global name_combobox
    global type_combobox
    global cal
    global command_get_payment_btn
    
    print("upd "+str(current_filepath))
    if current_filepath!="":
        if str(type_combobox.get())=="Повременная":
            new_user_btn.config(state="normal")
            change_name_btn.config(state="normal")
            save_sql_btn.config(state="normal")
            change_name_text.config(state="normal",background="white")
            name_combobox.config(state="normal",background="white")
            type_combobox.config(state="normal",background="white")

            stake_label.place(x=15,y=80)
            stake_text.place(x=120,y=80)
            hours_stake_label.place(x=15,y=110)
            hours_stake_text.place(x=120,y=115)
            hours_work_label.place(x=15,y=180)
            hours_work_text.place(x=120,y=185)
            hours_days_label.place(x=15,y=145)
            hours_days_text.place(x=120,y=150)
            items_cost_label.place_forget()
            items_cost_text.place_forget()
            items_count_label.place_forget()
            items_count_text.place_forget()

            stake_text.config(state="normal",background="white")
            hours_stake_text.config(state="normal",background="white")
            hours_days_text.config(state="normal",background="white")
            items_cost_text.config(state="disabled",background="whitesmoke")
            cal.config(state="normal",background="grey")
            
            day_hours_label.place(x=285,y=400)
            day_hours_text.place(x=390,y=400)
            day_items_label.place_forget()
            day_items_text.place_forget()
    
            day_hours_text.config(state="normal",background="white")
            day_items_text.config(state="disabled",background="whitesmoke")
            day_weekend_btn.config(state="normal")
            get_payment_btn.config(state="normal")
            
        else:
            new_user_btn.config(state="normal")
            change_name_btn.config(state="normal")
            save_sql_btn.config(state="normal")
            change_name_text.config(state="normal",background="white")
            name_combobox.config(state="normal",background="white")
            type_combobox.config(state="normal",background="white")

            stake_label.place_forget()
            stake_text.place_forget()
            hours_stake_label.place_forget()
            hours_work_text.place_forget()
            hours_work_label.place_forget()
            hours_stake_text.place_forget()
            hours_days_label.place_forget()
            hours_days_text.place_forget()
            items_cost_label.place(x=10,y=75)
            items_cost_text.place(x=120,y=80)
            items_count_label.place(x=10,y=110)
            items_count_text.place(x=120,y=115)

            stake_text.config(state="disabled",background="whitesmoke")
            hours_stake_text.config(state="disabled",background="whitesmoke")
            hours_days_text.config(state="disabled",background="whitesmoke")
            items_cost_text.config(state="normal",background="white")
            cal.config(state="normal",background="grey")
            
            day_hours_label.place_forget()
            day_hours_text.place_forget()
            day_items_label.place(x=285,y=400)
            day_items_text.place(x=390,y=400)
            
            day_hours_text.config(state="disabled",background="whitesmoke")
            day_items_text.config(state="normal",background="white")
            day_weekend_btn.config(state="normal")
            get_payment_btn.config(state="normal")


def open_existing_database():
    global current_filepath #Объявляем глобальные переменные.
    global current_user_id  #Без этого Python не поймёт, что
    global max_user_id      #переменные глобальные и их не нужно
    global max_day_id       #создавать как локальные.
    global con
    global cur
    print("!!")             #Все "print" - сообщения для отладки
    print(type(current_filepath))
    print(current_filepath) #в консоли
    con = sqlite3.connect(current_filepath)
    sqlite3.enable_callback_tracebacks(True)
    
    print(type(con))
    print(con)
    cur = con.cursor()
    string="select MAX(user_id) from USERS;"
    cur.execute(string)
    s = cur.fetchall()      #Максимальный идентификатор пользователя
    print("s1= "+str(s))    #в базе данных. Используется при создании
    for name in s:          #нового пользователя.
        max_user_id=name[0]
    con.commit()
    
    string="select MAX(day_id) from DAYS;"
    cur.execute(string)
    s = cur.fetchall()      #Максимальный идентификатор дня
    print("s2= "+str(s))    #в базе данных. Используется при создании
    for name in s:          #нового дня.
        max_day_id=name[0]
    if max_day_id==None:
        max_day_id=int(0)
            
    con.commit()
    current_user_id=1
    print("max_user_id = "+str(max_user_id))
    print("max_day_id = "+str(max_day_id))

def create_new_database():
    global current_filepath
    global current_user_id
    global max_user_id
    global max_day_id
    global con
    global cur
    print("!!")
    print(type(current_filepath))
    print(current_filepath)
    con = sqlite3.connect(current_filepath)
    sqlite3.enable_callback_tracebacks(True)
    
    print(type(con))
    print(con)
    cur = con.cursor()
    string="CREATE TABLE USERS ("
    string+="   user_id int PRIMARY KEY,"
    string+="   user_name text,"
    string+="   user_type int,"
    string+="   user_stake text,"
    string+="   user_hours_stake text,"
    string+="   user_days_stake text,"
    string+="   user_items_cost text"
    string+=");"
    cur.execute(string)
    
    string="CREATE TABLE DAYS ("
    string+="   day_id int PRIMARY KEY,"
    string+="   day_day text,"
    string+="   day_month text,"
    string+="   day_year text,"
    string+="   day_hours text,"
    string+="   day_items text,"
    string+="   day_owner int REFERENCES USERS"
    string+=");"
    cur.execute(string)

    string="insert into USERS (user_id,user_name,user_type,user_stake,user_hours_stake,user_days_stake,user_items_cost) "
    string+="values (1,'',0,'','40','','');"
    cur.execute(string)
    con.commit()
    
    max_user_id=1
    current_user_id=1
    max_day_id=int(0)
    print("max_id = "+str(max_user_id))
    
def set_name_values(ch=False):
    global user_id_for_combobox_number
    global current_user_id
    global max_user_id
    global con
    global cur
    global name_values
    global name_values_var
    global name_combobox

    currentitem=name_combobox.current()
    string="select user_id, user_name from USERS;"
    cur.execute(string)
    name_values = []
    user_id_for_combobox_number = []
    s = cur.fetchall()
    i = 0
    for name in s:
        i+=1
        name_values.append(name[1])
        user_id_for_combobox_number.append(name[0])

    con.commit()
    name_combobox.config(values=name_values)
    if ch:
        name_combobox.current(i-1)
    else:
        name_combobox.current(currentitem)

def is_number(value,integ=False):
    num=str(value)
    print("num="+num)
    print("type="+str(type(num)))
    if num=="":
        return True
    else:
        if (num[0] in numbers) and (num[-1] in numbers):
            boolcheck=False
            for cell in num[1:-1]:
                if cell=='.':
                    if boolcheck or not(integ):
                        print("exit2")
                        return False
                    else:
                        boolcheck=True
                elif not(cell in numbers):
                    print("exit3")
                    return False

            return True
        else:
            print("exit1")
            return False

def set_user_values(nm=False):
    global current_user_id
    global con
    global cur
    global name_combobox
    global change_name_text
    global stake_text
    global hours_stake_text
    global hours_days_text
    global items_cost_text
    
    username=str(change_name_text.get())
    print("username is "+username)
    
    if not(is_number(stake_text.get())):
        messagebox.showerror(title="Неправильные данные", message="Оклад должен быть числом")
        return 1

    if not(is_number(hours_stake_text.get())):
        messagebox.showerror(title="Неправильные данные", message="Часы оклада должны быть числом")
        return 1

    if not(is_number(hours_days_text.get(),True)):
        messagebox.showerror(title="Неправильные данные", message="Кол-во рабочих дней должно быть числом")
        return 1

    if not(is_number(items_cost_text.get())):
        print("items_cost_text="+str(items_cost_text.get()))
        messagebox.showerror(title="Неправильные данные", message="Цена продукта (услуги) должна быть числом")
        return 1
    

    string="select user_id, user_name, user_type, user_stake, user_hours_stake, user_days_stake, user_items_cost from USERS;"
    cur.execute(string)
    print(cur.fetchall())
    con.commit()
    
    print("current_user_id="+str(current_user_id))
    print("hours_days_text = "+str(hours_days_text.get()))
    string='update USERS set '
    if type_combobox.get()=="Повременная":
        if nm and str(change_name_text.get())!="":
            string+="user_name = '"+str(change_name_text.get())+"', "
        string+="user_type = 0, user_stake = '"+str(stake_text.get())+"', user_hours_stake = '"+str(hours_stake_text.get())+"', user_days_stake = '"+str(hours_days_text.get())+"', user_items_cost = '"+str(items_cost_text.get())+"'"
    else:
        if nm and str(change_name_text.get())!="":
            string+="user_name = '"+str(change_name_text.get())+"', "
        string+="user_type = 1, user_stake = '"+str(stake_text.get())+"', user_hours_stake = '"+str(hours_stake_text.get())+"', user_days_stake = '"+str(hours_days_text.get())+"', user_items_cost = '"+str(items_cost_text.get())+"'"

    string+='where user_id = '+str(current_user_id)+';'
    cur.execute(string)
    con.commit()
    set_name_values()

def on_closing():
    if messagebox.askokcancel("Выйти", "Уверены, что хотите выйти?"):
        tk.destroy()

def change_user():
    global current_user_id
    global con
    global cur
    global name_combobox
    global type_combobox
    global stake_text
    global hours_stake_text
    global hours_days_text
    global items_cost_text
    
    stake_text.config(state="normal")
    hours_stake_text.config(state="normal")
    hours_days_text.config(state="normal")
    items_cost_text.config(state="normal")
    day_hours_text.config(state="normal")
    day_items_text.config(state="normal")
    
    print("current_index = "+str(name_combobox.current()))
    newid = user_id_for_combobox_number[name_combobox.current()]
    if newid==current_user_id:
        print("good ending")
        return
    else:
        current_user_id = newid
        string='select user_type, user_stake, user_hours_stake, user_days_stake, user_items_cost from USERS '
        string+='where user_id = '+str(current_user_id)+';'
        cur.execute(string)
        s = cur.fetchall()
        print("sss= "+str(s))
        for name in s:
            if name[0]==0:
                type_combobox.current(0)
            else:
                type_combobox.current(1)
            stake_text.delete(0,tkinter.END)
            stake_text.insert(0,str(name[1]))
            hours_stake_text.delete(0,tkinter.END)
            hours_stake_text.insert(0,str(name[2]))
            hours_days_text.delete(0,tkinter.END)
            hours_days_text.insert(0,str(name[3]))
            items_cost_text.delete(0,tkinter.END)
            print("NAME3="+str(name[4]))
            items_cost_text.insert(0,str(name[4]))
            update_locked_cells()


        day_hours_text.delete(0,tkinter.END)
        day_items_text.delete(0,tkinter.END)

        string='select day_hours, day_items from DAYS '
        string+='where day_owner = '+str(current_user_id)+' and day_day = "'+str(current_day)+'" and day_month = "'+str(current_month)+'" and day_year = "'+str(current_year)+'";'
        cur.execute(string)
        s = cur.fetchall()
        print("ssss==="+str(s))
        con.commit()
        if s==[]:
            day_hours_text.insert(0,"")
            day_items_text.insert(0,"")
        else:
            for name in s:
                day_hours_text.insert(0,name[0])
                day_items_text.insert(0,name[1])


def write_day_sql():
    global max_day_id
    global current_day
    global current_month
    global current_year
    global current_user_id
    global con
    global cur
    global day_hours_text
    global day_items_text

    if not(is_number(day_hours_text.get()) and is_number(day_items_text.get())):
        messagebox.showerror(title="Неправильные данные", message="Данные должны быть числом")
        return 1
        
    string='select day_hours, day_items from DAYS '
    string+='where day_owner = '+str(current_user_id)+' and day_day = "'+str(current_day)+'" and day_month = "'+str(current_month)+'" and day_year = "'+str(current_year)+'";'
    cur.execute(string)
    s = cur.fetchall()
    print("write_day_sql, s==="+str(s))
    print("values="+str(day_items_text.get())+" "+str(day_hours_text.get()))
    con.commit()
    
    if s==[]:
        print("max_day_id!!!!!!!!!!!!!!!! = "+str(max_day_id))
        print(str(type(max_day_id)))
        max_day_id=max_day_id+1
        string='insert into DAYS (day_id,day_day,day_month,day_year,day_hours,day_items,day_owner) '
        string+='    values ('+str(max_day_id)+',"'+str(current_day)+'","'+str(current_month)+'","'+str(current_year)+'","'+str(day_hours_text.get())+'","'+str(day_items_text.get())+'",'+str(current_user_id)+');'
        cur.execute(string)
    else:
        string='update DAYS '
        string+='    set day_hours = "'+str(day_hours_text.get())+'", day_items = "'+str(day_items_text.get())+'" '
        string+='where day_owner = '+str(current_user_id)+' and day_day = "'+str(current_day)+'" and day_month = "'+str(current_month)+'" and day_year = "'+str(current_year)+'";'
        cur.execute(string)
        
    con.commit()

def floatt(ss):
    if ss=="":
        return float(0)
    else:
        return float(ss)
    
def intt(ss):
    if ss=="":
        return int(0)
    else:
        return int(ss)
    
def get_all_done():
    global current_month
    global current_year
    global current_user_id
    global con
    global cur

    global time_start_text
    global time_end_text
    global price_white_text
    global price_ndfl_text
    global price_summ_text
    global hours_work_text
    global items_count_text
    global name_combobox
    global type_combobox
    min_zp = float(16242)
    
    if set_user_values()==1:
        return



    if str(type_combobox.get())=="Повременная":
        string='select day_day, day_hours from DAYS '
        string+='where day_owner = '+str(current_user_id)+' and day_month = "'+str(current_month)+'" and day_year = "'+str(current_year)+'";'
        cur.execute(string)
        days = cur.fetchall()
        print("get_all_done, days==="+str(days))
        con.commit()
        
        string='select user_stake, user_hours_stake, user_days_stake, user_name from USERS '
        string+='where user_id = '+str(current_user_id)+';'
        cur.execute(string)
        users = cur.fetchall()
        print("get_all_done, users==="+str(users))
        con.commit()

        for name in users:
            stake=floatt(name[0])
            hours_stake=floatt(name[1])
            days_stake=floatt(name[2])
            user_fullname=name[3]
            print(str(stake)+" "+str(hours_stake)+" "+str(days_stake))

        hours=[float(0),float(0)]
        for name in days:
            if intt(name[0])<16:
                hours[0]=hours[0]+floatt(name[1])
            else:
                hours[1]=hours[1]+floatt(name[1])
        hours.append(hours[0]+hours[1])
        print("hours="+str(hours))
        if hours[2]==0.0:
            messagebox.showerror(title="Неправильные данные", message="Нет данных календаря")
            return 1
        if stake==0.0 or hours_stake==0.0 or days_stake==0.0:
            messagebox.showerror(title="Неправильные данные", message="Недостаточно данных оклада")
            return 1

        hours_work_text.config(state="normal")
        price_ndfl_text.config(state="normal")
        time_start_text.config(state="normal")
        time_end_text.config(state="normal")
        price_white_text.config(state="normal")
        price_summ_text.config(state="normal")
        
        hours_work_text.delete(0,tkinter.END)
        hours_work_text.insert(0,str(hours[2]))
        

        pay = round(stake*(hours[2]/(hours_stake/5*days_stake)),2)
        if pay<min_zp:
            pay=min_zp
                
        ndlf=round(pay*0.13,2)
        price_ndfl_text.delete(0,tkinter.END)
        price_ndfl_text.insert(0,str(ndlf))
            
        price1=round(pay/2,2)
        ndlf1=round(ndlf/2,2)
        result1=price1-ndlf1
        price2=pay-price1
        ndlf2=ndlf-ndlf1
        result2=round(price2-ndlf2,2)

    else:
        if current_month==1:
            old_month=12
        else:
            old_month=current_month-1
        string='select day_day, day_items from DAYS '
        string+='where day_owner = '+str(current_user_id)+' and day_month = "'+str(old_month)+'" and day_year = "'+str(current_year)+'";'
        cur.execute(string)
        days_old = cur.fetchall()
        print("get_all_done, days==="+str(days_old))
        con.commit()

        string='select day_day, day_items from DAYS '
        string+='where day_owner = '+str(current_user_id)+' and day_month = "'+str(current_month)+'" and day_year = "'+str(current_year)+'";'
        cur.execute(string)
        days = cur.fetchall()
        print("get_all_done, days==="+str(days))
        con.commit()
        
        string='select user_items_cost, user_name from USERS '
        string+='where user_id = '+str(current_user_id)+';'
        cur.execute(string)
        users = cur.fetchall()
        print("get_all_done, users==="+str(users))
        con.commit()

        for name in users:
            items_cost=floatt(name[0])
            user_fullname=name[1]
            print(str(items_cost))

        items_old=[float(0),float(0)]
        for name in days_old:
            if intt(name[0])<50:
                items_old[0]=items_old[0]+floatt(name[1])
            else:
                items_old[1]=items_old[1]+floatt(name[1])
                
        items=[float(0),float(0)]
        for name in days:
            if intt(name[0])<0:
                items[0]=items[0]+intt(name[1])
            else:
                items[1]=items[1]+intt(name[1])

        print("items="+str(items))
        items[0]=(items_old[0]//2)
        items.append(items[1])
        if items[0]>items[1]:
            items[0]=items[1]
            items[1]=0
        else:
            items[1]=items[1]-items[0]
        print("items="+str(items))
        if items[2]==0.0:
            messagebox.showerror(title="Неправильные данные", message="Нет данных календаря")
            return 1
        if items_cost==0.0:
            messagebox.showerror(title="Неправильные данные", message="Недостаточно данных стоимости")
            return 1
        
        hours_work_text.config(state="normal")
        items_count_text.config(state="normal")
        price_ndfl_text.config(state="normal")
        time_start_text.config(state="normal")
        time_end_text.config(state="normal")
        price_white_text.config(state="normal")
        price_summ_text.config(state="normal")
        
        items_count_text.delete(0,tkinter.END)
        items_count_text.insert(0,str(items[2]))

        pay = round(items_cost*items[2],2)
        print("pay="+str(pay))
        print("items_cost="+str(items_cost))
        if pay<min_zp:
            pay=min_zp
            
        ndlf=round(pay*0.13,2)
        price_ndfl_text.delete(0,tkinter.END)
        price_ndfl_text.insert(0,str(ndlf))
        
        price1=round(pay/items[2]*items[0],2)
        ndlf1=round(ndlf/items[2]*items[0],2)
        result1=price1-ndlf1
        price2=pay-price1
        ndlf2=ndlf-ndlf1
        result2=round(price2-ndlf2,2)


    
    time_start_text.delete(0,tkinter.END)
    time_start_text.insert(0,str(result1))

    time_end_text.delete(0,tkinter.END)
    time_end_text.insert(0,str(result2))
    
    price_white_text.delete(0,tkinter.END)
    price_white_text.insert(0,str(pay))

    black=pay-ndlf
    price_summ_text.delete(0,tkinter.END)
    price_summ_text.insert(0,str(black))

    print("ndlf=="+str(ndlf))
    print("pay=="+str(pay))
    print("result1=="+str(result1))
    print("result2=="+str(result2))
    print("pay=="+str(pay))
    print("black=="+str(black))
    
    hours_work_text.config(state="disabled")
    items_count_text.config(state="disabled")
    price_ndfl_text.config(state="disabled")
    time_start_text.config(state="disabled")
    time_end_text.config(state="disabled")
    price_white_text.config(state="disabled")
    price_summ_text.config(state="disabled")

    filetypes = (("Текстовый", "*.txt"),("Любой", "*"))
    filename = fd.asksaveasfilename(title="Сохранить отчёт",
            defaultextension ="*.txt",filetypes=filetypes)
    if filename:
        my_file = open(filename, "w")
        
        string=str(user_fullname)+", отчёт за "+str(current_month)+" месяц "
        string+=str(current_year)+" года:\n\n"
        days.sort(key=custom_key)
        print(days)
        if str(type_combobox.get())=="Повременная":
            for name in days:
                string+="   день "+str(name[0])+": "+str(floatt(name[1]))+" часов работы\n"
            string+="\n\nИтого: "+str(hours[2])+" часов работы.\n"

        else:
            for name in days:
                string+="   день "+str(name[0])+": "+str(floatt(name[1]))+" товаров (услуг)\n"
            string+="\n\nИтого: "+str(items[2])+" товаров (услуг).\n"

        string+="Чистая зарплата: "+str(pay)+" руб.\n"
        string+="НДФЛ: "+str(ndlf)+" руб.\n"
        string+="Итоговая сумма: "+str(black)+" руб.\n"
        string+="Из неё аванс: "+str(result1)+" руб.\n"
            
        my_file.write(string)
        my_file.close()

        
def custom_key(people):
    return int(people[0])
    
def command_cal_selected(e):
    global current_day
    global current_month
    global current_year
    global current_user_id
    global con
    global cur
    global day_hours_text
    global day_items_text
    global type_combobox
    print("день")

    datetime=cal.selection_get()
    new_day = int(str(datetime)[8:])
    new_month = int(str(datetime)[5:7])
    new_year = int(str(datetime)[:4])
    
    day_hours_text.config(state="normal")
    day_items_text.config(state="normal")
    if new_day!=current_day or new_month!=current_month or new_year!=current_year:
        current_day = new_day
        current_month = new_month
        current_year = new_year
        

        day_hours_text.delete(0,tkinter.END)
        day_items_text.delete(0,tkinter.END)

        string='select day_hours, day_items from DAYS '
        string+='where day_owner = '+str(current_user_id)+' and day_day = "'+str(current_day)+'" and day_month = "'+str(current_month)+'" and day_year = "'+str(current_year)+'";'
        cur.execute(string)
        s = cur.fetchall()
        print("s==="+str(s))
        con.commit()
        if s==[]:
            day_hours_text.insert(0,"")
            day_items_text.insert(0,"")
        else:
            for name in s:
                day_hours_text.insert(0,name[0])
                day_items_text.insert(0,name[1])

    if str(type_combobox.get())=="Повременная":
        day_hours_text.config(state="normal",background="white")
        day_items_text.config(state="disabled",background="white")
    else:
        day_hours_text.config(state="disabled",background="white")
        day_items_text.config(state="normal",background="white")
        
def command_cal_month_changed(e):
    print("месяц")
    cal.selection_clear()
    current_day = int(0)
    current_month = int(0)
    current_year = int(0)
    day_hours_text.delete(0,tkinter.END)
    day_hours_text.insert(0,"")
    day_hours_text.config(state="disabled",background="whitesmoke")
    day_items_text.delete(0,tkinter.END)
    day_items_text.insert(0,"")
    day_items_text.config(state="disabled",background="whitesmoke")
    
def command_open_sql_btn():
    global max_user_id
    global current_user_id
    global current_filepath
    global con
    global cur
    global stake_text
    global hours_stake_text
    global items_cost_text
    global change_name_text
    filetypes = (("База данных SQLite", "*.db"),("Любой", "*"))
    filename = fd.askopenfilename(title="Открыть файл",
            defaultextension ="*.db",filetypes=filetypes)
    if filename:
        if current_filepath!="":
            con.close()
        current_filepath=filename
        open_existing_database()
        update_locked_cells()
        set_name_values()
        tk.title("БыстрыйСчёт "+str(current_filepath))

        string='select user_type, user_stake, user_hours_stake, user_days_stake, user_items_cost from USERS '
        string+='where user_id = '+str(current_user_id)+';'
        cur.execute(string)
        s = cur.fetchall()
        for name in s:
            type_combobox.config(state="normal")
            hours_stake_text.config(state="normal")
            hours_days_text.config(state="normal")
            items_cost_text.config(state="normal")
            change_name_text.config(state="normal")
            if name[0]==0:
                type_combobox.current(0)
            else:
                type_combobox.current(1)
            stake_text.delete(0,tkinter.END)
            stake_text.insert(0,str(name[1]))
            hours_stake_text.delete(0,tkinter.END)
            hours_stake_text.insert(0,str(name[2]))
            hours_days_text.delete(0,tkinter.END)
            hours_days_text.insert(0,str(name[3]))
            items_cost_text.delete(0,tkinter.END)
            items_cost_text.insert(0,str(name[4]))
            change_name_text.delete(0,tkinter.END)
            change_name_text.insert(0,"")
            update_locked_cells()
            
        day_hours_text.config(state="normal")
        day_items_text.config(state="normal")

        day_hours_text.delete(0,tkinter.END)
        day_items_text.delete(0,tkinter.END)

        string='select day_hours, day_items from DAYS '
        string+='where day_owner = '+str(current_user_id)+' and day_day = "'+str(current_day)+'" and day_month = "'+str(current_month)+'" and day_year = "'+str(current_year)+'";'
        cur.execute(string)
        s = cur.fetchall()
        con.commit()
        if s==[]:
            day_hours_text.insert(0,"")
            day_items_text.insert(0,"")
        else:
            for name in s:
                day_hours_text.insert(0,name[0])
                day_items_text.insert(0,name[1])

        
def command_save_sql_btn():
    global current_filepath
    global con
    global cur
    filetypes = (("База данных SQLite", "*.db"),("Любой", "*"))
    filename = fd.asksaveasfilename(title="Сохранить файл",
            defaultextension ="*.db",filetypes=filetypes)
    if filename:
        con.close()
        shutil.copyfile(current_filepath,filename)
        current_filepath=filename
        con = sqlite3.connect(current_filepath)
        sqlite3.enable_callback_tracebacks(True)
        tk.title("БыстрыйСчёт "+str(current_filepath))
        cur = con.cursor()
        print("saved")
        print(current_filepath)

def command_new_sql_btn():
    global max_user_id
    global current_user_id
    global current_filepath
    global con
    global cur
    global stake_text
    global hours_stake_text
    global items_cost_text
    global change_name_text
    filetypes = (("База данных SQLite", "*.db"),("Любой", "*"))
    filename = fd.asksaveasfilename(title="Создать файл",
            defaultextension ="*.db",filetypes=filetypes)
    if filename:
        if current_filepath!="":
            con.close()
        print("created")
        current_filepath=filename
        print(current_filepath)
        print("!")
        
        create_new_database()
        print("max_user_id = "+str(max_user_id))
        update_locked_cells()
        set_name_values(True)
        tk.title("БыстрыйСчёт "+str(current_filepath))
        
        string='select user_type, user_stake, user_hours_stake, user_items_cost from USERS '
        string+='where user_id = '+str(current_user_id)+';'
        cur.execute(string)
        s = cur.fetchall()
        print("sss= "+str(s))
        for name in s:
            if name[0]==0:
                type_combobox.current(0)
            else:
                type_combobox.current(1)
            stake_text.delete(0,tkinter.END)
            stake_text.insert(0,str(name[1]))
            hours_stake_text.delete(0,tkinter.END)
            hours_stake_text.insert(0,str(name[2]))
            items_cost_text.delete(0,tkinter.END)
            items_cost_text.insert(0,str(name[3]))
            change_name_text.delete(0,tkinter.END)
            change_name_text.insert(0,"")
            update_locked_cells()
    
def command_new_user_btn():
    global current_user_id
    global max_user_id
    global con
    global cur
    print("new_user")
    max_user_id=max_user_id+1
    string="insert into USERS (user_id,user_name,user_type,user_stake,user_hours_stake,user_days_stake,user_items_cost) "
    string+="values ("+str(max_user_id)+",'',0,'','40','','');"
    cur.execute(string)
    con.commit()
    current_user_id=max_user_id
    set_name_values(True)

def command_name_combobox(e):
    print("combobox_name")
    print(str(name_combobox.get()))
    change_user()
    update_locked_cells()

def command_type_combobox(e):
    print("combobox_type")
    print(str(type_combobox.get()))
    update_locked_cells()

def command_change_name_btn():
    print("change_name_btn")
    set_user_values(True)

def command_stake_text(e):
    global stake_text
    print("wow")
    current_selection_cell='stake_text'
    current_selection_text=stake_text.get()
    print(str(stake_text.get()))
    
def command_stake_text2(e):
    global stake_text
    print("wow2")
    current_selection_cell='stake_text'
    current_selection_text=stake_text.get()
    print(str(stake_text.get()))

def command_day_weekend_btn():
    print("command_day_weekend_btn")
    write_day_sql()

def command_get_payment_btn():
    print("ENDING")
    get_all_done()


    
tk = tkinter.Tk()
tk.geometry("580x600")
tk.title("БыстрыйСчёт")
tk.resizable(width=False, height=False)
if os.path.exists("pick.ico"):
    tk.iconbitmap(default="pick.ico")

open_sql_btn = tkinter.Button(text="Открыть",width=9,command=command_open_sql_btn)
open_sql_btn.place(x=15,y=10)

save_sql_btn = tkinter.Button(text="Сохранить",width=9,command=command_save_sql_btn,state="disabled")
save_sql_btn.place(x=15,y=45)

new_sql_btn = tkinter.Button(text="Новый\nфайл",width=9,command=command_new_sql_btn)
new_sql_btn.place(x=100,y=10)

new_user_btn = tkinter.Button(text="Новый\nсотрудник",width=9,command=command_new_user_btn,state="disabled")
new_user_btn.place(x=230,y=10)

name_label = tkinter.Label(text="ФИО")
name_label.place(x=307,y=33)

name_values = ["","",""]
name_values_var = tkinter.StringVar(value=name_values[0])
name_combobox = ttk.Combobox(textvariable=name_values_var,values=name_values,state="disabled",background="whitesmoke")
name_combobox.place(x=340,y=10)
name_combobox.bind("<<ComboboxSelected>>", command_name_combobox)

change_name_text = tkinter.Entry(width=20,state="disabled",background="whitesmoke")
change_name_text.place(x=340,y=33)

change_name_btn = tkinter.Button(text="Сохранить\nсотрудника",command=command_change_name_btn,state="disabled")
change_name_btn.place(x=490,y=10)







stake_label = tkinter.Label(text="Оклад",width=13,anchor="e")
stake_label.place(x=15,y=80)

stake_text = tkinter.Entry(width=13,state="disabled",background="whitesmoke")
stake_text.place(x=120,y=80)
stake_text.bind("<ButtonPress>", command_stake_text)
stake_text.bind("<Deactivate>", command_stake_text2)

hours_stake_label = tkinter.Label(text="Часов в рабочей\nнеделе",width=13,anchor="e")
hours_stake_label.place(x=15,y=110)

hours_stake_text = tkinter.Entry(width=13,state="disabled",background="whitesmoke")
hours_stake_text.place(x=120,y=115)

hours_days_label = tkinter.Label(text="Рабочих дней\n за период",width=13,anchor="e")
hours_days_label.place(x=15,y=145)

hours_days_text = tkinter.Entry(width=13,state="disabled",background="whitesmoke")
hours_days_text.place(x=120,y=150)

hours_work_label = tkinter.Label(text="Часов работы\n за период",width=13,anchor="e")
hours_work_label.place(x=15,y=180)

hours_work_text = tkinter.Entry(width=13,state="disabled",background="whitesmoke")
hours_work_text.place(x=120,y=185)












type_label = tkinter.Label(text="Тип зарплаты",width=18,anchor="e")
type_label.place(x=315,y=80)

type_values = ["Повременная","Сдельная"]
type_values_var = tkinter.StringVar(value=type_values[0])
type_combobox = ttk.Combobox(width=11,textvariable=type_values_var,values=type_values,state="disabled",background="whitesmoke")
type_combobox.place(x=460,y=80)
type_combobox.bind("<<ComboboxSelected>>", command_type_combobox)

items_cost_label = tkinter.Label(text="Оплата за один\nпродукт (услугу)",width=14,anchor="e")
items_cost_label.place(x=15,y=80)
items_cost_label.place_forget()

items_cost_text = tkinter.Entry(width=13,state="disabled",background="whitesmoke")
items_cost_text.place(x=120,y=80)
items_cost_text.place_forget()

items_count_label = tkinter.Label(text="Продуктов (услуг)\nза период",width=14,anchor="e")
items_count_label.place(x=15,y=115)
items_count_label.place_forget()

items_count_text = tkinter.Entry(width=13,state="disabled",background="whitesmoke")
items_count_text.place(x=120,y=115)
items_count_text.place_forget()






cal = Calendar(selectmode = 'day',
               year = 2023, month = 1,
               day = 1,state="disabled",background="whitesmoke")
cal.place(x=15,y=400)
cal.bind("<<CalendarSelected>>", command_cal_selected)
cal.bind("<<CalendarMonthChanged>>", command_cal_month_changed)

day_hours_label = tkinter.Label(text="Часов работы\nза день",width=14,anchor="e")
day_hours_label.place(x=285,y=400)

day_hours_text = tkinter.Entry(width=9,state="disabled",background="whitesmoke")
day_hours_text.place(x=390,y=400)

day_items_label = tkinter.Label(text="Продуктов (услуг)\nза день",width=14,anchor="e")
day_items_label.place(x=285,y=400)
day_items_label.place_forget()

day_items_text = tkinter.Entry(width=9,state="disabled",background="whitesmoke")
day_items_text.place(x=390,y=470)
day_items_text.place_forget()

#day_to_sql_label = tkinter.Label(text="",width=10,anchor="e")
#day_to_sql_label.place(x=300,y=435)

day_weekend_btn = tkinter.Button(text="Записать",width=7,command=command_day_weekend_btn,state="disabled")
day_weekend_btn.place(x=390,y=430)




time_start_label = tkinter.Label(text="З.п. 1 (аванс)",height=2,width=14)
time_start_label.place(x=15,y=290)

time_start_text = tkinter.Entry(width=15,state="disabled",background="whitesmoke")
time_start_text.place(x=15,y=325)


time_end_label = tkinter.Label(text="З.п. 2",height=2,width=14)
time_end_label.place(x=145,y=290)

time_end_text = tkinter.Entry(width=15,state="disabled",background="whitesmoke")
time_end_text.place(x=145,y=325)

get_payment_btn = tkinter.Button(text="Сохранить данные\nи рассчитать",width=14,command=command_get_payment_btn,state="disabled")
get_payment_btn.place(x=267,y=305)






price_white_label = tkinter.Label(text="Начислено",height=2,width=14)
price_white_label.place(x=15,y=225)

price_white_text = tkinter.Entry(width=15,state="disabled",background="whitesmoke")
price_white_text.place(x=15,y=260)

price_ndfl_label = tkinter.Label(text="Вычтено: НДФЛ",height=2,width=14)
price_ndfl_label.place(x=145,y=225)

price_ndfl_text = tkinter.Entry(width=15,state="disabled",background="whitesmoke")
price_ndfl_text.place(x=145,y=260)

price_summ_label = tkinter.Label(text="Итого\nза месяц",width=14)
price_summ_label.place(x=275,y=225)

price_summ_text = tkinter.Entry(width=15,state="disabled",background="whitesmoke")
price_summ_text.place(x=275,y=260)




tk.protocol("WM_DELETE_WINDOW", on_closing)

tk.mainloop()
