#for TCP/IP connetion
import socket
#TLS/SSL şifreleme işlemleri için(for secure communication)
import ssl

#tüm TLS işlemlerini gerçekleştiren fonksiyon
def tls_handshake(host="httpbin.org", port= 443):
    print(f"\nTLS handshake başlatılıyor: {host}:{port}")

    print("TCP bağlantısı kuruluyor...")
    #socket nesnesi oluşturulur ve zaman aşımı süresi 10 saniye olarak ayarlanır.
    #socket.AF_INET IPv4 adres ailesini belirtir.
    #socket.SOCK_STREAM ise TCP protokolünü kullanarak bir bağlantı oluşturulacağını belirtir.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)  

    try:
        #TCP bağlantısı kurulur
        print(f"{host}:{port}")
        #connect() metodu ile sunucuya bağlanır.
        sock.connect((host, port))
        print("TCP bağlantısı başarılı!")

        print("TLS context oluşturuluyor...")
        #context: TLS ayarlarını saklayan bir değişken.
        #ssL.SSLContext(): SSL/TLS ayarları için bir konteyner oluşturur.
        #ssL.PROTOCOL_TLS_CLIENT: güvenli TLS bağlantıları için önerilen protokol sürümünü belirtir.
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        #CERT_REQUIRED, sunucunun sertifikasının doğrulanmasını zorunlu yapar.
        context.verify_mode = ssl.CERT_REQUIRED
        #sunucu adını sertifika ile karşılaştırarak doğrulama yapar.
        context.check_hostname = True
        #varsayılan sertifikaları yükler.
        context.load_default_certs()
    

        print("TLS handshake başlatılıyor...")
        #wrap_socket metodu TCP bağlantısını TLS ile sarmalar.
        #sunucuyla TLS handshake'i gerçekleştirir.
        #şifreli TLS socketi oluşturulur.
        tls_socket = context.wrap_socket(sock, server_hostname=host)
        print("TLS handshake başarılı!")

        print("TLS bilgileri alınıyor... \n")
        
        tls_version = tls_socket.version()
        print(f"TLS Sürümü: {tls_version}")

        #kullanılan şifreleme algoritması bilgilerini alır
        cipher = tls_socket.cipher()
        if cipher:
            #[0] algoritma, [1] şifreleme modu, [2] anahtar uzunluğu
            print(f"Cipher: {cipher[0]}, Mode: {cipher[1]}, Key Length: {cipher[2]} bits")


        print("Sertifika bilgileri: \n" )
        #sunucudan sertifikayı al ve cert değişkenine kaydet
        cert = tls_socket.getpeercert()
        if cert:
            #subject: sertifikayı alan sunucu bilgilerini içerir
            print(f"Subject: (sunucu):")
            for key, value in cert.get('subject', []):
                print(f"{key}: {value}")

            #issuer: sertifikayı imzalayan otorite (CA) bilgilerini içerir
            print(f"\nIssuer (CA):")
            for key, value in cert.get('issuer', []):
                print(f"{key}: {value}")

        print("Sertifika zinciri: \n")
        der_cert = tls_socket.getpeercert(binary_form=True)
        if der_cert:
            #sertifika zinciri bilgilerini alır
            print(f"Sertifika uzunluğu: {len(der_cert)} bytes")

        try:
            #TLS bağlantısında seçilen ALPN protokolünü alır
            alpn_protocol = tls_socket.selected_alpn_protocol()
            #none değilse ekrana yazdırır
            if alpn_protocol:
                print(f"\nALPN Protokolü: {alpn_protocol}")
        except AttributeError:
            print("\nALPN desteği yok.\n")
        
        print("Bağlantı kesiliyor...")


        request = f"GET /get HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        tls_socket.send(request.encode('utf-8'))
        
        response = b""
        for _ in range(3):
            chunk = tls_socket.recv(4096)
            if not chumk:
                break
            response += chunk

        response_text = response.decode('utf-8', errors='replace') #or ignore error
        if "HTTP" in response_text:
            print("HTTP cevabı alındı!")
            print(response_text)

        else:
            print("HTTP cevabı alınamadı.")

    
    except socket.error as e:
        print(f"Socket hatası: {e}")

    except ssl.SSLError as e:
        print(f"SSL hatası: {e}")

    except Exception as e:
        print(f"Genel hata: {e}")

    finally:
        print("Bağlantı kapatılıyor...")
        sock.close()
        tls_socket.close()
        print("Bağlantı kapatıldı.")
    

if __name__ == "__main__":
    tls_handshake()

