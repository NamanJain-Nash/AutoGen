from autogen import AssistantAgent,UserProxyAgent
# Setup the LLM Models Taking PHI and Mistral
 
config_list_mistral = [
{
'base_url': "http://localhost:20234",
'api_key': "NULL",
'model': "mistral"
}
]

config_list_phi = [
{
'base_url': "http://localhost:1904",
'api_key': "NULL",
'model': "phi"
}
]

llm_config_mistral={
"config_list": config_list_mistral,
}

llm_config_phi={
"config_list": config_list_phi,
}
# Setting up the autogen coder
coder = AssistantAgent(
name="Coder",
llm_config=llm_config_phi
)
# Setting up the proc
user_proxy = UserProxyAgent(
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
Write a python script to output numbers 1 to 100 and then the user_proxy agent should run the script
"""

user_proxy.initiate_chat(coder, message=task)



## In this need to use Litellm to start both the model by using 2 litlellm for these model after starting the different litllem of mistral and phi and then they can talk do use the coorect address only