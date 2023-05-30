import socket
import threading

class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.services = {
            'service1': False,
            'service2': False,
            'service3': False
        }

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.nodes = {}
        self.lock = threading.Lock()

    def handle_client(self, client_socket):
        connected_node = None

        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            if data.startswith('CONNECT_NODE'):
                if connected_node is None:
                    node_ip, node_port = data.split()[1], int(data.split()[2])
                    node_key = f'{node_ip}:{node_port}'

                    with self.lock:
                        if node_key in self.nodes:
                            connected_node = self.nodes[node_key]
                        else:
                            connected_node = Node(node_ip, node_port)
                            self.nodes[node_key] = connected_node

                    client_socket.send(f'Connected to node {node_ip}:{node_port}'.encode())
                else:
                    client_socket.send('A node is already connected'.encode())

            elif connected_node is not None:
                # Process received commands for the connected node
                if data.startswith('START'):
                    service_name = data.split()[1]
                    if service_name in connected_node.services:
                        connected_node.services[service_name] = True
                        client_socket.send(f'Started {service_name}'.encode())
                    else:
                        client_socket.send(f'Service {service_name} not found'.encode())

                elif data.startswith('STOP'):
                    service_name = data.split()[1]
                    if service_name in connected_node.services:
                        connected_node.services[service_name] = False
                        client_socket.send(f'Stopped {service_name}'.encode())
                    else:
                        client_socket.send(f'Service {service_name} not found'.encode())

                elif data.startswith('STATUS'):
                    service_name = data.split()[1]
                    if service_name in connected_node.services:
                        status = 'Running' if connected_node.services[service_name] else 'Stopped'
                        client_socket.send(f'Status of {service_name}: {status}'.encode())
                    else:
                        client_socket.send(f'Service {service_name} not found'.encode())

                else:
                    client_socket.send('Invalid command'.encode())
            else:
                client_socket.send('No node connected'.encode())

        client_socket.close()
        with self.lock:
            if connected_node is not None:
                del self.nodes[f'{connected_node.host}:{connected_node.port}']

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        print(f'Server listening on {self.host}:{self.port}')

        while True:
            client_socket, address = server_socket.accept()
            print(f'New connection from {address[0]}:{address[1]}')

            with self.lock:
                self.nodes[client_socket] = None

            thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            thread.start()


if __name__ == '__main__':
    server = Server('localhost', 3201)
    server.start()
