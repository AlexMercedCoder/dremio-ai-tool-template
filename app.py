from flask import Flask, request, render_template, session
from dremio_simple_query.connect import DremioConnection
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import os

# Load environment variables
load_dotenv()

# Flask setup with session handling
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Dremio connection setup
TOKEN = os.getenv("DREMIO_TOKEN")
ARROW_ENDPOINT = os.getenv("DREMIO_ARROW_ENDPOINT")
dremio = DremioConnection(TOKEN, ARROW_ENDPOINT)

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize LangChain chat model and memory
chat_model = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)
memory = ConversationBufferMemory(return_messages=True)

# Function to fetch and inject data from Dremio (only on the first question)
def fetch_dremio_data():
    print("Fetching full query results from Dremio")
    query = os.getenv("QUERY")
    df = dremio.toPandas(query)

    # Convert entire DataFrame to a string for the prompt
    full_data = df.to_string(index=False)
    
    return full_data

@app.route("/", methods=["GET", "POST"])
def index():
    response = None

    # Clear session on page refresh (GET request)
    if request.method == "GET":
        session.clear()

    # Initialize chat history if not already in session
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        print("Processing user question")
        user_question = request.form["question"]
        
        # Fetch data from Dremio only on the first request
        if not session.get("context_loaded", False):
            dremio_data = fetch_dremio_data()
            print("Dremio data injected into context")

            # Store full query result in memory
            memory.save_context({"input": "Dremio Data Context"}, {"output": dremio_data})
            session["context_loaded"] = True  # Mark context as loaded

        # Load conversation history
        messages = memory.load_memory_variables({})["history"]

        # Inject Dremio data as part of the prompt
        messages.append(SystemMessage(content="Here is relevant data from Dremio:\n" + memory.load_memory_variables({})["history"][-1].content))
        messages.append(HumanMessage(content=user_question))

        # Generate AI response
        response = chat_model.invoke(messages)

        # Save the new conversation exchange
        memory.save_context({"input": user_question}, {"output": response.content})
        session["chat_history"].append({"question": user_question, "answer": response.content})

    return render_template("index.html", chat_history=session["chat_history"], response=response)

if __name__ == "__main__":
    app.run(debug=True)

