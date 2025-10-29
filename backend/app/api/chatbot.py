from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.services.chatbot_service import ChatbotService

router = APIRouter()
chatbot_service = ChatbotService()

@router.post("/chatbot/message")
async def send_message(request: Dict[str, Any]):
    """Send a message to the chatbot"""
    try:
        user_message = request.get("message", "")
        page_context = request.get("context", {})
        
        if not user_message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        response = await chatbot_service.chat_response(user_message, page_context)
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

@router.post("/chatbot/clear")
async def clear_conversation():
    """Clear chatbot conversation memory"""
    try:
        chatbot_service.clear_memory()
        return {"message": "Conversation memory cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear memory: {str(e)}")

@router.get("/chatbot/health")
async def chatbot_health():
    """Check chatbot health"""
    return {"status": "healthy", "message": "Chatbot service is running"}