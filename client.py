import socket

def send_command(sock, command):
    sock.send(command.encode())
    response = sock.recv(1024).decode()
    return response

def connect_to_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

def start_node(sock, node_ip, node_port):
    command = f"CONNECT_NODE {node_ip} {node_port}"
    response = send_command(sock, command)
    print(response)

def start_service(sock, service_name):
    command = f"START {service_name}"
    response = send_command(sock, command)
    print(response)

def stop_service(sock, service_name):
    command = f"STOP {service_name}"
    response = send_command(sock, command)
    print(response)

def get_service_status(sock, service_name):
    command = f"STATUS {service_name}"
    response = send_command(sock, command)
    print(response)

if __name__ == '__main__':
    server_host = 'localhost'
    server_port = 3201

    client_socket = connect_to_server(server_host, server_port)

    while True:
        print("1. Start Node")
        print("2. Start Service")
        print("3. Stop Service")
        print("4. Get Service Status")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            node_ip = input("Enter the node IP: ")
            node_port = int(input("Enter the node port: "))
            start_node(client_socket, node_ip, node_port)

        elif choice == '2':
            service_name = input("Enter the service name: ")
            start_service(client_socket, service_name)

        elif choice == '3':
            service_name = input("Enter the service name: ")
            stop_service(client_socket, service_name)

        elif choice == '4':
            service_name = input("Enter the service name: ")
            get_service_status(client_socket, service_name)

        elif choice == '5':
            break

        else:
            print("Invalid choice. Try again.")

    client_socket.close()
