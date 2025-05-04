import os
import logging
from dotenv import load_dotenv
# Remove direct import if using client
# import openai
# Import the new client classes
from openai import AsyncOpenAI, OpenAIError

logger = logging.getLogger(__name__)
load_dotenv()

# --- OpenAI Client Setup --- 
# Use the new client initialization for openai >= 1.0.0
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    logger.warning("OPENAI_API_KEY not found in environment variables. LLM calls will fail.")
    # Set client to None or handle differently if key is missing
    client = None
else:
    try:
        client = AsyncOpenAI(api_key=API_KEY)
        logger.info("AsyncOpenAI client initialized.")
    except Exception as e:
        logger.exception("Failed to initialize AsyncOpenAI client")
        client = None

# --- Comment out or remove legacy setup --- 
# # For openai < 1.0.0 (older style)
# openai.api_key = os.getenv("OPENAI_API_KEY")
# if not openai.api_key:
#     logger.warning("OPENAI_API_KEY not found in environment variables. LLM calls will fail.")
#     # Optionally raise an error, or allow fallback/mocking
#     # raise ValueError("OPENAI_API_KEY is not set.")

# --- LLM Call Function --- 
async def call_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    """Calls the specified OpenAI model with the given prompt using the new client."""
    if not client:
        logger.error("OpenAI client not initialized. Cannot call LLM.")
        return "Error: LLM client not configured."

    logger.info(f"Calling LLM model {model}...")
    try:
        # --- Use the new client method --- 
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful financial analyst assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        content = response.choices[0].message.content.strip()
        logger.info(f"LLM call successful. Response length: {len(content)}")
        return content

        # --- Comment out or remove legacy call --- 
        # # --- Using openai library < 1.0.0 (Legacy) ---
        # response = await openai.ChatCompletion.acreate(
        #     model=model,
        #     messages=[
        #         {"role": "system", "content": "You are a helpful financial analyst assistant."},
        #         {"role": "user", "content": prompt}
        #     ],
        #     temperature=0.3
        # )
        # content = response.choices[0].message.content.strip()
        # logger.info(f"LLM call successful. Response length: {len(content)}")
        # return content

    except OpenAIError as e:
        # Catch specific OpenAI errors if needed
        logger.exception(f"OpenAI API error calling model {model}: {e}")
        return f"Error: OpenAI API call failed - {e}"
    except Exception as e:
        # Catch other potential errors
        logger.exception(f"Unexpected error calling LLM model {model}: {e}")
        return f"Error: LLM call failed unexpectedly - {e}" 