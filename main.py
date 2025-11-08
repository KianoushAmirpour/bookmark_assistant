from utils import loaders, logger, configs
from tools import agent_tools
from agents import assistants, judge
from prompts import classifier_prompts, recency_prompts, classifier_reflection_prompt, recency_reflection_prompt
import logfire


env_configs= loaders.load_env_vars(".env")

logfire.configure(token=env_configs["LOGFIRE_API_KEY"])
logfire.instrument_pydantic_ai()

logger = logger.setup_logger()

# load bookmarks file from the system, clean them and save them as json for later use.
sys_bookmarks_paths = loaders.load_bookmarks()
cleaned_sys_bookmarks_path = loaders.load_output_dir("cleaned_sys_bookmarks.json")
cleaned_bookmarks = agent_tools.load_extract_bookmarks(sys_bookmarks_paths)
agent_tools.write_extracted_bookmarks(cleaned_sys_bookmarks_path,cleaned_bookmarks)


def run_classification_agent():
    
    classifier_cfg = configs.AgentConfigs(
    agent_name=configs.AgentsName.CLASSIFIER.value,
    system_prompt=classifier_prompts.classifier_system_prompt,
    user_prompt=configs.UserPrompt(base_user_prompt=classifier_prompts.classifier_user_prompt,
                                   input_path=cleaned_sys_bookmarks_path,
                                   output_path=loaders.load_output_dir("classification_report.md"),
),
    retries=3,
    model_configs=configs.LlmConfigs(model_name=env_configs["LLM_MODEL"], api_key=env_configs["GEMINI_API_KEY"]),
    tools=[agent_tools.load_json_file_classifier, agent_tools.write_markdown_file]
)

    classifier_agent = assistants.BookmarkAssistant(configs=classifier_cfg)
    classifier_agent.run()
    
  
def run_classification_reflection_agent():
    classifier_reflector_cfg = configs.AgentConfigs(
        agent_name="classifier_reflector",
        user_prompt=configs.UserPrompt(base_user_prompt=classifier_reflection_prompt.reflection,
                                    input_path=loaders.load_output_dir("classification_report.md"),
                                    output_path=loaders.load_output_dir("classifier_reflector_report.md"),
    ),
        retries=3,
        model_configs=configs.LlmConfigs(model_name=env_configs["LLM_MODEL"], api_key=env_configs["GEMINI_API_KEY"]),
        tools=[agent_tools.open_markdown_file, agent_tools.write_markdown_file]
    )

    classifier_reflector_agent = judge.Judge(classifier_reflector_cfg)
    classifier_reflector_agent.run()

def run_recency_agent():
    recency_cfg = configs.AgentConfigs(
    agent_name=configs.AgentsName.RECENCY_RANKER.value,
    system_prompt=recency_prompts.recency_system_prompt,
    user_prompt=configs.UserPrompt(base_user_prompt=recency_prompts.recency_user_prompt,
                                    input_path=cleaned_sys_bookmarks_path,
                                    output_path=loaders.load_output_dir("recency_report.md"),
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
    
    
def run_recency_reflection_agent():
    recency_reflector_cfg = configs.AgentConfigs(
        agent_name="recency_reflector",
        user_prompt=configs.UserPrompt(base_user_prompt=recency_reflection_prompt.reflection,
                                    input_path=loaders.load_output_dir("recency_report.md"),
                                    output_path=loaders.load_output_dir("recency_reflection_report.md"),
    ),
        retries=3,
        model_configs=configs.LlmConfigs(model_name=env_configs["LLM_MODEL"], api_key=env_configs["GEMINI_API_KEY"]),
        tools=[agent_tools.open_markdown_file, agent_tools.write_markdown_file, agent_tools.find_datetime_and_urls]
    )

    recency_reflector_agent = judge.Judge(recency_reflector_cfg)
    recency_reflector_agent.run()

# run_classification_agent()
# print("Classification done")
# run_classification_reflection_agent()
run_recency_agent()
print("recency done")
run_recency_reflection_agent()

