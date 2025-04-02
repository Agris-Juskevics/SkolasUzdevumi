from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
import os

root = Tk()
root.title('TE')
root.geometry("1200x700")
root.minsize(400, 400)

#Visi globālie mainīgie
global opened_text_file #Mainīgais atvērtajam failam, ļauj saglabāt neatverot jaunu vai citu datni.
opened_text_file = False
global izveletais_teksts
izveletais_teksts = False

# Izveido rāmi programmatūrai
frame = Frame(root)
frame.pack(fill="both", expand = True, padx=10)

#Sākt jauna teksta datnes rakstīšanu
def atvert_jaunu():
    global opened_text_file
    opened_text_file = False
    text.delete(1.0, END)
    root.title("TE - jauns fails")
    status_bar.config(text="Jauns fails")
    
#Atvērs citus teksta formāta datnes.
def atvert_citu():
    text.delete(1.0, END)
    #Izskata failu un atjauno aplikācijas nosaukumu un statusa rādītāju
    text_file = filedialog.askopenfilename(initialdir=f"{os.path.expanduser('~')}/Documents", title = "Atvērt datni", filetypes=(("Teksta datnes", "*.txt;*.doc;*.docx"), ("All Files", "*.*")))
    status_bar.config(text=f"{text_file}")
    name = os.path.basename(text_file)
    root.title(f"TE - {name}")
    #Dod globālu atvērto tekstu datni
    if text_file:
        global opened_text_file
        opened_text_file = text_file
    #Atver pašu datni un izvelk tekstu.
    text_file= open(text_file, "r", encoding="utf-8")
    try:
        text.insert(END, text_file.read())
    except UnicodeDecodeError:
        status_bar.config(text="Datnē ir neatbalstīti dati, piemēram, bildes")
        text_from_file = None
    text_file.close()

#Saglabās datni lietotāja izvēlētajā vietā un datnes veidā.
def saglabat_ka():
    text_file = filedialog.asksaveasfilename(initialdir=f"{os.path.expanduser('~')}/Documents", title = "Saglabāt datni", filetypes=(("Teksta datnes", "*.txt;*.doc;*.docx"), ("All Files", "*.*")), defaultextension=".*")
    if text_file:
        #Atjauno aplikācijas nosaukumu un statusa rādītāju
        status_bar.config(text=f"{text_file} - saglabāts")
        name = os.path.basename(text_file)
        root.title(f"TE - {name}")
        #Saglabās datni
        text_file = open(text_file, "w", encoding="utf-8")
        text_file.write(text.get(1.0, END))
        text_file.close()
        
def saglabat():
    global opened_text_file
    if opened_text_file:
        text_file = open(opened_text_file, "w", encoding="utf-8")
        text_file.write(text.get(1.0, END))
        text_file.close()
        status_bar.config(text=f"{opened_text_file} - saglabāts")
    else:
        saglabat_ka()
        
#Basic teksta funkcijas 
def izgriezt_tekstu(e):
    global izveletais_teksts
    try:
        if e:
            izveletais_teksts = root.clipboard_get()
        else:    
            if text.selection_get():
                izveletais_teksts = text.selection_get() #norāda izvēlēto tekstu
                root.clipboard_clear()
                root.clipboard_append(izveletais_teksts)
                text.delete("sel.first", "sel.last") #izdzēš izvēlēto tekstu
                status_bar.config(text="Teksts izgriezts")
    except:
        status_bar.config(text="Izgriešana neizdevās - nav izvēlēts teksts")

def dublet_tekstu(e):
    global izveletais_teksts
    if e:
        izveletais_teksts = root.clipboard_get()
    if text.selection_get():
        izveletais_teksts = text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(izveletais_teksts)
    else:
        status_bar.config(text="Kopēšana neizdevās - nav izvēlēts teksts")

def iedublet_tekstu(e):
    global izveletais_teksts
    if e:
        izveletais_teksts = root.clipboard_get()
    else:
        if izveletais_teksts:
            kursors = text.index(INSERT)
            text.insert(kursors, izveletais_teksts)
        else:
            status_bar.config(text="Dublēšana neizdevās - nav izvēlēts teksts")


#Teksta apstrādašanas funkcijas
def get_combined_font(tags):
    new_font = font.Font(text, text.cget("font"))
    if "treknrakstā" in tags:
        new_font.configure(weight="bold", slant="roman")
    if "slīprakstā" in tags:
        new_font.configure(slant="italic", weight="normal")
    return new_font
def uzlikt_teksta_stilu(stils):
    try:
        start, end = text.index("sel.first"), text.index("sel.last")
        current_tags = set(text.tag_names(start))
        if stils in current_tags:
            text.tag_remove(stils, start, end)
            current_tags.remove(stils)
            status_bar.config(text=f"Teksts pārrakstīs ne{stils}")
        else:
            text.tag_add(stils, start, end)
            current_tags.add(stils)
            status_bar.config(text=f"Teksts pārrakstīs {stils}")
        bold = "treknrakstā" in current_tags
        italic = "slīprakstā" in current_tags

        new_font = font.Font(text, text.cget("font"))
        new_font.configure(weight="bold" if bold else "normal", slant="italic" if italic else "roman")

        text.tag_configure(stils, font=new_font)

    except TclError:
        status_bar.config(text="Nav izvēlēts teksts")
            
def treknraksts(e):
    uzlikt_teksta_stilu("treknrakstā")
    return "break"
        
def slipraksts(e):
    uzlikt_teksta_stilu("slīprakstā")
    return "break"
        
def nokrasot():
    krasa = colorchooser.askcolor()[1]
    krasainaisteksts = font.Font(text, text.cget("font"))
    text.tag_configure("colored", font=krasainaisteksts, foreground=krasa)
    try:
        text.tag_add("colored", "sel.first", "sel.last")
        status_bar.config(text="Teksts pārrakstīts izvēlētajā krāsā")
    except TclError:
        status_bar.config(text="Nav izvēlēts teksts")
        
#Iestatījuma izvēlnes funkcijas
def fona_krasa():
    fona_krasa = colorchooser.askcolor()[1]
    try:
        text.config(bg=fona_krasa)
    except:
        status_bar.config(text="Neizdevās")
def visa_teksta_krasa():
    visa_teksta_krasa = colorchooser.askcolor()[1]
    try:
        text.config(fg=visa_teksta_krasa)
    except:
        status_bar.config(text="Neizdevās")
        

    
#Teksta rakstīšanas un ritjoslas izveide, teksta stilu definēšana
scroller = Scrollbar(frame)
scroller.pack(side="right", fill="y")

text= Text(frame, width=70, height=5, font=('Helvetica', 16), selectbackground= "Gray", selectforeground= "black",undo= True,  yscrollcommand= scroller.set)
text.pack(fill="both", expand=True)


scroller.config(command=text.yview)

#Izvēlnes izveide
main_menu = Menu(root)
root.config(menu=main_menu)

#Datņu izvēlnes izveide
file_menu = Menu(main_menu, tearoff= False)
main_menu.add_cascade(label="Datne", menu=file_menu)
file_menu.add_command(label="Jauna", command = atvert_jaunu)
file_menu.add_command(label="Atvērt", command =  atvert_citu)
file_menu.add_command(label="Saglabāt", command = saglabat)
file_menu.add_command(label="Saglabāt kā", command = saglabat_ka)
file_menu.add_separator()
file_menu.add_command(label="Iziet", command=root.quit)

#Labošanas izvēlnes izveide
edit_menu = Menu(main_menu, tearoff= False)
main_menu.add_cascade(label="Labot", menu=edit_menu)
edit_menu.add_command(label="Izgriezt \t(Ctrl+X)", command = lambda: izgriezt_tekstu(False), accelerator= "Ctrl+X")
edit_menu.add_command(label="Nokopēt \t (Ctrl+C)", command = lambda: dublet_tekstu(False), accelerator= "Ctrl+C")
edit_menu.add_command(label="Iekopēt \t (Ctrl+V)", command = lambda: iedublet_tekstu(False), accelerator= "Ctrl+V")
edit_menu.add_command(label="Atsaukt \t (Ctrl+Z)", command = text.edit_undo, accelerator= "Ctrl+Z")
edit_menu.add_command(label="Atgriezt \t (Ctrl+Y)", command = text.edit_redo, accelerator= "Ctrl+Y")

#Teksta apstrādes izvēlnes izveide
text_menu = Menu(main_menu, tearoff= False)
main_menu.add_cascade(label="Teksts", menu=text_menu)
text_menu.add_command(label = "Treknrakstīt", command = lambda: treknraksts(False), accelerator = "Ctrl+B")
text_menu.add_command(label= "Slīprakstīt", command= lambda: slipraksts(False), accelerator= "Ctrl+I")
text_menu.add_command(label="Teksta krāsa", command= nokrasot)

#Iestatījuma izvēlnes izveide
options_menu = Menu(main_menu, tearoff= False)
main_menu.add_cascade(label="Iestatījumi", menu=options_menu)
options_menu.add_command(label="Fona krāsa", command = fona_krasa)
options_menu.add_command(label="Visa teksta krāsa",command = visa_teksta_krasa)


#Datnes statusa rādītājs
status_bar = Label(root, text='Teksta rediģēšanas programma - TE', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5, padx=16)

#Teksta rediģēšanas makrodefinīcijas
root.bind("<Control-Key-x>", izgriezt_tekstu)
root.bind("<Control-Key-c>", dublet_tekstu)
root.bind("<Control-Key-v>", iedublet_tekstu)
text.bind("<Control-Key-z>", text.edit_undo)
text.bind("<Control-Key-y>", text.edit_redo)
text.bind("<Control-Key-b>", treknraksts)
text.bind("<Control-Key-i>", slipraksts)



root.mainloop()