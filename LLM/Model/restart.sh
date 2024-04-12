# Remove old mar file
rm wizardlmtest.mar
# Make sure torch serve is stopped
torchserve --stop
# Create new mar file
torch-model-archiver --model-name wizardlmtest --version 1.0 \
    --serialized-file wizardlm-13b-v1.2.Q4_0.gguf \
    --extra-files "database_helper.py,index.faiss,index.pkl" \
    --handler model_handler.py --export-path .
## Wait a bit
#sleep 5
##Stop torch serve
#torchserve --stop
# Wait a bit longer
#sleep 10
#
#torchserve --start --model-store /opt/Fast-API-Test/LLM/Model --models wizardlm.mar
#
#sleep 5
#
## Check the list of models
#response=$(curl -s http://localhost:8081/models)
#
#if [[ $response == *"\"models\": []"* ]]; then
#  echo "No models registered. Registering the wizardlm model..."
#  curl -X POST "http://localhost:8081/models?url=wizardlmtest.mar&model_name=wizardlmtest&initial_workers=1&synchronous=true"
#  echo "Model registration completed."
#else
#  echo "Models already registered."
#fi

