from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_ai_summary(repository_context):
    """
    Production-grade summary generator that intelligently formats 
    complex repository contexts (lists, dicts, or strings).
    """
    
    context_str = str(repository_context) # Default
    
    if isinstance(repository_context, dict):
        formatted_parts = []
        for k, v in repository_context.items():
            # Agar list hai, toh use clean multi-line string mein convert karein
            if isinstance(v, list):
                val_str = "\n".join(map(str, v))
            else:
                val_str = str(v)
            
            formatted_parts.append(f"=== {k.upper()} ===\n{val_str}")
        
        context_str = "\n\n".join(formatted_parts)

    prompt = f"""
You are a Principal Software Engineer and Developer Onboarding Expert.
Analyze the repository context provided below and generate a professional Developer Onboarding Report.

IMPORTANT RULES:
- Use ONLY the provided repository context.
- If information is missing, write "Not identified from repository context."
- Return the response in the specified format.

# PROJECT OVERVIEW
- What problem it solves, why it exists, who uses it.

# TECH STACK
- Languages, Frameworks, Libraries, Tools.

# CORE FEATURES
- Bulleted list of key features.

# HOW IT WORKS
- Simple workflow steps.

# REPOSITORY STRUCTURE INSIGHTS
- Important files/folders.

# DEVELOPER ONBOARDING GUIDE
- Where to start, important files, concepts to learn.

# POTENTIAL USE CASES

# COMPLEXITY ASSESSMENT
- Level (Beginner/Intermediate/Advanced) and Reason.

---
REPOSITORY CONTEXT:
{context_str}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating AI summary: {e}")
        return "Summary could not be generated due to an internal error."