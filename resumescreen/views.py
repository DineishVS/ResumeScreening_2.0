import pdfplumber
from django.shortcuts import render
from django.http import HttpResponse
from .utils.resume_utils import (
    extract_contact_number_from_resume, extract_email_from_resume,
    extract_skills_from_resume, extract_education_from_resume, extract_name_from_resume,
    predict_category, job_recommendation
)
def home_view(request):
    return render(request, 'home.html')

def resumeextracter(request):
    return render(request, 'resume_extracter.html')

def resume(request):
    return render(request, 'upload.html')

# Function to extract text from a PDF file
def pdf_to_text(file):
    text = ""
    with pdfplumber.open(file) as pdf_file:
        for page in pdf_file.pages:
            text += page.extract_text()
    return text

# View to handle the resume upload and prediction
def predict_resume(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        file = request.FILES['resume']
        filename = file.name

        if filename.endswith('.pdf'):
            text = pdf_to_text(file)
        elif filename.endswith('.txt'):
            text = file.read().decode('utf-8')
        else:
            return render(request, 'resume.html', {'message': "Invalid file format. Please upload a PDF or TXT file."})

        try:
            predicted_category = predict_category(text)
            recommended_job = job_recommendation(text)
            phone = extract_contact_number_from_resume(text)
            email = extract_email_from_resume(text)
            extracted_skills = extract_skills_from_resume(text)
            extracted_education = extract_education_from_resume(text)
            name = extract_name_from_resume(text)

            return render(request, 'results.html', {
                'predicted_category': predicted_category,
                'recommended_job': recommended_job,
                'phone': phone,
                'email': email,
                'extracted_skills': extracted_skills,
                'extracted_education': extracted_education,
                'name': name
            })
        except Exception as e:
            return render(request, 'resume.html', {'message': f"Error processing resume: {e}"})

    else:
        return render(request, 'resume.html', {'message': "No resume file uploaded."})
