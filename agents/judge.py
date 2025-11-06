from pydantic_ai import Agent
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..utils import AgentConfigs

class Judge():
    def __init__(self, configs: "AgentConfigs"):
        self.configs = configs

    
    @property
    def _Agent(self):
        return Agent(model= self.configs.model_configs.prepare_model,
                     tools=self.configs.tools,
                     retries=self.configs.retries,
                    #  output_type=self.agent_configs.output_type
                     )
    
    def run(self):
        self._Agent.run_sync(user_prompt=self.configs.user_prompt.build)