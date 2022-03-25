
import datetime
import getpass


def mark_use_program(program_name):
    #Get user of windows
    user = getpass.getuser()

    #get date now in yyyy-MM-dd HH:mm
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    #text to add in front of file: date;user;program_name\r\n
    text_to_add = '\r\n' + date_now + ';' + user + ';' + program_name

    #path of csv
    csv_path = '\\\\heimerdinger\\docs\\Informatica\\Programas\\Moresco\\02 - Arquivos de Programas\\programas_usados.csv'

    #open file
    file = open(csv_path, 'a')

    #write text
    file.write(text_to_add)

    #close file
    file.close()