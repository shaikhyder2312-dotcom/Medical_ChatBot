import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_pinecone import PineconeVectorStore

from src.helper import download_embeddings
from src.prompt import system_prompt

app = Flask(__name__)

load_dotenv()

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
if not app.config["SECRET_KEY"]:
    raise RuntimeError("FLASK_SECRET_KEY must be configured.")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise RuntimeError("PINECONE_API_KEY must be configured.")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

embeddings = download_embeddings()

index_name = os.getenv("PINECONE_INDEX_NAME", "medicalbot")

docsearch = PineconeVectorStore.from_existing_index(
    embedding=embeddings,
    index_name=index_name
)

retriever = docsearch.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.60}
)

llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "llama3"),
    temperature=0.3,
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/reset", methods=["POST"])
def reset_chat():
    session.pop("last_topic_question", None)
    return jsonify(status="chat history cleared")


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form.get("msg", "").strip()

    if not msg:
        return "Please enter a question.", 400

    greeting = msg.lower().strip("!?. ,")

    basic_responses = {
        "hi": "Hello! How can I help you today?",
        "hello": "Hello! How can I help you today?",
        "hey": "Hello! How can I help you today?",
        "how are you": "I am doing well, thank you. How can I help you today?",
        "ok":"Is there another medical question I can help with",
        "who are you": (
            "I am a medical information chatbot. I answer using the medical "
            "reference provided to me."
        ),
        "what can you do": (
            "I can answer medical questions using the medical reference "
            "provided to this bot."
        ),
        "i dont know": (
            "That is okay. Ask me a specific medical question and I will check "
            "the medical reference."
        ),
        "i don't know": (
            "That is okay. Ask me a specific medical question and I will check "
            "the medical reference."
        ),
        "thanks": "You are welcome. Is there another medical question I can help with?",
        "thank you": "You are welcome. Is there another medical question I can help with?",
    }

    if greeting in basic_responses:
        return basic_responses[greeting]
    
    emergency_phrases = (
        "severe chest pain",
        "sudden chest pain",
        "chest pain and",
        "cannot breathe",
        "can't breathe",
        "difficulty breathing",
        "severe breathing trouble",
        "face drooping",
        "slurred speech",
        "unconscious",
        "seizure",
        "overdose",
        "severe bleeding",
        "suicidal",
        "self harm",
    )

    if any(phrase in greeting for phrase in emergency_phrases):
        return (
            "Your symptoms may require urgent medical care. Please call your "
            "local emergency number or go to the nearest emergency department "
            "now. Do not rely on this chatbot for emergency assessment."
        )

    out_of_scope_phrases = (
        "capital of",
        "weather",
        "news",
        "cricket",
        "football",
        "movie",
        "song",
        "joke",
        "write code",
        "programming",
        "stock price",
        "crypto",
    )

    if any(phrase in greeting for phrase in out_of_scope_phrases):
        return (
            "I can help only with medical questions using the medical reference "
            "provided to this bot."
        )

    last_topic = session.get("last_topic_question")

    follow_up_words = {"it", "this", "that", "they", "them", "these", "those"}
    is_follow_up = last_topic and bool(
        follow_up_words.intersection(greeting.split())
    )

    if is_follow_up:
        retrieval_input = (
            f"Original medical question: {last_topic}\n"
            f"Follow-up question: {msg}"
        )
    else:
        retrieval_input = msg
        session["last_topic_question"] = msg

    response = rag_chain.invoke({"input": retrieval_input})

    print("Response:", response["answer"])
    return str(response["answer"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)