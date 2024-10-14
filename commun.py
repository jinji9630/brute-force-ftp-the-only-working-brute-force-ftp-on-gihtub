from ftplib import FTP_TLS, error_perm
import threading

def read_ip_ports(filename):
    with open(filename, 'r') as file:
        return [line.strip().split(':') for line in file.readlines()]

def read_credentials(filename):
    with open(filename, 'r') as file:
        return [line.strip().split(':') for line in file.readlines()]

def test_login(ip, port, credentials, f):
    ftp = FTP_TLS()
    try:
        ftp.connect(ip, int(port))
        ftp.auth()
        ftp.prot_p()

        for username, password in credentials:
            print(f"Attempting to connect to {ip}:{port} with username: {username} password: {password}")
            try:
                ftp.login(username, password)
                print(f"Login successful for {username} with password '{password}' on {ip}:{port}")
                f.write(f"Login successful for {username} with password '{password}' on {ip}:{port}\n")
                return  # Exit on success
            except error_perm:
                pass  # Ignore failed logins

    except Exception as e:
        print(f"Connection failed for {ip}:{port}: {e}")
    finally:
        if 'ftp' in locals() and ftp.sock:
            ftp.quit()
            print("Connection closed")

def run_tests(servers, credentials, max_threads, f):
    threads = []
    for ip, port in servers:
        while len(threads) >= max_threads:
            for thread in threads:
                thread.join(timeout=0)  # Join threads with timeout to check if they're still alive
            threads = [thread for thread in threads if thread.is_alive()]

        thread = threading.Thread(target=test_login, args=(ip, port, credentials, f))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def get_thread_count():
    while True:
        try:
            input_value = input("Enter the number of threads to use (1-100, default is 10): ")
            if input_value == '':
                return 10  # Default value
            count = int(input_value)
            if 1 <= count <= 100:
                return count
            else:
                print("Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# Update to read from your specified file
servers = read_ip_ports('ipport.txt')
credentials = read_credentials('commun.txt')  # Read from commun.txt
f = open("rez.txt", "w")
max_threads = get_thread_count()
run_tests(servers, credentials, max_threads, f)

f.close()
print("All attempts completed.")
