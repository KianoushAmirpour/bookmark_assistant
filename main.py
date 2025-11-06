from utils import loaders, logger, configs
from tools import agent_tools
from agents import assistants
from prompts import classifier_prompts
import logfire

logfire.configure(token='pylf_v1_eu_YcmjFM2mRhQsBZtBQqMZ3sTSKqhHXJVTFTdRDyCQdHcW')
logfire.instrument_pydantic_ai()

env_dict= loaders.load_env_vars(".env")
# logger = logger.setup_logger()

# load bookmarks file from the system, clean them and save them as json for later use.
sys_bookmarks_paths = loaders.load_bookmarks()
cleaned_sys_bookmarks_path = loaders.load_output_dir("cleaned_sys_bookmarks.json")
cleaned_bookmarks = agent_tools.load_extract_bookmarks(sys_bookmarks_paths)
agent_tools.write_extracted_bookmarks(cleaned_sys_bookmarks_path,cleaned_bookmarks)


classifier_cfg = configs.AgentConfigs(
    agent_name=configs.AgentsName.CLASSIFIER.value,
    system_prompt=classifier_prompts.classifier_system_prompt,
    user_prompt=configs.UserPrompt(base_user_prompt=classifier_prompts.classifier_user_prompt,
                                   input_path=cleaned_sys_bookmarks_path,
                                   output_path=loaders.load_output_dir("classification_report.md"),
),
    retries=3,
    model_configs=configs.LlmConfigs(model_name=env_dict["LLM_MODELS_FEEDER"], api_key=env_dict["GEMINI_API_KEY"]),
    tools=[agent_tools.load_json_file, agent_tools.write_markdown_file]
)

classifier_agent = assistants.BookmarkAssistant(configs=classifier_cfg)
classifier_agent.run()

