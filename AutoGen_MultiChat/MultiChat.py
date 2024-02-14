import autogen
import semantic_kernel as sk
import random
def main():
    # LLM Models Configuration
    config_list_mistral = [
    {
    'base_url': "http://localhost:8000",
    'api_key': "NULL",
    'model': "mistral"
    }
    ]
    config_list_phi = [
    {
    'base_url': "http://localhost:13750",
    'api_key': "NULL",
    'model': "phi"
    }
    ]
    # Register the LLM and Functions
    llm_config_mistral={
    "config_list": config_list_mistral,
    }

    llm_config_phi={
    "config_list": config_list_phi,
    }

    # Setting up the autogen coder
    coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config_phi
    )
    # Setting up the proc
    user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config_mistral,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
    Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
    )

    task="""
    Can you give me a random number
    """
    user_proxy.initiate_chat(coder, message=task)
if __name__ == "__main__":
    main()
