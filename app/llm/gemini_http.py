from typing import Any

import httpx
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import Field


def _text_content(content: str | list[str | dict]) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
        return "\n".join(parts)
    return str(content)


def _to_gemini_payload(messages: list[BaseMessage]) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    system_lines: list[str] = []
    contents: list[dict[str, Any]] = []

    for message in messages:
        if isinstance(message, SystemMessage):
            system_lines.append(_text_content(message.content))
        elif isinstance(message, HumanMessage):
            contents.append(
                {"role": "user", "parts": [{"text": _text_content(message.content)}]},
            )
        elif isinstance(message, AIMessage):
            contents.append(
                {"role": "model", "parts": [{"text": _text_content(message.content)}]},
            )

    system_instruction = None
    if system_lines:
        system_instruction = {"parts": [{"text": "\n".join(system_lines)}]}
    return system_instruction, contents


def _check_gemini_response(response: httpx.Response) -> None:
    if response.is_success:
        return
    detail = response.text
    try:
        detail = response.json().get("error", detail)
    except Exception:
        pass
    raise RuntimeError(f"Gemini API {response.status_code}: {detail}")


class GeminiHttpChatModel(BaseChatModel):
    model: str = Field(description="Gemini model id, e.g. gemini-2.5-flash")
    api_key: str = Field(repr=False)
    temperature: float = 0
    timeout: float = 120.0

    @property
    def _llm_type(self) -> str:
        return "gemini-http"

    def _build_url(self) -> str:
        return (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent"
        )

    def _build_body(
        self,
        messages: list[BaseMessage],
        *,
        stop: list[str] | None,
    ) -> dict[str, Any]:
        system_instruction, contents = _to_gemini_payload(messages)
        body: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {"temperature": self.temperature},
        }
        if system_instruction is not None:
            body["systemInstruction"] = system_instruction
        if stop:
            body["generationConfig"]["stopSequences"] = stop
        return body

    def _parse_response(self, data: dict[str, Any]) -> str:
        candidates = data.get("candidates") or []
        if not candidates:
            raise RuntimeError(f"Gemini returned no candidates: {data}")
        parts = candidates[0].get("content", {}).get("parts") or []
        texts = [part.get("text", "") for part in parts if "text" in part]
        if not texts:
            raise RuntimeError(f"Gemini returned no text: {data}")
        return "\n".join(texts)

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        body = self._build_body(messages, stop=stop)
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                self._build_url(),
                params={"key": self.api_key},
                json=body,
            )
            _check_gemini_response(response)
            text = self._parse_response(response.json())
        generation = ChatGeneration(message=AIMessage(content=text))
        return ChatResult(generations=[generation])

    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        body = self._build_body(messages, stop=stop)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self._build_url(),
                params={"key": self.api_key},
                json=body,
            )
            _check_gemini_response(response)
            text = self._parse_response(response.json())
        generation = ChatGeneration(message=AIMessage(content=text))
        return ChatResult(generations=[generation])
