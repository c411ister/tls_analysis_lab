#for TCP/IP connetion
import socket


def send_http_request(host="httpbin.org", path="/get", port=80):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
