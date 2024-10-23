__author__ = 'Alexey Y Manikin'

# Определение JSON-схемы для ответа
json_schema = {
    "type": "object",
    "properties": {   
        "description":  {"type": "string"},
        "group":        {"type": "string"},
        "summ":         {"type": "number"},
        "type_s":       {"type": "string"},
        "date":         {"type": "string"}
    },
    "required": ["description", "group", "summ", "type_s"]
}

# URL вашего vLLM сервера
openai_api_url = "http://---/v1/chat/completions"
model_name = "Qwen"