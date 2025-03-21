from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from app.chains.conversation import ConversationChain
import asyncio
from functools import partial

load_dotenv()

app = Flask(__name__)
conversation_chain = ConversationChain()

def to_async(func):
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapper

@app.route('/webhook', methods=['POST'])
async def webhook():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        # Extract message data
        message = data['body']['data']['message'].get('conversation', '')
        user_id = data['body']['data']['key']['remoteJid']
        user_name = data['body']['data']['pushName']
        
        # Process message through conversation chain
        response = await conversation_chain.process_message(
            message=message,
            user_id=user_id,
            user_name=user_name
        )
        
        return jsonify({
            "status": "success",
            "response": response,
            "user_id": user_id
        })
        
    except KeyError as e:
        return jsonify({
            "error": "Invalid request format",
            "details": f"Missing field: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

@app.route('/clear-memory', methods=['POST'])
def clear_memory():
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({"error": "Please provide a user_id in the request body"}), 400
    
    user_id = data['user_id']
    conversation_chain.clear_user_memory(user_id)
    return jsonify({"status": "success", "message": f"Memory cleared for user {user_id}"})

if __name__ == '__main__':
    # Run with ASGI server
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)