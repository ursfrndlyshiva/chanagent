from langchain.prompts import PromptTemplate



prompt = PromptTemplate(
    input_variables=["query"],
    template="""
    You are a conversational assistant. 
    If the user asks a question about a database (like 'How many customers are there?'), convert it into an SQL query. 
    If the user greets you with "hi", "hello", or something casual, respond with a greeting.
    Otherwise, respond appropriately to their query.

    User's query: {query}
    """
)

summary_prompt = PromptTemplate(
        input_variables=["sql_result"],
        template="""The following is the result of a SQL query execution:
        {sql_result}
        Please summarize this data in a concise, human-readable format with out about database:
        """
    )