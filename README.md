# ollama
Ollama-Powered AI Chatbot

This is a simple AI chatbot built using LangChain and Ollama, leveraging the Llama 3 model for intelligent responses. The chatbot maintains conversation history and provides concise answers based on user queries.

Features
Uses Ollama to run a local AI model.
Maintains conversation context for better responses.
Handles errors gracefully and provides setup instructions.
Works via a simple command-line interface (CLI).

1 Install Ollama

  Download from https://ollama.com
  Open a terminal and run:
    -ollama pull llama3
    -ollama serve

2️ Install Dependencies

  -pip install langchain langchain-community

3️ Run the Chatbot

  -python chatbot.py


 How It Works
• Initializes Llama3 using LangChain's Ollama integration

• Uses a structured prompt to improve response quality

• Maintains conversation history for better AI understanding

• Runs in an interactive loop, allowing users to chat continuously
