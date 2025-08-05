#!/usr/bin/env python3
"""
AI-Powered Marketing Content Generator
Uses OpenAI or Anthropic APIs for intelligent product content generation.

This compact AI agent provides a complete solution for generating marketing content in under 50 lines. Here's what it does:
Key Features:

Multi-provider support: Works with both OpenAI and Anthropic APIs
Content types: Generates product titles, descriptions, meta tags, and blog posts
JSON output: Returns structured data ready for integration
Error handling: Gracefully handles API failures
Customizable: Easy to modify prompts or add new content types

Usage:

Replace "your-api-key-here" with your actual API key
Choose provider: "openai" or "anthropic"
Call generate_json_output() with your product information

Example output structure:
{
  "title": "Premium Wireless Bluetooth Headphones - Noise Cancelling",
  "description": "Experience crystal-clear audio with these premium wireless headphones...",
  "meta_title": "Best Wireless Bluetooth Headphones | Noise Cancelling Audio",
  "meta_description": "Discover premium wireless Bluetooth headphones with advanced noise cancellation...",
  "blog_post": "In today's fast-paced world, quality audio matters more than ever..."
}
The agent is production-ready and can be easily integrated into e-commerce platforms, content management systems, or marketing automation workflows.
"""
import json
import requests
from typing import Dict, Any

class AIContentGenerator:
    def __init__(self, api_key: str, provider: str = "openai"):
        self.api_key = api_key
        self.provider = provider
        self.endpoints = {
            "openai": "https://api.openai.com/v1/chat/completions",
            "anthropic": "https://api.anthropic.com/v1/messages"
        }
    
    def _make_request(self, prompt: str) -> str:
        if self.provider == "openai":
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            data = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": prompt}], "max_tokens": 500}
            response = requests.post(self.endpoints["openai"], headers=headers, json=data)
            return response.json()["choices"][0]["message"]["content"]
        elif self.provider == "anthropic":
            headers = {"x-api-key": self.api_key, "Content-Type": "application/json", "anthropic-version": "2023-06-01"}
            data = {"model": "claude-3-sonnet-20240229", "max_tokens": 500, "messages": [{"role": "user", "content": prompt}]}
            response = requests.post(self.endpoints["anthropic"], headers=headers, json=data)
            return response.json()["content"][0]["text"]
    
    def generate_product_content(self, product_info: str) -> Dict[str, Any]:
        prompts = {
            "title": f"Create a compelling product title for: {product_info}. Max 60 characters.",
            "description": f"Write a 2-3 sentence product description for: {product_info}",
            "meta_title": f"Create an SEO meta title (50-60 chars) for: {product_info}",
            "meta_description": f"Create an SEO meta description (150-160 chars) for: {product_info}",
            "blog_post": f"Write a 200-word blog post about the benefits of: {product_info}"
        }
        
        results = {}
        for content_type, prompt in prompts.items():
            try:
                results[content_type] = self._make_request(prompt).strip()
            except Exception as e:
                results[content_type] = f"Error generating {content_type}: {str(e)}"
        
        return results
    
    def generate_json_output(self, product_info: str) -> str:
        content = self.generate_product_content(product_info)
        return json.dumps(content, indent=2)

# Usage example
if __name__ == "__main__":
    # Initialize with your API key
    generator = AIContentGenerator("your-api-key-here", "openai")  # or "anthropic"
    
    # Generate content for a product
    product = "Wireless Bluetooth Headphones with Noise Cancellation"
    result = generator.generate_json_output(product)
    print(result)