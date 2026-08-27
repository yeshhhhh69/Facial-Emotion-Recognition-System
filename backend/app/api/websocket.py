"""
WebSocket endpoint for real-time emotion detection.
"""

import json
import base64
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import cv2
import numpy as np

from app.core.emotion_detector import get_detector

router = APIRouter(tags=["websocket"])

class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept and store new connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Remove connection."""
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific client."""
        await websocket.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/predict")
async def websocket_predict(websocket: WebSocket):
    """
    WebSocket endpoint for real-time emotion prediction.
    
    Client sends base64 encoded images, server responds with predictions.
    """
    await manager.connect(websocket)
    
    try:
        # Get detector
        detector = get_detector()
        
        while True:
            # Receive data from client
            data = await websocket.receive_text()
            
            try:
                # Parse JSON
                message = json.loads(data)
                
                if 'image' not in message:
                    await manager.send_personal_message({
                        'success': False,
                        'error': 'No image provided'
                    }, websocket)
                    continue
                
                # Decode base64 image
                base64_str = message['image']
                
                # Remove data URL prefix if present
                if ',' in base64_str:
                    base64_str = base64_str.split(',')[1]
                
                # Decode base64
                image_bytes = base64.b64decode(base64_str)
                nparr = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if image is None:
                    await manager.send_personal_message({
                        'success': False,
                        'error': 'Failed to decode image'
                    }, websocket)
                    continue
                
                # Detect and predict
                predictions = detector.detect_and_predict(image)
                
                # Send response
                await manager.send_personal_message({
                    'success': True,
                    'num_faces': len(predictions),
                    'predictions': predictions,
                    'timestamp': message.get('timestamp')
                }, websocket)
            
            except json.JSONDecodeError:
                await manager.send_personal_message({
                    'success': False,
                    'error': 'Invalid JSON'
                }, websocket)
            
            except Exception as e:
                await manager.send_personal_message({
                    'success': False,
                    'error': f'Prediction failed: {str(e)}'
                }, websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
