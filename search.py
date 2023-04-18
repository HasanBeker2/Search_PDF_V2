import os
from PyPDF2 import PdfReader
import openai
import fitz
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

templates_path = os.path.abspath('templates')
app = Flask(__name__, template_folder=templates_path)

openai.api_key = "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" # replace with your OpenAI API key

def search_text_in_pdf_file(pdf_file_path, search_text):
    with open(pdf_file_path, 'rb') as f:
        pdf_reader = PdfReader(f)
        for page_obj in pdf_reader.pages:
            text = page_obj.extract_text()
            if search_text in text:
                return True
                
    return False

# def search_text_in_pdf_file(filename, search_term):
#     doc = fitz.open(filename)
#     results = []
#     for page_num, page in enumerate(doc):
#         matches = page.search_for(search_term)
#         for match in matches:
#             results.append({
#                 'page': page_num + 1,
#                 'screen': match,
#                 'text': page.get_text('text', search_rect=match)
#             })
#     doc.close()
#     return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_text = request.form['search_text']
    pdf_files_path = "C:/Users/hasan/OneDrive/Desktop/Python Programming/PDF_Search_Engine/pdf_files"
    search_results = []
    for file_name in os.listdir(pdf_files_path):
        if file_name.endswith(".pdf"):
            pdf_file_path = os.path.join(pdf_files_path, file_name)
            if search_text_in_pdf_file(pdf_file_path, search_text):
                search_results.append(pdf_file_path)
    return render_template('search.html', search_results=search_results)

if __name__ == '__main__':
    app.run(debug=True)
