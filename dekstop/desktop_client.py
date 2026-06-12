import asyncio
import os
import websockets

SERVER_URL = os.environ.get("SERVER_URL", "ws://localhost:8000")
# AUTH_TOKEN = os.environ["AUTH_TOKEN"]
AUTH_TOKEN = "ASDFASDF"


def on_message(text: str):
    """Handle incoming text from the phone. Replace with your app logic."""
    print(f"Received: {text}")


async def connect():
    uri = f"{SERVER_URL}/ws?token={AUTH_TOKEN}"
    delay = 1

    while True:
        try:
            async with websockets.connect(uri) as ws:
                print("Connected to server.")
                delay = 1
                async for message in ws:
                    on_message(message)
        except (websockets.ConnectionClosed, OSError) as e:
            print(f"Disconnected: {e}. Reconnecting in {delay}s...")
            await asyncio.sleep(delay)
            delay = min(delay * 2, 60)


if __name__ == "__main__":
    asyncio.run(connect())
