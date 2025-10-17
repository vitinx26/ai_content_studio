"""
Rotas da API para o AI Content Studio
"""
from flask import Blueprint, request, jsonify, send_file
from src.services.search_service import SearchService
from src.services.image_service import ImageService
from src.services.presentation_service import PresentationService
from src.services.video_service import VideoService
import base64
from io import BytesIO

api_bp = Blueprint('api', __name__)

# Inicializa serviços
search_service = SearchService()
image_service = ImageService()
presentation_service = PresentationService()
video_service = VideoService()


@api_bp.route('/search', methods=['POST'])
def search():
    """
    Endpoint de pesquisa combinada (web + wikipedia)
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query não pode estar vazia'
            }), 400
        
        max_results = data.get('max_results', 5)
        results = search_service.combined_search(query, max_results)
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/search/web', methods=['POST'])
def search_web():
    """
    Endpoint de pesquisa web (DuckDuckGo)
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query não pode estar vazia'
            }), 400
        
        max_results = data.get('max_results', 5)
        results = search_service.search_web(query, max_results)
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/search/wikipedia', methods=['POST'])
def search_wikipedia():
    """
    Endpoint de pesquisa Wikipedia
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query não pode estar vazia'
            }), 400
        
        results = search_service.search_wikipedia(query)
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/generate/image', methods=['POST'])
def generate_image():
    """
    Endpoint de geração de imagens
    """
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({
                'success': False,
                'error': 'Prompt não pode estar vazio'
            }), 400
        
        negative_prompt = data.get('negative_prompt', '')
        use_placeholder = data.get('use_placeholder', False)
        
        if use_placeholder:
            # Gera placeholder local
            result = image_service.generate_simple_placeholder(prompt[:50])
        else:
            # Tenta gerar via Hugging Face
            result = image_service.generate_image(prompt, negative_prompt)
            
            # Se falhar, gera placeholder
            if not result['success'] and result.get('status') != 'rate_limited':
                result = image_service.generate_simple_placeholder(prompt[:50])
                result['fallback'] = True
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/generate/presentation', methods=['POST'])
def generate_presentation():
    """
    Endpoint de geração de apresentações
    """
    try:
        data = request.get_json()
        title = data.get('title', 'Apresentação').strip()
        
        # Verifica tipo de geração
        if 'topic' in data:
            # Gera a partir de tópico
            topic = data['topic'].strip()
            num_slides = data.get('num_slides', 5)
            result = presentation_service.generate_from_topic(topic, num_slides)
        
        elif 'text_content' in data:
            # Gera a partir de texto
            text_content = data['text_content'].strip()
            result = presentation_service.create_from_text(title, text_content)
        
        elif 'slides_data' in data:
            # Gera a partir de dados estruturados
            slides_data = data['slides_data']
            result = presentation_service.create_presentation(title, slides_data)
        
        else:
            return jsonify({
                'success': False,
                'error': 'Forneça topic, text_content ou slides_data'
            }), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/generate/video', methods=['POST'])
def generate_video():
    """
    Endpoint de geração de vídeos (slideshow)
    """
    try:
        data = request.get_json()
        images_data = data.get('images', [])
        
        if not images_data:
            return jsonify({
                'success': False,
                'error': 'Forneça pelo menos uma imagem'
            }), 400
        
        duration_per_image = data.get('duration_per_image', 3)
        title = data.get('title', 'Vídeo')
        description = data.get('description', '')
        
        # Cria frames do slideshow
        result = video_service.create_slideshow_frames(images_data, duration_per_image)
        
        if result['success']:
            # Adiciona metadados
            metadata = video_service.create_video_metadata(
                title,
                description,
                result['total_frames'],
                result['total_duration']
            )
            result['metadata'] = metadata
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/health', methods=['GET'])
def health():
    """
    Endpoint de health check
    """
    return jsonify({
        'status': 'healthy',
        'service': 'AI Content Studio API',
        'version': '1.0.0'
    }), 200

