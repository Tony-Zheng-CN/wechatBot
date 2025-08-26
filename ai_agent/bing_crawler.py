# bing_crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

def search_bing(query: str, limit: int = 3) -> list[dict]:
    try:
        """
        返回格式:
        [
            {"title": "...", "url": "...", "snippet": "..."},
            ...
        ]
        """
        url = f"https://www.bing.com/search?q={quote_plus(query)}&count={limit}"
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")
        results = []
        for li in soup.select("li.b_algo"):
            title_tag = li.select_one("h2 a")
            if not title_tag:
                continue
            results.append({
                "title": title_tag.get_text(strip=True),
                "url": title_tag["href"],
                "snippet": (li.select_one("p") or li.select_one(".b_caption p") or "").get_text(strip=True)
            })
        return results
    except Exception as e:
        print(f"[Error]Bing Crawler: {e}")
        return []

if __name__ == "__main__":
    print(search_bing("python"))