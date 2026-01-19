import streamlit as st
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def table_definition_prompt(df):
    return f"""
    Given the following pandas dataframe definition,
    write queries based on the request.

    ### df columns:
    {", ".join(df.columns)}
    """

st.title("DataFrame Query Assistant")

df = pd.read_excel('Adidas US Sales Datasets.xlsx', skiprows = 4) # 행을 스킵해주세요 - skiprows = 삭제할 행 개수
df = df.drop("Unnamed: 0", axis=1) 
question = st.text_input("질문을 입력하세요")

if st.button("실행") and question:
    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {
                "role": "system",
                "content": "You generate Pandas boolean indexing code. Output only one line of code starting with df."
            },
            {
                "role": "user",
                "content": table_definition_prompt(df) + question
            }
        ]
    )

    code = response.output_text
    st.code(code, language="python")

try:
    result = eval(code, {"df": df})

    if isinstance(result, pd.DataFrame):
        st.dataframe(result)

    elif isinstance(result, pd.Series):
        st.dataframe(result.to_frame())

    else:
        st.write(result)

except Exception as e:
    st.error(str(e))
