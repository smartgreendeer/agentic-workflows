# RetailX AI Assistant Documentation

## Project Overview

The RetailX AI Assistant is designed to answer questions about customer data and sales information from a SQLite database using natural language processing.

## Setup Instructions

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Set up environment variables in a `.env` file.
4. Run `streamlit run streamlit_app.py` to start the Streamlit app.

## Workflow Explanation

The AI workflow processes questions through several stages:
- **Check if can answer question**: Determines if the AI can provide an answer based on the question.
- **Write query**: Generates SQL queries based on the question and AI reasoning.
- **Execute query**: Executes the generated SQL query against the SQLite database.
- **Write answer**: Formats the SQL query results into a human-readable answer.
- **Explain no answer**: Provides an explanation if the AI cannot answer the question.

## Files and Modules

- **workflow_setup.py**: Contains the main workflow logic using LangChain and Streamlit.
- **data_preparation.py**: Prepares a sample dataset and sets up a SQLite database.
- **prompt.py**: Custom module for handling prompts in the workflow.

## Example Usage

To interact with the RetailX AI Assistant:
- Enter a question in the Streamlit interface.
- Click "Submit" to receive an answer based on the data in the SQLite database.

## Data Preparation

The SQLite database ('retail.db') contains a sample Retail dataset with customer information, product details, and purchase records.

## Error Handling

Error handling is implemented throughout the workflow to manage exceptions during SQL query execution, API interactions, and user input validation.

## Future Improvements

Future updates may include:
- Enhancing natural language understanding.
- Adding support for more complex SQL queries.
- Integrating with additional data sources and APIs.

## Appendix

For additional information or support, please contact `johnmuriithi7818@gmail.com`.
