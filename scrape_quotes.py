import json
import time
import sys
from pathlib import Path
from typing import Dict, List
import requests
from bs4 import BeautifulSoup

BASE = "http://quotes.toscrape.com"

def get_soup(url: str) -> BeautifulSoup:
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def scrape():
    quotes: List[dict] = []
    authors: Dict[str, dict] = {}  # ключ — повне ім'я

    page_url = f"{BASE}/"
    while True:
        soup = get_soup(page_url)

        for q in soup.select(".quote"):
            text = q.select_one(".text").get_text(strip=True)
            author_name = q.select_one(".author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in q.select(".tags a.tag")]

            quotes.append({
                "tags": tags,
                "author": author_name,
                "quote": text
            })

            # зберемо посилання на сторінку автора, щоб витягти деталі
            if author_name not in authors:
                rel = q.select_one("span a")["href"]  # /author/Albert-Einstein
                authors[author_name] = {"_author_url": BASE + rel}

        # пагінація
        next_btn = soup.select_one("li.next a")
        if not next_btn:
            break
        page_url = BASE + next_btn["href"]
        time.sleep(0.25)  # трішки ввічливості

    # дозбираємо дані про авторів з їхніх сторінок
    for name, data in list(authors.items()):
        soup = get_soup(data["_author_url"])
        born_date = soup.select_one(".author-born-date").get_text(strip=True)
        born_location = soup.select_one(".author-born-location").get_text(strip=True).replace("in ", "", 1)
        description = soup.select_one(".author-description").get_text(strip=True)

        authors[name] = {
            "fullName": name,
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        }
        time.sleep(0.2)

    # запис у файли
    out_authors = sorted(authors.values(), key=lambda x: x["fullName"])
    out_quotes = quotes

    Path("authors.json").write_text(json.dumps(out_authors, ensure_ascii=False, indent=2), encoding="utf-8")
    Path("quotes.json").write_text(json.dumps(out_quotes, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Готово ✅  Збережено {len(out_authors)} авторів у authors.json та {len(out_quotes)} цитат у quotes.json")

if __name__ == "__main__":
    try:
        scrape()
    except requests.HTTPError as e:
        print("HTTP помилка:", e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print("Неочікувана помилка:", e, file=sys.stderr)
        sys.exit(1)
