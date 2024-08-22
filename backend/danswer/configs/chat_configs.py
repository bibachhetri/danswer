import os


PROMPTS_YAML = "./danswer/chat/prompts.yaml"
PERSONAS_YAML = "./danswer/chat/personas.yaml"
INPUT_PROMPT_YAML = "./danswer/chat/input_prompts.yaml"

NUM_RETURNED_HITS = 50
# Used for LLM filtering and reranking
# We want this to be approximately the number of results we want to show on the first page
# It cannot be too large due to cost and latency implications
NUM_POSTPROCESSED_RESULTS = 20

# May be less depending on model
MAX_CHUNKS_FED_TO_CHAT = float(os.environ.get("MAX_CHUNKS_FED_TO_CHAT") or 10.0)
# For Chat, need to keep enough space for history and other prompt pieces
# ~3k input, half for docs, half for chat history + prompts
CHAT_TARGET_CHUNK_PERCENTAGE = 512 * 3 / 3072

# For selecting a different LLM question-answering prompt format
# Valid values: default, cot, weak
QA_PROMPT_OVERRIDE = os.environ.get("QA_PROMPT_OVERRIDE") or None
# 1 / (1 + DOC_TIME_DECAY * doc-age-in-years), set to 0 to have no decay
# Capped in Vespa at 0.5
DOC_TIME_DECAY = float(
    os.environ.get("DOC_TIME_DECAY") or 0.5  # Hits limit at 2 years by default
)
BASE_RECENCY_DECAY = 0.5
FAVOR_RECENT_DECAY_MULTIPLIER = 2.0
# Currently this next one is not configurable via env
DISABLE_LLM_QUERY_ANSWERABILITY = QA_PROMPT_OVERRIDE == "weak"
# For the highest matching base size chunk, how many chunks above and below do we pull in by default
# Note this is not in any of the deployment configs yet
# Currently only applies to search flow not chat
CONTEXT_CHUNKS_ABOVE = int(os.environ.get("CONTEXT_CHUNKS_ABOVE") or 1)
CONTEXT_CHUNKS_BELOW = int(os.environ.get("CONTEXT_CHUNKS_BELOW") or 1)
# Whether the LLM should be used to decide if a search would help given the chat history
DISABLE_LLM_CHOOSE_SEARCH = (
    os.environ.get("DISABLE_LLM_CHOOSE_SEARCH", "").lower() == "true"
)
DISABLE_LLM_QUERY_REPHRASE = (
    os.environ.get("DISABLE_LLM_QUERY_REPHRASE", "").lower() == "true"
)
# 1 edit per 20 characters, currently unused due to fuzzy match being too slow
QUOTE_ALLOWED_ERROR_PERCENT = 0.05
QA_TIMEOUT = int(os.environ.get("QA_TIMEOUT") or "60")  # 60 seconds
# Weighting factor between Vector and Keyword Search, 1 for completely vector search
HYBRID_ALPHA = max(0, min(1, float(os.environ.get("HYBRID_ALPHA") or 0.5)))
HYBRID_ALPHA_KEYWORD = max(
    0, min(1, float(os.environ.get("HYBRID_ALPHA_KEYWORD") or 0.4))
)
# Weighting factor between Title and Content of documents during search, 1 for completely
# Title based. Default heavily favors Content because Title is also included at the top of
# Content. This is to avoid cases where the Content is very relevant but it may not be clear
# if the title is separated out. Title is most of a "boost" than a separate field.
TITLE_CONTENT_RATIO = max(
    0, min(1, float(os.environ.get("TITLE_CONTENT_RATIO") or 0.10))
)

# A list of languages passed to the LLM to rephase the query
# For example "English,French,Spanish", be sure to use the "," separator
MULTILINGUAL_QUERY_EXPANSION = os.environ.get("MULTILINGUAL_QUERY_EXPANSION") or None
LANGUAGE_HINT = "\n" + (
    os.environ.get("LANGUAGE_HINT")
    or "IMPORTANT: Respond in the same language as my query!"
)
LANGUAGE_CHAT_NAMING_HINT = (
    os.environ.get("LANGUAGE_CHAT_NAMING_HINT")
    or "The name of the conversation must be in the same language as the user query."
)

# Agentic search takes significantly more tokens and therefore has much higher cost.
# This configuration allows users to get a search-only experience with instant results
# and no involvement from the LLM.
# Additionally, some LLM providers have strict rate limits which may prohibit
# sending many API requests at once (as is done in agentic search).
# Whether the LLM should evaluate all of the document chunks passed in for usefulness
# in relation to the user query
DISABLE_LLM_DOC_RELEVANCE = (
    os.environ.get("DISABLE_LLM_DOC_RELEVANCE", "").lower() == "true"
)

# Stops streaming answers back to the UI if this pattern is seen:
STOP_STREAM_PAT = os.environ.get("STOP_STREAM_PAT") or None

# The backend logic for this being True isn't fully supported yet
HARD_DELETE_CHATS = False

# Internet Search
BING_API_KEY = os.environ.get("BING_API_KEY") or None
