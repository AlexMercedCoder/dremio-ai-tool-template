# Dremio AI Chat - Comparison of `app.py/index.html` vs `app2.py/index2.html`

## Overview
The **Dremio AI Chat** is a Flask-based web application that integrates OpenAI's GPT-4 with real-time data retrieval from **Dremio**. The two versions of the application (`app.py/index.html` and `app2.py/index2.html`) have key differences in how they handle data retrieval and user interaction.

## Differences Between `app.py` and `app2.py`

### 1. **User Input and Context Retrieval**
- **`app.py`**
  - The user submits a question.
  - On the first request, a predefined **SQL query** runs against Dremio to fetch **general data**.
  - This data is **directly injected** into the AI prompt.
  - The AI uses this data to generate a response.
  - All subsequent responses reuse the **same fetched data** until the session is refreshed.

- **`app2.py`**
  - The user submits both a **customer name** and a **question**.
  - The app first queries Dremio to **retrieve the customer’s unique ID**.
  - Using the customer ID, a **second query fetches customer-specific data**.
  - The AI prompt is then dynamically generated using the **retrieved customer data**.
  - This ensures that each response is tailored to the specific customer.

### 2. **Querying and Data Integration**
- **`app.py`**
  - Fetches a single **static dataset** from Dremio on the first request.
  - The AI assistant operates based on this **preloaded data** for all user interactions.

- **`app2.py`**
  - Uses a **two-step querying approach**:
    1. Retrieves the customer ID from a lookup table.
    2. Fetches customer-specific records based on the retrieved ID.
  - Ensures that responses are **customized per customer**, rather than relying on a generic dataset.

### 3. **Session Handling**
- **`app.py`**
  - Maintains chat history during a session.
  - On **refresh**, the session is **automatically cleared**, resetting chat history and requiring the initial query to run again.

- **`app2.py`**
  - Also maintains chat history but allows users to specify a **new customer** at any time.
  - Session clears on **refresh**, ensuring each session starts with a fresh lookup.

### 4. **Frontend Differences**
- **`index.html` (Used with `app.py`)**
  - Displays a **single chat input** where users ask a question.
  - Uses a **sleek aquatic blue UI** with a **chat history display**.

- **`index2.html` (Used with `app2.py`)**
  - Includes **two input fields**: one for the **customer name** and another for the **user's question**.
  - Introduces a **"Typing..." loader animation** while the AI processes the response.
  - Formats AI responses using **`<pre>` tags**, ensuring structured data from Dremio is displayed in a **readable format**.

## Summary of Key Differences

| Feature                  | `app.py` / `index.html` | `app2.py` / `index2.html` |
|--------------------------|------------------------|---------------------------|
| **User Input**           | Single text input for questions | Customer name + question input fields |
| **Data Querying**        | One-time query on first question | Two-step query (customer lookup + data retrieval) |
| **Response Context**     | General dataset injected into prompt | Customer-specific data injected into prompt |
| **Personalization**      | Same data for all users | Unique responses per customer |
| **Session Handling**     | Resets on refresh | Resets on refresh |
| **Frontend Features**    | Basic chat layout | Customer field, loader animation, formatted AI response |

## Choosing the Right Version
- **Use `app.py/index.html`** if responses should be based on a **predefined dataset** and users only need to ask general questions.
- **Use `app2.py/index2.html`** if responses should be **customer-specific**, dynamically fetching and displaying tailored data for each interaction.

Both versions provide a **real-time AI chat experience** backed by Dremio, with the choice depending on the level of personalization required.

