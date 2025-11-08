from utils import loaders, configs
from tools import agent_tools
from agents import assistants
from prompts import recency_prompts
import logfire
from pathlib import Path

env_configs= loaders.load_env_vars(".env")

logfire.configure(token=env_configs["LOGFIRE_API_KEY"])
logfire.instrument_pydantic_ai()
logfire.instrument_google_genai()

eval_dir = Path("./eval_dataset").resolve()
eval_dir.mkdir(parents=True, exist_ok=True)
recency_eval_input_path = eval_dir/ "recency_eval.json"
recency_eval_output_path = eval_dir/ "recency_eval_report.md"

recency_cfg = configs.AgentConfigs(
    agent_name=configs.AgentsName.RECENCY_RANKER.value,
    system_prompt=recency_prompts.recency_system_prompt,
    user_prompt=configs.UserPrompt(base_user_prompt=recency_prompts.recency_user_prompt,
                                    input_path=recency_eval_input_path,
                                    output_path=recency_eval_output_path,
    ),
    retries=3,
    model_configs=configs.LlmConfigs(model_name=env_configs["LLM_MODEL"], api_key=env_configs["GEMINI_API_KEY"]),
    tools=[agent_tools.load_json_file_recency,
            agent_tools.write_markdown_file,
            agent_tools.convert_webkit_timestamp,
            agent_tools.sort_by_datetime,
            agent_tools.format_datetime]
    )

recency_agent = assistants.BookmarkAssistant(configs=recency_cfg)
recency_agent.run()
    
    
    