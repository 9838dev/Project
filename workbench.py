# creating workbech

from tkinter import * 
import sqlite3
from tkinter import Toplevel
from tkinter import messagebox

root = Tk()
root.title('Workbench')
root.geometry("300x300")

# create table

"""
create table address(
    first_name text,
    last_name text,
    address text,
    city text,
    state text,
    zipcode integer
)
    
"""

def set_record():
    db = sqlite3.connect('address_book.db')
    cursor = db.cursor()
    
    global update_box,first_name_entry_editor,last_name_entry_editor,address_entry_editor,city_entry_editor,state_entry_editor,zipcode_entry_editor,update,record_id
    
    cursor.execute("""
    UPDATE address SET
    first_name = :firstname,
    last_name = :lastname,
    address = :address,
    city = :city,
    state = :state,
    zipcode = :zipcode
    WHERE oid = :oid""",
    {
        'firstname':first_name_entry_editor.get(),
        'lastname':last_name_entry_editor.get(),
        'address':address_entry_editor.get(),
        'city':city_entry_editor.get(),
        'state':state_entry_editor.get(),
        'zipcode':zipcode_entry_editor.get(),
        'oid':record_id
    })
    
    db.commit()
    db.close()
    update.destroy()
    messagebox.showinfo("Update Message","Successfull Updated")

def update_record():
    global first_name_entry_editor,last_name_entry_editor,address_entry_editor,city_entry_editor,state_entry_editor,zipcode_entry_editor,up,update_box,record_id,update
    
    db = sqlite3.connect('address_book.db')
    # create cursor
    cursor = db.cursor()
    
    record_id = update_box.get()
    cursor.execute("Select * from address where oid = "+record_id)
    record = cursor.fetchall()
    
    #commit changes
    db.commit()

    # close connection
    db.close()
    up.destroy()
    
    if len(record) == 0:
        messagebox.showerror("Error","Record Not Found")
        
    else:
        update = Tk()
        update.title("Updating row")
        
        # Creating Labels
        first_name = Label(update,text='First Name:',padx=20,pady=20,font=10)
        last_name = Label(update,text='Last Name:',padx=20,pady=20,font=10)
        address = Label(update,text='Address:',padx=20,pady=20,font=10)
        city = Label(update,text='City:',padx=20,pady=20,font=10)
        state = Label(update,text='State:',padx=20,pady=20,font=10)
        zipcode = Label(update,text='Zipcode:',padx=20,pady=20,font=10)

        # Creating Entries
        first_name_entry_editor = Entry(update,width=30,borderwidth=3)
        last_name_entry_editor = Entry(update,width=30,borderwidth=3)
        address_entry_editor = Entry(update,width=30,borderwidth=3)
        city_entry_editor = Entry(update,width=30,borderwidth=3)
        state_entry_editor = Entry(update,width=30,borderwidth=3)
        zipcode_entry_editor = Entry(update,width=30,borderwidth=3)


        # Putting labels in window
        first_name.grid(row=0,column=0)  
        last_name.grid(row=1,column=0)
        address.grid(row=2,column=0)
        city.grid(row=3,column=0)
        state.grid(row=4,column=0)
        zipcode.grid(row=5,column=0)

        # Putting Entries in Window
        first_name_entry_editor.grid(row=0,column=1)  
        last_name_entry_editor.grid(row=1,column=1)
        address_entry_editor.grid(row=2,column=1)
        city_entry_editor.grid(row=3,column=1)
        state_entry_editor.grid(row=4,column=1)
        zipcode_entry_editor.grid(row=5,column=1)

        for rec in record:
            first_name_entry_editor.insert(0,rec[0])
            last_name_entry_editor.insert(0,rec[1])
            address_entry_editor.insert(0,rec[2])
            city_entry_editor.insert(0,rec[3])
            state_entry_editor.insert(0,rec[4])
            zipcode_entry_editor.insert(0,rec[5])

    
        # creating submit button
        submit_btn = Button(update,text='Save',command=set_record,borderwidth=3)

        submit_btn.grid(row=6,column=1,ipadx=100) 


def update_row():
    global up,update_box
    up = Tk()
    up.title('Updating Row')
    
    label = Label(up,text='Enter Row id : : :',padx=10,pady=10)
    update_box = Entry(up,width=50,borderwidth=3)
    btn = Button(up,text='Select',borderwidth=4,command=update_record)
    
    label.grid(row=0,column=0)
    update_box.grid(row=0,column=1,padx=10)
    btn.grid(row=1,column=1,pady=10,ipadx=100)
    

def delete():
    global dele,delete_box
    db = sqlite3.connect('address_book.db')

    cursor = db.cursor()
    
    cursor.execute("Delete from address where oid = "+delete_box.get())
    
    db.commit()
    db.close()
    
    dele.destroy()
    messagebox.showinfo("Delete","Row Deleted Successfully")

def delete_row():
    global dele,delete_box
    dele = Tk()
    dele.title('Deleting row')
    
    label = Label(dele,text='Enter Row id : : :',padx=10,pady=10)
    delete_box = Entry(dele,width=50,borderwidth=3)
    btn = Button(dele,text='Select',borderwidth=4,command=delete)
    
    label.grid(row=0,column=0)
    delete_box.grid(row=0,column=1,padx=10)
    btn.grid(row=1,column=1,pady=10,ipadx=100)

def show_record():
    top = Toplevel()
    top.title('Records')
    top.geometry("700x600")
    
    # creating database if not exists
    db = sqlite3.connect('address_book.db')

    # create cursor
    cursor = db.cursor()
    
    cursor.execute('select oid,* from address')
    records = cursor.fetchall()
    
    id_label = Label(top,text='id')
    first_name_label = Label(top,text='First_Name')
    last_name_label = Label(top,text='Last Name')
    address_label = Label(top,text='Address')
    city_label = Label(top,text='City')
    state_label = Label(top,text='State')
    zipcode_label = Label(top,text='Zipcode')
    
    
    id_label.grid(row=0,column=0,padx=10)
    first_name_label.grid(row=0,column=1,padx=20)
    last_name_label.grid(row=0,column=2,padx=20)
    address_label.grid(row=0,column=3,padx=20)
    city_label.grid(row=0,column=4,padx=20)
    state_label.grid(row=0,column=5,padx=20)
    zipcode_label.grid(row=0,column=6,padx=20)
    
    i=1
    for record in records:
        for col,row in enumerate(record):
            Label(top,text=str(row)).grid(row=i,column=col)
        i+=1
    
    #commit changes
    db.commit()

    # close connection
    db.close()
    
def submit():
    global add,first_name_entry,last_name_entry,address_entry,city_entry,state_entry,zipcode_entry
    
    # creating database if not exists
    db = sqlite3.connect('address_book.db')

    # create cursor
    cursor = db.cursor()
    
    # inserting into database
    cursor.execute("insert into address values(:first_name,:last_name,:address,:city,:state,:zipcode)",
                  {
                      'first_name':first_name_entry.get(),
                      'last_name':last_name_entry.get(),
                      'address':address_entry.get(),
                      'city':city_entry.get(),
                      'state':state_entry.get(),
                      'zipcode':zipcode_entry.get()
                  })
    
    #commit changes
    db.commit()

    # close connection
    db.close()
    
    add.destroy()
    messagebox.showinfo("showing info","Row added successfully")
    
def add_row():
    global add,first_name_entry,last_name_entry,address_entry,city_entry,state_entry,zipcode_entry
    add = Toplevel()
    add.config(bg='Black')
    
    # Creating Labels
    first_name = Label(add,text='First Name:',padx=20,pady=30,font=10,bg='Black',fg='White')
    last_name = Label(add,text='Last Name:',padx=20,pady=30,font=10,bg='Black',fg='White')
    address = Label(add,text='Address:',padx=20,pady=30,font=10,bg='Black',fg='White')
    city = Label(add,text='City:',padx=20,pady=30,font=10,bg='Black',fg='White')
    state = Label(add,text='State:',padx=20,pady=30,font=10,bg='Black',fg='White')
    zipcode = Label(add,text='Zipcode:',padx=20,pady=30,font=10,bg='Black',fg='White')

    # Creating Entries
    first_name_entry = Entry(add,width=30)
    last_name_entry = Entry(add,width=30)
    address_entry = Entry(add,width=30)
    city_entry = Entry(add,width=30)
    state_entry = Entry(add,width=30)
    zipcode_entry = Entry(add,width=30)


    # Putting labels in window
    first_name.grid(row=0,column=0)  
    last_name.grid(row=1,column=0)
    address.grid(row=2,column=0)
    city.grid(row=3,column=0)
    state.grid(row=4,column=0)
    zipcode.grid(row=5,column=0)

    # Putting Entries in Window
    first_name_entry.grid(row=0,column=1)  
    last_name_entry.grid(row=1,column=1)
    address_entry.grid(row=2,column=1)
    city_entry.grid(row=3,column=1)
    state_entry.grid(row=4,column=1)
    zipcode_entry.grid(row=5,column=1)


    # creating submit button
    submit_btn = Button(add,text='Submit',bg='Black',fg='White',
                                 command=submit,borderwidth=5)
    submit_btn.grid(row=6,column=1,padx=10,pady=10,ipadx=100)
    
    
info_label = Label(root,text="DB: address_book.db   TABLE: address",padx=5,pady=5,font=('Helvetica bold',11))    
btn_show = Button(root,text='Show Record',command=show_record,borderwidth=5,padx=5,pady=5)
btn_add = Button(root,text='Add Row',command=add_row,borderwidth=5,padx=15,pady=5)
btn_delete = Button(root,text='Delete Row',command=delete_row,borderwidth=5,padx=10,pady=5)
btn_update = Button(root,text='Update Row',command=update_row,borderwidth=5,padx=10,pady=5)

info_label.pack(padx=20,pady=10)
btn_show.pack(padx=10,pady=10)
btn_add.pack(padx=10,pady=10)
btn_delete.pack(padx=10,pady=10)
btn_update.pack(padx=10,pady=10)


root.mainloop()