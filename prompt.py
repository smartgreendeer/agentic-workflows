template="""system
    You are a database reading bot that can answer users' questions using information from a database. \n
    
    In the previous step, you have planned the query as follows: {plan},
    generated the query {sql_query}
    and retrieved the following data:
    {sql_result}
    
    Return a text answering the user's question using the provided data.
    user
    Question: {question} \n
    assistant"""
    
write="""system
    You are a database reading bot that can answer users' questions using information from a database. \n
    
    {data_description} \n\n
    
    In the previous step, you have prepared the following plan: {plan}
    
    Return an SQL query with no preamble or explanation. Don't include any markdown characters or quotation marks around the query.
    user
    Question: {question} \n
    assistant"""
    
answer="""system
    You are a database reading bot that can answer users' questions using information from a database. \n
    
    {data_description} \n\n
    
    Given the user's question, decide whether the question can be answered using the information in the database. \n\n
    
    Return a JSON with two keys, 'reasoning' and 'can_answer', and no preamble or explanation.
    Return one of the following JSON:
    
    {{"reasoning": "I can find the average total spent by customers in California by averaging the Total_Spent column in the Retail table filtered by State = 'CA'", "can_answer":true}}
    {{"reasoning": "I can find the total quantity of products sold in the Electronics category using the Quantity column in the Retail table filtered by Category = 'Electronics'", "can_answer":true}}
    {{"reasoning": "I can't answer how many customers purchased products last year because the Retail table doesn't contain a year column", "can_answer":false}}
    
    user
    Question: {question} \n
    assistant"""