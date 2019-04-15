# PythonRemoteController
Semplice applicazione client-server con interfaccia TCP ed FTP. Utile per avere accesso ai propri file ed alla shell del proprio pc da remoto senza dover configurare un servizio SSH ed in modo sicuro.

# Requirements 
Python 3.6.x o superiore

Le seguenti librerie esterne installate : 

- cryptography==2.6.1

- pyftpdlib==1.5.5

- pyOpenSSL==19.0.0

- termcolor==1.1.0



# Istruzioni per l'uso

**Passo 1 :** Installa le librerie necessarie con il comando 'pip install nomemodulo==versione'. Puoi trovare le librerie richieste per il programma nella sezione **Requirements**
  
Se non l'hai già fatto, apri le porte del tuo router perchè sia raggiungibile dall'esterno. Digita nella barra degli indirizzi '192.168.1.1' e dovresti trovarti di fronte ad una schermata di login. Se vedi direttamente il pannello di amministrazione della tua rete locale, salta al **Passo 2**, altrimenti prosegui nel **Passo 1**. Se non hai mai effettuato l'accesso al pannello di amministrazione del tuo router le credenziali di accesso saranno , generalmente, username=admin e password=admin.
Per maggiori informazioni consulta il manuale d'uso del tuo router.

**Passo 2:** Cerca una voce del tipo 'Port Mapping' o 'Port forwarding'; una volta trovata, cliccaci sopra con il mouse e cerca un bottone con un + o qualcosa del tipo 'Aggiungi una nuova regola di port mapping/forwarding personalizzata'. Scegli il procotollo TCP e poi alla voce 'Porta Esterna' o 'Porta remota' digita 52000 (se è possibile inserire un range di porte, digita 52000-52000). Se presente spunta la voce 'Stessa porta', cosa che reinvierà dal tuo ip_pubblico:52000 automaticamente a ip_locale:52000, altrimenti seleziona il dispositivo su cui eseguirai il server nella rete locale e imposta la porta locale a 52000. Ripeti la stessa operazione per le porte 2121-2123 (se è possibile inserire un range di porte, digita direttamente 2121-2123, altrimenti applica una regola per ogni porta dalla 2121 alla 2123)

**N.B.** Se hai molte regole di port forwarding personalizzate, potrebbe essere una buona idea dare alle regole appena create un nome appropriato del tipo "Python Server" .

**Passo 3:** Una volta scaricato il programma, assicurati che tutti i file siano nella stessa cartella e modifica il file server.py, inserendo, alla fine del file, al posto di XXX.XXX.XXX.XX il tuo ip locale e sostituisci l'indirizzo dentro la classe FTP con il tuo IP pubblico; contemporaneamente sostituisci l'ip dentro client.py con il tuo IP pubblico.
Prima di avviare il server è necessario generare un certificato di sicurezza tramite openssl, puoi trovare una guida dettagliata su come fare al link http://www.megalab.it/7090/come-generare-certificati-digitali-con-openssl-windows-e-linux.

Inserisci il file di certificato nella cartella cert, rinominandolo certfile.pem, e nella stessa cartella il file della chiave privata, rinominandolo key.pem; Se hai completato tutti i passi correttamente, puoi eseguire server.py .
Partirà il server TCP per l'esecuzione di comandi e contemporaneamente il server FTP over TLS. Il server mostrerà a schermo la chiave crittografica di sessione, dovrai inserirla nel client prima di connetterti al server per permettere una comunicazione sicura tra il server e il client.

**N.B. 2** Nella repository sono già presenti una chiave privata ed un certificato di esempio, ma è **vivamente sconsigliato utilizzarli** in quanto si perderebbe il senso di utilizzare una connessione TLS.


# Importante

Tutte le informazioni trasmesse da e verso il client/server sono crittografate secondo altissimi standard di sicurezza, al fine di prevenire attacchi di tipo MITM (Man In The Middle).

Le informazioni trasmesse attraverso il protocollo di rete TCP sono crittografate tramite l'algoritmo AES Fernet a chiave simmetrica.

Le informazioni trasmesse attraverso il protocollo FTP sono crittografate tramite un certificato Secure Socket Layer e il protocollo di crittografia TLS 1.3 .

Il programma è in versione alpha, quindi non è privo di errori e/o bug ed è distribuito senza alcuna garanzia (Per maggiori informazioni consulta la licenza allegata al software). Nel caso dovessi riscontrare qualche errore, per favore, contatta lo sviluppatore perchè possa risolverlo! Trovi il suo contatto in fondo al documento.

**N.B. 3** I più attenti fra voi avranno notato che questo software assomiglia molto ad un RAT (Remote Administration Tool).
Sappiate che non mi assumo nessuna responsabilità per l'uso che farete del codice in questa repository e che comunque l'uso di questo programma è condizionato dalla licenza scaricabile insieme allo stesso.

Questo programma era **solo** un modo per testare le mie potenzialità e impiegare molto tempo libero.

**N.B. 4** I comandi come sudo e login, che quindi richiedono in input nome utente e/o password, non sono ancora supportati.
Verranno aggiunti in una futura release, se possibile.

**N.B. 5** A breve sarà implementata la possibilità di aprire le porte del router automaticamente dal programma stesso, previa richiesta all'utente, in modo da semplificare la configurazione del server.

Enjoy :)

# Crediti & Menzioni Onorevoli

Vorrei ringraziare particolarmente :

- Enkidu -> Per le sue **furiose**, ma costruttive, critiche. Fate un salto sul suo profilo GitHub --> https://github.com/webdiamond

- Muflone -> Per avermi fatto capire cosa è e cosa non è OOP, oltre a molto aiuto tecnico. Toh, anche lui ha GitHub --> https://github.com/muflone

- Vympel -> Per il prezioso aiuto con i primi test del programma. Indovina un po'? Anche lui ha GitHub! --> https://github.com/vympel7

- Tutta la community di Python Italia -> Il vostro supporto è sempre fondamentale!

**Per qualsiasi problema, dubbi e/o domande** -> Contatta https://telegram.me/isgiambyy o via e-mail a hackhab@gmail.com

**Attenzione** Le pull requests, suggerimenti di modifica per migliorare il codice, sono sempre ben accette!

