## Resume Skill Extractor

One‑line: A Streamlit app that uses NLP (TF‑IDF + a classical classifier) to predict a candidate's skill category from an uploaded resume.

---

# Overview

Resume Skill Extractor is a lightweight proof‑of‑concept web app built with Streamlit and simple NLP components. It accepts an uploaded resume (PDF/DOCX/DOC/TXT), extracts and cleans text, vectorizes using a pre‑trained TF‑IDF transformer, and predicts a skill/category label using a pre‑trained classifier saved as a pickle file.

The README below documents how to run the app, what model artifacts are required, known limitations, and recommended improvements for production readiness.

---

# What’s included

* Streamlit app script (main app file).
* Pretrained model artifacts (expected in the project root):

  * `tfidf.pkl` — TF‑IDF vectorizer
  * `clf.pkl` — trained classifier (used by the app)
  * optionally `model.pkl` — any additional model/pipeline you maintain

> The app's logic (file upload → cleaning → `tfidf.transform` → `clf.predict`) is taken from the Streamlit script in this repository. (See project code for exact details.)

---

# Category mapping

The classifier outputs an integer category id which the app maps to human‑readable labels. Example mapping used by the app (IDs → labels):

```
0  : Advocate
1  : Arts
2  : Automation Testing
3  : Blockchain
4  : Business Analyst
5  : Civil Engineer
6  : Data Science
7  : Database
8  : Devops Engineer
9  : Dotnet Developer
10 : ETL Developer
11 : Electrical Engineering
12 : HR
13 : Hadoop
14 : Health and Fitness
15 : Java Developer
16 : Mechanical Engineer
17 : Network Security Engineer
18 : Operational Manager
19 : PMO
20 : Python Developer
21 : SAP Developer
22 : Sales
23 : Testing
24 : Web Designing
```

(If you re‑train or change classes, update this mapping to match your training labels.)

---

# How it works (high level)

1. User uploads a resume file in the Streamlit UI.
2. The app extracts raw bytes and attempts a text decode (falls back to `latin-1` if `utf-8` fails).
3. `clean_resume()` removes URLs, mentions, punctuation, non‑ASCII characters, and extra whitespace, and lowercases the text.
4. The cleaned text is vectorized with `tfidf.transform([cleaned_text])`.
5. The saved classifier (`clf.pkl`) predicts the category id; the app maps it to a label and displays the result.

---

# Quick start (run locally)

1. Clone the repo.

2. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# linux/mac
source .venv/bin/activate
# windows (powershell)
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies (example):

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, these packages are required at minimum:

streamlit
scikit-learn
nltk
numpy
pandas
matplotlib
seaborn
joblib
python-docx     # optional but recommended for .docx text extraction
pdfplumber      # optional but recommended for PDFs
PyPDF2          # alternative PDF extractor
```

4. Ensure model artifacts are in the project root:

```
clf.pkl
tfidf.pkl
# optional: model.pkl
```

5. Run the app (replace `app.py` with your script name if different):

```bash
streamlit run app.py
```

Open the URL printed by Streamlit (typically `http://localhost:8501`).

---

# Notes about the current implementation

* The app currently reads uploaded file bytes and decodes them directly (`utf-8` / `latin-1`). This will work for plain `.txt` files but is not a robust method for extracting text from binary formats like PDF or DOCX. For reliable extraction use libraries such as `python-docx` for `.docx` and `pdfplumber` or `PyPDF2` for PDFs.

* The app performs an on‑the‑fly `nltk.download('punkt')` and `nltk.download('stopwords')`. For production you should download these resources once during setup (or include them in your environment) to avoid repetitive downloads on every run.

* The app expects `tfidf.pkl` and `clf.pkl` to be pickles saved with a compatible `scikit-learn` version. Be cautious when loading pickles from untrusted sources — loading arbitrary pickles is a security risk.

---

# Recommended improvements (next steps)

* Text extraction: Use `python-docx` for `.docx`, `pdfplumber`/`PyPDF2` for PDFs, and `textract` or `tika` as a fallback for more formats.

* Skill extraction: Rather than predicting a single coarse category, extract fine‑grained skills using rule‑based NER or a dedicated skill extraction model (spaCy + custom entities or a transformer‑based model).

* Confidence and explainability: Return prediction probabilities (`clf.predict_proba`) and the top contributing features/words for the prediction to improve trust.

* Pipeline serialization: Save the entire preprocessing + estimator pipeline as one artifact (e.g., `joblib.dump(pipeline, 'model.pkl')`) so the app only needs to load one file.

* Model management: Use versioned model files and keep a `models/` folder with metadata (training date, classifier type, classes list).

* Batch processing & CSV export: Allow uploading multiple resumes at once and return a CSV with predictions.

* Tests & CI: Add unit tests that validate text extraction, cleaning, and prediction stubs.

* Deployment: Deploy on Streamlit Cloud, Heroku, or a Docker container for repeatable production deployments.

---

# How to re‑train and save models (brief)

1. Preprocess and clean your training resumes the same way as `clean_resume()`.
2. Fit a `TfidfVectorizer` and your classifier (e.g., `LogisticRegression`, `RandomForest`, etc.).
3. Save artifacts:

```python
import joblib
joblib.dump(tfidf, 'tfidf.pkl')
joblib.dump(clf, 'clf.pkl')
# OR save a pipeline
from sklearn.pipeline import make_pipeline
pipeline = make_pipeline(tfidf, clf)
joblib.dump(pipeline, 'model.pkl')
```

---

# Troubleshooting

* UnicodeDecodeError during upload: The app already tries a latin‑1 fallback. For binary formats switch to proper extractors as recommended above.

* Model / Pickle version errors: Ensure scikit‑learn version compatibility between training and serving environments.

* `nltk` downloads failing on CI or remote host: Preinstall NLTK data or bundle required corpora with your build process.

* `ModuleNotFoundError` for `sklearn.neighbours`: The correct module path is `sklearn.neighbors` (American English spelling); make sure imports match your code and scikit‑learn version.

---

# Project structure (suggested)

```
README.md
app.py                     # your Streamlit app script (rename as needed)
requirements.txt
models/
  ├─ clf.pkl
  ├─ tfidf.pkl
  └─ model.pkl (optional)
  |_Vectorise.pkl(optional)
assets/
  └─ screenshot.png
```

---

# License

This project is released under the MIT License — feel free to reuse and adapt.


