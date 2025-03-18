from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from app.agents.classifier import ClassifierAgent
import asyncio
from functools import partial

load_dotenv()

app = Flask(__name__)
classifier = ClassifierAgent()

def to_async(func):
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    return wrapper

@app.route('/classify', methods=['POST'])
async def classify():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "Please provide a message in the request body"}), 400
    
    message = data['message']
    result = await classifier.classify(message)
    return jsonify({"classification": result})

if __name__ == '__main__':
    # Run with ASGI server
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)