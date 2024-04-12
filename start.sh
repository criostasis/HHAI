#!/bin/bash

# Activate the Python virtual environment if needed
# source /path/to/your/venv/bin/activate

# Start the Flask application in the background
echo "Starting Flask application..."
#cd /home/criostasis/PycharmProjects/HHAI/backend/
cd /opt/HHAI/backend/
nohup python3 app.py > flask_app.log 2>&1 &

echo "Flask application started."

# Ensure Flask starts up before proceeding
sleep 5

# Start TorchServe
echo "Starting TorchServe..."
#cd /home/criostasis/PycharmProjects/HHAI/LLM/Model/
cd /opt/HHAI/LLM/Model/
nohup torchserve --start --ncs --model-store . --ts-config config.properties --models wizardlmtest.mar > torch_serve.log 2>&1 &

echo "TorchServe started."

# Ensure TorchServe starts up before proceeding
sleep 5

# Start the npm project
echo "Starting npm project..."
#cd /home/criostasis/PycharmProjects/HHAI/
cd /opt/HHAI/
nohup npm start > npm_project.log 2>&1 &

echo "npm project started."

echo "All services started successfully."

# Wait a little bit to let everything get started
sleep 45

# Use netstat to check ports and ensure everything is running
# Check for ports 3000, 5000, 8080, 8081, 8082 to be LISTEN
netstat -tln