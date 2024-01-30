from autogen import AssistantAgent,UserProxyAgent
import semantic_kernel as sk
from semantic_kernel.skill_definition import (
    sk_function,
    sk_function_context_parameter,
)
from semantic_kernel.orchestration.sk_context import SKContext
class MathPlugin:
    @sk_function(
        description="Takes the square root of a number",
        name="Sqrt",
        input_description="The value to take the square root of",
    )
    def square_root(self, number: str) -> str:
        return str(math.sqrt(float(number)))

    @sk_function(
        description="Adds two numbers together",
        name="Add",
    )
    @sk_function_context_parameter(
        name="input",
        description="The first number to add",
    )
    @sk_function_context_parameter(
        name="number2",
        description="The second number to add",
    )
    def add(self, context: SKContext) -> str:
        return str(float(context["input"]) + float(context["number2"]))

    @sk_function(
        description="Subtract two numbers",
        name="Subtract",
    )
    @sk_function_context_parameter(
        name="input",
        description="The first number to subtract from",
    )
    @sk_function_context_parameter(
        name="number2",
        description="The second number to subtract away",
    )
    def subtract(self, context: SKContext) -> str:
        return str(float(context["input"]) - float(context["number2"]))

    @sk_function(
        description="Multiply two numbers. When increasing by a percentage, don't forget to add 1 to the percentage.",
        name="Multiply",
    )
    @sk_function_context_parameter(
        name="input",
        description="The first number to multiply",
    )
    @sk_function_context_parameter(
        name="number2",
        description="The second number to multiply",
    )
    def multiply(self, context: SKContext) -> str:
        return str(float(context["input"]) * float(context["number2"]))

    @sk_function(
        description="Divide two numbers",
        name="Divide",
    )
    @sk_function_context_parameter(
        name="input",
        description="The first number to divide from",
    )
    @sk_function_context_parameter(
        name="number2",
        description="The second number to divide by",
    )
    def divide(self, context: SKContext) -> str:
        return str(float(context["input"]) / float(context["number2"]))
async def main():
    # LLM Models Configuration
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
    # Making Semantic kernel based functions
    kernel = sk.Kernel()
    kernel.import_skill(MathPlugin(), skill_name="MathPlugin")
    # Register the LLM and Functions
    llm_config_mistral={
    "functions":[
        kernel
    ],
    "config_list": config_list_mistral,
    }

    llm_config_phi={
    "config_list": config_list_phi,
    }
    # Use the llms

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
    Calculate 20*20*20
    """

    user_proxy.initiate_chat(coder, message=task)
