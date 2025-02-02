import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Load and store case summaries
cases = {
    "Vosburg v. Putney": {
        "Facts": "A schoolboy lightly kicked another boy, causing an unexpected serious injury due to a pre-existing condition.",
        "Issue": "Can intent transfer in a battery claim even if there was no intent to cause harm?",
        "Rule": "Intent to commit an unlawful act is sufficient for battery liability, even if harm was unintended.",
        "Holding": "Yes, the defendant was liable since the kick was unlawful in the school setting.",
        "Reasoning": "The court found that an unlawful act (kicking) was enough to establish battery, even if harm was unforeseen."
    },
    "Keel v. Hamline": {
        "Facts": "A classroom eraser fight led to a student being hit unintentionally.",
        "Issue": "Can intent transfer in battery cases where the harm was unintended?",
        "Rule": "Intent transfers between participants in a wrongful act, making them all potentially liable.",
        "Holding": "Yes, liability extended to participants, even if they did not directly cause harm.",
        "Reasoning": "Courts hold individuals accountable for group wrongful acts under transferred intent doctrine."
    },
    "Palsgraf v. Long Island Railroad Co.": {
        "Facts": "A passenger dropped a package, causing scales to fall and injure another passenger.",
        "Issue": "Was the railroad liable for injuries caused by an unforeseeable plaintiff?",
        "Rule": "Negligence requires a duty of care owed to the plaintiff, and harm must be foreseeable.",
        "Holding": "No, the railroad was not liable because the harm to the plaintiff was unforeseeable.",
        "Reasoning": "The court emphasized the importance of foreseeability in establishing negligence."
    },
    "Donoghue v. Stevenson": {
        "Facts": "A woman became ill after drinking ginger beer containing a decomposed snail.",
        "Issue": "Does a manufacturer owe a duty of care to the ultimate consumer?",
        "Rule": "Manufacturers owe a duty of care to consumers to avoid foreseeable harm.",
        "Holding": "Yes, the manufacturer was liable for negligence.",
        "Reasoning": "The court established the principle of duty of care in negligence law."
    }
}

# Create FAISS Vector Store
embedding_model = OpenAIEmbeddings()

# Store each case element as a separate document with metadata
documents = []
metadata = []
for case_name, case_data in cases.items():
    for element, text in case_data.items():
        documents.append(text)
        metadata.append({"case": case_name, "element": element})

vectorstore = FAISS.from_texts(documents, embedding_model, metadatas=metadata)
retriever = vectorstore.as_retriever()

# Q&A Chain with enhanced prompt
llm = OpenAI(model_name="gpt-4")
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=retriever,
    chain_type_kwargs={
        "prompt": """
        You are a legal assistant trained to help law students analyze case law. 
        When answering questions, always:
        1. Reference the specific case (e.g., Vosburg v. Putney).
        2. Break down your answer into Facts, Issue, Rule, Holding, and Reasoning.
        3. Use clear and concise language.
        """
    }
)

def answer_question(query):
    return qa_chain.run(query)

# Streamlit UI
st.title("Law Case AI - Case Law Q&A")
st.write("Ask questions about case law and get detailed answers.")

# Case selection dropdown
selected_case = st.selectbox("Select a case:", list(cases.keys()))

# Display case details
st.write(f"### {selected_case}")
st.write("**Facts:**", cases[selected_case]["Facts"])
st.write("**Issue:**", cases[selected_case]["Issue"])
st.write("**Rule:**", cases[selected_case]["Rule"])
st.write("**Holding:**", cases[selected_case]["Holding"])
st.write("**Reasoning:**", cases[selected_case]["Reasoning"])

# Question input
query = st.text_input("Enter your question:")
if query:
    response = answer_question(query)
    st.write("### Answer:")
    st.write(response)

    # Save question and answer to session state for history
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({"question": query, "answer": response})

# Display question history
if "history" in st.session_state and st.session_state.history:
    st.write("### Question History")
    for i, qa in enumerate(st.session_state.history, 1):
        st.write(f"**Q{i}:** {qa['question']}")
        st.write(f"**A{i}:** {qa['answer']}")
        st.write("---")