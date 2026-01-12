import requests
from bs4 import BeautifulSoup


def web_search(query, num_results=5):
    """
    Reliable Bing HTML search (works in Colab & locally).
    """
    url = f"https://www.bing.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)

    soup = BeautifulSoup(r.text, "html.parser")
    links = []

    for a in soup.select("li.b_algo h2 a"):
        href = a.get("href")
        if href and href.startswith("http"):
            links.append(href)
        if len(links) >= num_results:
            break

    return links


def read_webpage(url, max_chars=4000):
    """
    Fetch and clean webpage text.
    Rejects junk / redirect / JS-only pages.
    """
    r = requests.get(
        url,
        timeout=10,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = " ".join(soup.stripped_strings)

    junk_signals = [
        "enable javascript",
        "cookies",
        "redirecting",
        "access denied",
        "not found",
        "loading..."
    ]

    if len(text) < 500:
        raise ValueError("Page too short")

    if any(js in text.lower() for js in junk_signals):
        raise ValueError("Junk or redirect page")

    return text[:max_chars]