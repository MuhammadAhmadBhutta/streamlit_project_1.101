# modules/generator.py

import google.generativeai as genai

# Replace with your Gemini API key
genai.configure(api_key="")

def generate_action_plan(opportunities: str):
    """
    Uses Google Gemini 1.5 Flash to generate a business action plan.
    """
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    You are an expert business consultant.
    Given these detected opportunities:\n{opportunities}\n
    Write a clear, step-by-step action plan with:
    - Suggested product or service improvements
    - Pricing & discount strategies
    - Marketing ideas
    - Risk assessment
    - Tips to boost profit for loss-making areas
    """

    response = model.generate_content(prompt)

    plan = response.text.strip()
    return plan
