from pydantic import BaseModel, Field, FilePath, computed_field, ConfigDict
from typing import Literal, Annotated, List, Union
from enum import Enum
from pathlib import Path
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.settings import ModelSettings

class AgentsName(Enum):
    CLASSIFIER = "classifier"
    RECENCY_RANKER = "recency_ranker"
    
class UserPrompt(BaseModel):
    base_user_prompt: str
    input_path: FilePath
    output_path : Path
    
    @computed_field
    @property
    def build(self) -> str:
        return self.base_user_prompt.format(input_path=self.input_path, output_path=self.output_path)
    
class LlmConfigs(BaseModel):
    
    model_name: str
    api_key: str
    temperature: Annotated[float, Field(ge=0, le=1, default=0.05)]
    max_tokens: Annotated[int, Field(ge=0, le=65000, default=65000)]
    timeout: Annotated[int, Field(ge=0, le=100, default=60)]
    base_url : str | None = "https://generativelanguage.googleapis.com/v1beta/openai/"
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @computed_field
    @property
    def prepare_model(self) -> Union[GoogleModel, OpenAIChatModel]:
        model_settings = ModelSettings(max_tokens=self.max_tokens,
                                temperature=self.temperature,
                                timeout=self.timeout
                                )

        return OpenAIChatModel(model_name=self.model_name,
                                   provider=OpenAIProvider(base_url=self.base_url, api_key=self.api_key),
                                   settings=model_settings)
    
class AgentConfigs(BaseModel):
    agent_name: Literal["feeder", "classifier", "recency_ranker", "judge"]
    system_prompt : str | None = None
    user_prompt: UserPrompt
    retries: Annotated[int, Field(ge=0, le=5, default=4)]
    model_configs: LlmConfigs
    tools : List = Field(default_factory=list)
