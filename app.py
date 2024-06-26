import streamlit as st
import pickle
from utils import *

# Tải dữ liệu từ các file pickle
with open("./data/word_l.pickle", 'rb') as handle:
    word_l = pickle.load(handle)
    
with open("./data/vocab.pickle", 'rb') as handle:
    vocab = pickle.load(handle)

with open("./data/probs.pickle", 'rb') as handle:
    probs = pickle.load(handle)

def main():
    st.title("AUTO CORRECT")

    # Check and initialize the default value for text_input in session_state
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""

    # Get the current value of text input from the user
    user_input = st.text_input("Please enter text", key='user_input')

    if len(user_input.strip()) > 0:
        last_word = user_input.strip().split()[-1]
    else:
        last_word = ""

    # Updates suggestions based on input values
    if last_word:
        out_predict = get_corrections(last_word, probs, vocab, 10)
        suggestions = [tup[0] for tup in out_predict] if out_predict else []
    else:
        suggestions = []

    # Callback to update text input when an option is selected
    def update_input():
        st.session_state.user_input = st.session_state.user_input.rstrip(last_word) + st.session_state.suggestion


    # Create a selectbox with an updated list of options
    option = st.selectbox(
        "Suggestions",
        options= [last_word] +  suggestions,
        key='suggestion',
        on_change=update_input
    )

    st.write("You selected:", option)

if __name__ == "__main__":
    main()
