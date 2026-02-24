# TLS Analysis LAB

A Python project for analyzing TLS/SSL connections and sending HTTP requests.

## Features

- **HTTP Client**: Sends HTTP requests over TCP (port 80)
- **TLS Client**: Performs TLS handshake and analyzes connection
- **Certificate Analysis**: Shows TLS version, cipher suite, and certificate details
- **TLS Version Comparison**: Compares TLS 1.2 and TLS 1.3

## Requirements

- Python 3.7+ (recommended for TLS 1.3 support)
- No external dependencies (uses only Python standard library)

## Usage

### HTTP Client
```bash
python http_client.py
```

### TLS Client
```bash
python tls_client.py
```

### Run Tests
```bash
python test_tls.py
```

## Project Structure

- `http_client.py` - HTTP client implementation
- `tls_client.py` - TLS/SSL client with analysis features
- `test_tls.py` - Test script
