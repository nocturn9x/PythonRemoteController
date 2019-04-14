from termcolor import cprint
import sys
import os
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
import socket                                       # Importa le librerie necessarie
import time
import subprocess
import getpass
from threading import Thread
from cryptography.fernet import Fernet
import cryptography.fernet

# Creo la classe TCP Server


class TCP:

    def __init__(self,address,port,backlog=1):
        self.address = address
        self.port = port
        self.backlog = backlog

    clock = time.strftime('%d/%m/%y %H:%M:%S')

    def command_parser(self,conn,indirizzo_client,chiave,show_message=True):
        """Funzione che si occupa di ricevere i comandi dal client
        decrittografarli, poi eseguirli e restituire al client l'output criptato."""
        hostname = socket.gethostname()
        username = getpass.getuser()
        key = Fernet(chiave)    # Istanzio l'oggetto Fernet
        try:
            user_and_host = f"internal1:{hostname}:internal2:{username}"    # Comunico l'username e l'hostname al client
            conn.send(key.encrypt(user_and_host.encode()))
        except BrokenPipeError: # In caso di disconnessione anomala, catturo l'eccezione e la ignoro
            pass
        cprint(f"[{TCP.clock} Info - TCP Server] Hey, non vorrei mica disturbarti, ma qualcuno si è connesso! Indirizzo : {indirizzo_client[0]} Porta remota : {indirizzo_client[1]}", "green")
        if show_message is True:
            cprint(f"[{TCP.clock} Info - Command Parser] Heylà giovine, il command parser è avviato!","blue")
        else:
            pass
        while True:
            try:
                comando = conn.recv(4096)
                decode = key.decrypt(comando)  # Ricevo comandi dal client e li decrittografo Poi li decodifico in ASCII
                decoded = decode.decode("ascii")
            except ConnectionResetError:
                pass
            except cryptography.fernet.InvalidToken:
                pass
            if decoded.startswith("cd "):
                os.chdir(decoded[3:])
                try:
                    dir_modificata = b'Directory corrente modificata'
                    conn.send(key.encrypt(dir_modificata))
                except BrokenPipeError:
                    pass
            elif decoded.startswith("touch "):
                os.system(f"touch {decoded[6:]}")       # Verifico i comandi che non restituiscono output
                try:
                    file_creato = b'File Creato'
                    conn.send(key.encrypt(file_creato))
                except BrokenPipeError:
                    pass
            elif decoded.startswith("mkdir "):
                os.system(f"mkdir {decoded[6:]}")
                try:
                    directory_creata = b'Directory creata'
                    conn.send(key.encrypt(directory_creata))
                except BrokenPipeError:
                    pass
            elif decoded.startswith("rm "):
                try:
                    rm = os.system(f"rm {decoded[3:]}")
                    if rm == 0:
                        deleted_file = b'File eliminato'
                        conn.send(key.encrypt(deleted_file))
                    elif rm == 256:
                        err_256_plain = f"rm: {decoded[3:]}: è una directory o non esiste!"
                        err_256 = err_256_plain.encode()
                        conn.send(key.encrypt(err_256))
                except BrokenPipeError:
                    pass
            elif decoded.startswith("rmdir "):
                try :
                    rmdir = os.system(f"rmdir {decoded[6:]}")
                    if rmdir == 0:
                        deleted_dir = b'Directory Eliminata'
                        conn.send(key.encrypt(deleted_dir))
                    elif rmdir == 256:
                        err_256_1 = f'rmdir: {decoded[6:]} non è una directory oppure non esiste!'
                        conn.send(key.encrypt(err_256_1.encode()))
                except BrokenPipeError:
                    pass
            elif decoded == "ESC":
                    cprint(f"[{TCP.clock} Info - TCP Server] L'utente {indirizzo_client[0]}:{indirizzo_client[1]} si è disconnesso", "green")
                    break
            else :
                try :
                    # Non è nessuno dei comandi sopra? Eseguo un sottoprocesso e invio l'output cifrato
                    cmd = subprocess.run(decode,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    tosend = cmd.stdout + cmd.stderr
                    conn.send(key.encrypt(tosend))
                    if len(tosend.decode()) <= 0:           # Nessun Output? Invia \n
                        newline = "\n"
                        conn.send(key.encrypt(newline.encode()))
                except BrokenPipeError :
                    pass

    def restart(self,addr,backlog):
        """Funzione analoga a run(), eseguita come tentativo di riavvio del server"""
        try :
            s = socket.socket()
            s.bind(addr)
            s.listen(backlog)
            hostname = socket.gethostname()
            username = getpass.getuser()
        except Exception as errore :
            cprint(f"[{TCP.clock} Errore - TCP Server] Sembra proprio che ci sia qualcosa di sbagliato nella configurazione del server TCP, controlla l'indirizzo e la porta e riprova. Errore completo : {errore}","red")
            sys.exit(1)
        try:
            chiave = Fernet.generate_key()
            cipher_suite = Fernet(chiave)
            str_key = chiave.decode("utf-8")
        except Exception as exc:
            cprint(f"[{TCP.clock} Errore - TCP Server] Qualcosa è andato storto con la generazione della chiave crittografica. Stacktrace completo : {exc}","red")
        cprint(f"[{TCP.clock} Info - TCP Server] La chiave crittografica di questa sessione è {str_key}","green")
        while True:
            connessione, indirizzo_client = s.accept()
            thread1 = Thread(target=TCP.command_parser(connessione, indirizzo_client,str_key))
            thread1.start()



    def run(self,*args):
            """Creo un socket, effettuo il binding e genero la chiave crittografica.
                In caso di errore tento il riavvio"""
            try:
                s = socket.socket()
                s.bind((self.address, self.port))
                s.listen(self.backlog)
            except Exception as errore:
                cprint(f"[{TCP.clock} Errore - TCP Server] Accipicchia! Si è verificato un errore durante la creazione del socket, eccoti l'errore completo : {errore}","red")
                cprint(f"[{TCP.clock} Info - TCP Server] Tento il Riavvio...", "green")
                TCP.restart((self.address,self.port),self.backlog)
            cprint(f"[{TCP.clock} Info - TCP Server] Hey, sembra proprio che sia riuscito ad avviarmi correttamente","green")
            try:
                chiave = Fernet.generate_key()              # Genera la chiave crittografica AES Fernet
                str_key = chiave.decode("utf-8")
            except Exception as exc:
                cprint(f"[{TCP.clock} Errore - TCP Server] Qualcosa è andato storto con la generazione della chiave crittografica. Stacktrace completo : {exc}","red")
            cprint(f"[{TCP.clock} Info - TCP Server] La chiave crittografica di questa sessione è {str_key}","green")
            while True:
                connessione, indirizzo_client = s.accept()
                thread1 = Thread(target=TCP.command_parser,args=(connessione,indirizzo_client,chiave),name="CMD-PARSER")
                thread1.start()


# Classe FTP Server
class FTP:

    def __init__(self,address,port,user,pasw,banner):
        self.address = address
        self.port = port
        self.user = user
        self.pasw = pasw
        self.banner = banner

# Server FTP con certificato SSL
    def run(self,*args):
        """Avvio il server FTP"""
        authorizer = DummyAuthorizer()
        authorizer.add_user(self.user, self.pasw, f'{os.getcwd()}', perm='elradfmwMT') # Aggiunge un utente virtuale
        handler = TLS_FTPHandler
        handler.certfile = f'{os.getcwd()}/cert/certfile.pem' # Directory del certificato
        handler.keyfile = f'{os.getcwd()}/cert/key.pem'     # Directory della chiave
        handler.authorizer = authorizer
        handler.tls_control_required = True
        handler.tls_data_required = True
        handler.masquerade_address = '151.62.201.245' # Inserisci qui il tuo IP pubblico. Serve alla modalità PASV
        handler.passive_ports = range(2122,2124) # Porte passive
        handler.banner = self.banner
        address = (self.address,self.port)
        server = FTPServer(address, handler)
        server.max_cons = 20
        server.max_cons_per_ip = 2
        server.serve_forever()

if __name__ == "__main__":
    # Istanzio un oggetto TCP ed un oggetto FTP, poi avvio i Threads
    TCP = TCP("192.168.1.103",52000,backlog=5) # Inserisci qui il tuo IP locale
    FTP = FTP("192.168.1.103",2121,"Mattia Giambirtone","Password1971_","Benvenuto!") # Inserisci il tuo IP locale
    thread1 = Thread(target=FTP.run, args=(FTP,), name="FTP")
    thread2 = Thread(target=TCP.run,args=(TCP,),name="TCP")
    thread1.start()
    thread2.start()
