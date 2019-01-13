from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import tkinter.ttk as ttk
import time
import datetime
import sys
#========================================HOME PAGE==================================
#home page layout
root = Tk()
root.title("Inventory System")

width = 1024
height = 720
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#3cb371")

#========================================VARIABLES========================================
USERNAME = StringVar()
PASSWORD = StringVar()
PRODUCT_CODE = StringVar()
PRODUCT_QTY = IntVar()
PRODUCT_NAME = StringVar()
SEARCH = StringVar()

#========================================METHODS==========================================

#========================================LOG ON MENU==================================
# database connection and tabel setup
def Database():
    global conn, cursor
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `product` (product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, product_code TEXT, product_name TEXT, product_qty TEXT)")
    cursor.execute("SELECT * FROM `admin` WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `admin` (username, password) VALUES('admin', 'admin')")
        conn.commit()
# exiting request
def Exit():
    result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()
#exiting request
def Exit2():
    result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        Home.destroy()
        exit()
# log on box layout
def ShowLoginForm():
    global loginform
    loginform = Toplevel()
    loginform.title("Inventory System/Account Login")
    width = 400
    height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    loginform.resizable(0, 0)
    loginform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    LoginForm()
# log on access form layout    
def LoginForm():
    global lbl_result
    TopLoginForm = Frame(loginform, width=200, height=200, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=20)
    lbl_text = Label(TopLoginForm, text="Administrator Login", font=('arial', 18,), width=100)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(loginform, width=200)
    MidLoginForm.pack(side=TOP, pady=2)
    lbl_username = Label(MidLoginForm, text="Username:", font=('arial', 18), bd=2)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="Password:", font=('arial', 18), bd=2)
    lbl_password.grid(row=1)
    lbl_result = Label(MidLoginForm, text="", font=('arial', 18))
    lbl_result.grid(row=3, columnspan=2)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 12), width=10)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 12), width=10, show="*")
    password.grid(row=1, column=1)
    btn_login = Button(MidLoginForm, text="Login", font=('arial', 18), width=10, command=Login)
    btn_login.grid(row=2, columnspan=2, pady=2)
    btn_login.bind('<Return>', Login)

#========================================HOME PAGE==================================
# home page layout
def Home():
    global Home
    Home = Tk()
    Home.title("Inventory System")
    width = 1024
    height = 720
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    Home.resizable(0, 0)
    Title = Frame(Home, bd=1, relief=SOLID,)
    Title.pack(pady=10)
    lbl_display = Label(Title, text="Skillage I.T Inventory System", font=('arial', 25,))
    lbl_display.pack()
    menubar = Menu(Home)
    filemenu = Menu(menubar, tearoff=0)
    filemenu2 = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Logout", command=Logout)
    filemenu.add_command(label="Exit", command=Exit2)
    filemenu2.add_command(label="Add new", command=ShowAddNew)
    filemenu2.add_command(label="Edit/Search", command=ShowView)
    menubar.add_cascade(label="Account", menu=filemenu)
    menubar.add_cascade(label="Inventory", menu=filemenu2)
    Home.config(menu=menubar)
    Home.config(bg="cornflowerBlue")
    
#========================================EDITING FORMS==================================
#===========######Adding New Inventory, searching and editing##########
#new inventory background box layout
def ShowAddNew():
    global addnewform
    addnewform = Toplevel()
    addnewform.title("Inventory System/Add new")
    width = 500
    height = 200
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    addnewform.resizable(0, 0)
    AddNewForm()
#new products form layout
def AddNewForm():
    TopAddNew = Frame(addnewform, width=200, height=200, bd=1, relief=SOLID)
    TopAddNew.pack(side=TOP, pady=2)
    lbl_text = Label(TopAddNew, text="Add New Product", font=('arial', 18), width=100)
    lbl_text.pack(fill=X)
    MidAddNew = Frame(addnewform, width=200)
    MidAddNew.pack(side=TOP, pady=5)
    lbl_productcode = Label(MidAddNew, text="Product Code:", font=('arial', 18), bd=2, fg = "OrangeRed2")
    lbl_productcode.grid(row=0, sticky=W)
    lbl_productname = Label(MidAddNew, text="Product Name:", font=('arial', 18), bd=2, fg = "OrangeRed2")
    lbl_productname.grid(row=1, sticky=W)
    lbl_productqty = Label(MidAddNew, text="Product Qty:", font=('arial', 18), bd=2, fg = "OrangeRed2")
    lbl_productqty.grid(row=2, sticky=W)
    productcode = Entry(MidAddNew, textvariable=PRODUCT_CODE, font=('arial', 18), width=10)
    productcode.grid(row=0, column=1)
    productname = Entry(MidAddNew, textvariable=PRODUCT_NAME, font=('arial', 18), width=10)
    productname.grid(row=1, column=1)
    productqty = Entry(MidAddNew, textvariable=PRODUCT_QTY, font=('arial', 18), width=10)
    productqty.grid(row=2, column=1)
    btn_add = Button(MidAddNew, text="Save", font=('arial', 18), width=10, bg="#3cb371", command=AddNew)
    btn_add.grid(row=3, columnspan=2, pady=2)
    
# Adding new entry 
def AddNew():
    Database()
    cursor.execute("INSERT INTO `product` (product_code, product_name, product_qty) VALUES(?, ?, ?)", (str(PRODUCT_CODE.get()), str(PRODUCT_NAME.get()), int(PRODUCT_QTY.get())))
    conn.commit()
    PRODUCT_CODE.set("")
    PRODUCT_NAME.set("")
    PRODUCT_QTY.set("")
    cursor.close()
    conn.close()
#================#######Inventory Search and Editing#############
#search form layout
def ViewForm():
    global tree
    TopViewForm = Frame(viewform, width=200, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=200)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=640)
    MidViewForm.pack(side=RIGHT)
    lbl_text = Label(TopViewForm, text="View Products", font=('arial', 18), width=400)
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftViewForm, text="Search", font=('arial', 15))
    lbl_txtsearch.pack(side=TOP, anchor=W)
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('arial', 15), width=10)
    search.pack(side=TOP,  padx=10, fill=X)
    btn_search = Button(LeftViewForm, text="Search", command=Search)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_reset = Button(LeftViewForm, text="Reset Search", command=Reset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_delete = Button(LeftViewForm, text="Delete", command=Delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_report = Button(LeftViewForm, text="Run report", command=Report)
    btn_report.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=("ProductID", "Product Code", "Product Name", "Product Qty"), selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('ProductID', text="ProductID",anchor=W)
    tree.heading('Product Code', text="Product Code",anchor=W)
    tree.heading('Product Name', text="Product Name",anchor=W)
    tree.heading('Product Qty', text="Product Qty",anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=0)
    tree.column('#2', stretch=NO, minwidth=0, width=100)
    tree.column('#3', stretch=NO, minwidth=0, width=200)
    tree.column('#4', stretch=NO, minwidth=0, width=100)
    tree.pack()
    DisplayData()
# request display search request
def DisplayData():
    Database()
    cursor.execute("SELECT * FROM `product`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database()
        cursor.execute("SELECT * FROM `product` WHERE `product_name` LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

# resetting search request
def Reset():
     tree.delete(*tree.get_children())
     DisplayData()
     SEARCH.set("")
    
#deleting entry data
def Delete():
    if not tree.selection():
       print("ERROR")
    else:
        result = tkMessageBox.askquestion('Iventory System', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `product` WHERE `product_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()       
            
def Report():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database()
        cursor.execute("SELECT * FROM `product` WHERE `product_name` LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
            outF = open("file.txt", "w")
            outF.writelines(all_lines)
    print ("new report")

#Inventory layout
def ShowView():
    global viewform
    viewform = Toplevel()
    viewform.title("Inventory System/View Product")
    width = 550
    height = 400
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    viewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    viewform.resizable(0, 0)
    ViewForm()   

#========================================LOG OUT==================================

def Logout():
    result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to logout?', icon="warning")
    if result == 'yes': 
        admin_id = ""
        root.deiconify()
        Home.destroy()

#========================================LOG IN==================================

def Login(event=None):
    global admin_id
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
            data = cursor.fetchone()
            admin_id = data[0]
            USERNAME.set("")
            PASSWORD.set("")
            lbl_result.config(text="")
            ShowHome()
        else:
            lbl_result.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close() 

def ShowHome():
    root.withdraw()
    Home()
    loginform.destroy()


#========================================MENUBAR WIDGETS==================================
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="ACCOUNT", command=ShowLoginForm)
filemenu.add_command(label="EXIT", command=Exit)
menubar.add_cascade(label="LOG ON", menu=filemenu)
root.config(menu=menubar)

#========================================FRAME============================================
Title = Frame(root, bd=4, relief=SOLID)
Title.pack(pady=250)

#========================================LABEL WIDGET=====================================
lbl_display = Label(Title, text="Skillage I.T Inventory System", font=('arial', 45))
lbl_display.pack()

#========================================INITIALIZATION===================================
if __name__ == '__main__':
    root.mainloop()
