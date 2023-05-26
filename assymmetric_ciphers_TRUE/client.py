import socket
from DH_protocol import DH_Endpoint
from PortPool import PortPool

HOST = '127.0.0.1'
pool = PortPool(10)
PORT = pool.get_port()

sock = socket.socket()
sock.connect((HOST, PORT))

#создаем клиента по протоколу DH
clientDH = DH_Endpoint()
#создаем связку публичных ключей клиента и сервера и персональный ключ клиента
clientDH.bunch_of_public_keys()

keys = str(clientDH.client_public_key)+' '+str(clientDH.server_public_key)

sock.send(keys.encode())


msg = sock.recv(1024).decode()
if msg == 'Доступ разрешен':
    print(msg+'\nЧтобы выйти, отправьте \'exit\'')

    # получаем частичный ключ от сервера
    server_key_partial = int(sock.recv(1024).decode())
    # print(server_key_partial)


    client_partial_key = clientDH.generate_partial_key()
    sock.send(str(client_partial_key).encode())  # отправляем частичный ключ клиента (А) серверу

    # восстанавливаем полный ключ
    clientDH.generate_full_key(server_key_partial)

    while True:
        msg = input('>>')
        if msg.lower() == 'exit':
            sock.send(clientDH.encrypt_message(msg).encode())
            break
        # отправляем закодированное сообщение
        sock.send(clientDH.encrypt_message(msg).encode())
        msg = sock.recv(2024).decode()
        dec_msg = clientDH.decrypt_message(msg)
        print(f'Зашифрованное сообщение: {msg} \nРаcшифрованное сообщение: {dec_msg}\n')
    sock.close()

else:
    print('Доступ запрещен')
    sock.close()
