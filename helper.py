from typing import List, Dict
import streamlit as st

def verify_age(age: int) -> bool:
    """Verify if user meets age requirement."""
    return age >= 15

def get_major_recommendations(selected_subjects: List[str], subjects_to_majors: Dict) -> List[str]:
    """Get major recommendations based on selected subjects."""
    recommended_majors = set()
    for subject in selected_subjects:
        if subject in subjects_to_majors:
            recommended_majors.update(subjects_to_majors[subject])
    return list(recommended_majors)

def get_universities_for_major(major: str, universities: Dict) -> Dict:
    """Get UAE universities offering the selected major."""
    matching_universities = {}
    for uni_name, uni_data in universities.items():
        if major in uni_data["majors"]:
            matching_universities[uni_name] = {
                "location": uni_data["location"],
                "requirements": uni_data["majors"][major]
            }
    return matching_universities

def format_requirements(requirements: Dict) -> str:
    """Format university requirements for display."""
    formatted_reqs = f"Minimum GPA: {requirements['min_gpa']}\n"
    formatted_reqs += f"IELTS Score: {requirements['ielts']}\n"
    formatted_reqs += "Subject Requirements:\n"
    for req in requirements['requirements']:
        formatted_reqs += f"- {req}\n"
    return formatted_reqs