import streamlit as st
from data.majors import SUBJECTS_TO_MAJORS, MAJOR_DESCRIPTIONS
from data.universities import UAE_UNIVERSITIES
from data.quiz import QUIZ_QUESTIONS, calculate_interests
from utils.helper import verify_age, get_major_recommendations, get_universities_for_major, format_requirements
from streamlit_lottie import st_lottie
import requests
import json


def load_lottie_url(url: str):
    """Load Lottie animation from URL."""
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def main():
    st.set_page_config(page_title="UAE College Guide",
                       page_icon="🎓",
                       layout="wide")

    st.title("🎓 UAE College Selection Guide")
    st.write("Find your perfect college path based on your interests!")

    # Initialize session state
    if 'age_verified' not in st.session_state:
        st.session_state.age_verified = False
    if 'selected_major' not in st.session_state:
        st.session_state.selected_major = None
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False

    # Age verification
    if not st.session_state.age_verified:
        st.info("👋 Welcome! Please verify your age to continue.")
        age = st.number_input("Enter your age:",
                              min_value=0,
                              max_value=100,
                              value=15)
        if st.button("Verify Age"):
            if verify_age(age):
                st.session_state.age_verified = True
                st.rerun()
            else:
                st.error(
                    "Sorry, this tool is only for users aged 15 and above.")
            return

    # Main application flow
    if st.session_state.age_verified:
        if not st.session_state.quiz_completed:
            st.subheader("📝 Subject Interest Quiz")
            st.write(
                "Let's discover your academic interests through this interactive quiz!"
            )

            # Display current question
            current_q = QUIZ_QUESTIONS[st.session_state.current_question]

            # Load and display animation
            with st.container():
                col1, col2 = st.columns([1, 2])
                with col1:
                    lottie_anim = load_lottie_url(current_q["animation_url"])
                    if lottie_anim:
                        st_lottie(
                            lottie_anim,
                            key=f"question_{st.session_state.current_question}"
                        )

                with col2:
                    st.write(
                        f"### Question {st.session_state.current_question + 1}/{len(QUIZ_QUESTIONS)}"
                    )
                    st.write(current_q["question"])

                    # Create buttons for each option
                    for subject, description in current_q["options"].items():
                        if st.button(f"🔘 {description}", key=subject):
                            st.session_state.quiz_answers.append(subject)
                            if st.session_state.current_question < len(
                                    QUIZ_QUESTIONS) - 1:
                                st.session_state.current_question += 1
                                st.rerun()
                            else:
                                st.session_state.quiz_completed = True
                                st.rerun()

            # Display progress bar
            progress = (
                st.session_state.current_question) / len(QUIZ_QUESTIONS)
            st.progress(progress)

        else:
            # Quiz completed - show results and recommendations
            if st.session_state.quiz_answers:
                st.subheader("🎉 Your Quiz Results")
                recommended_subjects = calculate_interests(
                    st.session_state.quiz_answers)

                st.write("Based on your answers, you show strong interest in:")
                for subject in recommended_subjects:
                    st.write(f"- {subject}")

                st.subheader("2️⃣ Recommended Majors")
                recommended_majors = []
                for subject in recommended_subjects:
                    if subject in SUBJECTS_TO_MAJORS:
                        recommended_majors.extend(SUBJECTS_TO_MAJORS[subject])
                recommended_majors = list(set(recommended_majors))

                col1, col2 = st.columns([2, 1])
                with col1:
                    selected_major = st.selectbox("Choose a major to explore:",
                                                  options=recommended_majors)

                with col2:
                    if selected_major in MAJOR_DESCRIPTIONS:
                        st.info(
                            f"**Major Description:**\n\n{MAJOR_DESCRIPTIONS[selected_major]}"
                        )

                if selected_major:
                    st.session_state.selected_major = selected_major
                    st.subheader("3️⃣ Available Universities")

                    matching_universities = get_universities_for_major(
                        selected_major, UAE_UNIVERSITIES)

                    if matching_universities:
                        for uni_name, uni_data in matching_universities.items(
                        ):
                            with st.expander(
                                    f"📚 {uni_name} - {uni_data['location']}"):
                                st.markdown("#### Requirements")
                                st.text(
                                    format_requirements(
                                        uni_data['requirements']))
                    else:
                        st.warning(
                            "No universities found for this major in our database."
                        )

                # Add restart quiz button
                if st.button("🔄 Retake Quiz"):
                    st.session_state.quiz_completed = False
                    st.session_state.current_question = 0
                    st.session_state.quiz_answers = []
                    st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center'>
            <p>Made with ❤️ for UAE students</p>
            <p>Disclaimer: Requirements may vary. Please verify with individual universities.</p>
        </div>
        """,
                unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    if __name__ == "__main__":
        import os
        os.system(
            "streamlit run main.py --server.port 8080 --server.address 0.0.0.0"
        )
