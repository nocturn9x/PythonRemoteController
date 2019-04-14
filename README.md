# PythonRemoteController
Semplice applicazione client-server con interfaccia TCP ed FTP. Utile per avere accesso ai propri file ed alla shell del proprio pc da remoto senza dover configurare un servizio SSH ed in modo sicuro.

# Requirements 
Python 3.6.x o superiore

Le seguenti librerie esterne installate : 

- asn1crypto==0.24.0

- cffi==1.12.2

- cryptography==2.6.1

- pycparser==2.19

- pyftpdlib==1.5.5

- pyOpenSSL==19.0.0

- six==1.12.0

- termcolor==1.1.0



# Istruzioni per l'uso

**Passo 1 :** Installa le librerie necessarie con il comando 'pip install nomemodulo==versione'. Puoi trovare le librerie richieste per il programma nella sezione **Requirements**
  
Se non l'hai già fatto, apri le porte del tuo router perchè sia raggiungibile dall'esterno. Digita nella barra degli indirizzi '192.168.1.1' e dovresti trovarti di fronte ad una schermata di login. Se vedi direttamente il pannello di amministrazione della tua rete locale, salta al **Passo 2**, altrimenti prosegui nel **Passo 1**. Se non hai mai effettuato l'accesso al pannello di amministrazione del tuo router le credenziali di accesso saranno , generalmente, username=admin e password=admin.
Per maggiori informazioni consulta il manuale d'uso del tuo router.

**Passo 2:** Cerca una voce del tipo 'Port Mapping' o 'Port forwarding'; una volta trovata, cliccaci sopra con il mouse e cerca un bottone con un + o qualcosa del tipo 'Aggiungi una nuova regola di port mapping/forwarding personalizzata'. Scegli il procotollo TCP e poi alla voce 'Porta Esterna' o 'Porta remota' digita 52000 (se è possibile inserire un range di porte, digita 52000-52000). Se presente spunta la voce 'Stessa porta', cosa che reinvierà dal tuo ip_pubblico:52000 automaticamente a ip_locale:52000, altrimenti seleziona il dispositivo su cui eseguirai il server nella rete locale e imposta la porta locale a 52000. Ripeti la stessa operazione per le porte 2121-2123 (se è possibile inserire un range di porte, digita direttamente 2121-2123, altrimenti applica una regola per ogni porta dalla 2121 alla 2123)

**N.B.** Se hai molte regole di port forwarding personalizzate, potrebbe essere una buona idea dare alle regole appena create un nome appropriato del tipo "Python Server" .

**Passo 3:** Una volta scaricato il programma, assicurati che tutti i file siano nella stessa cartella e modifica il file main.py, inserendo, alla fine del file, al posto di XXX.XXX.XXX.XX il tuo ip locale e sostituisci l'indirizzo dentro la classe FTP con il tuo IP pubblico; contemporaneamente sostituisci l'ip dentro client.py con il tuo IP pubblico.
Prima di avviare il server è necessario generare un certificato di sicurezza tramite openssl, puoi trovare una guida dettagliata su come fare al link http://www.megalab.it/7090/come-generare-certificati-digitali-con-openssl-windows-e-linux.
Inserisci il file di certificato nella cartella cert, rinominandolo certfile.pem, e nella stessa cartella il file della chiave privata, rinominandolo key.pem; Se hai completato tutti i passi correttamente, puoi eseguire server.py .
Partirà il server TCP per l'esecuzione di comandi e contemporaneamente il server FTP over TLS. Il server mostrerà a schermo la chiave crittografica di sessione, dovrai inserirla nel client prima di connetterti al server per permettere una comunicazione sicura tra il server e il client.

**Per qualsiasi problema, dubbi e/o domande** -> Contatta https://telegram.me/isgiambyy

# Nota Bene 

Tutte le informazioni trasmesse da e verso il client/server sono crittografate secondo altissimi standard di sicurezza, al fine di prevenire attacchi di tipo MITM (Man In The Middle).

Enjoy :)
