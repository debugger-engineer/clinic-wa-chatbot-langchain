# WhatsApp AI Assistant with LangChain

A LangChain-powered WhatsApp chatbot that replicates n8n workflow functionality using pure Python. Built with modern AI components for intelligent conversation management and appointment scheduling.

## Overview

This project reimplements a complex n8n workflow as a Python application, leveraging LangChain's powerful components to create a flexible and maintainable chatbot system. The bot uses AI agents and memory systems to provide intelligent responses and manage appointments.

## Key Features

- 🤖 **AI Agents**
  - Message classification using LangChain agents
  - Structured output parsing for reliable flow control
  - Conversation management with context awareness

- 🧠 **Memory System**
  - LangChain Buffer Memory for conversation history
  - Efficient in-memory state management
  - Conversation timeout handling

- 🔄 **Flow Management**
  - Dynamic flow routing based on message classification
  - Structured conversation flows
  - Error handling and recovery

## Project Structure
```
project_root/
├── app/
│   ├── __init__.py
│   ├── agents/
│   │   ├── classifier.py     # Message classification
│   │   └── bot.py           # Main conversation agent
│   ├── memory/
│   │   └── buffer.py        # Conversation memory
│   ├── chains/
│   │   └── conversation.py  # Conversation chains
│   └── config/
│       ├── settings.py      # Application settings
│       └── prompts.py       # Prompt templates
├── tests/
├── .env
└── app.py                   # Main application
```

## Current Status

The project is under active development. Currently implemented:

✅ Basic project structure  
✅ Classifier agent with structured output  
✅ Initial API endpoint  
✅ Memory system  
⏳ Main conversation agent (planned)  
⏳ Flow management (planned)

## Prerequisites

- Python 3.8+
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your actual credentials:
```bash
cp .env.example .env
# Edit .env with your preferred editor and add your OpenAI API key
```

5. Create necessary directories:
```bash
mkdir -p app/agents app/memory app/chains app/config
```

## Quick Start

1. Run the application:
```bash
python app.py
```

2. Test the classifier:
```bash
curl -X POST http://localhost:5001/classify \
-H "Content-Type: application/json" \
-d '{"message": "oi, tudo bem?"}'
```

## Development

The project follows a modular architecture based on LangChain components:

- **Agents**: Handle specific tasks like classification and conversation
- **Memory**: Manage conversation state and history
- **Chains**: Orchestrate the flow of operations

## Testing

```bash
# Run tests
pytest tests/
```

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## License

[Add License Information]

## Roadmap

1. Add conversation timeout handling
2. Implement main conversation agent
3. Add flow management system
4. Integrate WhatsApp API
5. Add appointment scheduling

## Current Limitations

- Only classifier functionality is implemented
- Basic memory management
- Limited to message classification
- No WhatsApp integration yet

For more detailed information about the development plan, see [MIGRATION_PLAN.md](MIGRATION_PLAN.md). 