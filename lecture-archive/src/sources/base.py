from abc import ABC, abstractmethod

from src.agent.context import AgentContext
from src.agent.models import Observation


class SourceObserver(ABC):
    @abstractmethod
    async def inspect(self, context: AgentContext) -> Observation: ...

