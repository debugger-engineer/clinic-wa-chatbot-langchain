from langchain.memory import ConversationBufferMemory as LangChainBufferMemory
from typing import List, Dict, Any
import time

class ConversationBufferMemory(LangChainBufferMemory):
    def __init__(self, memory_key: str = "chat_history", return_messages: bool = True, timeout: int = 900):
        """Initialize the conversation buffer memory
        
        Args:
            memory_key: The key to store/retrieve memory
            return_messages: Whether to return memory as a list of messages
            timeout: Conversation timeout in seconds (default 15 minutes)
        """
        super().__init__(memory_key=memory_key, return_messages=return_messages)
        self.last_interaction = time.time()
        self.timeout = timeout
        
    def add_user_message(self, message: str) -> None:
        """Add a user message to memory and update last interaction time"""
        super().add_user_message(message)
        self.last_interaction = time.time()
        
    def add_ai_message(self, message: str) -> None:
        """Add an AI message to memory and update last interaction time"""
        super().add_ai_message(message)
        self.last_interaction = time.time()
        
    def is_expired(self) -> bool:
        """Check if the conversation has timed out"""
        return (time.time() - self.last_interaction) > self.timeout
        
    def get_memory_variables(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Get memory variables, checking for timeout first"""
        if self.is_expired():
            self.clear()
        return super().get_memory_variables(*args, **kwargs)
        
    def clear(self) -> None:
        """Clear the memory and reset last interaction time"""
        super().clear()
        self.last_interaction = time.time()

class ConversationBuffer:
    def __init__(self):
        self.conversations: Dict[str, ConversationBufferMemory] = {}
        
    def get_memory(self, conversation_id: str) -> ConversationBufferMemory:
        """Get or create a conversation memory for a specific chat"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
        return self.conversations[conversation_id]
        
    def clear_memory(self, conversation_id: str):
        """Clear the memory for a specific conversation"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
        
    def save_memory(self, conversation_id: str, memory: ConversationBufferMemory):
        """Save conversation memory to Redis"""
        # TODO: Implement memory serialization and storage
        pass
        
    def load_memory(self, conversation_id: str) -> ConversationBufferMemory:
        """Load conversation memory from Redis"""
        # TODO: Implement memory deserialization and loading
        return self.get_memory(conversation_id) 