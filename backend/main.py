import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, status
from fastapi.websockets import WebSocketState

app = FastAPI()

# AUTH_TOKEN = os.environ["AUTH_TOKEN"]
AUTH_TOKEN = "ASDFASDF"
connected_desktop: WebSocket | None = None


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.post("/send")
async def send_text(body: dict):
    """Phone app calls this to forward text to the desktop."""
    token = body.get("token")
    if token != AUTH_TOKEN:
        return {"error": "unauthorized"}, 401

    text = body.get("text", "")
    if connected_desktop and connected_desktop.client_state == WebSocketState.CONNECTED:
        await connected_desktop.send_text(text)
        return {"status": "delivered"}
    return {"status": "desktop_not_connected"}


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(default=""),
):
    if token != AUTH_TOKEN:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    global connected_desktop
    await websocket.accept()
    connected_desktop = websocket

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_desktop = None
