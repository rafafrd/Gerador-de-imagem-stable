import os
import base64
import requests
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv()

class ImageGenerator:
    API_BASE_URL = "https://api.stability.ai/v1/generation"
    
    @staticmethod
    def generate_image(
        prompt: str,
        negative_prompt: str = "",
        width: int = 512,
        height: int = 512,
        engine_id: str = "stable-diffusion-v1-6",
        steps: int = 30,
        cfg_scale: float = 7.0,
        samples: int = 1,
        style_preset: Optional[str] = None
    ) -> Dict:
        """Gera imagens usando a API do Stability AI
        
        Args:
            prompt: Descrição da imagem desejada
            negative_prompt: Elementos a serem evitados
            width: Largura da imagem
            height: Altura da imagem
            engine_id: Modelo de IA a ser usado
            steps: Número de passos de refinamento
            cfg_scale: Criatividade vs. fidelidade ao prompt
            samples: Número de imagens a gerar
            style_preset: Estilo pré-definido (opcional)
        
        Returns:
            Dict: Resposta da API contendo as imagens geradas
        """
        api_key = os.getenv("STABILITY_API_KEY")
        if not api_key:
            raise ValueError("🔑 Chave da API não encontrada. Verifique seu arquivo .env")
        
        url = f"{ImageGenerator.API_BASE_URL}/{engine_id}/text-to-image"
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "text_prompts": [{"text": prompt, "weight": 1.0}],
            "cfg_scale": cfg_scale,
            "clip_guidance_preset": "FAST_BLUE",
            "height": height,
            "width": width,
            "samples": samples,
            "steps": steps,
            "sampler": "K_DPM_2_ANCESTRAL"
        }
        
        if negative_prompt:
            payload["text_prompts"].append({"text": negative_prompt, "weight": -1.0})
            
        if style_preset:
            payload["style_preset"] = style_preset
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"🔴 Erro na API: {str(e)}")
            if hasattr(e, 'response') and e.response:
                print(f"Detalhes: {e.response.text}")
            return {}

    @staticmethod
    def decode_base64(base64_string: str) -> bytes:
        """Decodifica string base64 para bytes"""
        return base64.b64decode(base64_string)


# Funções de conveniência para compatibilidade
def generate_image(*args, **kwargs):
    return ImageGenerator.generate_image(*args, **kwargs)

def decode_base64(base64_string: str) -> bytes:
    return ImageGenerator.decode_base64(base64_string)