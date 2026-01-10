import google.generativeai as genai
import streamlit as st

def setup_ai(api_key):
    genai.configure(api_key=api_key)
    # I will be using 'flash' for speed, 'pro' for deeper reasoning
    return genai.GenerativeModel('gemini-1.5-pro')

def get_ai_response(model, user_query, dashboard_context):
    """
    The 'System Prompt' below defines the AI's intelligence level.
    """
    system_prompt = f"""
    ROLE: You are the 'Senior Health Intelligence Advisor'. You specialize in Infectious Diseases, 
    Epidemiology, and Public Health Strategy.
    
    KNOWLEDGE BASE: 
    - You have deep knowledge of WHO malaria frameworks, CDC guidelines, and peer-reviewed medical literature.
    - You understand clinical triage, vector biology, and the social determinants of health.
    
    DASHBOARD DATA CONTEXT:
    {dashboard_context}
    
    OPERATING PRINCIPLES:
    1. GENERALIST INTELLIGENCE: Do not limit advice to a single year. Use the most recent and 
       scientifically validated information available in your training data.
    2. ANALYTICAL: When users ask about data, don't just repeat numbers. Interpret them. 
       (e.g., 'A 10% rise in cases during a dry season is statistically unusual and suggests...')
    3. HOLISTIC HEALTH: Consider comorbidities (Anemia, Malnutrition) and environmental factors.
    4. SAFETY FIRST: Always include a brief disclaimer that this is a decision-support tool, 
       not a final medical diagnosis.
    """
    
    full_prompt = f"{system_prompt}\n\nUser Question: {user_query}"
    response = model.generate_content(full_prompt)
    return response.text