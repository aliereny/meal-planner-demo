# We import os and load_dotenv to load our API key from a .env file
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# We import the OpenAI as the language model
from langchain.llms import OpenAI

# We import the PromptTemplate class to create a template for our prompt
from langchain.prompts import PromptTemplate

# We import the LLMChain class to create a chain of language models
from langchain.chains import LLMChain, SequentialChain

# We import streamlit to create a simple web app
import streamlit as st

# We create an instance of the OpenAI language model with a temperature of 0.9
# Temperature is a hyperparameter that controls the randomness of the language model
# The higher the temperature, the more random the language model will be
# The lower the temperature, the more predictable the language model will be
llm = OpenAI(temperature=0.9, openai_api_key=OPENAI_API_KEY)

# We create a PromptTemplate instance to create a template for our prompt
# The template is a string that contains variables that will be replaced by the user
# The variables are defined in the input_variables list
# The variables are replaced by the user's input
meal_pt = PromptTemplate(
    template="""
    Name me a meal could be made using the following ingredients: {ingredients}. Only respond with the meal name, 
    nothing else.
    Example: "Chicken and rice"
    """,
    input_variables=["ingredients"],
)

# We create an LLMChain instance to create a chain of language models
# The chain will prompt the user with the meal_pt template
meal_chain = LLMChain(llm=llm, prompt=meal_pt, verbose=True, output_key="meal")

# We create another PromptTemplate instance to create a template for our prompt
shopping_list_pt = PromptTemplate(
    template="""
    Create me a shopping list to make the following meal: {meal}. Only respond with the name of the meal and then the 
    numbered shopping list, nothing else.
    Example: "Chicken and rice
    1. 2 chicken breasts
    2. 1 cup of rice
    ..."
    """,
    input_variables=["meal"],
)

# We create another LLMChain instance to create a chain of language models
shopping_list_chain = LLMChain(
    llm=llm, prompt=shopping_list_pt, verbose=True, output_key="list"
)

# We create another PromptTemplate instance to create a template for our prompt
instructions_pt = PromptTemplate(
    template="""
    Write me the instructions to make the following meal with the given resources: {list} 
    Only respond with the numbered instructions, nothing else.
    Example: "1. Boil water
    2. Cook chicken
    3. Serve chicken on rice
    ..."
    """,
    input_variables=["list"],
)

# We create another LLMChain instance to create a chain of language models
instructions_chain = LLMChain(
    llm=llm, prompt=instructions_pt, verbose=True, output_key="instructions"
)

# We create a SequentialChain instance to create a chain of language models
# The chains list contains the chains that will be executed in order
# The input_variables list contains the variables that the user will input
# The output_variables list contains the variables that the chain will output
cook_chain = SequentialChain(
    chains=[meal_chain, shopping_list_chain, instructions_chain],
    input_variables=["ingredients"],
    output_variables=["meal", "list", "instructions"],
)


# We create a simple web app using streamlit
st.title("Meal planner")
# We write a simple description of the web app
st.write(
    """
    This is a simple meal planner that uses the OpenAI API to generate a meal, shopping list, and instructions.
    """
)
# We create a text input for the user to input a comma-separated list of ingredients
user_prompt = st.text_input("Enter a comma-separated list of ingredients")
# We create a button to generate the meal, shopping list, and instructions
if st.button("Generate") and user_prompt:
    # We use the st.spinner context manager to display a loading message
    with st.spinner("Hold still..."):
        # We create a dictionary of the user's input
        output = cook_chain({"ingredients": user_prompt})

        # We display the meal, shopping list, and instructions in three columns
        col1, col2, col3 = st.columns(3)
        col1.header("Meal")
        col1.write(output["meal"])
        col2.header("Shopping list")
        col2.write(output["list"])
        col3.header("Instructions")
        col3.write(output["instructions"])
