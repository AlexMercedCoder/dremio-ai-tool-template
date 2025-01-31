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

# Function 1: Get customer ID based on the entered name
def get_customer_id(customer_name):
    print("getting customer id")
    query = f"""
    SELECT * FROM "@alex.merced@dremio.com"."ai_agent_views"."customer_lookup" WHERE LOWER(customer) LIKE '{customer_name.lower()}%';
    """
    df = dremio.toPandas(query)
    
    if not df.empty:
        print("got customer id")
        return df.iloc[0]['id']
    return None

# Function 2: Get customer-specific data using the customer ID
def get_customer_data(customer_id):
    print("getting customer data")
    query = f"""
    SELECT * FROM "@alex.merced@dremio.com"."ai_agent_views"."refined_opps" where company_id = '{customer_id}';
    """
    
    df = dremio.toPandas(query)

    if not df.empty:
        print("got customer data")
        return df.to_string(index=False)  # Convert DataFrame to readable text
    return "No data found for this customer."

@app.route("/", methods=["GET", "POST"])
def index():
    response = None

    # Clear session on page refresh
    if request.method == "GET":
        session.clear()

    if request.method == "POST":
        customer_name = request.form["customer"]
        user_question = request.form["question"]

        # Step 1: Get customer ID
        customer_id = get_customer_id(customer_name)
        if not customer_id:
            response = f"Customer '{customer_name}' not found."
        else:
            # Step 2: Get customer data
            customer_data = get_customer_data(customer_id)

            # Step 3: Inject data and question into prompt
            prompt = f"""
            Customer Name: {customer_name}
            Customer ID: {customer_id}
            Customer Data:
            {customer_data}

            User's Question: {user_question}
            """

            # Generate AI response
            messages = [SystemMessage(content="You are an AI assistant answering customer inquiries."), HumanMessage(content=prompt)]
            response = chat_model.invoke(messages).content
            print(response)

            # Store chat history
            if "chat_history" not in session:
                session["chat_history"] = []
            session["chat_history"].append({"customer": customer_name, "question": user_question, "answer": response})

    return render_template("index2.html", chat_history=session.get("chat_history", []), response=response)

if __name__ == "__main__":
    app.run(debug=True)
