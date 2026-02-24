#for TCP/IP connection
import socket
#TLS/SSL encryption operations (for secure communication)
import ssl

#function that performs all TLS operations
def tls_handshake(host="httpbin.org", port= 443, tls_version=ssl.PROTOCOL_TLS_CLIENT):
    print(f"\nStarting TLS handshake: {host}:{port}")

    print("Establishing TCP connection...")
    #socket object is created and timeout is set to 10 seconds.
    #socket.AF_INET specifies IPv4 address family.
    #socket.SOCK_STREAM specifies using TCP protocol for connection.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)  
    tls_socket = None

    try:
        #TCP connection is established
        print(f"{host}:{port}")
        #connect to server with connect() method.
        sock.connect((host, port))
        print("TCP connection successful!")

        print("Creating TLS context...")
        #context: a variable that stores TLS settings.
        #ssl.SSLContext(): creates a container for SSL/TLS settings.
        #tls_version parameter specifies the TLS protocol version to use.
        context = ssl.SSLContext(tls_version)
        #CERT_REQUIRED makes server certificate verification mandatory.
        context.verify_mode = ssl.CERT_REQUIRED
        #verifies by comparing server name with certificate.
        context.check_hostname = True
        #loads default certificates.
        context.load_default_certs()
    

        print("Starting TLS handshake...")
        #wrap_socket method wraps TCP connection with TLS.
        #performs TLS handshake with server.
        #encrypted TLS socket is created.
        tls_socket = context.wrap_socket(sock, server_hostname=host)
        print("TLS handshake successful!")

        print("Getting TLS information... \n")
        
        negotiated_version = tls_socket.version()
        print(f"TLS Version: {negotiated_version}")

        #gets information about used encryption algorithm
        cipher = tls_socket.cipher()
        if cipher:
            #[0] algorithm, [1] encryption mode, [2] key length
            print(f"Cipher: {cipher[0]}, Mode: {cipher[1]}, Key Length: {cipher[2]} bits")


        print("Certificate information: \n" )
        #get certificate from server and save in cert variable
        cert = tls_socket.getpeercert()
        if cert:
            #subject: contains server information receiving the certificate
            print(f"Subject (server):")
            for key, value in cert.get('subject', []):
                print(f"{key}: {value}")

            #issuer: contains information of authority (CA) signing the certificate
            print(f"\nIssuer (CA):")
            for key, value in cert.get('issuer', []):
                print(f"{key}: {value}")

        print("Certificate chain: \n")
        der_cert = tls_socket.getpeercert(binary_form=True)
        if der_cert:
            #gets certificate chain information
            print(f"Certificate length: {len(der_cert)} bytes")

        try:
            #gets selected ALPN protocol in TLS connection
            alpn_protocol = tls_socket.selected_alpn_protocol()
            #prints if not none
            if alpn_protocol:
                print(f"\nALPN Protocol: {alpn_protocol}")
        except AttributeError:
            print("\nNo ALPN support.\n")
        
        request = f"GET /get HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        tls_socket.send(request.encode('utf-8'))
        
        response = b""
        for _ in range(3):
            chunk = tls_socket.recv(4096)
            if not chunk:
                break
            response += chunk

        response_text = response.decode('utf-8', errors='replace') #or ignore error
        if "HTTP" in response_text:
            print("HTTP response received!")
            print(response_text)

        else:
            print("HTTP response not received.")

    
    except socket.error as e:
        print(f"Socket error: {e}")

    except ssl.SSLError as e:
        print(f"SSL error: {e}")

    except Exception as e:
        print(f"General error: {e}")

    finally:
        print("Closing connection...")
        if tls_socket:
            tls_socket.close()
        sock.close()
        print("Connection closed.")
    

def compare_tls_versions(host="httpbin.org", port=443):
    print("TLS 1.2 and TLS 1.3 comparison:")

    #TLS 1.2 test
    print("\nTLS 1.2 test:")
    tls_handshake(host, port, ssl.PROTOCOL_TLSv1_2)

    #TLS 1.3 test
    print("\nTLS 1.3 test:")
    tls_handshake(host, port, ssl.PROTOCOL_TLSv1_3)

    print("\nComparison completed.")


if __name__ == "__main__":
    tls_handshake()
    compare_tls_versions()
    

