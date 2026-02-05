"""
Unified LLM client for Claude, GPT-4o, and Groq.
Provides a consistent interface for all three providers.
"""

import os
import json
import logging
import time
from typing import Dict, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Standardized response from any LLM."""
    content: str
    model: str
    provider: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float = 0.0

    def parse_json(self) -> Dict:
        """Parse JSON from response content."""
        content = self.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        return json.loads(content.strip())


class UnifiedLLMClient:
    """Unified interface for Claude, GPT-4o, and Groq."""

    COST_RATES = {
        "claude-sonnet-4-5-20250929": {"input": 0.003, "output": 0.015},
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "llama-3.3-70b-versatile": {"input": 0.00059, "output": 0.00079},
    }

    def __init__(self):
        self.clients = {}
        self._init_anthropic()
        self._init_openai()
        self._init_groq()
        self.total_cost = 0.0

    def _init_anthropic(self):
        try:
            import anthropic
            self.clients["anthropic"] = anthropic.Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
            logger.info("Anthropic client initialized")
        except Exception as e:
            logger.warning(f"Anthropic not available: {e}")

    def _init_openai(self):
        try:
            import openai
            self.clients["openai"] = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
            logger.info("OpenAI client initialized")
        except Exception as e:
            logger.warning(f"OpenAI not available: {e}")

    def _init_groq(self):
        try:
            from groq import Groq
            self.clients["groq"] = Groq(
                api_key=os.getenv("GROQ_API_KEY")
            )
            logger.info("Groq client initialized")
        except Exception as e:
            logger.warning(f"Groq not available: {e}")

    def is_available(self, provider: str) -> bool:
        return provider in self.clients

    def get_available_providers(self):
        return list(self.clients.keys())

    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        rates = self.COST_RATES.get(model, {"input": 0.01, "output": 0.03})
        return (input_tokens * rates["input"] + output_tokens * rates["output"]) / 1000

    def call(
        self,
        provider: str,
        model: str,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 4000,
        retry_count: int = 2,
        retry_delay: float = 2.0,
    ) -> Optional[LLMResponse]:
        """Call an LLM provider with standardized interface."""
        if provider not in self.clients:
            logger.error(f"Provider {provider} not available")
            return None

        for attempt in range(retry_count + 1):
            try:
                if provider == "anthropic":
                    return self._call_anthropic(model, prompt, system_prompt, temperature, max_tokens)
                elif provider == "openai":
                    return self._call_openai(model, prompt, system_prompt, temperature, max_tokens)
                elif provider == "groq":
                    return self._call_groq(model, prompt, system_prompt, temperature, max_tokens)
            except Exception as e:
                logger.warning(f"Attempt {attempt+1} failed for {provider}: {e}")
                if attempt < retry_count:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    logger.error(f"All retries failed for {provider}/{model}")
                    return None

    def _call_anthropic(self, model, prompt, system_prompt, temperature, max_tokens):
        msgs = [{"role": "user", "content": prompt}]
        kwargs = {"model": model, "max_tokens": max_tokens, "temperature": temperature, "messages": msgs}
        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.clients["anthropic"].messages.create(**kwargs)
        content = response.content[0].text
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cost = self._calculate_cost(model, input_tokens, output_tokens)
        self.total_cost += cost

        return LLMResponse(
            content=content, model=model, provider="anthropic",
            input_tokens=input_tokens, output_tokens=output_tokens, cost=cost
        )

    def _call_openai(self, model, prompt, system_prompt, temperature, max_tokens):
        msgs = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        msgs.append({"role": "user", "content": prompt})

        response = self.clients["openai"].chat.completions.create(
            model=model, messages=msgs, temperature=temperature, max_tokens=max_tokens
        )
        content = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        cost = self._calculate_cost(model, input_tokens, output_tokens)
        self.total_cost += cost

        return LLMResponse(
            content=content, model=model, provider="openai",
            input_tokens=input_tokens, output_tokens=output_tokens, cost=cost
        )

    def _call_groq(self, model, prompt, system_prompt, temperature, max_tokens):
        msgs = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        msgs.append({"role": "user", "content": prompt})

        response = self.clients["groq"].chat.completions.create(
            model=model, messages=msgs, temperature=temperature, max_tokens=max_tokens
        )
        content = response.choices[0].message.content
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        cost = self._calculate_cost(model, input_tokens, output_tokens)
        self.total_cost += cost

        return LLMResponse(
            content=content, model=model, provider="groq",
            input_tokens=input_tokens, output_tokens=output_tokens, cost=cost
        )
