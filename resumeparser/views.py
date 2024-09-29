from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx2txt

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""

def matchresume(request):
    return render(request, 'matchresume.html')

def matcher(request):
    if request.method == 'POST':
        job_description = request.POST.get('job_description')
        resume_files = request.FILES.getlist('resume')

        if not job_description:
            return render(request, 'matchresume.html', {'message': "Please enter a job description."})

        fs = FileSystemStorage()
        job_description_text = [job_description]
        similarity_scores = []

        for resume_file in resume_files:
            filename = fs.save(resume_file.name, resume_file)
            file_path = fs.path(filename)
            resume_text = extract_text(file_path)

            # Vectorize job description and resume
            vectorizer = TfidfVectorizer().fit_transform(job_description_text + [resume_text])
            vectors = vectorizer.toarray()

            # Calculate cosine similarity
            job_vector = vectors[0]
            resume_vector = vectors[1]
            similarity_score = cosine_similarity([job_vector], [resume_vector])[0][0]

            similarity_scores.append({
                'resume_name': resume_file.name,
                'similarity_score': round(similarity_score, 2)
            })

        return render(request, 'matchresume.html', {
            'similarity_scores': similarity_scores
        })

    return render(request, 'matchresume.html')
