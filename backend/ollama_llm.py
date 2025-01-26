# ollama_llm.py
from langchain.llms.base import LLM
from typing import Optional, List, Dict, Any
import requests
import json

class OllamaLLM(LLM):
    model_name: str  # Define as class variable with type annotation
    base_url: str = 'http://localhost:11434'  # Default value

    @property
    def _llm_type(self) -> str:
        return 'ollama'

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        payload = {
            'model': self.model_name,
            'prompt': prompt
        }
        if stop is not None:
            payload['stop'] = stop
        headers = {
            'Accept': 'application/json'
        }
        response = requests.post(
            f'{self.base_url}/api/generate',
            json=payload,
            headers=headers,
            stream=True
        )
        response.raise_for_status()
        # Streaming response handling
        generated_text = ''
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                generated_text += data.get('response', '')
        return generated_text

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {'model_name': self.model_name, 'base_url': self.base_url}
