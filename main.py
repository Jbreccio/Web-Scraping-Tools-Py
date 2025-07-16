import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv
import time
from datetime import datetime
import logging
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse
import re
from dataclasses import dataclass
from pathlib import Path
import sqlite3
from fake_useragent import UserAgent
from datetime import timedelta

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ScrapingConfig:
    """Configuração para scraping"""
    delay: float = 1.0  # Delay entre requests
    timeout: int = 10
    max_retries: int = 3
    use_random_agent: bool = True
    output_format: str = 'csv'  # csv, json, excel, sqlite
    output_path: str = 'scraped_data'

class WebScraper:
    """Classe base para web scraping"""
    
    def __init__(self, config: ScrapingConfig):
        self.config = config
        self.session = requests.Session()
        self.ua = UserAgent() if config.use_random_agent else None
        self.scraped_data = []
        
        # Headers padrão
        self.headers = {
            'User-Agent': self.get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.session.headers.update(self.headers)
    
    def get_user_agent(self) -> str:
        """Retorna user agent"""
        if self.ua:
            return self.ua.random
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    def make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """Faz requisição com retry e delay"""
        for attempt in range(self.config.max_retries):
            try:
                time.sleep(self.config.delay)
                
                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.config.timeout,
                    **kwargs
                )
                
                if response.status_code == 200:
                    return response
                else:
                    logger.warning(f"Status {response.status_code} para {url}")
                    
            except Exception as e:
                logger.warning(f"Tentativa {attempt + 1} falhou para {url}: {str(e)}")
                
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.delay * (attempt + 1))
        
        logger.error(f"Falha ao acessar {url} após {self.config.max_retries} tentativas")
        return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parseia HTML com BeautifulSoup"""
        return BeautifulSoup(html, 'html.parser')
    
    def save_data(self, data: List[Dict], filename: str):
        """Salva dados no formato especificado"""
        if not data:
            logger.warning("Nenhum dado para salvar")
            return
        
        # Criar diretório se não existir
        Path(self.config.output_path).mkdir(parents=True, exist_ok=True)
        
        filepath = Path(self.config.output_path) / filename
        
        try:
            if self.config.output_format == 'csv':
                df = pd.DataFrame(data)
                df.to_csv(f"{filepath}.csv", index=False, encoding='utf-8')
                
            elif self.config.output_format == 'json':
                with open(f"{filepath}.json", 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    
            elif self.config.output_format == 'excel':
                df = pd.DataFrame(data)
                df.to_excel(f"{filepath}.xlsx", index=False)
                
            elif self.config.output_format == 'sqlite':
                self.save_to_sqlite(data, f"{filepath}.db")
            
            logger.info(f"Dados salvos em: {filepath}.{self.config.output_format}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar dados: {str(e)}")
    
    def save_to_sqlite(self, data: List[Dict], db_path: str):
        """Salva dados em SQLite"""
        conn = sqlite3.connect(db_path)
        df = pd.DataFrame(data)
        df.to_sql('scraped_data', conn, if_exists='replace', index=False)
        conn.close()

class JobScraper(WebScraper):
    """Scraper para vagas de emprego"""
    
    def scrape_jobs(self, search_terms: List[str], location: str = "São Paulo"):
        """Scrapa vagas de emprego"""
        jobs_data = []
        
        # Exemplo com dados simulados (substitua por sites reais)
        for term in search_terms:
            logger.info(f"Buscando vagas para: {term}")
            
            # Simulação de dados de vagas
            sample_jobs = self.generate_sample_jobs(term, location)
            jobs_data.extend(sample_jobs)
        
        return jobs_data
    
    def generate_sample_jobs(self, term: str, location: str) -> List[Dict]:
        """Gera dados simulados de vagas"""
        import random
        
        companies = [
            "TechCorp", "InnovaSoft", "DataSolutions", "CloudTech", 
            "StartupXYZ", "MegaCorp", "DigitalLabs", "CodeFactory"
        ]
        
        levels = ["Júnior", "Pleno", "Sênior"]
        salaries = [3000, 4500, 6000, 8000, 10000, 12000]
        
        jobs = []
        for i in range(random.randint(5, 15)):
            job = {
                'title': f"Desenvolvedor {term} {random.choice(levels)}",
                'company': random.choice(companies),
                'location': location,
                'salary': f"R$ {random.choice(salaries):,}",
                'description': f"Vaga para {term} com experiência em desenvolvimento web",
                'requirements': f"Python, {term}, Git, SQL",
                'url': f"https://example.com/job/{i}",
                'posted_date': datetime.now().strftime('%Y-%m-%d'),
                'scraped_at': datetime.now().isoformat()
            }
            jobs.append(job)
        
        return jobs

class EcommerceScraper(WebScraper):
    """Scraper para dados de e-commerce"""
    
    def scrape_products(self, categories: List[str]) -> List[Dict]:
        """Scrapa produtos de e-commerce"""
        products_data = []
        
        for category in categories:
            logger.info(f"Buscando produtos da categoria: {category}")
            
            # Simulação de dados de produtos
            sample_products = self.generate_sample_products(category)
            products_data.extend(sample_products)
        
        return products_data
    
    def generate_sample_products(self, category: str) -> List[Dict]:
        """Gera dados simulados de produtos"""
        import random
        
        base_products = {
            'eletrônicos': ['Smartphone', 'Tablet', 'Notebook', 'Fone', 'Câmera'],
            'roupas': ['Camiseta', 'Calça', 'Vestido', 'Casaco', 'Tênis'],
            'casa': ['Mesa', 'Cadeira', 'Sofá', 'Cama', 'Geladeira'],
            'livros': ['Romance', 'Técnico', 'Biografia', 'Ficção', 'História']
        }
        
        products = base_products.get(category.lower(), ['Produto Genérico'])
        
        product_list = []
        for i in range(random.randint(8, 20)):
            product = {
                'name': f"{random.choice(products)} {random.randint(1, 100)}",
                'category': category,
                'price': round(random.uniform(50, 2000), 2),
                'rating': round(random.uniform(3.0, 5.0), 1),
                'reviews_count': random.randint(10, 500),
                'availability': random.choice(['Em estoque', 'Últimas unidades', 'Indisponível']),
                'brand': f"Marca {random.choice(['A', 'B', 'C', 'D'])}",
                'url': f"https://example.com/product/{i}",
                'scraped_at': datetime.now().isoformat()
            }
            product_list.append(product)
        
        return product_list

class NewsScraper(WebScraper):
    """Scraper para notícias"""
    
    def scrape_news(self, topics: List[str]) -> List[Dict]:
        """Scrapa notícias"""
        news_data = []
        
        for topic in topics:
            logger.info(f"Buscando notícias sobre: {topic}")
            
            # Simulação de dados de notícias
            sample_news = self.generate_sample_news(topic)
            news_data.extend(sample_news)
        
        return news_data
    
    def generate_sample_news(self, topic: str) -> List[Dict]:
        """Gera dados simulados de notícias"""
        import random
        
        sources = ["TechNews", "InfoDaily", "TechCrunch Brasil", "StartupBR", "DevNews"]
        
        news_list = []
        for i in range(random.randint(5, 12)):
            news = {
                'title': f"Últimas novidades sobre {topic} - {random.randint(1, 100)}",
                'source': random.choice(sources),
                'author': f"Autor {random.randint(1, 10)}",
                'published_date': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
                'topic': topic,
                'summary': f"Resumo da notícia sobre {topic}...",
                'url': f"https://example.com/news/{i}",
                'scraped_at': datetime.now().isoformat()
            }
            news_list.append(news)
        
        return news_list

class DataAnalyzer:
    """Classe para análise dos dados coletados"""
    
    def __init__(self, data: List[Dict]):
        self.data = data
        self.df = pd.DataFrame(data) if data else pd.DataFrame()
    
    def get_basic_stats(self) -> Dict:
        """Retorna estatísticas básicas"""
        if self.df.empty:
            return {}
        
        stats = {
            'total_records': len(self.df),
            'columns': list(self.df.columns),
            'data_types': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'unique_values': {col: self.df[col].nunique() for col in self.df.columns}
        }
        
        return stats
    
    def analyze_text_data(self, text_column: str) -> Dict:
        """Analisa dados de texto"""
        if text_column not in self.df.columns:
            return {}
        
        text_data = self.df[text_column].dropna()
        
        analysis = {
            'total_entries': len(text_data),
            'average_length': text_data.str.len().mean(),
            'max_length': text_data.str.len().max(),
            'min_length': text_data.str.len().min(),
            'most_common_words': self.get_common_words(text_data.str.cat(sep=' '))
        }
        
        return analysis
    
    def get_common_words(self, text: str, top_n: int = 10) -> List[tuple]:
        """Retorna palavras mais comuns"""
        # Limpar texto
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Remover stop words básicas
        stop_words = {'de', 'da', 'do', 'com', 'para', 'em', 'e', 'o', 'a', 'os', 'as', 'um', 'uma'}
        words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Contar frequência
        word_count = {}
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # Retornar top N
        return sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:top_n]

def main():
    """Função principal para demonstração"""
    print("🕷️  Web Scraping Tools - Demonstração")
    print("=" * 50)
    
    # Configuração
    config = ScrapingConfig(
        delay=1.0,
        output_format='csv',
        output_path='scraped_data'
    )
    
    # 1. Scraping de Vagas de Emprego
    print("\n💼 Scraped Jobs...")
    job_scraper = JobScraper(config)
    jobs_data = job_scraper.scrape_jobs(['Python', 'Django', 'JavaScript'], 'São Paulo')
    job_scraper.save_data(jobs_data, 'jobs_data')
    
    # 2. Scraping de E-commerce
    print("\n🛒 Scraping E-commerce...")
    ecommerce_scraper = EcommerceScraper(config)
    products_data = ecommerce_scraper.scrape_products(['eletrônicos', 'roupas', 'casa'])
    ecommerce_scraper.save_data(products_data, 'products_data')
    
    # 3. Scraping de Notícias
    print("\n📰 Scraping Notícias...")
    news_scraper = NewsScraper(config)
    news_data = news_scraper.scrape_news(['Python', 'IA', 'Tecnologia'])
    news_scraper.save_data(news_data, 'news_data')
    
    # 4. Análise dos Dados
    print("\n📊 Análise dos Dados...")
    
    # Analisar dados de jobs
    job_analyzer = DataAnalyzer(jobs_data)
    job_stats = job_analyzer.get_basic_stats()
    
    print(f"✅ Jobs coletados: {job_stats.get('total_records', 0)}")
    print(f"✅ Produtos coletados: {len(products_data)}")
    print(f"✅ Notícias coletadas: {len(news_data)}")
    
    # Análise de texto dos títulos de jobs
    if jobs_data:
        text_analysis = job_analyzer.analyze_text_data('title')
        print(f"📝 Análise de títulos de vagas:")
        print(f"   - Média de caracteres: {text_analysis.get('average_length', 0):.1f}")
        print(f"   - Palavras mais comuns: {text_analysis.get('most_common_words', [])[:5]}")
    
    # Resumo final
    print("\n🎉 Scraping Concluído!")
    print(f"📁 Dados salvos em: {config.output_path}")
    print(f"📊 Total de registros: {len(jobs_data) + len(products_data) + len(news_data)}")
    
    # Exemplo de uso avançado
    print("\n🔧 Exemplo de Uso Avançado:")
    print("job_scraper = JobScraper(config)")
    print("data = job_scraper.scrape_jobs(['Python Junior'], 'São Paulo')")
    print("job_scraper.save_data(data, 'python_jobs')")

if __name__ == "__main__":
    main()

