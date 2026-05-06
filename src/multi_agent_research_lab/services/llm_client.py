import logging
from dataclasses import dataclass

from langchain_google_genai import ChatGoogleGenerativeAI
from tenacity import retry, stop_after_attempt, wait_exponential

from multi_agent_research_lab.core.config import get_settings


@dataclass(frozen=True)
class LLMResponse:
    content: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None


class LLMClient:
    """Gemini LLM client."""

    def __init__(self) -> None:
        self.settings = get_settings()
        if not self.settings.google_api_key:
            logging.warning("GOOGLE_API_KEY not set. LLM calls will fail.")
        
        self.client = ChatGoogleGenerativeAI(
            model=self.settings.google_model,
            google_api_key=self.settings.google_api_key,
            project=self.settings.gcp_project_id,
            temperature=0,
            timeout=self.settings.timeout_seconds,
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Return a model completion from Gemini."""
        
        messages = [
            ("system", system_prompt),
            ("user", user_prompt),
        ]
        
        response = self.client.invoke(messages)
        
        # Track tokens (Gemini uses usage_metadata in newer langchain-google-genai versions)
        usage = getattr(response, "usage_metadata", {})
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")
        
        # Fallback to response_metadata if usage_metadata is empty
        if not input_tokens:
            usage = response.response_metadata.get("token_usage", {})
            input_tokens = usage.get("prompt_tokens")
            output_tokens = usage.get("completion_tokens")
        
        # Simple cost estimation for gemini-2.0-flash / 1.5-flash
        cost = 0.0
        if input_tokens and output_tokens:
            # $0.075 / 1M tokens input, $0.3 / 1M tokens output
            cost = (input_tokens * 0.000000075) + (output_tokens * 0.0000003)

        return LLMResponse(
            content=str(response.content),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
        )
