import sys
import subprocess

def main():
    print("Starting TLS test..\n")
          
    print("Testing TLS client...")
    result = subprocess.run([sys.executable, "tls_client.py"], capture_output=True, text=True)

    if "TLS handshake successful" in result.stdout:
        print("Successful!")
        
    else:
        print("Failed!")
        print("Output:")
        print(result.stdout)
        print("Error:")
        print(result.stderr)


    print("Testing HTTP client...")
    result = subprocess.run([sys.executable, "http_client.py"], capture_output=True, text=True)

    if "HTTP response received" in result.stdout:
        print("HTTP client test successful!")
        
    else:
        print("HTTP client test failed!")
        print("Output:")
        print(result.stdout)
        print("Error:")
        print(result.stderr)

if __name__ == "__main__":
    main()