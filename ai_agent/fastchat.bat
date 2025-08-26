python -m fastchat.serve.controller --host 0.0.0.0 --port 8001
python -m fastchat.serve.model_worker --model-path fnlp/moss-moon-003-sft --trust-remote-code
python -m fastchat.serve.openai_api_server --host 0.0.0.0 --port 8000