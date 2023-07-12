import socket
import sys

host = 'localhost'
port = 4646


def logging():
    login = input("Wpisz login: ")
    password = input("Wpisz haslo: ")
    if password == "" or login == "":
        login = "q"
        password = "q"
    return login, password




def authentication(client_socket):
    while True:
        login, password = logging()
        client_socket.send(login.encode('utf-8'))
        client_socket.send(password.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(response)
        if response.startswith("Poprawny login i haslo."):
            return True


def menu():
    opt_choice = (input(f"============\nWybierz opcje:\n1. Sprawdz stan konta.\n2. Wplac srodki."
                           f"\n3. Wyplac srodki.\n4. Przelew na konto\n5. Wyjdz z aplikacji"
                           f"\n============\nProsze wpisac numer wybranej opcji: "))
    if opt_choice == "":
        opt_choice = "9"
    return opt_choice


def menu_check(client_socket):
    while True:
        opt_choice = menu()
        client_socket.send((opt_choice).encode('utf-8'))
        s_response = client_socket.recv(1024).decode('utf-8')
        print(s_response)
        if s_response.startswith("Wybrano opcje numer:"):
            choice_action(client_socket)



def choice_action(client_socket):
    action_response = client_socket.recv(1024).decode('utf-8')
    print(action_response)
    if action_response.startswith("Zamykanie aplikacji..."):
        client_socket.close()
        sys.exit()
    elif action_response.startswith("Wplacanie srodkow na konto."):
        response = client_socket.recv(1024).decode('utf-8')
        print(response)
        number = input("Prosze wpisac wysokosc wplaty: ")
        client_socket.send(number.encode('utf-8'))
        fund_inf = client_socket.recv(1024).decode('utf-8')
        print(fund_inf)
    elif action_response.startswith("Wyplacanie srodkow z konta."):
        response = client_socket.recv(1024).decode('utf-8')
        print(response)
        number = input("Prosze wpisac wysokosc wyplaty srodkow: ")
        client_socket.send(number.encode('utf-8'))
        fund_inf = client_socket.recv(1024).decode('utf-8')
        print(fund_inf)
    elif action_response.startswith("Przelew na konto odbiorcy."):
        response = client_socket.recv(1024).decode('utf-8')
        print(response)
        acc_number = input("Prosze wpisac numer konta odbiorcy: ")
        client_socket.send(acc_number.encode('utf-8'))
        number = input("Prosze wpisac kwote przelewu: ")
        client_socket.send(number.encode('utf-8'))
        transfer_status = client_socket.recv(1024).decode('utf-8')
        print(transfer_status)




def start_client():
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
        except socket.error as e:
            print(f"Error connecting to the server: {e}")
            exit(-1)

        print(f"Polaczono do {host}:{port}")

        authenticated = False
        while not authenticated:
            authenticated = authentication(client_socket)

        menu_selected = False
        while not menu_selected:
            menu_selected = menu_check(client_socket)

        if not menu_selected:
            break


start_client()





