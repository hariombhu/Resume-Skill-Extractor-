import streamlit as st
import pickle
import re
import nltk

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load pre-trained models
clf = pickle.load(open('clf.pkl', 'rb'))
tfidf = pickle.load(open('tfidf.pkl', 'rb'))

# Category ID to name mapping
category_mapping = {
    15: "Java Developer",
    23: "Testing",
    8: "Devops Engineer",
    20: "Python Developer",
    24: "Web Designing",
    12: "HR",
    13: "Hadoop",
    3: "Blockchain",
    10: "ETL Developer",
    18: "Operational Manager",
    6: "Data Science",
    22: "Sales",
    16: "Mechanical Engineer",
    1: "Arts",
    7: "Database",
    11: "Electrical Engineering",
    14: "Health and Fitness",
    19: "PMO",
    4: "Business Analyst",
    9: "Dotnet Developer",
    2: "Automation Testing",
    17: "Network Security Engineer",
    21: "SAP Developer",
    5: "Civil Engineer",
    0: "Advocate"
}

# Resume cleaning function
def clean_resume(resume_text):
    clean_text = re.sub(r'http\S+\s*', ' ', resume_text)
    clean_text = re.sub(r'RT|cc', ' ', clean_text)
    clean_text = re.sub(r'#\S+', ' ', clean_text)
    clean_text = re.sub(r'@\S+', ' ', clean_text)
    clean_text = re.sub(r'[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
    clean_text = re.sub(r'[^\x00-\x7f]', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    clean_text = clean_text.lower()
    return clean_text

# Streamlit web app
def main():
    st.title("🧠 Resume Skill Extractor")
    st.write("Upload your resume and let the AI predict your skill category!")

    upload_file = st.file_uploader("Upload Resume", type=['pdf', 'docx', 'doc', 'txt'])

    if upload_file is not None:
        try:
            resume_bytes = upload_file.read()
            resume_text = resume_bytes.decode('utf-8')
        except UnicodeDecodeError:
            resume_text = resume_bytes.decode('latin-1')

        cleaned_text = clean_resume(resume_text)
        vectorized_text = tfidf.transform([cleaned_text])
        prediction_id = clf.predict(vectorized_text)[0]
        category_name = category_mapping.get(prediction_id, "Unknown")

        st.success(f"🔍 Predicted Skill Category: **{category_name}**")

# Run the app
if __name__ == '__main__':
    main()