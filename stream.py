import json
import websocket
import config


def on_open(web_socket):
    print("opened")
    auth_data = {
        "action": "authenticate",
        "data": {"key_id": config.APCA_API_KEY_ID, "secret_key": config.APCA_API_SECRET_KEY}
    }

    web_socket.send(json.dumps(auth_data))

    listen_message = {"action": "listen", "data": {"streams": ["AM.TSLA"]}}

    web_socket.send(json.dumps(listen_message))


def on_message(web_socket, message):
    print("received a message")
    print(message)


def on_close(web_socket):
    print("closed connection")


socket = "wss://data.alpaca.markets/stream"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()

# {"action": "auth", "key": "PKXK3FH7S5OGG9MUUIHN", "secret": "O06CbQJ8kLDjo0EL301CN0bxkfjYZgLzqRwtBkeE"}
