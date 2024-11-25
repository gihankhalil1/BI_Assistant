from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain.schema import AIMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import time
import os

class SchemaDescriber:
    def __init__(self, gemini_api_key, output_file="schema_descriptions.txt"):
        """
        Initialize the SchemaDescriber.

        Parameters:
        - gemini_api_key: API key for Google Gemini API.
        - output_file: Path to the single output file for all schema descriptions.
        """
        self.gemini_api_key = gemini_api_key
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=self.gemini_api_key)
        self.output_file = output_file
    
    def generate_description(self, schema_info):
        """
        Generate a concise description for the entire schema. The LLM will infer the table structure from the full schema.
        The description should include:
        - Columns, data types, and constraints (primary/foreign keys).
        - An example row for each table in the schema.
        - Keep it concise, yet informative, ensuring all necessary details are captured.
        
        Parameters:
        - schema_info: The raw schema information of the database, which includes all tables.

        Returns:
        - A string containing the concise description for the schema.
        """
        template = f"""
        You are given a database schema. For each table, provide only the following:
        - A list of columns with their data types.
        - Primary and foreign key constraints, if any.
        - One example row of data.

        Keep the description as brief as possible while including all critical details.

        Schema:
        {schema_info}

        Description:
        """ 
        prompt = ChatPromptTemplate.from_template(template)
        prompt_text = prompt.format(schema_info=schema_info)
        response = self.llm.invoke(prompt_text)
        return response.content.strip()
    
    def save_descriptions(self, descriptions):
        """
        Save all schema descriptions to a single file.

        Parameters:
        - descriptions: The full description of all tables.
        """
        with open(self.output_file, "a", encoding="utf-8") as file:
            file.write(descriptions)
            file.write("\n" + "-" * 80 + "\n")  # Separator for readability
        
        print(f"All descriptions saved to {self.output_file}")
    
    def load_existing_descriptions(self):
        """
        Load existing descriptions from the output file if it exists.

        Returns:
        - The content of the existing description file or an empty string if the file doesn't exist.
        """
        if os.path.exists(self.output_file):
            with open(self.output_file, "r", encoding="utf-8") as file:
                return file.read()
        return ""

    def describe_and_save_all(self, database_schema):
        """
        Generate and save descriptions for all tables in the database schema.
        This method will only generate new descriptions if the output file doesn't exist.

        Parameters:
        - database_schema: The complete schema information for all tables in the database.

        Returns:
        - The description of all tables in the schema.
        """
        # Check if the output file already exists and return its content if it does
        existing_descriptions = self.load_existing_descriptions()
        if existing_descriptions:
            print(f"Descriptions already exist in {self.output_file}. Returning existing descriptions.")
            return existing_descriptions

        # Generate the description for the full schema
        print("Generating descriptions for the entire schema...")
        description = self.generate_description(database_schema)

        # Save the description to a file
        self.save_descriptions(description)
        return description

class DatabaseConnector:
    """Handles the connection to the SQL database."""
    def __init__(self):
        self.db = None

    def connect(self, user: str, password: str, host: str, port: str, database: str):
        """Initialize database connection."""
        db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        self.db = SQLDatabase.from_uri(db_uri)
        return self.db
    
# Classifies user questions as serious or non-serious.
class QuestionClassifier:
    """Classifies user questions as serious or non-serious."""
    def __init__(self, gemini_api_key: str):
        self.gemini_api_key = gemini_api_key
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=self.gemini_api_key)
        
    def classify_question(self, question: str):
        """Classify the question as serious or non-serious."""
        template = """
        Classify the following question as either "Serious" or "Non-Serious." 
        Serious questions are related to database queries, business matters, or technical inquiries, such as questions about the company's operations, employees, products, sales, or other business processes. 
        Non-serious questions may be humorous, light-hearted, or irrelevant to these topics.

        The user can ask in either Arabic or English. Your response must match the language used by the user.

        Question: {question}
        
        Respond with either "Serious" or "Non-Serious".
        """
        prompt = ChatPromptTemplate.from_template(template)
        
        prompt_text = prompt.format(question=question)
        response = self.llm.invoke(prompt_text)

        return response.content.strip().lower()  # Return "serious" or "non-serious"

# Verifies whether the question is related to the database schema.
class SchemaVerifier:
    """Verifies if the serious question relates to the schema of the database."""
    def __init__(self, gemini_api_key: str):
        self.gemini_api_key = gemini_api_key
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=self.gemini_api_key)

    def verify_schema_relevance(self, question: str, schema_info: str):
        """Verifies if the serious question is related to the database schema."""
        template = """
        You are a highly intelligent system designed to classify user questions as either **related** or **not related** to a database schema. 
        The database is a data warehouse that contains information about the company's operations, including data about employees, products, sales, and other related business processes. 
        The schema follows specific naming conventions where tables may start with prefixes like 'dim' (e.g., dimEmployee, dimDate, dimProduct) for dimension tables and 'fact' (e.g., factResellerSales) for fact tables.

        The question must be classified as "Related" only if the data requested can be extracted from the database based on the provided schema. 
        User questions may be in English or Arabic. Consider both the schema and the database context when making your determination.
        
        <SCHEMA>{schema_info}</SCHEMA>
        
        Question: {question}
        
        If the question is related to the schema and data can be extracted from the database, respond with "Related".
        
        Otherwise, respond with "Not related".
        """

        prompt = ChatPromptTemplate.from_template(template)
        
        prompt_text = prompt.format(question=question, schema_info=schema_info)
        response = self.llm.invoke(prompt_text)

        return response.content.strip().lower()  # "related" or "not related"


# Provides playful or humorous responses for non-serious questions.
class NonSeriousAssistant:
    """Handles non-serious, playful, or humorous responses."""
    def __init__(self, gemini_api_key: str):
        self.gemini_api_key = gemini_api_key
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=self.gemini_api_key)

    def get_non_serious_response(self, question: str):
        """Generates a humorous response for non-serious questions."""
        template = """

     . You handle both serious managers inquiries and casual questions in a way that maintains an engaging conversation with the user. You're expected to create a seamless transition between small talk and business-related topics. When casual or non-serious questions are asked, your responses should reflect your helpful, approachable identity.
       Guidelines:
        - The Question might be in Arabic, or English, you must reply in the same question language
        * if the question in arabic the output must be in arabic.
        * if the question in english the output must be in english.
        * do not mix between arabic and english.
        
    - For casual questions, provide friendly and engaging responses. Keep the interaction light, but maintain your identity as a financial expert.
    - When switching to serious company questions, shift to a more professional tone while remaining approachable.
    - The question can be informal or formal, but ensure that your personality remains consistent across all responses.
    - Your responses should reinforce your role, without overwhelming the user with excessive formality in casual conversations.

    Example Responses:
    - "Hello": "Hello! How can I assist you with your database today?"
    - "How old are you?": "I'm as old as the insights I provide—timeless!"
    - "What's your name?": "I'm a BIZAssistant, ready to help you manage your company!"
    - "Tell me a joke": "Why did the accountant break up with the calculator? It just didn't add up!" or "ﻣﺮﺓ ﻣﺤﺎﺳﺐ ﺗﺠﻮﺯ ﻣﺤﺎﺳﺒﺔ ﻛﺘﺒﻮﺍ ﻛﺘﺎﺑﻬﻢ ﻋﻠﻰ ﺩﻓﺘﺮ"
    - For a business-related question: "Let's dive into the numbers. How can I assist you with your database today?"
    -If a user asks: “How can you help me manage my company?”
        Please respond as follows: “I can help you by analyzing your database, forecasting your financial future, and managing cash flow.”


        Question: {question}
        
        Provide a creative, non-serious response.
        """
        prompt = ChatPromptTemplate.from_template(template)
        
        prompt_text = prompt.format(question=question)
        response = self.llm.invoke(prompt_text)

        return response.content.strip()


class SQLAssistant:
    """Manages LLM-driven SQL query generation and response handling."""
    def __init__(self, gemini_api_key_1: str, gemini_api_key_2: str):
        self.gemini_api_key_1 = gemini_api_key_1
        self.gemini_api_key_2 = gemini_api_key_2
        self.gemini_api_key_3 = os.getenv('GEMINI_API_KEY_2')
        self.describer = SchemaDescriber(self.gemini_api_key_3)

    def get_sql_chain(self, db: SQLDatabase):
        """Creates a chain to generate SQL queries from user input."""
        template = """
        You are a data analyst at a company, working with a data warehouse. The database schema follows a naming convention where column and table names may start with prefixes like 'dim' for dimension tables (e.g., dimEmployee, dimDate, dimProduct) and 'fact' for fact tables (e.g., factResellerSales). You are interacting with a user who is asking questions about this data warehouse.

        The user's question may be in English or Arabic. Based on the table schema provided below and the conversation history, write an SQL query that would answer the user's question. Take the conversation history into account.

        <SCHEMA>{schema}</SCHEMA>
        
        Conversation History: {chat_history}
        
        Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
        """
        prompt = ChatPromptTemplate.from_template(template)
        llm_1 = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=self.gemini_api_key_1)

        def get_schema(_):
            schema_info = db.get_table_info()
            descriptions = self.describer.describe_and_save_all(schema_info)
            return descriptions

        return (
            RunnablePassthrough.assign(schema=get_schema)
            | prompt
            | llm_1
            | StrOutputParser()
        )

    def generate_response(self, user_query: str, db: SQLDatabase, chat_history: list):
        """Generates a natural language response to the SQL query."""
        sql_chain = self.get_sql_chain(db)

        response_template = """
        You are a data analyst at a company.Response in the same language as the user's question. You are interacting with a user who is asking you questions about the company's database.
        Based on the table schema below, question, SQL query, and SQL response, write a natural language response.

        if user ask in Arabic,write a natural language explanation in Arabic only.
        if user ask in English, write it in English only. 

        <SCHEMA>{schema}</SCHEMA>

        Conversation History: {chat_history}
        SQL Query: <SQL>{query}</SQL>
        User question: {question}
        SQL Response: {response}
        """
        prompt = ChatPromptTemplate.from_template(response_template)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=self.gemini_api_key_2)

        def get_schema(_):
            schema_info = db.get_table_info()
            descriptions = self.describer.describe_and_save_all(schema_info)
            return descriptions

        chain = (
            RunnablePassthrough.assign(query=sql_chain).assign(
                schema=lambda _: get_schema,
                response=lambda vars: db.run(vars["query"]),
            )
            | prompt
            | llm
            | StrOutputParser()
        )


        try:
            # Attempt to invoke the chain
            time.sleep(10)
            return chain.invoke({
                "question": user_query,
                "chat_history": chat_history,
            })
        except Exception as e:
            # Handle API-related errors or any other exceptions
            error_message = (
                "An error occurred while processing your request. "
                "This could be due to hitting the API limit or other issues. Please try again later."
            )
            st.error(error_message)  # Display the error message in the Streamlit app
            return error_message


# The main Streamlit app to interact with the user.
class ChatApp:
    """Streamlit app to interact with the SQL assistant."""
    def __init__(self):
        load_dotenv()
        self.gemini_api_key_1 = os.getenv('GEMINI_API_KEY_1')
        self.gemini_api_key_2 = os.getenv('GEMINI_API_KEY_2')
        self.gemini_api_key_3 = os.getenv('GEMINI_API_KEY_3')
        self.gemini_api_key_4 = os.getenv('GEMINI_API_KEY_4')
        self.gemini_api_key_5 = os.getenv('GEMINI_API_KEY_5')
        self.gemini_api_key_6 = os.getenv('GEMINI_API_KEY_6')
        self.db_connector = DatabaseConnector()
        self.describer = SchemaDescriber(self.gemini_api_key_2)
        self.sql_assistant = SQLAssistant(self.gemini_api_key_4, self.gemini_api_key_1)
        self.schema_verifier = SchemaVerifier(self.gemini_api_key_3)
        self.non_serious_assistant = NonSeriousAssistant(self.gemini_api_key_5)
        self.question_classifier = QuestionClassifier(self.gemini_api_key_6)
        self.init_session_state()

    def init_session_state(self):
        """Initialize Streamlit session state variables."""
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                AIMessage(content="Hello! I'm SQL assistant. Ask me anything about your database."),
            ]
        if "db" not in st.session_state:
            st.session_state.db = None

    def sidebar(self):
        """Render the sidebar for database connection settings."""
        st.sidebar.subheader("Settings")
        st.sidebar.text_input("Host", value="localhost", key="Host")
        st.sidebar.text_input("Port", value="3306", key="Port")
        st.sidebar.text_input("User", value="root", key="User")
        st.sidebar.text_input("Password", type="password", value="admin", key="Password")
        st.sidebar.text_input("Database", value="AdventureWorksDW2022_copy", key="Database")

        if st.sidebar.button("Connect"):
            with st.spinner("Connecting to database..."):
                try:
                    st.session_state.db = self.db_connector.connect(
                        st.session_state["User"],
                        st.session_state["Password"],
                        st.session_state["Host"],
                        st.session_state["Port"],
                        st.session_state["Database"]
                    )
                    st.success("Connected to the database!")
                except Exception as e:
                    st.error(f"Failed to connect: {e}")

    def display_chat_history(self):
        """Render the chat history in the app."""
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI"):
                    st.markdown(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("Human"):
                    st.write(message.content)
    def handle_user_query(self):
        """Process user input and generate responses."""
        user_query = st.chat_input("Type a message...")
        if user_query:
            st.session_state.chat_history.append(HumanMessage(user_query))

            with st.chat_message("Human"):
                st.markdown(user_query)

            with st.chat_message("AI"):
                if st.session_state.db:
                    # First classify the question
                    classification = self.question_classifier.classify_question(user_query)

                    if classification == "serious":
                        # Check if the serious question is related to the schema
                        schema_info = st.session_state.db.get_table_info()  # Retrieve schema information
                        descriptions = self.describer.describe_and_save_all(schema_info)
                        relevance = self.schema_verifier.verify_schema_relevance(user_query, descriptions)

                        if relevance == "related":
                            response = self.sql_assistant.generate_response(
                                user_query,
                                st.session_state.db,
                                st.session_state.chat_history[-2:]
                            )
                            st.markdown(response)
                            st.session_state.chat_history.append(AIMessage(content=response))

                        else:
                            response = "Thank you for your question! It doesn't seem to be related to the database. Feel free to ask anything related to the database, such as queries about employees, products, sales, or other business data, and I'll be happy to assist you!"
                            st.markdown(response)
                            st.session_state.chat_history.append(AIMessage(content=response))

                    else:
                        # Handle non-serious questions with the playful assistant
                        response = self.non_serious_assistant.get_non_serious_response(user_query)
                        st.markdown(response)
                        st.session_state.chat_history.append(AIMessage(content=response))


    def run(self):
        """Run the Streamlit app."""
        st.set_page_config(page_title="Chat with Database", page_icon=":speech_balloon:")
        st.title("Chat with Database")
        self.sidebar()
        self.display_chat_history()
        self.handle_user_query()


# Instantiate and run the Streamlit app
if __name__ == "__main__":
    app = ChatApp()
    app.run()

