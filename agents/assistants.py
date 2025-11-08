from pydantic_ai import Agent
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..utils import AgentConfigs


class BookmarkAssistant():
    def __init__(self, configs: "AgentConfigs"):
        self.configs = configs

    
    @property
    def _Agent(self):
        return Agent(model= self.configs.model_configs.prepare_model,
                     system_prompt=self.configs.system_prompt,
                     tools=self.configs.tools,
                     retries=self.configs.retries,
                     )
    
    def run(self):
        self._Agent.run_sync(user_prompt=self.configs.user_prompt.build)
        

    