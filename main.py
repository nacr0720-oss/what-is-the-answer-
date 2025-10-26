import streamlit as st

def cols(vertical: str, col: str) -> str:
    try:
        colleft, colcenter, colright = st.columns([1,1,1], vertical_alignment=vertical)
        if col == 'l':
            return colleft
        elif col == 'c':
            return colcenter
        elif col == 'r':
            return colright
    except:
        print('ERROR')

with open('questions', 'r') as q:
    questions = set(q.read())

with cols('top', 'r'):
    col1, col2 = st.columns([3, 1], )
    with col1:
        search = st.text_input('', placeholder='search', key='phyllacossefalo').lower()
        def cancel_text():
            st.session_state.phyllacossefalo = ''
    with col2:
        cancel = st.button('✖', type='tertiary', on_click=cancel_text)

if search == '':
    st.title('all questions in the world')
    st.write('and your answers')
    st.divider()
    for question, resoluction in questions.items():
        st.write(f'{question} '.capitalize(), f'{resoluction}'.capitalize())
else:
    st.title(f'search result for "{search}"')
    st.divider()
    for result, answer in questions.items():
        if search in result:
            st.title(f'{result} '.capitalize())
            st.title(f'{answer}'.capitalize())
        else:
            st.title(f'Sorry no exist "{search}" in this site')






