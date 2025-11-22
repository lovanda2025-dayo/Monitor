import requests
from bs4 import BeautifulSoup

# Função para fazer scraping do último post de uma página do Facebook
def get_last_post(page_url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
    }

    try:
        html = requests.get(page_url, headers=headers, timeout=10).text
    except:
        return None

    soup = BeautifulSoup(html, "html5lib")

    # Tenta achar posts por padrões comuns (Facebook é dinâmico, mas isso funciona para mobile)
    possible_posts = soup.find_all("div")
    texts = []

    for post in possible_posts:
        text = post.get_text(strip=True)
        if text and len(text) > 30:
            texts.append(text)

    if not texts:
        return None

    return texts[0]  # devolve o primeiro post encontrado