"""
Serviço de criação de vídeos simples (slideshow)
"""
import os
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import json


class VideoService:
    def __init__(self):
        self.default_width = 1280
        self.default_height = 720
        self.default_fps = 30
    
    def create_slideshow_frames(self, images_data, duration_per_image=3):
        """
        Cria frames para um vídeo slideshow
        
        Args:
            images_data: Lista de dicionários com dados das imagens
                [
                    {
                        'image': 'base64_string ou path',
                        'caption': 'Texto opcional'
                    }
                ]
            duration_per_image: Duração de cada imagem em segundos
        
        Returns:
            Informações sobre os frames gerados
        """
        try:
            frames_info = []
            total_frames = 0
            
            for idx, img_data in enumerate(images_data):
                # Processa imagem
                if isinstance(img_data.get('image'), str):
                    if img_data['image'].startswith('data:image'):
                        # Remove header do base64
                        img_base64 = img_data['image'].split(',')[1]
                        img_bytes = base64.b64decode(img_base64)
                        img = Image.open(BytesIO(img_bytes))
                    else:
                        # Assume que é um caminho de arquivo
                        img = Image.open(img_data['image'])
                else:
                    # Cria imagem placeholder
                    img = self._create_placeholder_image(f"Slide {idx + 1}")
                
                # Redimensiona para tamanho padrão
                img = img.resize((self.default_width, self.default_height), Image.Resampling.LANCZOS)
                
                # Adiciona legenda se fornecida
                if img_data.get('caption'):
                    img = self._add_caption(img, img_data['caption'])
                
                # Calcula número de frames
                num_frames = duration_per_image * self.default_fps
                total_frames += num_frames
                
                # Converte para base64
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                frames_info.append({
                    'index': idx,
                    'frame_data': f'data:image/png;base64,{img_base64}',
                    'duration': duration_per_image,
                    'num_frames': num_frames
                })
            
            return {
                'success': True,
                'frames': frames_info,
                'total_frames': total_frames,
                'fps': self.default_fps,
                'total_duration': len(images_data) * duration_per_image,
                'resolution': f'{self.default_width}x{self.default_height}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_placeholder_image(self, text):
        """
        Cria uma imagem placeholder
        """
        img = Image.new('RGB', (self.default_width, self.default_height), color=(100, 100, 150))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # Centraliza texto
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = ((self.default_width - text_width) // 2, (self.default_height - text_height) // 2)
        
        draw.text(position, text, fill=(255, 255, 255), font=font)
        
        return img
    
    def _add_caption(self, img, caption):
        """
        Adiciona legenda na parte inferior da imagem
        """
        draw = ImageDraw.Draw(img)
        
        # Cria retângulo semi-transparente para o texto
        caption_height = 100
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle(
            [(0, self.default_height - caption_height), (self.default_width, self.default_height)],
            fill=(0, 0, 0, 180)
        )
        
        # Combina overlay com imagem original
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        img = img.convert('RGB')
        
        # Adiciona texto
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        except:
            font = ImageFont.load_default()
        
        # Quebra texto em múltiplas linhas se necessário
        words = caption.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] < self.default_width - 40:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Desenha linhas de texto
        y_offset = self.default_height - caption_height + 20
        for line in lines[:2]:  # Máximo 2 linhas
            draw.text((20, y_offset), line, fill=(255, 255, 255), font=font)
            y_offset += 35
        
        return img
    
    def create_video_metadata(self, title, description, frames_count, duration):
        """
        Cria metadados para o vídeo
        """
        return {
            'title': title,
            'description': description,
            'frames_count': frames_count,
            'duration': duration,
            'format': 'slideshow',
            'resolution': f'{self.default_width}x{self.default_height}',
            'fps': self.default_fps,
            'note': 'Vídeo criado como slideshow de imagens. Para exportar como MP4, use ferramentas de conversão.'
        }

