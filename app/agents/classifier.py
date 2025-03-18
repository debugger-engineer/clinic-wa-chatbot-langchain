from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import os

# Define the output schema
response_schemas = [
    ResponseSchema(
        name="flow",
        description="The flow classification result",
        type="string",
        enum=["FLOW = TEMPLATE INTRODUCTION", "FLOW = BOT"]
    )
]

class ClassifierAgent:
    def __init__(self):
        # Initialize the language model
        self.llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-3.5-turbo",
            temperature=0
        )
        
        # Create output parser
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """STRICT OUTPUT PROTOCOL

Your role is to analyze user input and respond ONLY with one of these two exact outputs:
1. FLOW = TEMPLATE INTRODUCTION
2. FLOW = BOT

Output Rules:
- Only these two responses are allowed
- No additional text, explanations, or messages
- No variations in formatting
- No greetings or closings

FLOW = TEMPLATE INTRODUCTION triggers when:
- Message contains greetings: "oi", "olá", "bom dia", etc.
- Including variations with typos or different cases
- Only at conversation start or after 15+ minutes inactivity

FLOW = BOT triggers when:
- Questions about treatments (Caminho de Volta, FPF, Naturaleza, Studio services)
- Price inquiries
- Treatment care questions
- Any message not matching greeting criteria

{format_instructions}"""),
            ("human", "{input}")
        ])
        
    async def classify(self, message: str) -> str:
        """Classify the input message using LangChain's structured output"""
        # Format the prompt with parser instructions
        prompt_with_output = self.prompt.format_messages(
            format_instructions=self.output_parser.get_format_instructions(),
            input=message
        )
        
        # Get response from LLM
        response = await self.llm.ainvoke(prompt_with_output)
        
        # Parse the structured output
        parsed_response = self.output_parser.parse(response.content)
        
        return parsed_response["flow"] 