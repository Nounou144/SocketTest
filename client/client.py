import socket
import threading
import pickle
from protocols import Protocols

class Client:
    # Initiate Client
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        self.connected = False

        #Count
        self.count = None
    
    # Start a thread to receive
    def run(self):
        print("Client created!")
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
    
    # Client Bootup
    def connect(self):
        self.send(Protocols.COUNT, None)
        self.connected = True
        print(self.connected)

    # Receive Responses
    def receive(self):
        while True:
            try:
                # Get Response
                response = pickle.loads(self.server.recv(2048))
                self.handle_response(response)
            except:
                # Server likely disconnected
                print("Server Disconnected...")
                break
        
        self.close()
    
    # Handle Responses
    def handle_response(self, response):
        r_type = response.get("type")
        data = response.get("data")

        # Message
        if r_type == Protocols.MESSAGE:
            print(f"[RECEIVED]: {data}")
        # Count
        elif r_type == Protocols.COUNT:
            self.count = data
            print(data)
            
    # Sending Messages
    def send(self, r_type, data):
        message = {"type": r_type, "data": data}
        print(f"[SENDING]: {message}")
        message = pickle.dumps(message)
        self.server.sendall(message)
    
    # Close Client
    def close(self):
        print(f"Disconnected from {self.server}")
        self.server.close()