import os
from langchain.prompts import PromptTemplate
from llm import llm
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from prompts import prompt, summary_prompt
from nl2sql import execute_sql

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

chat_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

def query_to_sql(query: str):
    response = chat_chain.run(query)
    return response.strip().replace("```sql", "").replace("```", "").strip()

def summarize_sql_result(sql_result):
    result_str = str(sql_result)
    llm_chain_for_summary = LLMChain(llm=llm, prompt=summary_prompt, memory=memory)
    summary = llm_chain_for_summary.run(sql_result=result_str)
    return summary

def interact_with_agent(user_query):
    if user_query.lower() in ["exit", "quit", "bye"]:
        return "Goodbye!"

    sql_or_greeting = query_to_sql(user_query)

    if sql_or_greeting.lower().startswith("select"):
        try:
            result = execute_sql(sql_or_greeting)
            
            if result:
                summary = summarize_sql_result(result)
                return summary
            else:
                return "Hmm, I couldn't find any relevant data for that query. Maybe try rephrasing it?"
        
        except Exception as e:
            return f"Oops! Something went wrong while executing the query. Error: {str(e)}"

    return sql_or_greeting
