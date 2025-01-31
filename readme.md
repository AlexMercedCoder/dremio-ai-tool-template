# **Dremio AI Chat**

## Getting Started

- fork/clone the repo
- cd into the repo
- create a virtual environment `python -m venv venv`
- activate the virtual environment `source venv/bin/activate`
- install the requirements `pip install -r requirements.txt`
- run the app `python app3.py`
- open your browser and go to `http://localhost:5000`

---

Comparison of `app.py/index.html`, `app2.py/index2.html`, and `app3.py/index3.html`

## **Overview**
The **Dremio AI Chat** is a Flask-based web application that integrates OpenAI's GPT-4 with real-time data retrieval from **Dremio**. It allows users to query sales opportunities dynamically. The three versions of the application—`app.py/index.html`, `app2.py/index2.html`, and `app3.py/index3.html`—differ in how they handle data retrieval, user interaction, and session management.

---

## **Comparison of `app.py`, `app2.py`, and `app3.py`**

### **1. User Input and Context Retrieval**
- **`app.py`**  
  - Users submit **a question only**.  
  - On the first request, a **predefined SQL query** fetches general data from Dremio.  
  - The retrieved data is **injected once** into the AI prompt.  
  - All subsequent responses reuse the **same dataset**.  

- **`app2.py`**  
  - Users submit **a customer name and a question**.  
  - The app first queries Dremio to **find the customer’s unique ID**.  
  - Then, it uses that ID to **retrieve customer-specific data**.  
  - The AI assistant uses this data to **generate a personalized response**.  

- **`app3.py`**  
  - Users submit **a single natural language question** without specifying a customer.  
  - The AI agent decides when to:  
    1. **Retrieve a customer list** (to verify customer name spelling).  
    2. **Find the customer ID**.  
    3. **Fetch customer-specific data** from Dremio.  
  - The AI dynamically **calls the necessary tools** to retrieve and incorporate data into its response.  
  - **Context from previous messages is preserved**, allowing for a **continuous, conversational experience**.  

---

### **2. Querying and Data Integration**
- **`app.py`**  
  - Executes **one SQL query** on the first request.  
  - Uses a **preloaded dataset** for all responses.  

- **`app2.py`**  
  - Uses a **two-step SQL query process**:  
    1. Retrieve customer ID.  
    2. Fetch data for that specific customer.  
  - Ensures responses are **tailored to a specific customer**.  

- **`app3.py`**  
  - Uses **LangChain tools** to execute **on-demand queries**.  
  - The AI agent determines **when to query** for customer names, IDs, or customer-specific data.  
  - Responses **dynamically adapt** based on retrieved data.  

---

### **3. Chat Session and Context Management**
- **`app.py`**  
  - Maintains chat history for a session.  
  - **Resets on page refresh**, requiring the first query to run again.  

- **`app2.py`**  
  - Maintains chat history during a session.  
  - Allows users to start a new conversation **by entering a new customer name**.  
  - **Resets on refresh**.  

- **`app3.py`**  
  - Maintains **a continuous chat experience**, preserving context across responses.  
  - **Chat history accumulates naturally** like a real chat app.  
  - **Resets on refresh**, but within a session, it **remembers previous exchanges**.  

---

### **4. Frontend and User Experience**
#### **`index.html` (Used with `app.py`)**
- Simple chat UI with **a single input field**.  
- The user can **only ask general questions** based on the preloaded dataset.  
- Uses **a clean aquatic UI** with a **chat history display**.  

#### **`index2.html` (Used with `app2.py`)**
- Includes **two input fields**: one for **customer name** and one for **the question**.  
- Introduces a **"Typing..." loading animation**.  
- AI responses are formatted with **`<pre>` tags** to ensure structured Dremio data is **readable**.  

#### **`index3.html` (Used with `app3.py`)**
- **Chat input remains at the bottom** (like modern messaging apps).  
- **Messages accumulate correctly** instead of replacing previous ones.  
- AI automatically determines whether it needs to fetch additional data.  
- **Auto-scrolls to the latest message** for a seamless experience.  

---

## **📊 Summary of Key Differences**

| Feature                  | `app.py` / `index.html` | `app2.py` / `index2.html` | `app3.py` / `index3.html` |
|--------------------------|------------------------|---------------------------|---------------------------|
| **User Input**           | Single question field  | Customer + question fields | Single natural language question |
| **Data Querying**        | One-time query        | Two-step query (customer lookup + data retrieval) | AI calls tools to fetch customer details as needed |
| **Response Context**     | Static dataset        | Customer-specific data per request | Dynamic, AI-driven retrieval of necessary data |
| **Personalization**      | Generic responses     | Personalized responses per customer | Fully adaptive to user needs |
| **Session Handling**     | Resets on refresh     | Resets on refresh, allows customer changes | Preserves context within session, resets on refresh |
| **Frontend Features**    | Simple chat UI        | Customer field, loader animation, formatted response | Full chat-like experience, messages accumulate, auto-scroll |

---

## **🚀 Choosing the Right Version**
### **✅ Use `app.py/index.html` if:**
- Responses should be based on **a static dataset**.  
- Users will ask **general questions**.  
- Performance is a priority (no need for multiple queries).  

### **✅ Use `app2.py/index2.html` if:**
- Responses should be **customer-specific**.  
- Users should **manually specify the customer name**.  
- The assistant should **fetch relevant data dynamically** before answering.  

### **✅ Use `app3.py/index3.html` if:**
- You want a **fully conversational chat experience**.  
- Users should **not need to specify customer details manually**.  
- The AI should determine **when and how to fetch data dynamically**.  
- **Context from past messages should be remembered** for a continuous conversation.  

---

## **🎯 Final Thoughts**
Each version provides a **real-time AI-powered chat experience** backed by **Dremio's data engine**.  
- **`app.py` is the simplest**, but lacks personalization.  
- **`app2.py` improves personalization**, but requires manual input for customer selection.  
- **`app3.py` is the most advanced**, allowing **fully dynamic** and **context-aware** conversations.  

🚀 **Choose the right version based on your needs!** 🚀
