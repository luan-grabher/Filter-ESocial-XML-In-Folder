
'''
**Processo:**
- Pegar mês e ano
- Pegar arquivo csv com CPFs
- Para cada linha do csv, pegar 3 coluna e remover tudo diferente de numeros
- Pegar pasta com os arquivos XML
- Listar arquivos XML
- Para cada arquivo XML que conter <tot tipo="S5001", conter <tot tipo="S5003":
    - Percorrer todos cpfs
        - Se contiver o cpf, guarda o nome do arquivo
- Criar uma subpasta com nome 'S5001 e S5003'
- Para cada arquivo guardado, copiar para a pasta criada
- Avisar para o usuário que os arquivos estão na nova pasta criada

'''

# Importações
from argparse import FileType
import datetime
import tkinter as tk
from tkinter import Button, OptionMenu, StringVar, Tk, filedialog
from tkinter import simpledialog
from tkinter import messagebox
import re
import os
import shutil
import sys
from user_program_use import mark_use_program


# Show tk input to get 'Mês' int and 'Ano' int
def get_mes_ano():
    # Lista de meses por extenso para mostrar no option list
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    # year now
    year = datetime.datetime.now().year
    # Lista com ano passado e ano atual para mostrar no option list
    anos = [year-1, year]

    master = Tk()
    master.title('Filtrar XML E-Social por CPF')
    master.geometry('350x100')
    # Center window
    master.update_idletasks()
    x = (master.winfo_screenwidth() - master.winfo_reqwidth()) / 2
    y = (master.winfo_screenheight() - master.winfo_reqheight()) / 2
    master.geometry("+%d+%d" % (x, y))

    mes_select = StringVar(master)
    mes_select.set(meses[0])  # default value

    mes_options = OptionMenu(master, mes_select, *meses)
    mes_options.pack()

    ano_select = StringVar(master)
    ano_select.set(anos[1])  # default value

    ano_options = OptionMenu(master, ano_select, *anos)
    ano_options.pack()

    # Button to call function 'run' when clicked
    button = Button(master, text="Filtrar", command=master.quit)
    button.pack()

    # Wait for user to click button
    master.mainloop()

    # mes is position in list of months + 1
    mes = meses.index(mes_select.get()) + 1
    ano = ano_select.get()

    return mes, ano

# function to get from user with filedialogs cpfs from csv and folder with xml files
def getFiles():
    #tk.messagebox.showinfo('CSV com CPFs', 'Selecione o arquivo csv com os CPFs')
    csv_cpfs = filedialog.askopenfilename(
        initialdir="./", title="Selecione o arquivo csv com os CPFs")
    #tk.messagebox.showinfo('Pasta', 'Selecione a pasta')
    pasta = filedialog.askdirectory()

    return csv_cpfs, pasta

# Para cada linha do csv, pegar 3 coluna e remover tudo diferente de numeros
def get_cpfs_from_file(csv_cpfs):
    cpfs = []
    with open(csv_cpfs, 'r') as csv_file:
        for line in csv_file:
            cpf = line.split(';')[2]
            # Remover tudo diferente de numeros
            cpf = re.sub('[^0-9]', '', cpf)
            # if cpf has 11 digits
            if len(cpf) == 11:
                cpfs.append(cpf)
    return cpfs

# Function to filter XML files with cpfs, mes e ano
def filter_xml_files(cpfs, mes, ano, pasta):
    # Listar arquivos XML da pasta
    xml_files = [f for f in os.listdir(pasta) if f.endswith('.xml')]

    xml_files_filtered = []

    mes = "<indApuracao>{}</indApuracao>".format(mes)
    ano = "<perApur>" + ano

    # Para cada arquivo XML que conter <tot tipo="S5001", conter <tot tipo="S5003"
    for xml_file in xml_files:
        # pega o texto do arquivo usando enconding utf-8
        xml_text = open(pasta + '/' + xml_file, 'r',
                        encoding='ISO-8859-1').read()

        # Se o arquivo XML conter '<tot tipo="S5001"' ou conter '<tot tipo="S5003"'
        if '<tot tipo="S5001"' in xml_text or '<tot tipo="S5003"' in xml_text:
            # Se o arquivo XML conter o mes e o ano
            if str(mes) in xml_text and str(ano) in xml_text:
                # Para cada CPF
                for cpf in cpfs:
                    # Se o arquivo XML conter o  texto '<cpfTrab>' + CPF
                    if '<cpfTrab>' + cpf in xml_text:
                        # Guarda o path do arquivo
                        xml_files_filtered.append(pasta + '/' + xml_file)
                        break

    return xml_files_filtered

# Function to save files in a new folder
def save_files(xml_files_filtered, pasta):
    # Criar pasta
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    #Limpa a pasta
    for file in os.listdir(pasta):
        os.remove(pasta + '/' + file)

    # Para cada arquivo XML guardado
    for xml_file in xml_files_filtered:
        # Copiar arquivo no windows para a pasta
        shutil.copy(xml_file, pasta)

    # Avisar para o usuário que os arquivos estão na nova pasta criada
    tk.messagebox.showinfo('Aviso', 'Os arquivos foram salvos na pasta ' + pasta)

# function run reciving mes and ano
def run():
    # Get mes and ano
    mes, ano = get_mes_ano()

    # Get csv and folder
    csv_cpfs, pasta = getFiles()

    # Get cpfs from csv
    cpfs = get_cpfs_from_file(csv_cpfs)

    # Filter xml files
    xml_files_filtered = filter_xml_files(cpfs, mes, ano, pasta)

    #name os new folder is 'Filtrados ' + mes + ' ' + ano + ' S5001 e S5003'
    pasta_filtrados = 'Filtrados ' + str(mes) + ' ' + str(ano) + ' S5001 e S5003'

    # Save files
    save_files(xml_files_filtered, pasta + '/' + pasta_filtrados)

try:
    # Start program gettings mes and ano
    run()
    mark_use_program("Filtrar XML E-Social por CPF")
except:
    pass
finally:
    # Close program
    sys.exit()