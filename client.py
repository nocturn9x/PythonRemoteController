import sys
import socket
from termcolor import colored,cprint   # Importo le librerie necessarie
import time
from cryptography.fernet import Fernet
import os

# Definisco la classe main
class Main :

    def __init__(self,addr,port):
        self.addr = addr
        self.port = port

    @staticmethod
    def invia_comandi(s,chiave): #Invia e riceve i comandi crittografati
        try :
            fernet = Fernet(chiave)
            user_and_host = s.recv()
            user_and_host_decrypted = fernet.decrypt(user_and_host) # Riceve e decripta hostname/username della macchina remota
            split = user_and_host_decrypted.decode("utf-8").split(":")
            hostname = split[1]
            username = split[3]
        except ConnectionResetError :
            cprint("[Errore] Qualcosa è andato storto...") # Ops, qualcosa è andato storto, esco
            s.close()
            sys.exit(4)
        while True :
            try :  
                comando = input(f"{hostname}@{username} ")   # Richiedo un comando da inviare
                if len(comando) <= 0 :
                    cprint("[Errore] Non puoi inviare un comando vuoto :)","red",sep="\n") # Input vuoto? No, grazie
                elif comando == "ESC" :   # Vuoi uscire? Esco...
                    cprint("[Info] Ok. A presto","green")
                    esc = "ESC"
                    s.send(fernet.encrypt(esc.encode()))
                    s.close()
                    sys.exit(2)
                elif comando == "clear":  # Simulo il comando 'clear' su diversi SO
                    if os.name == "posix":
                        os.system("clear")
                    else :
                        os.system("cls")
                else :
                    s.send(fernet.encrypt(comando.encode())) # Invio l'input criptato
                    data = s.recv(4096)     # Ricevo l'output
                    toprint = fernet.decrypt(data)  # Decodifico l'oggetto byte ricevuto
                    print(toprint.decode())         # Stampo a video la stringa decodificata
            except KeyboardInterrupt : # Ctrl+C? Esco...
                cprint("[Info] Ok. A presto", "green")  
                s.close()
                sys.exit(2)
            except ConnectionResetError :
                cprint("Whoops! Mi sono disconnesso in maniera anomala dal server")
                s.close()
                sys.exit(3)


    def connect_server(self):
        try:
            chiave = input(colored(f"[{time.strftime('%d/%m/%y %H:%M:%S')} Input ] Inserisci la chiave crittografica di questa sessione : ", "yellow"))
        except KeyboardInterrupt:
            cprint("[Info] Ok. A presto", "green")
            sys.exit(2)
        try :
            s = socket.socket()
            s.connect((self.addr,self.port))
            cprint(f"[{time.strftime('%d/%m/%y %H:%M:%S')} Info ] Connessione al server stabilita all'indirizzo {self.addr} e porta {self.port}","green")
        except Exception as errore :
            cprint(f"[{time.strftime('%d/%m/%y %H:%M:%S')} Errore] Qualcosa è andato storto con la connessione, stacktrace completo : {errore} ","red")
            sys.exit(1)
        Main.invia_comandi(s,chiave)


if __name__ == "__main__":
    addr = Main("XXX.XXX.XX.X",52000) #Inserisci qui il tuo IP pubblico
    Main.connect_server(addr)

