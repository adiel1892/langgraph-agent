import uuid

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_tavily import TavilySearch

load_dotenv()
checkpointer = InMemorySaver()

def get_current_stock_price(stock_ticker: str) -> str:
    """
    Use this tool when the user asks for the current price of a specific stock (e.g., 'What is the price of META?').
    This tool searches for and returns the latest trading price for the given stock ticker.
    """
    print("---GOT TO STOCK PRICE TOOL---")
    search = TavilySearch()
    # You might want to tweak the query for better accuracy:
    query = f"Current price of {stock_ticker} stock"
    return search.run(query)

def get_stock_news(stock_ticker: str) -> str:
    """
    Use this tool when the user requests the latest news about a specific stock (e.g., 'Show me news about META').
    This tool searches and returns recent news articles and updates for the given stock ticker.
    """
    print("---GOT TO STOCK NEWS TOOL---")
    search = TavilySearch()
    query = f"Latest news about {stock_ticker} stock"
    return search.run(query)


def irrelevant_query(query: str) -> str:
    """
        Use this tool when the user's request is not related to finance.
        Respond in a friendly and polite way, letting the user know you can only assist with finance-related topics, and invite them to ask another finance question.
        """
    print("---GOT TO IRRELEVANT QUERY TOOL---")
    messages = [
        {
            "role": "system",
            "content":
                "You are an expert finance assistant. "
                "If the user's question is not about finance, respond in a friendly, humorous, and polite way. "
                "You can make a light joke, for example, if asked about sports, say something like 'I can't track football scores, but I can help you keep score of your investments!' "
                "Always invite the user to ask a finance-related question instead."
        },
        {"role": "user", "content": query}
    ]
    response = model.invoke(messages)

    return response.content if hasattr(response, "content") else response


model = init_chat_model(
    "google_genai:gemini-2.0-flash",
    temperature=0
)

agent = create_react_agent(
    model=model,
    tools=[get_stock_news, get_current_stock_price, irrelevant_query],
    checkpointer=checkpointer,
    prompt="""
        You are a helpful assistant for financial questions.
        When the user asks about the latest stock news, always use the 'get_stock_news' tool.
        When the user asks for the current stock price, always use the 'get_current_stock_price' tool.
        If the user's request is not about stocks, politely let them know you only assist with stock-related queries.
        """
)

# Run the agent

def run_agent(user_input: str):

    run_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": run_id}}


    response = agent.invoke(
        {"messages": [{"role": "user" , "content": user_input}]},
        config
    )
    for msg in response["messages"]:
        if msg.__class__.__name__ == "HumanMessage":
            print("User:", msg.content)
        if msg.__class__.__name__ == "AIMessage" and msg.content.strip():
            print("AI:", msg.content)
    return [msg.content for msg in response["messages"] if hasattr(msg, "content")]


if __name__ == '__main__':
    run_agent("what is the price of META?")

# for msg in response["messages"]:
#     if msg.__class__.__name__ == "HumanMessage":
#         print("User:", msg.content)
#     if msg.__class__.__name__ == "AIMessage" and msg.content.strip():
#         print("AI:", msg.content)
#  "Can you tell me the current price of META? and can you tell me some news about NKE?"



# irrelevant_response = agent.invoke(
#     {"messages": [{"role": "user", "content": "Who won the premier league in 2022?"}]},
#     config
# )
# for msg in irrelevant_response["messages"]:
#     if msg.__class__.__name__ == "HumanMessage":
#         print("User:", msg.content)
#     if msg.__class__.__name__ == "AIMessage" and msg.content.strip():
#         print("AI:", msg.content)





# def run_agent():
#     while True:
#         user_input = input("Enter: ")
#         if user_input.lower() == 'exit':
#             print("Goodbye")
#             break
#         for event in agent.stream(
#                 {"messages": [{"role": "user", "content": user_input}]},
#                 config,
#         ):
#             for value in event.values():
#                 if isinstance(value, dict) and "messages" in value:
#                     print("Assistant:", value["messages"][-1].content)
#
# if __name__ == '__main__':
#     run_agent()