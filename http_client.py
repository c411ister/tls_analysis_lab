import socket

def send_http_request(host="httpbin.org", path="/get", port=80):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"Connecting to {host}:{port}...")

        client_socket.connect((host, port))
        print("Connection successful!")

        request = f"GET {path} HTTP/1.1\r\n"
        request += f"Host: {host}\r\n"
        request += "Connection: close\r\n"
        request += "\r\n"

        print("Sending HTTP request...")
        #convert string to bytes because socket can only send bytes.
        client_socket.send(request.encode('utf-8'))

        print("Receiving HTTP response...")
        #empty byte array is created and data from server is collected here with recv() method.
        response = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response += chunk

        print("HTTP response received!")
        print(response.decode('utf-8'))


    except socket.error as e:
        print(f"Socket error: {e}")

    finally:
        client_socket.close()
        print("Socket closed.")


if __name__ == "__main__":
    send_http_request()