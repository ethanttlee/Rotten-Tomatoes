
import streamlit as st 
from aitextgen import aitextgen 

temperatures = [0.2,0.5,1.0,1.2]

st.title("Text Generator")

description='Utilizing both GPT-2 as well as aitextgen, the text generation model is trained on the critic reviews from the top four most popular genres. The model then takes in a prompt inputted by the user and generates 100 characters of text. The prompt can be a movie title or a user written review. The model has a temperature parameter that essentially determines how conservative(lower values) or risky(higher values) the model\'s prediction will be. In the example, a phrase is inputted with varying temperature values. The lower valued temperature examples more closely resemble actual phrases used in the critic reviews while the higher values become more unintelligible.'

st.write(description)

ex = aitextgen(model_folder="comedy_trained_model",
                tokenizer_file="comedy_aitextgen.tokenizer.json")

st.text("Example:'Chicken Run is a good movie'")
for temperature in temperatures:
    t='Temperature:'+str(temperature)
    st.text(t)
    gpt_text = ex.generate_one(prompt="Chicken Run is a good movie",
            max_length = 100,temperature=temperature)
    st.write(gpt_text)


option = st.selectbox('Select a Genre',('comedy', 'drama', 'documentary','mystery'))
st.write('You selected:', option)

ai = aitextgen(model_folder=f"{option}_trained_model",
    tokenizer_file=f"{option}_aitextgen.tokenizer.json")
    
prompt_text = st.text_input(label = "Enter your prompt:",
    value = " ")

if len(prompt_text) >1:
    with st.spinner("Generating text..."):
        gpt_text = ai.generate_one(prompt=prompt_text,
                max_length = 100,temperature=0.2)
    st.success("Successfully generated the text below! ")

    print(gpt_text)

    st.text(gpt_text)






