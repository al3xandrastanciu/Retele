import socket

HOST = "127.0.0.1"
PORT = 3333
BUFFER_SIZE = 1024

def receive_full_message(sock):
    try:
        buffer = ""
        while " " not in buffer:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                return None
            buffer += data.decode('utf-8')
        
        first_space = buffer.find(' ')
        if first_space == -1 or not buffer[:first_space].isdigit():
            return "Invalid response format from server"
        
        message_length = int(buffer[:first_space])
        buffer = buffer[first_space + 1:]
        
        while len(buffer) < message_length:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                return None
            buffer += data.decode('utf-8')
        
        return buffer[:message_length]
    except Exception as e:
        return f"Error: {e}"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to server. Type commands (add/get/remove/update/pop/list/count/clear/quit) or 'exit' to quit client.")

        while True:
            command = input('client> ').strip()
            if command.lower() == 'exit':
                break

            s.sendall(command.encode('utf-8'))
            response = receive_full_message(s)
            print(f"Server response: {response}")

if __name__ == "__main__":
    main()
