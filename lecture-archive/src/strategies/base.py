from abc import ABC, abstractmethod

from src.agent.context import AgentContext
from src.agent.models import ExecutionResult


class DownloadStrategy(ABC):
    name: str

    @abstractmethod
    async def can_handle(self, context: AgentContext) -> bool: ...

    @abstractmethod
    async def execute(self, context: AgentContext) -> ExecutionResult: ...

