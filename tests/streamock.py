import socket, threading

result = b''
server = None

def loop():
    global server, result
    client, _ = server.accept()
    result = b''
    while True:
        data = client.recv(1024)
        if data:
            result += data
        else: 
            break

def start(args):
    global server
    stream = (args.get("STREAM_HOST"), int(args.get("STREAM_PORT")))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(stream)
    server.listen(5)
    thread = threading.Thread(target=loop)
    thread.start()
    return thread

def result(thread):
    global result, server
    thread.join()
    server.close()
    return result
