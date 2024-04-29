#!/bin/bash

rm wizardlmtest.mar

torch-model-archiver --model-name wizardlmtest --version 1.0 --serialized-file wizardlm-13b-v1.2.Q4_0.gguf --extra-files "database_helper.py,index.faiss,index.pkl" --handler model_handler.py --export-path .
