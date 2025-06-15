# DAWN - Deep Learning Research Project

DAWN is a consciousness engine that implements a tick-based system for processing and analyzing neural data. The project consists of a Python backend for the core consciousness engine and a React-based frontend for visualization and interaction.

## Project Structure

```
DAWN/
├── backend/
│   ├── main.py                    # Core consciousness engine
│   ├── start_api_fixed.py         # FastAPI server with WebSocket support
│   ├── modules/                   # Python process modules
│   ├── utils/                     # Backend utilities
│   └── requirements.txt           # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   │   └── Terminal.tsx     # Terminal-based UI
│   │   ├── services/            # Frontend services
│   │   │   └── websocket.ts     # WebSocket connection
│   │   └── styles/              # CSS styles
│   └── package.json             # Frontend dependencies
│
└── README.md
```

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Backend Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```bash
   python start_api_fixed.py
   ```

The server will start on `http://localhost:8000` with WebSocket support at `ws://localhost:8000/ws`.

## Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`.

## Features

- Real-time consciousness engine data visualization
- WebSocket-based communication between frontend and backend
- Terminal-style UI for monitoring engine state
- Core metrics tracking (SCUP, Entropy, Mood)

## Development

### Backend

The backend is built with:
- FastAPI for the web server
- WebSockets for real-time communication
- PyTorch for neural processing
- AsyncIO for concurrent operations

### Frontend

The frontend is built with:
- React for the UI
- TypeScript for type safety
- WebSocket for real-time updates
- CSS for styling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 