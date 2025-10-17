"""
Serviço de geração de imagens usando Hugging Face
"""
import os
import requests
import base64
from io import BytesIO
from PIL import Image
import time


class ImageService:
    def __init__(self, hf_token=None):
        self.hf_token = hf_token or os.getenv('HUGGINGFACE_TOKEN')
        self.api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
        self.headers = {}
        if self.hf_token:
            self.headers["Authorization"] = f"Bearer {self.hf_token}"
    
    def generate_image(self, prompt, negative_prompt="", num_inference_steps=25):
        """
        Gera uma imagem a partir de um prompt de texto
        """
        try:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "negative_prompt": negative_prompt,
                    "num_inference_steps": num_inference_steps
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 503:
                # Modelo está carregando
                return {
                    'success': False,
                    'error': 'O modelo está carregando. Por favor, tente novamente em alguns segundos.',
                    'status': 'loading'
                }
            
            if response.status_code == 429:
                return {
                    'success': False,
                    'error': 'Limite de requisições atingido. Por favor, aguarde alguns minutos.',
                    'status': 'rate_limited'
                }
            
            if response.status_code != 200:
                return {
                    'success': False,
                    'error': f'Erro na API: {response.status_code} - {response.text}',
                    'status': 'error'
                }
            
            # Converte a resposta em imagem
            image = Image.open(BytesIO(response.content))
            
            # Converte para base64 para enviar ao frontend
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return {
                'success': True,
                'image': f'data:image/png;base64,{img_str}',
                'format': 'png',
                'size': image.size
            }
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Timeout na requisição. O modelo pode estar sobrecarregado.',
                'status': 'timeout'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status': 'error'
            }
    
    def generate_simple_placeholder(self, text, width=512, height=512):
        """
        Gera uma imagem placeholder simples quando a API não está disponível
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Cria imagem com gradiente
            img = Image.new('RGB', (width, height), color=(73, 109, 137))
            draw = ImageDraw.Draw(img)
            
            # Adiciona texto
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Centraliza texto
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            position = ((width - text_width) // 2, (height - text_height) // 2)
            
            draw.text(position, text, fill=(255, 255, 255), font=font)
            
            # Converte para base64
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            return {
                'success': True,
                'image': f'data:image/png;base64,{img_str}',
                'format': 'png',
                'size': (width, height),
                'note': 'Imagem placeholder gerada localmente'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

