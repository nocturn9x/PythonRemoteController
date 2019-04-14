import sys
import socket
from termcolor import colored,cprint
import time
from cryptography.fernet import Fernet
import os


class Main :

    def __init__(self,addr,port):
        self.addr = addr
        self.port = port

    @staticmethod
    def invia_comandi(s,chiave):
        try :
            fernet = Fernet(chiave)
            user_and_host = s.recv(4096)
            user_and_host_decrypted = fernet.decrypt(user_and_host)
            split = user_and_host_decrypted.decode("utf-8").split(":")
            hostname = split[1]
            username = split[3]
        except ConnectionResetError :
            cprint("[Errore] Qualcosa è andato storto...")
            s.close()
            sys.exit(4)
        while True :
            try :
                comando = input(f"{hostname}@{username} ")
                if len(comando) <= 0 :
                    cprint("[Errore] Non puoi inviare un comando vuoto :)","red",sep="\n")
                elif comando == "ESC" :
                    cprint("[Info] Ok. A presto","green")
                    esc = "ESC"
                    s.send(fernet.encrypt(esc.encode()))
                    s.close()
                    sys.exit(2)
                elif comando == "clear":
                    if os.name == "posix":
                        os.system("clear")
                    else :
                        os.system("cls")
                else :
                    s.send(fernet.encrypt(comando.encode()))
                    data = s.recv(4096)
                    toprint = fernet.decrypt(data)
                    print(toprint.decode())
            except KeyboardInterrupt :
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
    addr = Main("XXX.XX.XX.XX",52000)
    Main.connect_server(addr)

