from tkinter import *
import sqlite3
from tkinter import ttk
import csv

root = Tk()
root.title("Database Toko Bulat")
root.iconbitmap("./Image/Design.ico")
root.geometry("600x600")

#select a.kode, a.nama, b.tanggal, b.akun, b.qty, b.harga
#from barang a inner join pembelian b
#on a.kode = b.kode
#database
#create a database or connect to one
conn = sqlite3.connect("./db/tokobulat.db")

#create cursor
c = conn.cursor()
print("Database created and Successfully Connected to SQLite")

#create table 
c.execute("""CREATE TABLE IF NOT EXISTS Barang (
    Kode CHAR PRIMARY KEY,
    Nama STRING,
    DKecil NUMERIC,
    DBesar NUMERIC,
    HPP NUMERIC,
    QTY NUMERIC,
    QTYGud NUMERIC,
    QTYBeli NUMERIC,
    QTYJual NUMERIC 
    )
    """)

c.execute("""CREATE TABLE IF NOT EXISTS Pembelian (
    Tanggal DATE,
    Akun STRING,
    Kode CHAR REFERENCES Barang (Kode) ON DELETE CASCADE
                                       ON UPDATE CASCADE,
    QTY NUMERIC,
    Harga NUMERIC
    )
    """)

c.execute("""CREATE TABLE IF NOT EXISTS Penjualan (
    Tanggal DATE,
    Pembeli STRING,
    Kode CHAR REFERENCES Barang (Kode) ON DELETE CASCADE
                                       ON UPDATE CASCADE,
    QTY NUMERIC,
    Harga NUMERIC,
    PotToped NUMERIC,
    PotOng NUMERIC
    )
    """)

c.execute("""CREATE TABLE IF NOT EXISTS Kedatangan (
    Tanggal DATE,
    Akun STRING,
    Kode CHAR REFERENCES Barang (Kode) ON DELETE CASCADE
                                       ON UPDATE CASCADE,
    QTY NUMERIC
    )
    """)

c.execute("""CREATE TABLE IF NOT EXISTS Pembayaran (
    Tanggal DATE,
    Pembeli STRING,
    Nominal STRING
    )
    """)

#penjualan
def penjualan():
    penjualan_query = Tk()
    penjualan_query.title("Input Penjualan")
    penjualan_query.iconbitmap("./Image/Design.ico")
    penjualan_query.geometry("350x200")
    
    def submit():
        #create a database or connect to one
        conn = sqlite3.connect("./db/tokobulat.db")
        #create cursor
        c = conn.cursor()
        print("Database created and Successfully Connected to SQLite")
        #insert into table
        c.execute("INSERT INTO Penjualan Values (:tanggal, :pembeli, :kode, :qty, :harga, :potToped, :potOng )",
                {
                    "tanggal": tanggal.get(),
                    "pembeli": pembeli.get(),
                    "harga": harga.get(),
                    "kode": kode.get(),
                    "qty": qty.get(),
                    "potOng": potOng.get(),
                    "potToped":potToped.get()
                    
                })
        #:qty itu bisa bebas tergantung kalau ini qty.get
        c.execute("update Barang set QTYGud = QTYGud - :qty where kode = :kode", 
                  {
                    "kode": kode.get(),
                    "qty": qty.get()
                  })
        
        c.execute("update Barang set QTYJual = QTYJual + :qty  where kode = :kode", 
                  {
                    "kode": kode.get(),
                    "qty": qty.get()
                  })
        #commit changes
        conn.commit()
        print("SQLite table created")
        #close connection
        conn.close() 
        #clear the text boxes
        kode.delete(0, END)
        pembeli.delete(0, END)
        tanggal.delete(0, END)
        harga.delete(0, END)
        qty.delete(0, END) 
        potOng.delete(0, END)
        potToped.delete(0, END) 
    
    #create text boxes
    tanggal = Entry(penjualan_query, width=30)
    tanggal.grid(row=0, column=1, padx=20, pady=(10,0))
    pembeli = Entry(penjualan_query, width=30)
    pembeli.grid(row=1, column=1)
    kode = Entry(penjualan_query, width=30)
    kode.grid(row=2, column=1)
    qty = Entry(penjualan_query, width=30)
    qty.grid(row=3, column=1)
    harga = Entry(penjualan_query, width=30)
    harga.grid(row=4, column=1)
    potOng = Entry(penjualan_query, width=30)
    potOng.grid(row=5, column=1)
    potToped = Entry(penjualan_query, width=30)
    potToped.grid(row=6, column=1)


    #create text labels
    kode_label = Label(penjualan_query, text="Tanggal")
    kode_label.grid(row=0, column=0, pady=(10,0))
    nama_label = Label(penjualan_query, text="Pembeli")
    nama_label.grid(row=1, column=0)
    dkecil_label = Label(penjualan_query, text="Kode")
    dkecil_label.grid(row=2, column=0)
    dbesar_label = Label(penjualan_query, text="Quantity")
    dbesar_label.grid(row=3, column=0)
    hpp_label = Label(penjualan_query, text="Harga")
    hpp_label.grid(row=4, column=0)
    hpp_label = Label(penjualan_query, text="Potongan Ongkir")
    hpp_label.grid(row=5, column=0)
    hpp_label = Label(penjualan_query, text="Potongan Toped")
    hpp_label.grid(row=6, column=0)

    #submit button
    submit_btn = Button(penjualan_query, text="Input Data", command=submit)
    submit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#pembelian
def pembelian():
    pembelian_query = Tk()
    pembelian_query.title("Input Pembelian")
    pembelian_query.iconbitmap("./Image/Design.ico")
    pembelian_query.geometry("350x200")
    
    def submit():
        #create a database or connect to one
        conn = sqlite3.connect("./db/tokobulat.db")
        #create cursor
        c = conn.cursor()
        print("Database created and Successfully Connected to SQLite")
        #insert into table
        c.execute("INSERT INTO Pembelian Values (:tanggal, :akun, :kode, :qty, :harga)",
                {
                    "tanggal": tanggal.get(),
                    "akun": akun.get(),
                    "harga": harga.get(),
                    "kode": kode.get(),
                    "qty": qty.get()
                    
                })
        
        
        c.execute("update Barang set hpp = (((:harga)+(qty * hpp))/ (qty + :qty)) where kode = :kode", 
                  {
                    "harga": harga.get(),
                    "kode": kode.get(),
                    "qty": qty.get()
                  })
        
        c.execute("update Barang set qty = qty + :qty  where kode = :kode", 
                  {
                    "kode": kode.get(),
                    "qty": qty.get()
                  })

        c.execute("update Barang set QTYBeli = QTYBeli + :qty  where kode = :kode", 
                  {
                    "kode": kode.get(),
                    "qty": qty.get()
                  })
        #commit changes
        conn.commit()
        print("SQLite table created")
        #close connection
        conn.close() 
        #clear the text boxes
        kode.delete(0, END)
        akun.delete(0, END)
        tanggal.delete(0, END)
        harga.delete(0, END)
        qty.delete(0, END) 
    
    #create text boxes
    tanggal = Entry(pembelian_query, width=30)
    tanggal.grid(row=0, column=1, padx=20, pady=(10,0))
    akun = Entry(pembelian_query, width=30)
    akun.grid(row=1, column=1)
    kode = Entry(pembelian_query, width=30)
    kode.grid(row=2, column=1)
    qty = Entry(pembelian_query, width=30)
    qty.grid(row=3, column=1)
    harga = Entry(pembelian_query, width=30)
    harga.grid(row=4, column=1)


    #create text labels
    kode_label = Label(pembelian_query, text="Tanggal")
    kode_label.grid(row=0, column=0, pady=(10,0))
    nama_label = Label(pembelian_query, text="Akun")
    nama_label.grid(row=1, column=0)
    dkecil_label = Label(pembelian_query, text="Kode")
    dkecil_label.grid(row=2, column=0)
    dbesar_label = Label(pembelian_query, text="Quantity")
    dbesar_label.grid(row=3, column=0)
    hpp_label = Label(pembelian_query, text="Harga")
    hpp_label.grid(row=4, column=0)

    #submit button
    submit_btn = Button(pembelian_query, text="Input Data", command=submit)
    submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#kedatangan
def kedatangan():
    kedatangan_query = Tk()
    kedatangan_query.title("Input Kedatangan")
    kedatangan_query.iconbitmap("./Image/Design.ico")
    kedatangan_query.geometry("350x200")
    
    def submit():
        #create a database or connect to one
        conn = sqlite3.connect("./db/tokobulat.db")
        #create cursor
        c = conn.cursor()
        print("Database created and Successfully Connected to SQLite")
        #insert into table
        c.execute("INSERT INTO kedatangan Values (:tanggal, :akun, :kode, :qty)",
                {
                    "tanggal": tanggal.get(),
                    "akun": akun.get(),
                    "kode": kode.get(),
                    "qty": qty.get()
                    
                })
        c.execute("update Barang set QTYGud = QTYGud + :qty where kode = :kode", 
                  {
                    "kode": kode.get(),
                    "qty": qty.get()
                  })
        
        c.execute("update Barang set QTYBeli = QTYBeli - :qty  where kode = :kode", 
                  {
                    "kode": kode.get(),
                    "qty": qty.get()
                  })
        #commit changes
        conn.commit()
        print("SQLite table created")
        #close connection
        conn.close() 
        #clear the text boxes
        kode.delete(0, END)
        akun.delete(0, END)
        tanggal.delete(0, END)
        qty.delete(0, END) 
    
    #create text boxes
    tanggal = Entry(kedatangan_query, width=30)
    tanggal.grid(row=0, column=1, padx=20, pady=(10,0))
    akun = Entry(kedatangan_query, width=30)
    akun.grid(row=1, column=1)
    kode = Entry(kedatangan_query, width=30)
    kode.grid(row=2, column=1)
    qty = Entry(kedatangan_query, width=30)
    qty.grid(row=3, column=1)



    #create text labels
    kode_label = Label(kedatangan_query, text="Tanggal")
    kode_label.grid(row=0, column=0, pady=(10,0))
    nama_label = Label(kedatangan_query, text="Akun")
    nama_label.grid(row=1, column=0)
    dkecil_label = Label(kedatangan_query, text="Kode")
    dkecil_label.grid(row=2, column=0)
    dbesar_label = Label(kedatangan_query, text="Quantity")
    dbesar_label.grid(row=3, column=0)

    #submit button
    submit_btn = Button(kedatangan_query, text="Input Data", command=submit)
    submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#pembayaran
def pembayaran():
    pembayaran_query = Tk()
    pembayaran_query.title("Input pembayaran")
    pembayaran_query.iconbitmap("./Image/Design.ico")
    pembayaran_query.geometry("350x200")
    
    def submit():
        #create a database or connect to one
        conn = sqlite3.connect("./db/tokobulat.db")
        #create cursor
        c = conn.cursor()
        print("Database created and Successfully Connected to SQLite")
        #insert into table
        c.execute("INSERT INTO pembayaran Values (:tanggal, :pembeli, :nominal)",
                {
                    "tanggal": tanggal.get(),
                    "pembeli": pembeli.get(),
                    "nominal": nominal.get(),
                })
        
        c.execute("Select * FROM Penjualan Where pembeli = :pembeli", 
                  {
                    "pembeli": pembeli.get(),
                    "nominal": nominal.get(),
                  })
        result = c.fetchall()
        for row in result:
            code = (row[2])
            quantity = (row[3])
        
            c.execute("Update Barang SET QTYJual = QTYJual - :quantity  where kode = :kode", 
                      {
                        "quantity": quantity,
                        "kode": code
                      })

            c.execute("Update Barang SET QTY = QTY - :quantity  where kode = :kode", 
                      {
                        "kode": code,
                        "quantity": quantity
                      })

        c.execute("DELETE FROM Penjualan WHERE pembeli = :pembeli", 
                  {
                    "pembeli": pembeli.get(),
                  })



        
        #commit changes
        conn.commit()
        print("SQLite table created")
        #close connection
        conn.close() 
        #clear the text boxes
        pembeli.delete(0, END)
        tanggal.delete(0, END)
        nominal.delete(0, END)

    
    #create text boxes
    tanggal = Entry(pembayaran_query, width=30)
    tanggal.grid(row=0, column=1, padx=20, pady=(10,0))
    pembeli = Entry(pembayaran_query, width=30)
    pembeli.grid(row=1, column=1)
    nominal = Entry(pembayaran_query, width=30)
    nominal.grid(row=2, column=1)

    

    #create text labels
    kode_label = Label(pembayaran_query, text="Tanggal")
    kode_label.grid(row=0, column=0, pady=(10,0))
    nama_label = Label(pembayaran_query, text="Pembeli")
    nama_label.grid(row=1, column=0)
    hpp_label = Label(pembayaran_query, text="Nominal")
    hpp_label.grid(row=2, column=0)


    #submit button
    submit_btn = Button(pembayaran_query, text="Input Data", command=submit)
    submit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#search function
def search_barangs():
    search_barang = Tk()
    search_barang.title("All List")
    search_barang.iconbitmap("./Image/Design.ico")
    search_barang.geometry("1000x600")
    #create a database or connect to one
    conn = sqlite3.connect("./db/tokobulat.db")
    #create cursor
    c = conn.cursor()
    
    main_frame = Frame (search_barang)
    main_frame.pack(fill=BOTH, expand=1)
    #create a canvas
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH,expand=1)
    # add a scrollbar to the canvas
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    #configure the canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind("<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    #create another frame inside the canvas
    second_frame = Frame(my_canvas)
    # add that new frame to a window in the second frame
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")
    
    def search_now():
        
        #create a main frame
        selected = drop.get()
        sql = ""
        if selected == "Search by...":
           test = Label(second_frame, text="Drop down masih belum dipilih!")
           test.grid(row=0, column=4)
        if selected == "Nama Barang":
           sql = "SELECT * FROM Barang WHERE nama LIKE ?" 
           test = Label(second_frame, text="Kamu memilih Nama Barang")
           test.grid(row=0, column=4)
        if selected == "Kode Barang":
           sql = "SELECT * FROM Barang WHERE kode LIKE ?"
           test = Label(second_frame, text="Kamu memilih Kode Barang")
           test.grid(row=0, column=4)
        if selected == "Quantity":
           sql = "SELECT * FROM Barang WHERE qty LIKE ?"
           test = Label(second_frame, text="Kamu memilih Quantity")
           test.grid(row=0, column=4)
             
        searched = search_box.get()
        #sql = "SELECT * FROM Barang WHERE nama LIKE ?"
        name = (searched, )
        
        result = c.execute(sql, name)
        result = c.fetchall()
        
        
        
        if not result:
           result = "Record Not Found..."
           searched_label = Label(second_frame, text=result)
           searched_label.grid(row=3, column=0, padx=10)
           
        else:
           for index, x in enumerate(result):
              num = 0
              for y in x:
                  header = [" Kode Barang  ", "  Nama Barang  ", " Dos Kecil ", "  Dos Besar "," Dos Kecil ", "  Harga Pokok ", "  Quantity  ", " Quantity Gudang ", " Quantity Beli ", " Quantity Jual "]
                  header = Label(second_frame, text=header[num])
                  header.grid(row=4, column=num)
                  searched_label = Label(second_frame, text=y)
                  searched_label.grid(row=index+6, column=num, padx=10)
                  num += 1    
        csv_button = Button(second_frame, text="Save to Excel", command=lambda: write_to_csv(result))
        csv_button.grid(row=1, column=2) 
    
    #entry box
    search_box = Entry(second_frame)
    search_box.grid(row=0, column=1, pady=10, padx=10)
    #entry box label
    search_box_label = Label(second_frame, text="Search")
    search_box_label.grid(row=0, column=0, pady=10, padx=10)
    #dropdown box
    drop = ttk.Combobox(second_frame, value=["Search by...", "Kode Barang", "Nama Barang", "Quantity"])
    drop.current(0)
    drop.grid(row=0, column=2)
    #entry box label
    search_button = Button(second_frame, text="Search Barang", command=search_now)
    search_button.grid(row=1, column=0, padx=10)
    
#write to csv Excel function
def write_to_csv(result):
    with open("Database Toko Bulat.csv", "a", newline="") as f:
        w = csv.writer(f, dialect="excel")
        for record in result:
            w.writerow(record)  
    
#list 
def list():
  
    list_query = Tk()
    list_query.title("All List")
    list_query.iconbitmap("./Image/Design.ico")
    list_query.geometry("800x600")
    
    #create a main frame
    main_frame = Frame(list_query)
    main_frame.pack(fill=BOTH, expand=1)
    #create a canvas
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH,expand=1)
    # add a scrollbar to the canvas
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    #configure the canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind("<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    #create another frame inside the canvas
    second_frame = Frame(my_canvas)
    # add that new frame to a window in the second frame
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")
    
    #create a database or connect to one
    conn = sqlite3.connect("./db/tokobulat.db")
    #create cursor
    c = conn.cursor()
    
    
    #query the database
    c.execute("SELECT * FROM Barang")
    result = c.fetchall()

    
    for index, x in enumerate(result):
        num = 0
        for y in x:
            header = [" Kode Barang  ", "  Nama Barang  " ,"  Dos Kecil "," Dos Besar ", "  Harga Pokok ", "  Quantity  ", " Quantity Gudang ", " Quantity Beli ", " Quantity Jual "]
            header = Label(second_frame, text=header[num])
            header.grid(row=1, column=num)
            lookup_label = Label(second_frame, text=y)
            lookup_label.grid(row=index + 2, column=num)
            num += 1  
        csv_button = Button(second_frame, text="Save to Excel", command=lambda: write_to_csv(result))
        csv_button.grid(row=0, column=3) 
    
    
    #commit changes
    conn.commit()
    conn.close()

#create edit function to update a record
def update():
    #create a database or connect to one
    conn = sqlite3.connect("./db/tokobulat.db")
    #create cursor
    c = conn.cursor()
    
    record_id  = delete_box.get()
    c.execute("""UPDATE Barang SET
        kode = :kode,
        nama = :nama,
        dkecil = :dkecil,
        dbesar = :dbesar,
        hpp = :hpp,
        qty = :qty
        
        WHERE oid = :oid""",
        {"kode": kode_editor.get(),
         "nama" : nama_editor.get(),
         "dkecil" : dkecil_editor.get(),
         "dbesar" : dbesar_editor.get(),
         "hpp" : hpp_editor.get(),
         "qty" : qty_editor.get(),
         
         "oid": record_id
        })
    
    #commit changes
    conn.commit()
    #close connection
    conn.close() 

    editor.destroy()
    
#create edit function to update a record
def edit():
    global editor
    editor = Tk()
    editor.title("Data Editor")
    editor.iconbitmap("./Image/Design.ico")
    editor.geometry("400x200")
    #create a database or connect to one
    conn = sqlite3.connect("./db/tokobulat.db")
    #create cursor
    c = conn.cursor()
    
    record_id = delete_box.get()
    #query the database
    c.execute("SELECT * FROM Barang WHERE oid = " + record_id)
    records = c.fetchall()    

    #create global variables for text box names
    global kode_editor
    global nama_editor
    global dkecil_editor
    global dbesar_editor
    global hpp_editor
    global qty_editor
    

    #create text boxes
    kode_editor = Entry(editor, width=30)
    kode_editor.grid(row=0, column=1, padx=20, pady=(10,0))
    nama_editor = Entry(editor, width=30)
    nama_editor.grid(row=1, column=1)
    dkecil_editor = Entry(editor, width=30)
    dkecil_editor.grid(row=2, column=1)
    dbesar_editor = Entry(editor, width=30)
    dbesar_editor.grid(row=3, column=1)
    hpp_editor = Entry(editor, width=30)
    hpp_editor.grid(row=4, column=1)
    qty_editor = Entry(editor, width=30)
    qty_editor.grid(row=5, column=1)

    #create text labels
    kode_label = Label(editor, text="Kode Barang")
    kode_label.grid(row=0, column=0, pady=(10,0))
    nama_label = Label(editor, text="Nama Barang")
    nama_label.grid(row=1, column=0)
    dkecil_label = Label(editor, text="Isi Dos Kecil")
    dkecil_label.grid(row=2, column=0)
    dbesar_label = Label(editor, text="Isi Dos Besar")
    dbesar_label.grid(row=3, column=0)
    hpp_label = Label(editor, text="HPP")
    hpp_label.grid(row=4, column=0)
    qty_label = Label(editor, text="Quantity")
    qty_label.grid(row=5, column=0)
    
    #Loop through results
    for record in records:
        kode_editor.insert(0, record[0])
        nama_editor.insert(0, record[1])
        dkecil_editor.insert(0, record[2])
        dbesar_editor.insert(0, record[3])
        hpp_editor.insert(0, record[4])
        qty_editor.insert(0, record[5])
    
    #create save button to save edited record
    edit_btn = Button(editor, text="Save Records", command=update)
    edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#create function to delete
def delete():
    #create a database or connect to one
    conn = sqlite3.connect("./db/tokobulat.db")
    #create cursor
    c = conn.cursor()
    #delete a record
    
    c.execute("DELETE FROM Barang WHERE kode = ?", (delete_box.get(),))
    
    #commit changes
    conn.commit()
    #close connection
    conn.close()
    
#create submit function
def submit():
    #create a database or connect to one
    conn = sqlite3.connect("./db/tokobulat.db")
    #create cursor
    c = conn.cursor()
    print("Database created and Successfully Connected to SQLite")
    #insert into table
    c.execute("INSERT INTO Barang Values (:kode, :nama, :dkecil, :dbesar, :hpp, :qty, 0, 0, 0)",
            {
                "kode": kode.get(),
                "nama": nama.get(),
                "dkecil": dkecil.get(),
                "dbesar": dbesar.get(),
                "hpp": hpp.get(),
                "qty": qty.get()
                
            })
    #commit changes
    conn.commit()
    print("SQLite table created")
    #close connection
    conn.close() 
    #clear the text boxes
    kode.delete(0, END)
    nama.delete(0, END)
    dkecil.delete(0, END)
    dbesar.delete(0, END)
    hpp.delete(0, END)
    qty.delete(0, END)   
    
#create text boxes
kode = Entry(root, width=30)
kode.grid(row=0, column=1, padx=20, pady=(10,0))
nama = Entry(root, width=30)
nama.grid(row=1, column=1)
dkecil = Entry(root, width=30)
dkecil.grid(row=2, column=1)
dbesar = Entry(root, width=30)
dbesar.grid(row=3, column=1)
qty = Entry(root, width=30)
qty.grid(row=4, column=1)
hpp = Entry(root, width=30)
hpp.grid(row=5, column=1)
delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)

#create text labels
kode_label = Label(root, text="Kode Barang")
kode_label.grid(row=0, column=0, pady=(10,0))
nama_label = Label(root, text="Nama Barang")
nama_label.grid(row=1, column=0)
dkecil_label = Label(root, text="Isi Dos Kecil")
dkecil_label.grid(row=2, column=0)
dbesar_label = Label(root, text="Isi Dos Besar")
dbesar_label.grid(row=3, column=0)
qty_label = Label(root, text="Quantity")
qty_label.grid(row=4, column=0)
hpp_label = Label(root, text="HPP")
hpp_label.grid(row=5, column=0)
delete_box_label = Label(root, text="Select Kode")
delete_box_label.grid(row=9, column=0, pady=5)

#submit button
submit_btn = Button(root, text="Input Data", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
#create a delete button
delete_btn = Button(root, text="Delete Records", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
#create and update button
edit_btn = Button(root, text="Edit Records", command=edit)
edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
#list button
list_customers_btn = Button(root, text="List Barang", command=list)
list_customers_btn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
#search button
search_btn = Button(root, text="Search Barang", command=search_barangs)
search_btn.grid(row=13, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
#pembelian button
search_btn = Button(root, text="Pembelian", command=pembelian)
search_btn.grid(row=14, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
#penjualan button
search_btn = Button(root, text="Penjualan", command=penjualan)
search_btn.grid(row=16, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
#kedatangan button
search_btn = Button(root, text="Kedatangan", command=kedatangan)
search_btn.grid(row=15, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
#pembayaran button
search_btn = Button(root, text="Pembayaran", command=pembayaran)
search_btn.grid(row=17, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


#commit changes
conn.commit()
print("SQLite has been commited")
#close connection
conn.close()
root.mainloop()