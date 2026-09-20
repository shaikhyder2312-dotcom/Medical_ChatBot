# Medical ChatBot

An AI-powered medical question-answering application using **Retrieval-Augmented Generation (RAG)**, **Llama 3**, **Ollama**, and **Pinecone** to provide responses from a medical knowledge base.

![Medical ChatBot](screenshots/Medical1.png)

## Overview

Medical ChatBot is a web-based AI application that allows users to ask medical-related questions through a simple chat interface.

The application uses a **RAG pipeline** to retrieve relevant information from a medical knowledge base before generating a response with the **Llama 3** language model.

The backend is built with **Python and Flask**, while the application is containerized using **Docker** and deployed using **Azure Virtual Machine, Azure Container Registry, and Nginx**.

## Features

* Medical question answering
* Retrieval-Augmented Generation (RAG)
* Semantic search using vector embeddings
* Pinecone vector database
* Llama 3 integration through Ollama
* Context-aware follow-up questions
* Medical scope control
* Emergency query detection
* Chat reset functionality
* Flask REST endpoints
* Docker containerization
* Azure cloud deployment
* Nginx reverse proxy
* GitHub Actions CI/CD

## Tech Stack

### Programming & Frameworks

* Python
* Flask
* HTML
* CSS
* JavaScript

### AI / ML

* Llama 3
* Ollama
* LangChain
* Sentence Transformers
* Hugging Face Transformers
* PyTorch

### Database

* Pinecone Vector Database

### Cloud & DevOps

* Microsoft Azure
* Azure Virtual Machine
* Azure Container Registry (ACR)
* Docker
* Nginx
* GitHub Actions
* Git

## RAG Architecture

```text
User Question
      │
      ▼
Question Processing
      │
      ▼
Generate Embedding
      │
      ▼
Pinecone Vector Search
      │
      ▼
Relevant Medical Context
      │
      ▼
Llama 3 + Retrieved Context
      │
      ▼
Generated Response
      │
      ▼
User
```

## How It Works

1. The user enters a medical question.
2. Flask receives the request.
3. The question is processed by the RAG pipeline.
4. The question is converted into an embedding.
5. Pinecone searches for relevant medical information.
6. Relevant context is retrieved from the vector database.
7. The retrieved context is provided to Llama 3.
8. Llama 3 generates the response.
9. The response is returned to the user.

## Requirements

* Python 3.10+
* Git
* Ollama
* Llama 3
* Pinecone account
* Pinecone API key
* Docker *(optional for local execution)*

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shaikhyder2312-dotcom/Medical_ChatBot.git
cd Medical_ChatBot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Run Ollama

Install Ollama and download Llama 3:

```bash
ollama pull llama3
```

Verify:

```bash
ollama list
```

### 5. Configure Environment Variables

Create a `.env` file:

```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_pinecone_index
FLASK_SECRET_KEY=your_secret_key
OLLAMA_MODEL=llama3
OLLAMA_BASE_URL=http://localhost:11434
```

> Never commit API keys or secrets to GitHub.

### 6. Run the Application

```bash
python app.py
```

Open:

```text
http://localhost:8080
```

## Screenshots

### Chatbot Interface

![Chatbot Interface](screenshots/Medical1.png)

### Medical Question and Response

![Question and Response](screenshots/Medical2.png)

## Technical Implementation

### Flask

Flask is used as the backend framework to handle:

* Chat requests
* User sessions
* Health checks
* Chat reset
* Communication with the RAG pipeline

### LangChain

LangChain connects the retrieval system, vector database, prompt, and language model.

```text
User Query
    ↓
Retriever
    ↓
Relevant Context
    ↓
Prompt
    ↓
Llama 3
    ↓
Response
```

### Pinecone

Pinecone is used as the vector database for storing and retrieving embeddings from the medical knowledge base.

The application performs similarity search to retrieve relevant information for the user's question.

### Sentence Transformers

Sentence Transformers are used to generate embeddings for semantic search.

The embeddings allow the application to compare the semantic meaning of the user query with stored medical information.

### Ollama & Llama 3

Ollama provides the local runtime for Llama 3.

The retrieved medical context is provided to Llama 3 along with the user's question to generate the final response.

## API Endpoints

### Home

```text
GET /
```

Loads the chatbot interface.

### Chat

```text
POST /get
```

Processes the user's question and returns the generated response.

### Health Check

```text
GET /health
```

Checks whether the application is running.

### Reset

```text
POST /reset
```

Clears the current chat context.

## Project Structure

```text
Medical_ChatBot/
│
├── .github/
│   └── workflows/
│
├── data/
├── medicalbot/
├── research/
├── src/
│   ├── helper.py
│   └── prompt.py
├── static/
├── templates/
├── screenshots/
│   ├── chatbot-interface.png
│   ├── question-response.png
│   └── deployment.png
├── app.py
├── Dockerfile
├── requirements.txt
├── setup.py
├── .dockerignore
├── .gitignore
├── LICENSE
└── README.md
```

## Docker

The application is containerized using Docker.

### Build Image

```bash
docker build -t medicalbot:local .
```

### Run Container

```bash
docker run -p 8080:8080 --env-file .env medicalbot:local
```

Check the container:

```bash
docker ps
```

View logs:

```bash
docker logs <container_name>
```

## Azure Deployment

The application was deployed using:

* Azure Container Registry
* Azure Virtual Machine
* Docker
* Nginx
* GitHub Actions

### Deployment Architecture

```text
GitHub Repository
       │
       ▼
GitHub Actions
       │
       ▼
Docker Build
       │
       ▼
Azure Container Registry
       │
       ▼
Azure Virtual Machine
       │
       ▼
Docker Container
       │
       ▼
Flask Application
       │
       ▼
Nginx
       │
       ▼
User
```

## Azure Container Registry

Azure Container Registry (ACR) was used to store the Docker image.

```text
Docker Build
     ↓
Docker Image
     ↓
Push to ACR
     ↓
Azure VM
     ↓
Pull Image
     ↓
Run Container
```

## Azure Virtual Machine

An Azure Linux Virtual Machine was used to host the application.

The VM runs:

* Docker
* Flask application
* Nginx
* Supporting deployment components

## Nginx Reverse Proxy

Nginx is used as a reverse proxy in front of the Flask application.

```text
Internet
    │
    ▼
Nginx :80
    │
    ▼
Docker :8080
    │
    ▼
Flask Application
```

Example configuration:

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## CI/CD Pipeline

GitHub Actions was used to automate the Docker build and deployment workflow.

```text
Git Push
   ↓
GitHub Actions
   ↓
Build Docker Image
   ↓
Push Image to ACR
   ↓
Connect to Azure VM
   ↓
Pull Latest Image
   ↓
Run Docker Container
```


## Troubleshooting

### Ollama

Check whether Llama 3 is installed:

```bash
ollama list
```

Install it if required:

```bash
ollama pull llama3
```

### Pinecone

Verify:

```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_pinecone_index
```

### Docker

Check containers:

```bash
docker ps -a
```

View logs:

```bash
docker logs <container_name>
```

### Nginx

Test the configuration:

```bash
sudo nginx -t
```

Restart Nginx:

```bash
sudo systemctl restart nginx
```

## Limitations

* The chatbot is intended for informational purposes only.
* It should not replace professional medical advice.
* Generated responses may contain incorrect or incomplete information.
* Response quality depends on the medical knowledge base.
* Emergency situations should be handled by qualified medical professionals.

## Future Enhancements

* Add source citations to responses
* Improve retrieval and ranking
* Add conversation history
* Add document upload functionality
* Add authentication
* Improve RAG evaluation
* Add application monitoring
* Add HTTPS using Nginx
* Add automated security scanning
* Improve CI/CD automation

## Security

* Store API keys using environment variables.
* Never commit `.env` files.
* Use GitHub Secrets for CI/CD credentials.
* Restrict Azure VM network access.
* Use HTTPS for production.
* Keep Docker images and dependencies updated.

## License

This project is licensed under the **Apache License 2.0**.

See the [LICENSE](LICENSE) file for more information.

## Author

**Shaik Hyder Ali**

GitHub:
https://github.com/shaikhyder2312-dotcom
