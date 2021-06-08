import psycopg2
from tkinter import *

window = Tk()
window.title('Database')
window.resizable(False, False)

#Functions

def submit():
    con = psycopg2.connect(host='localhost', database='test', user='postgres', password='postgres')
    cur = con.cursor()

    nota = enota.get()
    volumes = evolumes.get()
    peso = epeso.get()
    cliente = ecliente.get()

    sql = '''INSERT INTO carga(nota, volumes, peso, cliente) VALUES (%s, %s, %s, %s)'''
    cur.execute(sql, (nota, volumes, peso, cliente))

    con.commit()
    con.close()
    #Clear the Text Boxes
    enota.delete(0, END)
    evolumes.delete(0, END)
    epeso.delete(0, END)
    ecliente.delete(0, END)

    query_label_notas.destroy()
    query_label_volumes.destroy()
    query_label_peso.destroy()
    query_label_cliente.destroy()

def query():
    
    con = psycopg2.connect(host='localhost', database='test', user='postgres', password='postgres')
    cur = con.cursor()
    cur.execute("SELECT * FROM carga")

    records = cur.fetchall()

    global query_label_notas
    global query_label_volumes
    global query_label_peso
    global query_label_cliente

    print_notas = ' '
    for record in records:
        print_notas += str(record[0]) + "\n"

    query_label_notas = Label(window, text=print_notas)
    query_label_notas.grid(row=6, column=0)

    print_volumes = ' '
    for record in records:
        print_volumes += str(record[1]) + "\n"

    query_label_volumes = Label(window, text=print_volumes)
    query_label_volumes.grid(row=6, column=1)

    print_peso = ' '
    for record in records:
        print_peso += str(record[2]) + "\n"

    query_label_peso = Label(window, text=print_peso)
    query_label_peso.grid(row=6, column=2)

    print_cliente = ' '
    for record in records:
        print_cliente += str(record[3]) + "\n"

    query_label_cliente = Label(window, text=print_cliente)
    query_label_cliente.grid(row=6, column=3)

    con.commit()
    con.close()

def delete():
    con = psycopg2.connect(host='localhost', database='test', user='postgres', password='postgres')
    cur = con.cursor()

    query_label_notas.destroy()
    query_label_volumes.destroy()
    query_label_peso.destroy()
    query_label_cliente.destroy()

    cur.execute("DELETE FROM carga WHERE nota = " + edelete.get())
    con.commit()
    con.close()

def save(): 
    con = psycopg2.connect(host='localhost', database='test', user='postgres', password='postgres')
    cur = con.cursor()

    nota = enota_editor.get()
    volumes = evolumes_editor.get()
    peso = epeso_editor.get()
    cliente = ecliente_editor.get()
    record_id = edelete.get()

    sql = '''UPDATE carga SET nota = %s, volumes = %s, peso = %s, cliente = %s WHERE nota = %s'''
    cur.execute(sql, (nota, volumes, peso, cliente, record_id))

    con.commit()
    con.close()

    query_label_notas.destroy()
    query_label_volumes.destroy()
    query_label_peso.destroy()
    query_label_cliente.destroy()

    editor.destroy()
    
def update():
    global editor

    editor = Tk()
    editor.title('Update a Record')
    editor.resizable(False, False)

    global enota_editor
    global evolumes_editor
    global epeso_editor
    global ecliente_editor

    lnota_editor = Label(editor, text="NOTA", width=10)
    lnota_editor.grid(row=0, column=0)

    lvolumes_editor = Label(editor, text="VOLUMES", width=10)
    lvolumes_editor.grid(row=0, column=1)

    lpeso_editor = Label(editor, text="PESO", width=10)
    lpeso_editor.grid(row=0, column=2)

    lcliente_editor = Label(editor, text="CLIENTE", width=30)
    lcliente_editor.grid(row=0, column=3)

    enota_editor = Entry(editor, width=10)
    enota_editor.grid(row=1, column=0)

    evolumes_editor = Entry(editor, width=10)
    evolumes_editor.grid(row=1, column=1)

    epeso_editor = Entry(editor, width=10)
    epeso_editor.grid(row=1, column=2)

    ecliente_editor = Entry(editor, width=30)
    ecliente_editor.grid(row=1, column=3)

    save_button = Button(editor, text="Save Changes", command=save)
    save_button.grid(row=2, column=0, columnspan=4, pady=10, padx=10, ipadx=100)

    con = psycopg2.connect(host='localhost', database='test', user='postgres', password='postgres')
    cur = con.cursor()

    query_label_notas.destroy()
    query_label_volumes.destroy()
    query_label_peso.destroy()
    query_label_cliente.destroy()

    record_id = edelete.get()
    cur.execute("SELECT * FROM carga WHERE nota = " + record_id)
    records = cur.fetchall()
    
    for record in records:
        enota_editor.insert(0, record[0])
        evolumes_editor.insert(0, record[1])
        epeso_editor.insert(0, record[2])
        ecliente_editor.insert(0, record[3])

  

#Labels
lnota = Label(window, text="NOTA", width=10)
lnota.grid(row=0, column=0)

lvolumes = Label(window, text="VOLUMES", width=10)
lvolumes.grid(row=0, column=1)

lpeso = Label(window, text="PESO", width=10)
lpeso.grid(row=0, column=2)

lcliente = Label(window, text="CLIENTE", width=30)
lcliente.grid(row=0, column=3)

lselect = Label(window, text="Nota", width=10)
lselect.grid(row=3, column=1)

#Text Boxes
enota = Entry(window, width=10)
enota.grid(row=1, column=0)

evolumes = Entry(window, width=10)
evolumes.grid(row=1, column=1)

epeso = Entry(window, width=10)
epeso.grid(row=1, column=2)

ecliente = Entry(window, width=30)
ecliente.grid(row=1, column=3)

edelete = Entry(window, width=10)
edelete.grid(row=3, column=2)

#Buttons
submit_button = Button(window, text="Add Record to Database", command=submit)
submit_button.grid(row=2, column=0, columnspan=4, pady=10, padx=10, ipadx=100)

query_button = Button(window, text="Show Records", command=query)
query_button.grid(row=5, column=0, columnspan=4, pady=10, padx=10, ipadx=100)

delete_button = Button(window, text="Delete Record", command=delete)
delete_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

update_button = Button(window, text="Update Record", command=update)
update_button.grid(row=4, column=2, columnspan=2, pady=10, padx=10, ipadx=100)


window.mainloop()
