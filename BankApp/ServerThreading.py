import socket
import threading
import json
import portalocker



def balance_check(num_client, client_socket):
    lock = portalocker.Lock("Clients.json.lock")
    with lock:
        with open("Clients.json", "r") as file:
            data = json.load(file)
        for client in data:
            if client["login"] == num_client["login"]:
                saldo = client["saldo"]
                client_socket.send(f"Saldo: {saldo}".encode('utf-8'))
                break
    with lock:
        pass




def inc_funds(num_client, client_socket):
    client_socket.send("Wplacanie srodkow na konto.".encode('utf-8'))
    while True:
        client_socket.send("Maksymalna wysokosc wplaty wynosi 1000.0.".encode('utf-8'))
        rnumber = float(client_socket.recv(1024).decode('utf-8'))
        number = round(rnumber, 2)

        if number < 0 or number > 1000:
            client_socket.send("Niewlasciwa kwota. Prosze sprobowac ponownie.".encode('utf-8'))
            break
        else:
            lock = portalocker.Lock("Clients.json.lock")
            with lock:
                with open("Clients.json", "r") as file:
                    data = json.load(file)

            for client in data:
                if client["login"] == num_client["login"]:
                    client["saldo"] += number
                    num_client["saldo"] = client["saldo"]
                    client_socket.send(f"Wplacono srodki o wysokosci: {number}".encode('utf-8'))
                    save_json(data)
                    break

            lock.release()
            break


def dec_funds(num_client, client_socket):
    client_socket.send("Wyplacanie srodkow z konta.".encode('utf-8'))
    while True:
        client_socket.send("Maksymalna suma wyciagu z konta wynosi 500.0.".encode('utf-8'))
        c_number = float(client_socket.recv(1024).decode('utf-8'))
        dec_number = round(c_number, 2)

        if dec_number < 0 or dec_number > 500:
            client_socket.send("Niewlasciwa kwota. Prosze sprobowac ponownie.".encode('utf-8'))
            break
        if dec_number > num_client["saldo"]:
            client_socket.send("Niewystarczajaca ilosc srodkow na koncie.".encode('utf-8'))
            break
        else:
            lock = portalocker.Lock("Clients.json.lock")
            with lock:
                with open("Clients.json", "r") as file:
                    data = json.load(file)

            for client in data:
                if client["login"] == num_client["login"]:
                    client["saldo"] -= dec_number
                    num_client["saldo"] = client["saldo"]
                    client_socket.send(f"Wyplacono srodki. Kwota na koncie zmniejszyla sie o: {dec_number}".encode('utf-8'))
                    save_json(data)
                    break

            lock.release()
            break


def send_funds(num_client, client_socket):
    client_socket.send("Przelew na konto odbiorcy.".encode('utf-8'))
    while True:
        client_socket.send("Przelew na kwote maksymalna 10000.0".encode('utf-8'))
        acc_number = int(client_socket.recv(1024).decode('utf-8'))
        gnumber = float(client_socket.recv(1024).decode('utf-8'))
        number = round(gnumber, 2)

        lock = portalocker.Lock("Clients.json.lock")
        with lock:
            with open("Clients.json", "r") as file:
                data = json.load(file)

            sender = None
            recipient = None
            for client in data:
                if client["login"] == num_client["login"]:
                    sender = client
                elif client["numer_konta"] == acc_number:
                    recipient = client

            if not recipient:
                client_socket.send("Nie znaleziono numeru konta bankowego w bazie danych.".encode('utf-8'))
                break
            if number > sender["saldo"]:
                client_socket.send("Niewystarczajaca ilosc srodkow na koncie.".encode('utf-8'))
                break
            if number < 0 or number > 10000:
                client_socket.send("Niewlasciwa kwota.".encode('utf-8'))
                break

            sender["saldo"] -= number
            recipient["saldo"] += number

            client_socket.send(f"Przelano kwote {number} na konto {acc_number} z powodzeniem.".encode('utf-8'))

            save_json(data)

        lock.release()
        break




def exit_app(client_socket):
    client_socket.send("Zamykanie aplikacji...".encode('utf-8'))
    client_socket.close()



def login_client(client_socket):
    with open("Clients.json", "r") as file:
        data = json.load(file)

    while True:
        login = client_socket.recv(1024).decode('utf-8')
        password = client_socket.recv(1024).decode('utf-8')

        found = False
        client_data = None
        for client in data:
            if client["login"] == login and client["haslo"] == password:
                found = True
                client_data = client
                break
        if found:
            imie = client_data["imie"]
            client_socket.send(f"Poprawny login i haslo. Witaj {imie}!".encode('utf-8'))
            return client_data
        else:
            client_socket.send("Niepoprawny login lub haslo. Sprobuj ponownie.".encode('utf-8'))


def menu_client(client_socket):
    while True:
        opt_choice = client_socket.recv(1024).decode('utf-8')
        if opt_choice in ["1", "2", "3", "4", "5"]:
            client_socket.send(f"Wybrano opcje numer: {opt_choice}".encode('utf-8'))
            return opt_choice
        else:
            client_socket.send("Cos poszlo nie tak. Wybierz ponownie: ".encode('utf-8'))


def choice_clientaction(opt_choice, client_data, client_socket):
    num_choice = opt_choice
    num_client = client_data
    if num_choice == "1":
        balance_check(num_client, client_socket)
    elif num_choice == "2":
        inc_funds(num_client, client_socket)
    elif num_choice == "3":
        dec_funds(num_client, client_socket)
    elif num_choice == "4":
        send_funds(num_client, client_socket)
    elif num_choice == "5":
        exit_app(client_socket)


def save_json(data):
    with open("Clients.json", "w") as file:
        json.dump(data, file, indent=4)



class EchoServerThread(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.socket = client_socket

    def run(self):
        thread_name = threading.current_thread().name
        client_data = login_client(self.socket)
        while not client_data:
            client_data = login_client(self.socket)

        while True:
            opt_choice = menu_client(self.socket)
            while not opt_choice:
                opt_choice = menu_client(self.socket)

            if opt_choice == "5":
                exit_app(self.socket)
                break

            choice_clientaction(opt_choice, client_data, self.socket)

        print(f"Zamknieto polaczenie od klienta: ({client_data['id']})")




def start_threadserver(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server pracuje na {}:{}".format(host, port))

    while True:
        client_socket, client_address = server_socket.accept()
        print("Zaakceptowano połączenie od: {}".format(client_address))


        thread = EchoServerThread(client_socket)
        thread.start()


start_threadserver('localhost', 4646)