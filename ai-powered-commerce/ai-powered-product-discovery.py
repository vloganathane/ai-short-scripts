#!/usr/bin/env python3
"""
AI-Powered Product Discovery
Uses OpenAI or Anthropic APIs for intelligent product discovery.

Key Components:

AI Query Refinement: Uses Anthropic's Claude API to extract keywords and budget from natural language input
Amazon Search: Scrapes Amazon.in search results with proper headers to avoid blocking
AI-Powered Ranking: Re-ranks products based on relevance to the original query
Clean Output: Displays top 3 recommendations with titles, prices, and links

Setup Requirements:

Install dependencies: 
pip install requests beautifulsoup4 anthropic

Usage Example:
Enter your product need: best budget wireless earbuds under ₹2000 for workouts
🔍 Analyzing your request...
🎯 Searching for: wireless earbuds workout (Budget: ₹2000)

🏆 Top Recommendations:
1. boAt Airdopes 131 Wireless Earbuds with 60H Playback
   💰 ₹1,299
   🔗 https://amazon.in/dp/...

Features:

- Extracts budget constraints automatically
- Filters products by price if budget is specified
- Uses AI to rank products by relevance to user intent
- Handles errors gracefully with timeouts and exception handling
- Lightweight and fast execution

Replace "your_anthropic_api_key_here" with your actual Anthropic API key to use the script. 
The script respects Amazon's structure and includes proper headers for ethical scraping.

"""
import requests
from bs4 import BeautifulSoup
import anthropic
import re
from urllib.parse import quote

# Configuration
ANTHROPIC_API_KEY = "your_anthropic_api_key_here"
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def refine_query(user_input):
    """Use AI to extract key search terms and budget from user input"""
    prompt = f"Extract search keywords and budget from: '{user_input}'. Return only: keywords|budget_max"
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=50,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()

def search_amazon(query, max_price=None):
    """Search Amazon and extract product info"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    url = f"https://www.amazon.in/s?k={quote(query)}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        
        for item in soup.find_all('div', {'data-component-type': 's-search-result'})[:5]:
            title_elem = item.find('h2', class_='a-size-mini')
            price_elem = item.find('span', class_='a-price-whole')
            link_elem = item.find('h2').find('a') if item.find('h2') else None
            
            if title_elem and price_elem and link_elem:
                title = title_elem.get_text().strip()
                price_text = price_elem.get_text().replace(',', '')
                price = int(re.findall(r'\d+', price_text)[0]) if re.findall(r'\d+', price_text) else 0
                link = "https://amazon.in" + link_elem.get('href')
                
                if not max_price or price <= max_price:
                    products.append({'title': title[:80], 'price': price, 'link': link})
        
        return products[:3]
    except Exception as e:
        print(f"Search error: {e}")
        return []

def rank_products(products, original_query):
    """Use AI to rank products by relevance"""
    if not products:
        return []
    
    product_text = "\n".join([f"{i+1}. {p['title']} - ₹{p['price']}" for i, p in enumerate(products)])
    prompt = f"Rank these products for query '{original_query}' by relevance (1-3): \n{product_text}\nReturn only numbers: 1,2,3"
    
    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=20,
            messages=[{"role": "user", "content": prompt}]
        )
        ranking = [int(x)-1 for x in response.content[0].text.strip().split(',')]
        return [products[i] for i in ranking if i < len(products)]
    except:
        return products

def main():
    user_query = input("Enter your product need: ")
    print("🔍 Analyzing your request...")
    
    # Refine query with AI
    refined = refine_query(user_query)
    parts = refined.split('|')
    keywords = parts[0] if parts else user_query
    budget = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
    
    print(f"🎯 Searching for: {keywords}" + (f" (Budget: ₹{budget})" if budget else ""))
    
    # Search and rank products
    products = search_amazon(keywords, budget)
    ranked_products = rank_products(products, user_query)
    
    # Display results
    print("\n🏆 Top Recommendations:")
    for i, product in enumerate(ranked_products, 1):
        print(f"{i}. {product['title']}")
        print(f"   💰 ₹{product['price']}")
        print(f"   🔗 {product['link']}\n")

if __name__ == "__main__":
    main()