from typing import Literal

from homeassistant.components import conversation
from homeassistant.components.conversation.models import (
    ConversationInput,
    ConversationResult,
)
from homeassistant.helpers import intent



class MockAgent(conversation.AbstractConversationAgent):
    """Test Agent."""

    def __init__(
        self, agent_id: str, supported_languages: list[str] | Literal["*"]
    ) -> None:
        """Initialize the agent."""
        self.agent_id = agent_id
        self.calls = []
        self.response = "Test response"
        self._supported_languages = supported_languages

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return self._supported_languages

    async def async_process(self, user_input: ConversationInput) -> ConversationResult:
        """Process some text."""
        self.calls.append(user_input)
        response = intent.IntentResponse(language=user_input.language)
        response.async_set_speech(self.response)
        return ConversationResult(
            response=response, conversation_id=user_input.conversation_id
        )