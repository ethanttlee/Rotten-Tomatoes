
import streamlit as st 
from aitextgen import aitextgen 

st.title("Text Generator")

option = st.selectbox('Select a Genre',('drama', 'comedy', 'documentary','mystery'))
st.write('You selected:', option)

ai = aitextgen(model_folder=f"{option}_trained_model",
    tokenizer_file=f"{option}_aitextgen.tokenizer.json")
    
prompt_text = st.text_input(label = "Enter your prompt:",
    value = " ")

if len(prompt_text) >1:
    with st.spinner("Generating text..."):
        gpt_text = ai.generate_one(prompt=prompt_text,
                max_length = 100 )
    st.success("Successfully generated the text below! ")
    st.balloons()

    print(gpt_text)

    st.text(gpt_text)






