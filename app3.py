from flask import Flask, request, render_template, session
from dremio_simple_query.connect import DremioConnection
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
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
chat_model = ChatOpenAI(model_name="gpt-4o", openai_api_key=OPENAI_API_KEY)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Tool 1: Get Customer List
def get_customer_list(_input=None):
    print("Fetching full customer list")
    query = """SELECT DISTINCT id, customer FROM "@alex.merced@dremio.com"."ai_agent_views"."customer_lookup";"""
    df = dremio.toPandas(query)
    if not df.empty:
        
        return f"""CUSTOMER LIST
    {df.to_string(index=True)}
    """
    return "No customers found."

get_customer_list_tool = Tool(
    name="get_customer_list",
    func=get_customer_list,
    description="Retrieves a list of all customer names and ids from the database."
)

# # Tool 2: Get Customer ID
# def get_customer_id(customer_name: str):
#     print(f"Fetching customer ID for {customer_name}")
#     query = f"""
#     SELECT id FROM "@alex.merced@dremio.com"."ai_agent_views"."customer_lookup" 
#     WHERE LOWER(customer) LIKE '{customer_name.lower()}%';
#     """
#     df = dremio.toPandas(query)
#     if not df.empty:
#         customer_id = df.iloc[0]['id']
#         print(f"Customer ID found: {customer_id}")
#         return str(customer_id)
#     return "Customer not found."

# get_customer_id_tool = Tool(
#     name="get_customer_id",
#     func=get_customer_id,
#     description="Retrieves a customer ID from the database given a customer name."
# )

# Tool 3: Get Customer Data
def get_customer_data(customer_id: str):
    print(f"Fetching data for customer ID {customer_id}")
    query = f"""
    SELECT * FROM "@alex.merced@dremio.com"."ai_agent_views"."refined_opps" 
    WHERE company_id = '{customer_id}';
    """
    df = dremio.toPandas(query)
    if not df.empty:
        print("Customer data retrieved.")
        return df.to_string(index=False)
    return "No data found for this customer."

get_customer_data_tool = Tool(
    name="get_customer_data",
    func=get_customer_data,
    description="Retrieves customer-specific data given a customer ID."
)

# Initialize AI Agent with tools
tools = [get_customer_list_tool, get_customer_data_tool]
agent = initialize_agent(
    tools, 
    chat_model, 
    agent="chat-conversational-react-description", 
    memory=memory, 
    verbose=True
)

@app.route("/", methods=["GET", "POST"])
def index():
    response = None

    # Clear session on refresh
    if request.method == "GET":
        session.clear()

    if request.method == "POST":
        user_prompt = f"""
        You are a cheerful assistant for a sales agent looking to help understand existing deals. In the agents question they may mispell the customers name, so to make sure to pull the right data:
        
        1. Get the customer list and look for a customers name that approximately matches the customers name from the question.
        2. Get the customer id
        3. Get the customer data using the customer id
        
        4. Then answer the customers question cheerfully, the question is below:
        
        {request.form["question"]}
        """

        # Ensure chat history is passed to the agent
        agent_inputs = {
            "chat_history": memory.load_memory_variables({})["chat_history"],  # Load past messages
            "input": user_prompt
        }

        # Let the AI agent decide if it needs to call a tool
        response = agent.run(agent_inputs)

        # Store chat history
        if "chat_history" not in session:
            session["chat_history"] = []
        session["chat_history"].append({"question": user_prompt, "answer": response})

    return render_template("index3.html", chat_history=session.get("chat_history", []), response=response)

if __name__ == "__main__":
    app.run(debug=True)


