import yaml
import subprocess
import autogen
from autogen import AssistantAgent,UserProxyAgent,GroupChat,GroupChatManager

def run_check_docker_script(compose_content):
    message
    try:
        # Write the Docker Compose configuration to a temporary file
        with open('temp-docker-compose.yml', 'w') as compose_file:
            compose_file.write(compose_content)

        # Run 'docker-compose up' in the background
        subprocess.run(['docker-compose', '-f', 'temp-docker-compose.yml', 'up', '-d'], check=True)

        # Run 'docker-compose ps' to check the status
        result = subprocess.run(['docker-compose', '-f', 'temp-docker-compose.yml', 'ps'], capture_output=True, text=True, check=True)

        # Check if any containers have an "Exit" status (indicating an error)
        if 'Exit' in result.stdout:
            message=("Error: Some containers have exited. Check 'docker-compose ps' for details.")
        else:
            message=("script is valid!")

    except subprocess.CalledProcessError as e:
        message=(f"Error: {e}")

    finally:
        # Clean up by stopping and removing the containers, volumes, and images
        subprocess.run(['docker-compose', '-f', 'temp-docker-compose.yml', 'down', '-v'], check=False)
        subprocess.run(['docker', 'volume', 'prune', '-f'], check=False)
        subprocess.run(['docker', 'image', 'prune', '-f'], check=False)
        subprocess.run(['docker', 'container', 'prune', '-f'], check=False)
        return message
def check_docker_script(script):
    try:
        #validate the Yaml
        ci_data = yaml.safe_load(script)
        #Check the script with running
        return run_check_docker_script(script)

    except yaml.YAMLError as e:
        # If there's an error parsing the YAML, print the error
        return(f"Error parsing CI script: {e}")
model="gpt-35-turbo-16k"
file="config.json"
config_list = autogen.config_list_from_json(
    file,
    filter_dict={
        "model": [model]
    }
)
custom_function_list=[
    {
        "name":"check_docker_script",
        "description":"Run the docker compose and test it",
        "parameters": {
                "type": "object",
                "properties": {
                    "script":{
                        "type": "string",
                        "description": "The docker compose file",
                    },
                },
                "required": ["script"],
            },
    }
]
# Register the LLM and Functions
llm_config={
"config_list": config_list
}
llm_config_function={
"config_list": config_list,
"functions":custom_function_list
}
# Setting up the autogen coder
dockerchecker = AssistantAgent(
name="dockerchecker",
llm_config=llm_config_function,
system_message="""Check the docker compose
Reply TERMINATE when the task is done.
Reply TERMINATE when script is valid.
Reply TERMINATE when user's content is empty.""",
)
assistant=AssistantAgent(
    name="Assistant",
    llm_config=llm_config,
    system_message="""Create a docker compose of the using one
    Reply TERMINATE when the task is done.
    Reply TERMINATE when script is valid.
    Reply TERMINATE when user's content is empty."""
)
# Setting up the proc
user_proxy = UserProxyAgent(
"user_proxy",
is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
human_input_mode="NEVER",
function_map={
            "check_docker_script": check_docker_script,
        })
groupchat=GroupChat(agents=[user_proxy, assistant, dockerchecker], messages=[], max_round=10)
manager=GroupChatManager(groupchat=groupchat,llm_config=llm_config)
task="""
Give me a docker compose for a react app and also check it before giving
"""
user_proxy.initiate_chat(manager, message=task)