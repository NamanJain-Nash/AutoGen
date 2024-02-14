from autogen import AssistantAgent,UserProxyAgent
import semantic_kernel as sk
import random
from semantic_kernel.plugin_definition import kernel_function
class GenerateNumberPlugin:
    """
    Description: Generate a number between 3-x.
    """

    @kernel_function(
        description="Generate a random number between 3-x",
        name="GenerateNumberThreeOrHigher",
    )
    def generate_number_three_or_higher(self, input: str) -> str:
        """
        Generate a number between 3-<input>
        Example:
            "8" => rand(3,8)
        Args:
            input -- The upper limit for the random number generation
        Returns:
            int value
        """
        try:
            return str(random.randint(3, int(input)))
        except ValueError as e:
            print(f"Invalid input {input}")
            raise e

def main():
    # Making Semantic kernel based functions
    kernel = sk.Kernel()
    kernel.import_plugin(GenerateNumberPlugin(), "GenerateNumberPlugin")
    # Register the LLM
    config_list_mistral = [
    {
    'base_url': "http://localhost:8000",
    'api_key': "NULL",
    'model': "mistral"
    }
    ]
    config_list_phi = [
    {
    'base_url': "http://localhost:8000",
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
    sk_planner=AutoGenPlanner(kernel,llm_config_mistral)
    # Setting up the autogen coder
    assistant = sk_planner.create_assistant_agent("Assistant") 
    worker = sk_planner.create_user_agent("Worker", max_auto_reply=4, human_input="NEVER")  
    print("Agents ready.") 
    question="""
    Can you give me a random number
    """
    worker.initiate_chat(assistant, message=question)
if __name__ == "__main__":
    main()