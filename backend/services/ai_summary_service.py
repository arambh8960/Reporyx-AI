import os
import json
import logging
from typing import Any, Union
from dotenv import load_dotenv
from groq import Groq, APIConnectionError, RateLimitError, APIStatusError

load_dotenv()

logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Consistent production model
DEFAULT_MODEL = "openai/gpt-oss-120b"


def _format_context(context: Union[dict, list, str], max_chars: int = 120_000) -> str:
    """Format and guard repository context size."""
    if isinstance(context, (dict, list)):
        formatted = json.dumps(
            context,
            indent=2,
            ensure_ascii=False,
            default=str
        )
    else:
        formatted = str(context).strip()

    if len(formatted) > max_chars:
        logger.warning(f"Context length ({len(formatted)} chars) exceeds threshold. Truncating.")
        return formatted[:max_chars] + "\n\n[Context truncated due to size limits]"

    return formatted


def generate_ai_summary(
    repository_context: Any,
    project_name: str = "the project",
    model: str = DEFAULT_MODEL
) -> str:
    """
    Generate a concise, 7-section developer onboarding report.
    Guaranteed no tables, no raw pipe characters, and no meta-commentary.
    """
    context_str = _format_context(repository_context)

    if not context_str.strip():
        return "Insufficient repository context to generate a summary."

    system_instruction = (
        "You are a Staff Software Architect writing crisp, production-grade internal "
        "onboarding documentation for an engineering team. You state technical facts directly, "
        "cite concrete implementation files, and strictly avoid boilerplate or decorative language."
    )

    prompt = f"""You are a Senior Software Engineer creating technical documentation for developers joining an existing project.
Analyze the repository context and write a professional, concise, and easy-to-understand Developer Onboarding Report for {project_name}.

STRICT CONTENT & VOICE RULES:
1. Ground every point strictly in verified repository evidence.
2. Never invent features, APIs, tools, or dependencies.
3. Do not quote README text or reference README metadata (e.g., NEVER say 'indicated by badge', 'according to README', or 'as stated in markdown'). State technical facts directly.
4. Keep paragraphs short (maximum 3 sentences).
5. Prefer concrete file paths (`src/...`, `app.py`, etc.) over vague descriptions.
6. If an item cannot be confirmed, write exactly: 'Not identified from repository context.'
7. Avoid meta-commentary or repetitive filler.

STRICT FORMATTING RULES (CRITICAL):
- Use clean Markdown with proper headings (## and ###).
- Use standard bullet points (- item).
- ABSOLUTELY NO TABLES: Do not use Markdown tables under any circumstances.
- FORBIDDEN CHARACTER: Never output the pipe character (|). Do not attempt ASCII tables or column alignments.
- ABSOLUTELY NO RAW HTML: No <div>, <br>, <span>, or <p> tags.
- Keep bold text minimal and strictly limited to sub-labels (e.g., - **Component**: description).

REPORT STRUCTURE (EXACTLY 7 SECTIONS):

# Developer Onboarding Report — {project_name}

## 1. Project Overview
Explain what the project does, the core engineering problem it solves, and its primary audience in 2 to 3 concise sentences.

## 2. Technology Stack
Group verified technologies into bullet points. For each item, state its practical role in one concise sentence:
- **Languages**: 
- **Frontend**: 
- **Backend**: 
- **Database / Storage**: 
- **AI/ML & Data Processing**: 
- **Tools & Infrastructure**: 
(If a category is absent in the codebase, mark it as 'Not identified from repository context.')

## 3. Key Features
List the main functional capabilities of the system.
- Format each feature on two clean lines:
  - **Feature Name**: What the feature does from an end-user/system perspective.
  - *Implemented in*: Path(s) to the actual files handling this logic (or 'Not identified from repository context').

## 4. System Architecture
Explain how the system pieces connect:
- High-level architecture pattern (e.g., client-server, monolithic ML pipeline, event-driven).
- Data flow: How requests move from user input through processing/ML inference to output.
- Inter-component communication protocols or internal data handoffs.

## 5. Execution Workflow
Provide a numbered step-by-step trace of what happens at runtime:
1. Application initialization and dependency loading.
2. Dataset/model loading or backend startup.
3. User interaction, input processing, and validation.
4. Core logic or inference execution.
5. Response dispatch and rendering.

## 6. Important Files & Responsibilities
Highlight only the 4 to 6 most critical files in the codebase:
- `path/to/file`: Primary responsibility, key functions/classes it contains, and which files it imports or feeds into.

## 7. Getting Started
Provide an actionable quickstart guide for a developer:
- **Prerequisites**: Required runtimes, package managers, and external tools.
- **Environment Setup**: Verified config files, virtual environment setup, and dependency install commands found in the repo.
- **Local Execution**: Exact run commands to spin up the local server or application.
- **Where to Begin Reading**: Recommend the first 2 files a new developer should open to understand the system.

<repository_context>
{context_str}
</repository_context>

Generate the 7-section Developer Onboarding Report now:"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Keeps the model strictly compliant with the structure
            max_tokens=4096,
            top_p=0.9
        )
        return response.choices[0].message.content

    except RateLimitError:
        logger.error("Groq API rate limit reached.")
        return "Summary generation temporarily unavailable due to rate limits."
    except APIConnectionError:
        logger.error("Network error communicating with Groq API.")
        return "Summary generation failed due to a network connection error."
    except APIStatusError as e:
        logger.error(f"Groq API returned an error ({e.status_code}): {e.message}")
        return f"Summary generation failed due to API error ({e.status_code})."
    except Exception as e:
        logger.exception(f"Unexpected error in summary generation: {e}")
        return "An unexpected error occurred while generating the onboarding report."