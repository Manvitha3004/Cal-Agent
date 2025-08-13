# Calendar Agent

A simplified calendar agent with FastAPI backend and React frontend.

## Tech Stack
- **Backend:** FastAPI, Socket.IO, MongoDB (Motor), Google Gemini API, JWT (python-jose)
- **Frontend:** React, socket.io-client

## Environment Variables
Create a `.env` file in the root:
```
MONGODB_URI=mongodb://localhost:27017/calendar_agent
GEMINI_API_KEY=your_gemini_api_key
JWT_SECRET=your_jwt_secret_key
```

## Backend Setup
1. Install MongoDB and run locally:
   - Download from https://www.mongodb.com/try/download/community
   - Start with `mongod`
2. Install Python dependencies:
   ```sh
   cd calendar-agent/backend
   pip install -r requirements.txt
   ```
3. Run backend:
   ```sh
   uvicorn main:app --reload
   ```

## Frontend Setup
1. Install Node.js (https://nodejs.org/)
2. Install dependencies:
   ```sh
   cd calendar-agent/frontend
   npm install
   ```
3. Start frontend:
   ```sh
   npm start
   ```

## Gemini API Key
- Get a Gemini API key from Google AI Studio: https://aistudio.google.com/
- Add to `.env` as `GEMINI_API_KEY`

## Features
- Register/Login (JWT)
- Chat with bot to schedule meetings
- Meetings stored in MongoDB
- Real-time chat via Socket.IO
- Reminders sent 5 minutes before meetings
- Conflict detection for overlapping meetings
