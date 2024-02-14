
import autogen
import dotenv
import os
from typing import Literal
from typing_extensions import Annotated

dotenv.load_dotenv()

model="gpt-35-turbo-16k"
file="config.json"
config_list = autogen.config_list_from_json(
    file,
    filter_dict={
        "model": [model]
    }
)

llm_config = {
    "config_list": config_list,
    "timeout":600
}

chatbot = autogen.AssistantAgent(
    name="chatbot",
    system_message="""For currency exchange tasks,
    only use the functions you have been provided with.
    Reply TERMINATE when the task is done.
    Reply TERMINATE when user's content is empty.""",
    llm_config=llm_config,
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().find("TERMINATE") >= 0,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
)
from typing import Literal
CurrencySymbol = Literal["USD", "EUR"]


def exchange_rate(base_currency: CurrencySymbol, quote_currency: CurrencySymbol) -> float:
    if base_currency == quote_currency:
        return 1.0
    elif base_currency == "USD" and quote_currency == "EUR":
        return 1 / 1.1
    elif base_currency == "EUR" and quote_currency == "USD":
        return 1.1
    else:
        raise ValueError(f"Unknown currencies {base_currency}, {quote_currency}")


from pydantic import BaseModel, Field
from typing_extensions import Annotated

class Currency(BaseModel):
    currency: Annotated[CurrencySymbol, Field(..., description="Currency symbol")]
    amount: Annotated[float, Field(..., description="Amount of currency", ge=0)]

@user_proxy.register_for_execution()
@chatbot.register_for_llm(description="Currency exchange calculator.")
def currency_calculator(
    base: Annotated[Currency, "Base currency: amount and currency symbol"],
    quote_currency: Annotated[CurrencySymbol, "Quote currency symbol"] = "USD",
) -> Currency:
    quote_amount = exchange_rate(base.currency, quote_currency) * base.amount
    return Currency(amount=quote_amount, currency=quote_currency)
print(chatbot.llm_config["tools"])
# start the conversation
user_proxy.initiate_chat(
    chatbot,
    message="How much is 123.45 USD in EUR?",
)