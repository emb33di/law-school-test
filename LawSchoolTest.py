import streamlit as st


# The VosburgVPutneyAI class from earlier
class VosburgVPutneyAI:
    def __init__(self):
        self.facts = [
            "Vosburg, a 14-year-old boy, was sitting in a classroom.",
            "Putney, another student, kicked Vosburg in the leg while sitting on the same bench.",
            "Vosburg was not immediately injured, but the kick resulted in a serious leg injury.",
            "The injury occurred due to an underlying condition that was aggravated by the kick."
        ]

        self.holding = "The court held that Putney was liable for the injury caused by the intentional act of kicking, even if he did not intend the specific injury."

        self.reasoning = [
            "The court determined that even though Putney did not intend to cause the specific injury, his intentional act of kicking was sufficient to establish liability.",
            "The key issue was whether the act was a battery, which the court concluded it was, as the kick was intentional.",
            "The court held that it was unnecessary to show that the defendant intended the precise harm caused, just the act itself.",
            "The court emphasized that an intentional act, even without harmful intent, can result in liability.",
            "The injury to Vosburg was not the result of an accident, but rather an intentional, unlawful act.",
            "The underlying condition of Vosburg's leg did not absolve Putney of liability; instead, it made the injury more severe.",
            "The court focused on the general principle of intentional torts and the importance of intent in establishing liability.",
            "The court found that the law protects individuals from intentional harm, even if the harm caused was unforeseen.",
            "The case reinforced the rule that intent to commit the tort is the critical element in determining liability in battery cases.",
            "The court decided that the defendant was fully responsible for the injuries, despite the fact that they were more severe than expected."
        ]

    def generate_brief(self):
        return {
            "facts": self.facts,
            "holding": self.holding,
            "reasoning": self.reasoning
        }

    def answer_question(self, question):
        if "facts" in question.lower():
            return self.facts
        elif "holding" in question.lower():
            return self.holding
        elif "reasoning" in question.lower():
            return self.reasoning
        else:
            return "I'm sorry, I can only answer questions about the facts, holding, and reasoning of the case."


# Streamlit app
st.title("Vosburg v. Putney AI Agent")
st.write("This agent can answer questions and generate a law school-style brief for the case of Vosburg v. Putney.")

# Initialize the AI agent
vosburg_case_ai = VosburgVPutneyAI()

# Display a dropdown for the user to choose the section they want to learn about
section_choice = st.selectbox("Select a Section", ["Facts", "Holding", "Reasoning", "Generate Cold Call Brief"])

if section_choice == "Facts":
    st.subheader("Facts of the Case:")
    for fact in vosburg_case_ai.facts:
        st.write(f"• {fact}")
elif section_choice == "Holding":
    st.subheader("Holding of the Case:")
    st.write(f"• {vosburg_case_ai.holding}")
elif section_choice == "Reasoning":
    st.subheader("Reasoning Behind the Decision:")
    for reason in vosburg_case_ai.reasoning:
        st.write(f"• {reason}")
elif section_choice == "Generate Cold Call Brief":
    brief = vosburg_case_ai.generate_brief()
    st.subheader("Cold Call Brief")
    st.write("### Facts:")
    for fact in brief["facts"]:
        st.write(f"• {fact}")
    st.write("### Holding:")
    st.write(f"• {brief['holding']}")
    st.write("### Reasoning:")
    for reason in brief["reasoning"]:
        st.write(f"• {reason}")

# Add a text input for questions
question = st.text_input("Ask a question about the case:")

if question:
    answer = vosburg_case_ai.answer_question(question)
    st.subheader("Answer:")
    st.write(answer)
