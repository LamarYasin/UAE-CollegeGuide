# Quiz questions and options for subject interest assessment
QUIZ_QUESTIONS = [
    {
        "question": "When solving problems, I prefer to:",
        "options": {
            "Mathematics": "Work with numbers and equations",
            "Computer Studies": "Use logical step-by-step approaches",
            "Art": "Think creatively and visualize solutions",
            "Business Studies": "Analyze different perspectives and strategies"
        },
        "animation_url": "https://assets9.lottiefiles.com/packages/lf20_xyadoh9h.json"
    },
    {
        "question": "In a group project, I enjoy:",
        "options": {
            "English": "Writing and communicating ideas",
            "Business Studies": "Leading and organizing the team",
            "Art": "Adding creative and visual elements",
            "Computer Studies": "Planning and structuring the work"
        },
        "animation_url": "https://assets9.lottiefiles.com/packages/lf20_cznnfmdf.json"
    },
    {
        "question": "I am most interested in learning about:",
        "options": {
            "Biology": "Living organisms and natural processes",
            "Physics": "How things work and natural laws",
            "Chemistry": "Substances and their interactions",
            "Environmental Science": "Environmental impacts and sustainability"
        },
        "animation_url": "https://assets9.lottiefiles.com/packages/lf20_wdqlpxxy.json"
    },
    {
        "question": "In my free time, I like to:",
        "options": {
            "Computer Studies": "Explore new technologies",
            "Art": "Create or appreciate art",
            "English": "Read or write stories",
            "Biology": "Learn about nature and living things"
        },
        "animation_url": "https://assets9.lottiefiles.com/packages/lf20_yriifcob.json"
    }
]

def calculate_interests(answers):
    """Calculate subject interests based on quiz answers."""
    subject_scores = {}
    for answer in answers:
        if answer in subject_scores:
            subject_scores[answer] = subject_scores[answer] + 1
        else:
            subject_scores[answer] = 1
    
    # Get top subjects (those with highest scores)
    max_score = max(subject_scores.values())
    top_subjects = [subject for subject, score in subject_scores.items() 
                   if score == max_score]
    
    return top_subjects
