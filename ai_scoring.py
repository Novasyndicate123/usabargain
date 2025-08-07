import os
import openai

# You must set your OpenAI API key as an environment variable for security
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(title, description):
    prompt = f"Summarize the following deal for maximum viral appeal:\nTitle: {title}\nDescription: {description}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=60,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def compute_ai_score(title, description):
    prompt = f"Rate the following deal's viral potential on a scale of 0 to 100:\nTitle: {title}\nDescription: {description}\nScore:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=5,
        temperature=0
    )
    score_str = response.choices[0].text.strip()
    try:
        score = float(score_str)
        score = max(0, min(100, score))
    except:
        score = 50  # fallback score
    return score
