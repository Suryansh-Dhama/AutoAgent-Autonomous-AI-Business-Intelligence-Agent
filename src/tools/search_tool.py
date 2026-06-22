from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query: str) -> str:
    """Real-time web search karta hai"""
    try:
        response = client.search(
            query=query,
            search_depth="basic",
            max_results=3
        )
        
        results = []
        for r in response["results"]:
            results.append(f"Title: {r['title']}\nContent: {r['content']}\n")
        
        return "\n".join(results)
    
    except Exception as e:
        return f"Search error: {str(e)}"

if __name__ == "__main__":
    result = web_search("Latest AI news today")
    print("=== SEARCH RESULTS ===")
    print(result)