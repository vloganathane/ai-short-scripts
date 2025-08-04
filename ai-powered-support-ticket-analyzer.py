#!/usr/bin/env python3
"""
AI-Powered Support Ticket Analyzer
Uses OpenAI or Anthropic APIs for intelligent ticket triage.
"""

import json
import os
from openai import OpenAI
# Alternative: from anthropic import Anthropic

def analyze_ticket_with_openai(ticket_id, message):
    """Analyze ticket using OpenAI API."""
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    prompt = f"""
    Analyze this support ticket and return JSON with these fields:
    - summary: Brief 1-2 sentence summary
    - category: "Bug", "Feature Request", or "Billing Issue"  
    - sentiment: "Positive", "Neutral", or "Negative"
    - urgency: "Low", "Medium", or "High"
    - suggested_action: Recommended next step
    
    Ticket: {message}
    
    Return only valid JSON.
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    return json.loads(response.choices[0].message.content)

def analyze_ticket_with_anthropic(ticket_id, message):
    """Analyze ticket using Anthropic API."""
    # Uncomment and install: pip install anthropic
    # client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    # 
    # response = client.messages.create(
    #     model="claude-3-sonnet-20240229",
    #     max_tokens=200,
    #     messages=[{
    #         "role": "user", 
    #         "content": f"Analyze this support ticket and return JSON: {message}"
    #     }]
    # )
    # return json.loads(response.content[0].text)
    pass

def format_output(result):
    """Format the analysis result."""
    print(f"Summary: {result['summary']}")
    print(f"Category: {result['category']}")
    print(f"Sentiment: {result['sentiment']}")
    print(f"Urgency: {result['urgency']}")
    print(f"Suggested Action: {result['suggested_action']}")

# Example usage
if __name__ == "__main__":
    # Set your API key: export OPENAI_API_KEY="your-key-here"
    
    ticket_msg = "Hi, I was charged twice for my subscription this month. Please look into this and issue a refund ASAP. This is very frustrating!"
    
    try:
        result = analyze_ticket_with_openai("12345", ticket_msg)
        format_output(result)
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set OPENAI_API_KEY environment variable")
