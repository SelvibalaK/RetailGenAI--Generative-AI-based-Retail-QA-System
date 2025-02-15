import streamlit as st
import importlib.util

spec = importlib.util.spec_from_file_location(
    "langretailmain", 
    r"D:\User1\langchainretail\setup\langretailmain.py"
)
sql_assistant_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sql_assistant_module)
SQLAssistant = sql_assistant_module.SQLAssistant

def format_response(response):
    if isinstance(response, dict):
        return str(response.get('result', ''))
    return str(response)

def main():
    # Page configuration
    st.set_page_config(page_title="T-Shirt Inventory Assistant", page_icon="👕")
    
    # Sidebar
    st.sidebar.title("📚 Sample Questions")
    example_questions = [
        "How many white Levi's t-shirts do we have in large size?",
        "What's the total value of small size t-shirts?",
        "How much revenue will we get from Nike shirts with discounts?",
        "How many blue Van Heusen shirts are in stock?",
        "What's the total inventory value of all brands?"
    ]
    
    st.sidebar.markdown("### Try these examples:")
    for question in example_questions:
        if st.sidebar.button(f"🔹 {question}"):
            st.session_state.question = question
            
    # Main content
    st.title("👕 T-Shirt Inventory Assistant")
    st.markdown("### Your AI-powered inventory query assistant")
    
    # Initialize assistant
    if 'assistant' not in st.session_state:
        st.session_state.assistant = SQLAssistant()
    if 'question' not in st.session_state:
        st.session_state.question = ""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        
    # Input area with any previous selection
    user_question = st.text_input("💭 Ask anything about the T-shirt inventory:", value=st.session_state.question)
    
    if st.button("🔍 Get Answer"):
        if user_question:
            with st.spinner("🤔 Analyzing inventory data..."):
                response = st.session_state.assistant.get_response(user_question)
                formatted_response = format_response(response)
                
                # Add to chat history
                st.session_state.chat_history.append((user_question, formatted_response))
                
                # Display result in a clean format
                st.markdown("### 📊 Answer:")
                st.success(formatted_response)
                
        else:
            st.warning("⚠️ Please enter a question!")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 📜 Previous Queries")
        for i, (q, a) in enumerate(st.session_state.chat_history[-5:], 1):
            with st.expander(f"Query {i}: {q[:50]}..."):
                st.write("Question: ", q)
                st.write("Answer: ", a)

if __name__ == "__main__":
    main()
