from socket import *
import threading

#Fontes de pesquisa e créditos:
#https://www.youtube.com/watch?v=5G_bNVKdECk
#https://stackoverflow.com/questions/27139240/i-need-the-server-to-send-messages-to-all-clients-python-sockets
#https://stackoverflow.com/questions/10810249/python-socket-multiple-clients - onde tirei a ideia da funcao clientes
#https://medium.com/@denizhalil/advanced-socket-programming-with-python-multi-client-and-server-communication-c0416836c3bd - principal fonte que utilizei pra prazer o código
#https://docs.python.org/pt-br/3/howto/sockets.html#creating-a-socket - documentação do socket part 1
#https://docs.python.org/3/library/socket.html#socket-objects - documentação do socket part 2

PORT = 12000
HOST = "localhost"
serverSocket = socket(AF_INET, SOCK_STREAM) # Cria o socket do servidor; Main Thread

clientes_conectados = [] # Lista onde vou colocar os clientes
lista_lock = threading.Lock() # Exclusividade Mútua. Funciona como um Mutex

def broadcast(msg, rmt_conn = None):
    #Criando uma função própria para propagar a mensagem para os cliente
    with lista_lock: # Carrega o Mutex
        for client in clientes_conectados: # Percorre cada cliente
            try:
                client.send(msg)# o socket manda a mensagem para cada cliente
            except:
                pass


def lidar_clientes(conn, addr):
    print(f'Conexão estabelecida com {addr}')

    with lista_lock:
        clientes_conectados.append(conn) # adiciona de forma segura (MUTEX) na zona crítica

    print(f"Clientes conectados atualmente: {len(clientes_conectados)}")
        
    try:
        while True:
            sentence = conn.recv(1024) # ler a mensagem recebida no socket de mensagem
            if not sentence:
                break

            # converte uma sequencia de bytes em uma string de texto
            mensagemDecodificada = sentence.decode() 
            print(f"Mensagem de {addr}: {mensagemDecodificada}")

            # Prepara a mensagem formatada para mandar a todos
            resposta = f"[{addr[0]}:{addr[1]}]: {mensagemDecodificada}".encode()
            broadcast(resposta)

    except ConnectionResetError:
        print(f"Cliente {addr} foi desconectado abruptamente.")

    finally:
        # Remove o cliente da lista ao desconectar
        with lista_lock:
            if conn in clientes_conectados:
                clientes_conectados.remove(conn)
        
        try:
            conn.shutdown(SHUT_RDWR) #disables both sending and receiving operations on a full-duplex socket connection,
            conn.close()
            print(f"Conecxão com {addr} fechada.")
        except:
            pass
        
        print(f"Conexão com {addr} fechada. Clientes restantes: {len(clientes_conectados)}")
    

def start_server():
    with serverSocket as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Servidor escutando em {HOST}:{PORT}...")
        while True:
            connectionSocket, addr = s.accept()
            thread = threading.Thread(target=lidar_clientes, args=(connectionSocket, addr))
            thread.daemon = True
            thread.start()

if __name__ == "__main__":
    start_server()