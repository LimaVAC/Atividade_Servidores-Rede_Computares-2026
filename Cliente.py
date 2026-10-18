from socket import *
import threading
PORT = 12000
HOST = "localhost"

def receber_mensagens(sock):
    """Função rodando em background para escutar mensagens do servidor continuamente."""
    while True:
        try:
            mensagem = sock.recv(1024)
            if not mensagem:
                print("\n[Desconectado do servidor]")
                break
            # Exibe a mensagem recebida de forma limpa na tela
            print(f"\n{mensagem.decode()}")
            print("Mensagem: ", end="", flush=True)
        except:
            break

def start_client():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.connect((HOST, PORT))
        print(f"Conectado ao chat em {HOST}:{PORT}. Digite 'exit' para sair.\n")

        # Inicia uma thread separada para escutar o servidor
        thread_escuta = threading.Thread(target = receber_mensagens, args=(clientSocket,))
        thread_escuta.daemon = True
        thread_escuta.start()

        while True:
            sentence = input('Mensagem:')
            if sentence.lower() == 'exit':
                print('Saindo...')
                break
            if sentence.strip() == '':
                continue
            clientSocket.send(sentence.encode())

    except Exception as e:
        print(f"Erro na conexão: {e}")

    finally:
        try:
            clientSocket.shutdown(SHUT_RDWR)
            clientSocket.close()
        except:
            pass
        print('Conexão terminada.')

if __name__ == "__main__":
    start_client()