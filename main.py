import os
import asyncio
import traceback
import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

app = FastAPI(title="IELTS Speaking Practice Backend")

# Enable CORS so the React app can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.get("/api/health")
async def health_check():
    key_configured = bool(GEMINI_API_KEY and GEMINI_API_KEY.strip())
    return {
        "status": "healthy",
        "gemini_api_key_configured": key_configured
    }

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # 1. Check API Key
    api_key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
    if not api_key or not api_key.strip():
        await websocket.send_json({
            "error": "GEMINI_API_KEY is not set in the backend .env file. Please add it to d:\\Games\\ielts_speaking\\.env"
        })
        await websocket.close(code=4001)
        return
        
    # 2. Connect to Google Gemini Live API
    # The Live API is hosted on the v1beta endpoint
    uri = f"wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent?key={api_key.strip()}"
    
    print("Connecting proxy to Gemini Live API...")
    try:
        async with websockets.connect(uri) as gemini_ws:
            print("Successfully connected to Gemini. Starting bidirection tunnel...")
            
            # Browser to Gemini tunnel
            async def browser_to_gemini():
                try:
                    while True:
                        # Receive frame from client browser (text/json)
                        data = await websocket.receive_text()
                        # Forward immediately to Google's WebSocket
                        await gemini_ws.send(data)
                except WebSocketDisconnect:
                    print("Browser client disconnected websocket.")
                except Exception as e:
                    print(f"Error forwarding Browser -> Gemini: {e}")
            
            # Gemini to Browser tunnel
            async def gemini_to_browser():
                try:
                    async for message in gemini_ws:
                        # Forward text or binary message from Gemini to browser
                        if isinstance(message, bytes):
                            await websocket.send_bytes(message)
                        else:
                            await websocket.send_text(message)
                except Exception as e:
                    print(f"Error forwarding Gemini -> Browser: {e}")
                    
            # Run both tunnels concurrently and stop as soon as either side closes or errors
            done, pending = await asyncio.wait(
                [
                    asyncio.create_task(browser_to_gemini()),
                    asyncio.create_task(gemini_to_browser())
                ],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel the remaining tasks immediately
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            
    except Exception as e:
        print(f"Proxy websocket connection error: {e}")
        traceback.print_exc()
        try:
            await websocket.send_json({"error": f"Failed to connect or maintain connection to Gemini Live: {str(e)}"})
        except:
            pass
    finally:
        print("Closing client websocket...")
        try:
            await websocket.close()
        except Exception:
            pass
