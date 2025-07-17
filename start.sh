#!/bin/bash

echo "Starting eCFR Analysis Dashboard..."

# Start backend server in background
echo "Starting backend server on port 8001..."
cd backend
source .venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend server
echo "Starting frontend server on port 9000..."
cd frontend
python3 -m http.server 9000 &
FRONTEND_PID=$!
cd ..

echo ""
echo "Dashboard is running!"
echo "Frontend: http://localhost:9000"
echo "Backend API: http://localhost:8001"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user interrupt
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 