from bs4 import BeautifulSoup
import requests


# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_contents(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # 1. Get Title
        title = soup.title.string if soup.title else "No title"
        
        # 2. Clean irrelevant tags
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
            
        # 3. Target main text tags ONLY (p, h1, h2, h3)
        # This removes 90% of the 'ununderstandable' noise
        main_content = [t.get_text(strip=True) for t in soup.find_all(['p', 'h1', 'h2', 'h3'])]
        text = "\n".join(main_content)
        
        return f"Title: {title}\n\nContent:\n{text}"[:2000]
    except Exception as e:
        return f"Error fetching site: {e}"


def fetch_website_links(url):
    """
    Return the links on the webiste at the given url
    I realize this is inefficient as we're parsing twice! This is to keep the code in the lab simple.
    Feel free to use a class and optimize it!
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]
