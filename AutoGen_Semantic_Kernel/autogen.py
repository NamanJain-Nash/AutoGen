# Load SK AutoGen Planner
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
from planning.autogen_planner import AutoGenPlanner

kernel = sk.Kernel()
print("Kernel ready.")

sk_planner = AutoGenPlanner(kernel, llm_config)

assistant = sk_planner.create_assistant_agent("Assistant")
worker = sk_planner.create_user_agent("Worker", max_auto_reply=4, human_input="NEVER")

print("Agents ready.")

