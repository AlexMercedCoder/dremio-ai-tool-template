# Dremio AI Chat - Flask Application Documentation

## Overview
The **Dremio AI Chat** is a Flask-based web application that enables users to interact with an AI-powered assistant while leveraging real-time data from **Dremio**. The AI model, powered by OpenAI's **GPT-4**, provides contextual responses based on query results fetched from Dremio.

## How It Works
1. **User Interaction:**  
   - Users enter a question in the chat interface.  
   - The AI assistant processes the question and responds with relevant insights.  

2. **Dremio Data Integration:**  
   - When a user submits the **first** question, the application queries Dremio using a predefined SQL query.  
   - The retrieved data is injected directly into the AI's prompt for better contextual awareness.  

3. **AI Response Generation:**  
   - The OpenAI GPT-4 model receives the user query along with the Dremio data.  
   - The model processes the input and generates an appropriate response.  
   - The conversation history is maintained during the session.  

4. **Session Handling & Auto-Reset:**  
   - A user session is created to store conversation history.  
   - If the page is **refreshed**, the session is **automatically cleared**, ensuring a fresh chat experience.  

## Features
- **Dynamic Dremio Querying:** Fetches live data from Dremio and integrates it into AI responses.  
- **Context-Aware Responses:** The AI uses real-time query results to enhance response relevance.  
- **Session-Based Chat:** Maintains an interactive conversation until the page is refreshed.  
- **Automatic Reset on Refresh:** Clears session data upon page reload to start a new chat.  

## Usage Flow
1. **User opens the chat interface.**  
2. **User submits a question.**  
3. **Dremio query runs (only on the first question).**  
4. **AI generates a response using the fetched data.**  
5. **User can continue the conversation with stored context.**  
6. **Refreshing the page resets the session and starts a new conversation.**  

This application provides an intuitive, real-time AI chat experience backed by structured data from Dremio, ensuring accurate and context-rich insights for users.
