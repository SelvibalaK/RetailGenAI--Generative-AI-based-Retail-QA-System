from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
import sys
sys.path.insert(0, r"D:\User1\langchainretail\setup\envconfig.py")
from config import GOOGLE_API_KEY, DB_CONFIG, TEMPERATURE, MODEL_NAME


class SQLAssistant:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            google_api_key=GOOGLE_API_KEY,
            temperature=TEMPERATURE
        )
        
        self.db = SQLDatabase.from_uri(
            f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
        )
        
        self.prompt = PromptTemplate(
            input_variables=["input", "table_info"],
            template="""
            Based on the database schema below:
            {table_info}
            Generate a SQL query to answer this question:
            {input}
            Important: Return ONLY the raw SQL query without any markdown formatting, backticks, or sql tags.
            """
        )
        
        self.db_chain = SQLDatabaseChain.from_llm(
            llm=self.llm,
            db=self.db,
            prompt=self.prompt,
            verbose=True,
            use_query_checker=False,
            return_direct=True
        )
    
    def get_response(self, question):
        try:
            response = self.db_chain.invoke(question)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
