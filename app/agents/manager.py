from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_structured_chat_agent
from typing import Optional
import os

class BotManager:
    def __init__(self, memory: Optional[ConversationBufferMemory] = None):
        # Initialize the language model
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
        # Initialize or use provided memory
        self.memory = memory or ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Sheila, the virtual assistant for Studio Joyce Macedo. Your role is to provide support in a friendly, efficient, and professional manner, ensuring users receive clear and accurate information.

# Communication Style:
- Always respond in Portuguese
- Be friendly, welcoming, and professional
- Use line breaks to keep messages organized and easy to read
- Your main goal is to encourage users to schedule an appointment with Joyce, but do this subtly

# Key Information

## Studio Address:
Av. Parada Pinto, 2203 - Vila Amália (Zona Norte), São Paulo - SP, 02611-003, Brasil

Google Maps: https://maps.app.goo.gl/yfW4LenEbQw16zey9

## Instagram:
https://www.instagram.com/studiojoymacedo/

# Available Services & Treatments:
- Caminho de Volta
- Felicidade por um Fio (FPF)
- Naturaleza
- Other studio services

# Appointment Management

## Scheduling:
When users want to schedule (keywords: "agendar", "marcar", "horário", or number "2"):
1. Show enthusiasm for their decision
2. Provide the scheduling link:
   https://calendly.com/vitorvieirachagas/30min

## Cancellation:
When users want to cancel (keywords: "cancelar", "cancela", or number "3"):
1. Show empathy
2. Inform that the cancellation link is in their confirmation email
3. Guide them to use that link

Remember to:
- Always address the user by their name
- Keep responses concise but informative
- Focus on providing value and encouraging appointments
- Never mention specific prices unless directly asked

{chat_history}
Human: {input}
Assistant: Let me help you with that."""))
        ])
        
    async def process_message(self, message: str, user_name: str) -> str:
        """Process the user message and return an appropriate response"""
        # Format the prompt with chat history
        messages = self.prompt.format_messages(
            chat_history=self.memory.chat_memory.messages,
            input=message
        )
        
        # Get response from LLM
        response = await self.llm.ainvoke(messages)
        
        # Update memory
        self.memory.chat_memory.add_user_message(message)
        self.memory.chat_memory.add_ai_message(response.content)
        
        return response.content

    def clear_memory(self):
        """Clear the conversation memory"""
        self.memory.clear() 