import re
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from .skills_list import skills_list

# Define paths for model files
MODEL_PATHS = {
    'categorization_rf': './models/rf_classifier_categorization.pkl',
    'categorization_tfidf': './models/tfidf_vectorizer_categorization.pkl',
    'recommendation_rf': './models/rf_classifier_job_recommendation.pkl',
    'recommendation_tfidf': './models/tfidf_vectorizer_job_recommendation.pkl'
}

# Load models
def load_model(model_path):
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        raise FileNotFoundError(f"Model file '{model_path}' not found. Please ensure the file exists.")

tfidf_vectorizer_categorization = load_model(MODEL_PATHS['categorization_tfidf'])
rf_classifier_categorization = load_model(MODEL_PATHS['categorization_rf'])
tfidf_vectorizer_recommendation = load_model(MODEL_PATHS['recommendation_tfidf'])
rf_classifier_recommendation = load_model(MODEL_PATHS['recommendation_rf'])

def clean_resume(txt):
    clean_text = re.sub('http\S+\s', ' ', txt)
    clean_text = re.sub('RT|cc', ' ', clean_text)
    clean_text = re.sub('#\S+\s', ' ', clean_text)
    clean_text = re.sub('@\S+', '  ', clean_text)
    clean_text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
    clean_text = re.sub(r'[^\x00-\x7f]', ' ', clean_text)
    clean_text = re.sub('\s+', ' ', clean_text)
    return clean_text

def extract_contact_number_from_resume(text):
    pattern = r'\b(?:\+\d{1,2}\s)?\d{10}\b'
    match = re.search(pattern, text)
    if match:
        return match.group()
    return None

def extract_email_from_resume(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(pattern, text)
    if match:
        return match.group()
    return None

def predict_category(resume_text):
    cleaned_text = clean_resume(resume_text)
    resume_tfidf = tfidf_vectorizer_categorization.transform([cleaned_text])
    predicted_category = rf_classifier_categorization.predict(resume_tfidf)[0]
    return predicted_category

def job_recommendation(resume_text):
    cleaned_text = clean_resume(resume_text)
    resume_tfidf = tfidf_vectorizer_recommendation.transform([cleaned_text])
    recommended_job = rf_classifier_recommendation.predict(resume_tfidf)[0]
    return recommended_job

def extract_skills_from_resume(text):
    skills = []
    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)
    return skills

def extract_education_from_resume(text):
    education = []
    education_keywords = [
        'Computer Science', 'Information Technology', 'Software Engineering', 'Electrical Engineering',
        'Mechanical Engineering', 'Civil Engineering', 'Chemical Engineering', 'Biomedical Engineering',
        'Aerospace Engineering', 'Nuclear Engineering', 'Industrial Engineering', 'Systems Engineering',
        'Environmental Engineering', 'Petroleum Engineering', 'Geological Engineering', 'Marine Engineering',
        'Robotics Engineering', 'Biotechnology', 'Biochemistry', 'Microbiology', 'Genetics', 'Molecular Biology',
        'Bioinformatics', 'Neuroscience', 'Biophysics', 'Biostatistics', 'Pharmacology', 'Physiology', 'Anatomy',
        'Pathology', 'Immunology', 'Epidemiology', 'Public Health', 'Health Administration', 'Nursing', 'Medicine',
        'Dentistry', 'Pharmacy', 'Veterinary Medicine', 'Medical Technology', 'Radiography', 'Physical Therapy',
        'Occupational Therapy', 'Speech Therapy', 'Nutrition', 'Sports Science', 'Kinesiology', 'Exercise Physiology',
        'Sports Medicine', 'Rehabilitation Science', 'Psychology', 'Counseling', 'Social Work', 'Sociology',
        'Anthropology', 'Criminal Justice', 'Political Science', 'International Relations', 'Economics', 'Finance',
        'Accounting', 'Business Administration', 'Management', 'Marketing', 'Entrepreneurship', 'Hospitality Management',
        'Tourism Management', 'Supply Chain Management', 'Logistics Management', 'Operations Management',
        'Human Resource Management', 'Organizational Behavior', 'Project Management', 'Quality Management',
        'Risk Management', 'Strategic Management', 'Public Administration', 'Urban Planning', 'Architecture',
        'Interior Design', 'Landscape Architecture', 'Fine Arts', 'Visual Arts', 'Graphic Design', 'Fashion Design',
        'Industrial Design', 'Product Design', 'Animation', 'Film Studies', 'Media Studies', 'Communication Studies',
        'Journalism', 'Broadcasting', 'Creative Writing', 'English Literature', 'Linguistics', 'Translation Studies',
        'Foreign Languages', 'Modern Languages', 'Classical Studies', 'History', 'Archaeology', 'Philosophy', 'Theology',
        'Religious Studies', 'Ethics', 'Education', 'Early Childhood Education', 'Elementary Education',
        'Secondary Education', 'Special Education', 'Higher Education', 'Adult Education', 'Distance Education',
        'Online Education', 'Instructional Design', 'Curriculum Development', 'Library Science', 'Information Science',
        'Computer Engineering', 'Software Development', 'Cybersecurity', 'Information Security', 'Network Engineering',
        'Data Science', 'Data Analytics', 'Business Analytics', 'Operations Research', 'Decision Sciences',
        'Human-Computer Interaction', 'User Experience Design', 'User Interface Design', 'Digital Marketing',
        'Content Strategy', 'Brand Management', 'Public Relations', 'Corporate Communications', 'Media Production',
        'Digital Media', 'Web Development', 'Mobile App Development', 'Game Development', 'Virtual Reality',
        'Augmented Reality', 'Blockchain Technology', 'Cryptocurrency', 'Digital Forensics', 'Forensic Science',
        'Criminalistics', 'Crime Scene Investigation', 'Emergency Management', 'Fire Science', 'Environmental Science',
        'Climate Science', 'Meteorology', 'Geography', 'Geomatics', 'Remote Sensing', 'Geoinformatics', 'Cartography',
        'GIS (Geographic Information Systems)', 'Environmental Management', 'Sustainability Studies', 'Renewable Energy',
        'Green Technology', 'Ecology', 'Conservation Biology', 'Wildlife Biology', 'Zoology'
    ]
    for keyword in education_keywords:
        pattern = r"(?i)\b{}\b".format(re.escape(keyword))
        match = re.search(pattern, text)
        if match:
            education.append(match.group())
    return education

def extract_name_from_resume(text):
    name = None
    pattern = r"(\b[A-Z][a-z]+\b)\s(\b[A-Z][a-z]+\b)"
    match = re.search(pattern, text)
    if match:
        name = match.group()
    return name
