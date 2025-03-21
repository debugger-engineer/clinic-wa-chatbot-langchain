from typing import Dict, Optional
from app.agents.classifier import ClassifierAgent
from app.agents.manager import BotManager
from app.memory.buffer import ConversationBufferMemory

class ConversationChain:
    def __init__(self):
        self.classifier = ClassifierAgent()
        self.memories: Dict[str, ConversationBufferMemory] = {}
        self.bots: Dict[str, BotManager] = {}
        
    def get_or_create_bot(self, user_id: str) -> BotManager:
        """Get an existing bot instance or create a new one for the user"""
        if user_id not in self.bots:
            # Create new memory if needed
            if user_id not in self.memories:
                self.memories[user_id] = ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True
                )
            
            # Create new bot with user's memory
            self.bots[user_id] = BotManager(memory=self.memories[user_id])
            
        return self.bots[user_id]
        
    async def process_message(self, message: str, user_id: str, user_name: str) -> str:
        """Process an incoming message and return the appropriate response"""
        # First classify the message
        flow = await self.classifier.classify(message)
        
        if flow == "FLOW = BOT":
            # Get or create bot for this user
            bot = self.get_or_create_bot(user_id)
            
            # Process message with bot
            response = await bot.process_message(message, user_name)
            
            return response
            
        elif flow == "FLOW = TEMPLATE INTRODUCTION":
            # Clear any existing memory for this user
            if user_id in self.memories:
                self.memories[user_id].clear()
            if user_id in self.bots:
                del self.bots[user_id]
                
            # Return introduction template
            return f"""Olá, {user_name}! Seja bem-vindo(a) ao Studio Joyce Macedo! 👩🏼‍⚕️✨

Eu sou a Sheila, assistente virtual da Joy, e estou aqui para ajudar você no que precisar! 😊

Aqui estão algumas formas como posso te ajudar:

*Tratamentos e Dúvidas* 💆‍♀️
*Agendar Atendimento* 📅
*Cancelar Atendimento* ❌"""
        
        else:
            raise ValueError(f"Unknown flow type: {flow}")
            
    def clear_user_memory(self, user_id: str):
        """Clear the conversation memory for a specific user"""
        if user_id in self.memories:
            self.memories[user_id].clear()
        if user_id in self.bots:
            del self.bots[user_id]