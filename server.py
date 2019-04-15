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

    def __init__(self, address, port, backlog=1):
        self.address = address
        self.port = port
        self.backlog = backlog

    @staticmethod
    def clock():
        """Aggiorna l'orologio interno del server"""
        clock = time.strftime('%d/%m/%y %H:%M:%S')
        return clock

    @staticmethod
    def command_parser(conn, client_address, chiave, show_message=True):
        """Funzione che si occupa di ricevere i comandi dal client
        decrittografarli, poi eseguirli e restituire al client l'output criptato."""
        hostname = socket.gethostname()
        username = getpass.getuser()
        key = Fernet(chiave)    # Istanzio l'oggetto Fernet
        try:
            user_and_host = f'internal1:{hostname}:internal2:{username}'   # Comunico l'username e l'hostname al client
            conn.send(key.encrypt(user_and_host.encode()))
        except BrokenPipeError:  # In caso di disconnessione anomala, catturo l'eccezione e la ignoro
            pass
        cprint(f'[{TCP.clock()} Info - TCP Server] Qualcuno si è connesso! Indirizzo -> {client_address[0]}:{client_address[1]}', 'green')
        if show_message is True:
            cprint(f'[{TCP.clock()} Info - Command Parser] Command parser per {client_address[0]}:{client_address[1]} avviato!', 'blue')
        else:
            pass
        while True:
            try:
                command = conn.recv()
                decrypted = key.decrypt(command)  # Ricevo comandi dal client, li decrittografo e li decodifico in ASCII
                decoded = decrypted.decode("ascii")
            except ConnectionResetError:
                cprint(f'[{TCP.clock()} Info - TCP Server] {client_address[0]}:{client_address[1]} si è disconnesso', 'green')
                break
            except cryptography.fernet.InvalidToken:
                cprint(f'[{TCP.clock()} Info - TCP Server] {client_address[0]}:{client_address[1]} si è disconnesso', 'green')
                break
            if decoded.startswith('cd '):
                os.chdir(decoded[3:])
                try:
                    dir_changed = b'Directory corrente modificata'
                    conn.send(key.encrypt(dir_changed))
                except BrokenPipeError:
                    pass
            elif decoded.startswith('touch '):
                os.system(f'touch {decoded[6:]} >/dev/null 2>&1')      # Verifico i comandi che non restituiscono output
                try:
                    file_created = b'File Creato'
                    conn.send(key.encrypt(file_created))
                except BrokenPipeError:
                    pass
            elif decoded.startswith('mkdir '):
                os.system(f'mkdir {decoded[6:]} >/dev/null 2>&1')
                try:
                    directory_created = b'Directory creata'
                    conn.send(key.encrypt(directory_created))
                except BrokenPipeError:
                    pass
            elif decoded.startswith('rm '):
                try:
                    rm = os.system(f'rm {decoded[3:]} >/dev/null 2>&1')
                    if rm == 0:
                        deleted_file = b'File eliminato'
                        conn.send(key.encrypt(deleted_file))
                    elif rm == 256:
                        err_256_plain = f'rm: {decoded[3:]}: è una directory o non esiste!'
                        err_256 = err_256_plain.encode()
                        conn.send(key.encrypt(err_256))
                except BrokenPipeError:
                    pass
            elif decoded.startswith('rmdir '):
                try:
                    rmdir = os.system(f'rmdir {decoded[6:]} >/dev/null 2>&1')
                    if rmdir == 0:
                        deleted_dir = b'Directory Eliminata'
                        conn.send(key.encrypt(deleted_dir))
                    elif rmdir == 256:
                        err_256_1 = f'rmdir: {decoded[6:]} non è una directory oppure non esiste!'
                        conn.send(key.encrypt(err_256_1.encode()))
                except BrokenPipeError:
                    pass
            elif decoded == 'ESC':
                    cprint(f'[{TCP.clock()} Info - TCP Server] {client_address[0]}:{client_address[1]} si è disconnesso', 'green')
                    break
            else:
                try:
                    # Non è nessuno dei comandi sopra? Eseguo un sottoprocesso e invio l'output cifrato
                    cmd = subprocess.run(decoded, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    to_send = cmd.stdout + cmd.stderr
                    conn.send(key.encrypt(to_send))
                    if len(to_send.decode()) <= 0:           # Nessun Output? Invia \n
                        newline = "\n"
                        conn.send(key.encrypt(newline.encode()))
                except BrokenPipeError:
                    pass

    @staticmethod
    def restart(address, backlog):
        """Funzione analoga a run(), eseguita come tentativo di riavvio del server"""
        try:
            s = socket.socket()
            s.bind(address)
            s.listen(backlog)
        except Exception as error:
            cprint(f'[{TCP.clock()} Errore - TCP Server] Qualcosa non va con il server TCP. Controlla indirizzo e porta e riprova. Errore completo : {error}','red')
            sys.exit(1)
        try:
            key = Fernet.generate_key()
            str_key = key.decode("ascii")
        except socket.error as exc:
            cprint(f'[{TCP.clock()} Errore - TCP Server] Errore durante la generazione della chiave crittografica : {exc}','red')
        cprint(f'[{TCP.clock()} Info - TCP Server] La chiave crittografica di questa sessione è {str_key}','green')
        while True:
            connection, client_address = s.accept()
            command_thread = Thread(target=TCP.command_parser(connection, client_address, str_key), name="PARSER")
            command_thread.start()



    def run(self,*args):
            """Creo un socket, effettuo il binding e genero la chiave crittografica.
                In caso di errore tento il riavvio"""
            try:
                s = socket.socket()
                s.bind((self.address, self.port))
                s.listen(self.backlog)
            except Exception as error:
                cprint(f'[{TCP.clock()} Errore - TCP Server] Si è verificato un errore durante la creazione del socket, errore completo : {error}', 'red')
                cprint(f'[{TCP.clock()} Info - TCP Server] Tento il Riavvio...', 'green')
                TCP.restart((self.address, self.port), self.backlog)
            cprint(f'[{TCP.clock()} Info - TCP Server] Avvio completato', 'green')
            try:
                key = Fernet.generate_key()              # Genera la chiave crittografica AES Fernet
                str_key = key.decode("ascii")
            except socket.error as exc:
                cprint(f'[{TCP.clock()} Errore - TCP Server] Errore durante la generazione della chiave crittografica. Errore completo : {exc}', 'red')
            cprint(f'[{TCP.clock()} Info - TCP Server] La chiave crittografica di questa sessione è {str_key}', 'green')
            while True:
                connection, client_address = s.accept()
                command_thread = Thread(target=TCP.command_parser, args=(connection, client_address, key), name="PARSER")
                command_thread.start()


# Classe FTP Server
class FTP:

    def __init__(self, address, port, user, pasw, banner):
        self.address = address
        self.port = port
        self.user = user
        self.pasw = pasw
        self.banner = banner

# Server FTP con certificato SSL
    def run(self, *args):
        """Avvio il server FTP"""
        authorizer = DummyAuthorizer()
        authorizer.add_user(self.user, self.pasw, f'{os.getcwd()}', perm='elradfmwMT')  # Aggiunge un utente virtuale
        handler = TLS_FTPHandler
        handler.certfile = f'{os.getcwd()}/cert/certfile.pem'  # Directory del certificato
        handler.keyfile = f'{os.getcwd()}/cert/key.pem'     # Directory della chiave
        handler.authorizer = authorizer
        handler.tls_control_required = True
        handler.tls_data_required = True
        handler.masquerade_address = 'XXX.XX.XX.X'  # Inserisci qui il tuo IP pubblico. Serve alla modalità PASV
        handler.passive_ports = range(2122, 2124)  # Porte passive
        handler.banner = self.banner
        address = (self.address, self.port)
        server = FTPServer(address, handler)
        server.max_cons = 20
        server.max_cons_per_ip = 2
        try:
            server.serve_forever()
        except Exception as exc:
            cprint(f'[{TCP.clock()} Errore - FTP Server] Errore nel server FTP -> {exc}', 'red')


if __name__ == "__main__":
    # Istanzio un oggetto TCP ed un oggetto FTP, poi avvio i Threads
    TCP = TCP("XXX.XX.XX.X", 52000, backlog=5)  # Inserisci qui il tuo IP locale
    FTP = FTP("XXX.XX.XX.X", 2121, "Mattia Giambirtone", "Password1971_", "Benvenuto!")  # Inserisci il tuo IP locale
    TCP_Thread = Thread(target=FTP.run, args=(FTP,), name="FTP")
    FTP_Thread = Thread(target=TCP.run, args=(TCP,), name="TCP")
    TCP_Thread.start()
    FTP_Thread.start()
