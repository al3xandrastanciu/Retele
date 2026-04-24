import socket

HOST        = '127.0.0.1'
PORT        = 9999
BUFFER_SIZE = 1024

clienti_conectati = {}
mesaje = {}
id_counter = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print("=" * 50)
print(f"  SERVER UDP pornit pe {HOST}:{PORT}")
print("  Asteptam mesaje de la clienti...")
print("=" * 50)

while True:
    try:
        date_brute, adresa_client = server_socket.recvfrom(BUFFER_SIZE)
        mesaj_primit = date_brute.decode('utf-8').strip()

        parti = mesaj_primit.split(' ', 1)
        comanda = parti[0].upper()
        argumente = parti[1] if len(parti) > 1 else ''

        print(f"\n[PRIMIT] De la {adresa_client}: '{mesaj_primit}'")

        if comanda == 'CONNECT':
            if adresa_client in clienti_conectati:
                raspuns = "EROARE: Esti deja conectat la server."
            else:
                clienti_conectati[adresa_client] = True
                nr_clienti = len(clienti_conectati)
                raspuns = f"OK: Conectat cu succes. Clienti activi: {nr_clienti}"
                print(f"[SERVER] Client nou conectat: {adresa_client}")

        elif comanda == 'DISCONNECT':
            if adresa_client in clienti_conectati:
                del clienti_conectati[adresa_client]
                raspuns = "OK: Deconectat cu succes. La revedere!"
                print(f"[SERVER] Client deconectat: {adresa_client}")
            else:
                raspuns = "EROARE: Nu esti conectat la server."

        elif comanda == 'PUBLISH':
            if adresa_client not in clienti_conectati:
                raspuns = "EROARE: Nu esti conectat. Foloseste CONNECT mai intai."
            elif not argumente.strip():
                raspuns = "EROARE: Trebuie sa specifici un mesaj pentru PUBLISH."
            else:
                id_counter += 1
                mesaje[id_counter] = {'autor': adresa_client, 'text': argumente}
                raspuns = f"OK: Mesaj publicat cu ID={id_counter}"
                print(f"[SERVER] Mesaj nou ID={id_counter} de la {adresa_client}")

        elif comanda == 'DELETE':
            if adresa_client not in clienti_conectati:
                raspuns = "EROARE: Nu esti conectat. Foloseste CONNECT mai intai."
            else:
                try:
                    id_mesaj = int(argumente)
                    if id_mesaj not in mesaje:
                        raspuns = f"EROARE: Nu exista niciun mesaj cu ID={id_mesaj}."
                    elif mesaje[id_mesaj]['autor'] != adresa_client:
                        raspuns = f"EROARE: Nu poti sterge mesajul ID={id_mesaj}. Nu esti autorul."
                    else:
                        del mesaje[id_mesaj]
                        raspuns = f"OK: Mesajul ID={id_mesaj} a fost sters."
                        print(f"[SERVER] Mesaj sters ID={id_mesaj} de la {adresa_client}")
                except ValueError:
                    raspuns = "EROARE: ID-ul trebuie sa fie un numar intreg."

        elif comanda == 'LIST':
            if adresa_client not in clienti_conectati:
                raspuns = "EROARE: Nu esti conectat. Foloseste CONNECT mai intai."
            elif not mesaje:
                raspuns = "OK: Nu exista niciun mesaj publicat."
            else:
                lista = []
                for mid, m in mesaje.items():
                    lista.append(f"ID={mid}: {m['text']}")
                raspuns = "OK: " + " | ".join(lista)

        else:
            raspuns = f"EROARE: Comanda '{comanda}' este necunoscuta. Comenzi valide: CONNECT, DISCONNECT, PUBLISH, DELETE, LIST"

        server_socket.sendto(raspuns.encode('utf-8'), adresa_client)
        print(f"[TRIMIS]  Catre {adresa_client}: '{raspuns}'")

    except KeyboardInterrupt:
        print("\n[SERVER] Oprire server...")
        break
    except Exception as e:
        print(f"[EROARE] {e}")

server_socket.close()
print("[SERVER] Socket inchis.")
