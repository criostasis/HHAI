#!/bin/bash

# Terminate the Flask backend running in the tmux session
tmux kill-session -t my_session
echo "tmux session for Flask backend has been terminated."

# Retrieve PIDs for any process listening on ports 3000 and 5000
node_pids=$(lsof -ti :3000)
flask_pids=$(lsof -ti :5000)

echo "Node.js PIDs: $node_pids"
echo "Flask PIDs: $flask_pids"

# Directly iterate over and kill Node.js processes on port 3000
if [ -n "$node_pids" ]; then
  for pid in $node_pids; do
    echo "Killing Node.js process on port 3000 with PID: $pid"
    kill -9 $pid
    # Optionally, use kill -9 $pid for a forceful kill
  done
else
  echo "No running Node.js process found on port 3000."
fi

# Directly iterate over and kill Flask processes on port 5000
# This serves as a fallback since Flask is terminated with tmux.
if [ -n "$flask_pids" ]; then
  for pid in $flask_pids; do
    echo "Killing Flask process on port 5000 with PID: $pid"
    kill $pid
    # Optionally, use kill -9 $pid for a forceful kill
  done
else
  echo "No running Flask process should be found on port 5000 after tmux session termination."
fi

# Kill the torch server
torchserve --stop