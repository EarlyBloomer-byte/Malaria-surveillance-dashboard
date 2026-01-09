import google.generativeai as genai
import streamlit as st

# Configure the AI
def setup_ai(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-3-flash-preview')

def get_ai_response(model, user_query, dashboard_context):
    """
    Sends the user query along with the current dashboard data to the AI.
    """
    system_prompt = f"""
    You are the 'Malaria Surveillance AI Advisor', an expert consultant trained on WHO 2025 protocols.
    
    CURRENT DATA CONTEXT:
    {dashboard_context}
    
    INSTRUCTIONS:
    1. Use the provided context to answer questions. 
    2. If cases are high, suggest interventions like 'Indoor Residual Spraying' or 'Distributing Insecticide-Treated Nets'.
    3. Refer to the '2nd Edition of WHO Malaria Surveillance Manual (2025)' when giving advice.
    4. Keep answers professional, concise, and action-oriented.
    """
    
    full_prompt = f"{system_prompt}\n\nUser Question: {user_query}"
    
    response = model.generate_content(full_prompt)
    return response.text