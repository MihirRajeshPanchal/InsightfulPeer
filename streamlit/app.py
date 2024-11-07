import streamlit as st
from g1 import generate_response
import json
import groq

client = groq.Groq()

def main():
    st.set_page_config(page_title="C-o-T Peer Review", page_icon="🧠", layout="wide")
    
    st.title("Chain of Thought Reasoning Peer Review (Exhaustive or Trivial)")
    
    
    example_1 = ". . . Main comments:. - The idea of building 3D adversarial objects is novel so the study is interesting. "
    example_2 = "In particular, this could be a first step towards better understanding the optimization landscape of memory-augmented neural networks (Memory Networks, Neural Turing Machines, etc) which try to learn reasoning tasks or algorithms."

    
    user_query = st.text_input("Enter a Review Sentence ", placeholder="e.g., However, the paper is incomplete, with a very low number of references, only 2 conference papers if we assume the list is up to date.")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Example 1",key="example1"):
            user_query = example_1

    with col2:
        if st.button("Example 2",key="example2"):
            user_query = example_2

    if user_query:     
        st.write(f"Query: {user_query}")
        
        user_query += " Classify the following sentence as trivial or exhaustive ('Trivial' typically refers to something that is unimportant or lacking in significance, whereas 'exhaustive' implies a thorough or comprehensive treatment of a subject.) Give end result as Trivial or Exhaustive."
        
        st.write("Generating response...")
        
        response_container = st.empty()
        time_container = st.empty()
        
        for steps, total_thinking_time in generate_response(user_query, client):
            with response_container.container():
                for i, (title, content, thinking_time) in enumerate(steps):
                    
                    if not isinstance(content, str):
                        content = json.dumps(content)
                    if title.startswith("Final Answer"):
                        st.markdown(f"### {title}")
                        if '```' in content:
                            parts = content.split('```')
                            for index, part in enumerate(parts):
                                if index % 2 == 0:
                                    st.markdown(part)
                                else:
                                    if '\n' in part:
                                        lang_line, code = part.split('\n', 1)
                                        lang = lang_line.strip()
                                    else:
                                        lang = ''
                                        code = part
                                    st.code(part, language=lang)
                        else:
                            st.markdown(content.replace('\n', '<br>'), unsafe_allow_html=True)
                    else:
                        with st.expander(title, expanded=True):
                            st.markdown(content.replace('\n', '<br>'), unsafe_allow_html=True)
            
            if total_thinking_time is not None:
                time_container.markdown(f"**Total thinking time: {total_thinking_time:.2f} seconds**")

if __name__ == "__main__":
    main()