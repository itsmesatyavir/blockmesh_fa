import websocket
import json
import threading
import time

def get_credentials():
    # Ask the user if they want to change the email and API token
    change = input("Do you want to change the email and API token? (yes/no): ").strip().lower()
    
    if change == 'yes':
        email = input("Enter your email: ").strip()
        api_token = input("Enter your API token: ").strip()
    else:
        # Default credentials
        email = "business.forestarmy@gmail.com"
        api_token = "ffe5d4fa-9bdd-4cd7-936-7fd1211cd540"
    
    return email, api_token

def setup_websocket(email, api_token):
    # WebSocket URL with email and API token
    ws_url = f"wss://ws.blockmesh.xyz/ws?email={email}&api_token={api_token}"

    # Custom headers to mimic browser request
    headers = {
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "connection": "Upgrade",
        "host": "ws.blockmesh.xyz",
        "origin": "chrome-extension://obfhoiefijlolgdmphcekifedagnkfjp",
        "pragma": "no-cache",
        "sec-websocket-extensions": "permessage-deflate; client_max_window_bits",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    }

    # Event handler: When WebSocket connection is established
    def on_open(ws):
        print("WebSocket connection established!")

        # Function to send ping messages every 10 seconds
        def run(*args):
            while True:
                ping_message = json.dumps({"action": "ping"})
                ws.send(ping_message)
                print(f"Sent ping message: {ping_message}")
                time.sleep(10)

        # Run ping in a separate thread
        threading.Thread(target=run).start()

    # Event handler: When a message is received from server
    def on_message(ws, message):
        print(f"Received message from server: {message}")

    # Event handler: When an error occurs
    def on_error(ws, error):
        print(f"WebSocket error: {error}")

    # Event handler: When connection is closed
    def on_close(ws, close_status_code, close_msg):
        print("WebSocket connection closed")

    # Create WebSocket connection
    ws = websocket.WebSocketApp(
        ws_url,
        header=[f"{key}: {value}" for key, value in headers.items()],
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    # Run the WebSocket connection indefinitely
    ws.run_forever()

if __name__ == "__main__":
    email, api_token = get_credentials()
    setup_websocket(email, api_token)
