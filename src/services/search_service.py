"""
Serviço de pesquisa usando DuckDuckGo e Wikipedia
"""
import wikipediaapi
from duckduckgo_search import DDGS


class SearchService:
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia(
            user_agent='AIContentStudio/1.0',
            language='pt'
        )
    
    def search_web(self, query, max_results=5):
        """
        Pesquisa na web usando DuckDuckGo
        """
        try:
            results = []
            with DDGS() as ddgs:
                search_results = ddgs.text(query, max_results=max_results)
                for result in search_results:
                    results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('body', ''),
                        'url': result.get('href', '')
                    })
            return {
                'success': True,
                'results': results,
                'source': 'DuckDuckGo'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'results': []
            }
    
    def search_wikipedia(self, query):
        """
        Pesquisa na Wikipedia
        """
        try:
            page = self.wiki.page(query)
            
            if not page.exists():
                # Tenta buscar páginas relacionadas
                search_results = self.wiki.search(query, results=3)
                if search_results:
                    return {
                        'success': True,
                        'found': False,
                        'suggestions': search_results,
                        'message': 'Página não encontrada. Sugestões disponíveis.'
                    }
                return {
                    'success': False,
                    'found': False,
                    'message': 'Nenhum resultado encontrado na Wikipedia.'
                }
            
            return {
                'success': True,
                'found': True,
                'title': page.title,
                'summary': page.summary[:500] + '...' if len(page.summary) > 500 else page.summary,
                'url': page.fullurl,
                'full_text': page.text[:2000] if len(page.text) > 2000 else page.text
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'found': False
            }
    
    def combined_search(self, query, max_web_results=5):
        """
        Combina resultados de DuckDuckGo e Wikipedia
        """
        web_results = self.search_web(query, max_web_results)
        wiki_results = self.search_wikipedia(query)
        
        return {
            'query': query,
            'web': web_results,
            'wikipedia': wiki_results
        }

