# 🤖 AIGenesis

A comprehensive collection of AI agents built with Python and Google Gemini API, featuring conversational agents, guardrails, RAG (Retrieval-Augmented Generation), and multi-agent systems.

## 🌟 Features

### 1. **Simple Conversational Agent**
- Natural conversation with memory
- Conversation history tracking
- Save conversations to file
- Session statistics

### 2. **Guardrail Agent**
- Input/output validation
- Content safety checks
- Length limits
- Blocked topics filtering

### 3. **Custom Agent Builder**
- Create agents with custom roles
- Add custom tools and functions
- Flexible instruction system
- Tool execution framework

### 4. **RAG Agent (Basic)**
- Simple keyword-based retrieval
- Knowledge base management
- Context-aware responses

### 5. **Advanced RAG Agent**
- Document chunking and processing
- Enhanced similarity search
- Confidence scoring
- Load documents from files
- Keyword search in knowledge base

### 6. **Multi-Agent System**
- Multiple specialized agents (CodeMaster, DataWizard, SecurityGuard, etc.)
- Intelligent query routing
- Role-based expertise
- Automatic agent selection

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API key (free at https://aistudio.google.com/)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd AIGenesis
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Key
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Run the Application
```bash
python main_menu.py
```

Or run individual agents:
```bash
# Simple agent
python enhanced_simple_agent.py

# Guardrail agent
python agent_with_guardrails.py

# Multi-agent system
python multi_agent_system.py

# Advanced RAG
python advanced_rag_agent.py
```

## 📁 Project Structure

```
AIGenesis/
├── main_menu.py                 # Main application with menu
├── simple_agent.py              # Basic conversational agent
├── enhanced_simple_agent.py     # Enhanced agent with features
├── agent_with_guardrails.py     # Agent with safety checks
├── agent_builder.py             # Custom agent builder
├── rag_agent.py                 # Basic RAG implementation
├── advanced_rag_agent.py        # Advanced RAG with features
├── multi_agent_system.py        # Multi-agent system
├── requirements.txt             # Python dependencies
├── .env                         # API keys (create this)
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

## 💡 Usage Examples

### Simple Agent
```python
from simple_agent import SimpleAgent

agent = SimpleAgent()
response = agent.send_message("What is Python?")
print(response)
```

### Guardrail Agent
```python
from agent_with_guardrails import GuardrailAgent

agent = GuardrailAgent()
response = agent.process("Tell me about AI")
print(response)
```

### RAG Agent
```python
from advanced_rag_agent import AdvancedRAGAgent

agent = AdvancedRAGAgent()
agent.add_document("Python is a programming language.")
result = agent.answer_question("What is Python?")
print(result['answer'])
```

### Multi-Agent System
```python
from multi_agent_system import MultiAgentSystem, SpecializedAgent

system = MultiAgentSystem()
system.add_agent(SpecializedAgent(
    name="CodeHelper",
    role="Software Engineer",
    expertise="Python, debugging, best practices"
))

result = system.process_query("How do I optimize Python code?")
print(result['response'])
```

### Custom Agent with Tools
```python
from agent_builder import AgentBuilder, Tool

def get_weather():
    return "Sunny, 25°C"

agent = AgentBuilder(
    role="Weather Assistant",
    instructions="Provide weather information"
)

agent.add_tool(Tool(
    name="get_weather",
    description="Get current weather",
    function=get_weather
))

response = agent.chat("What's the weather?")
print(response)
```

## 🛠️ Available Commands

Most agents support these interactive commands:

- `exit` or `quit` - Exit the agent
- `clear` - Clear conversation history (where applicable)
- `stats` - Show statistics (where applicable)
- `save` - Save conversation to file (where applicable)
- `help` - Show help message (where applicable)

## 🔧 Configuration

### Guardrail Agent Configuration
Edit `agent_with_guardrails.py`:
```python
self.blocked_topics = ['violence', 'harmful', 'illegal']
self.max_tokens = 1000
```

### RAG Agent Configuration
Edit `advanced_rag_agent.py`:
```python
# Adjust chunk size for document processing
agent.add_documents_from_text(text, chunk_size=500)

# Adjust number of retrieved documents
result = agent.answer_question(query, top_k=3)
```

## 📊 API Usage Limits

**Google Gemini Free Tier:**
- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per minute

## 🎯 Use Cases

1. **Chatbots** - Build conversational assistants
2. **Documentation Q&A** - Answer questions from documents
3. **Code Assistance** - Get help with programming
4. **Multi-domain Support** - Route queries to specialized agents
5. **Safe AI** - Implement content filtering and validation
6. **Knowledge Management** - Build custom knowledge bases

## 🔐 Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Use environment variables** - Don't hardcode API keys
3. **Validate user input** - Use guardrails
4. **Limit response length** - Prevent abuse
5. **Monitor usage** - Track API calls

## 🐛 Troubleshooting

### API Key Issues
```bash
# Check if .env file exists
ls -la .env

# Verify API key is set
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Rate Limit Errors
- Wait a minute between requests
- Reduce request frequency
- Consider upgrading to paid tier

## 🚀 Advanced Features

### Creating Custom Agents

```python
from agent_builder import AgentBuilder, Tool

# Define custom tools
def search_database(query):
    # Your database search logic
    return "Search results..."

# Create specialized agent
agent = AgentBuilder(
    role="Database Expert",
    instructions="Help users query and understand database operations"
)

agent.add_tool(Tool(
    name="search",
    description="Search the database",
    function=search_database
))
```

### Loading Documents for RAG

```python
agent = AdvancedRAGAgent()

# From text
agent.add_documents_from_text(large_text, chunk_size=500)

# From file
agent.load_from_file("knowledge.txt")

# Direct addition
agent.add_document("Important information here")
```

## 📈 Future Enhancements

- [ ] Vector embeddings for better retrieval
- [ ] Function calling with Gemini
- [ ] Streaming responses
- [ ] Agent memory persistence
- [ ] Web search integration
- [ ] Image understanding
- [ ] Multi-modal agents
- [ ] Agent collaboration framework

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Google Gemini API for powering the agents
- Python community for excellent libraries
- Open source contributors

## 📞 Support

- Create an issue on GitHub
- Check existing issues for solutions
- Review Google Gemini documentation

## 🔗 Resources

- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Python Documentation](https://docs.python.org/)
- [RAG Overview](https://www.promptingguide.ai/techniques/rag)

---

**Made with ❤️ using Google Gemini API**

*Happy Building! 🚀*