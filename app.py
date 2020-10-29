
import PyPDF2 as pdf
from flask import Flask, request, render_template
import spacy
import docx2txt

app = Flask(__name__)
nlp = spacy.load('resume_model')

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/predict',methods=["GET", "POST"])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    
    global f1
    file = request.files['file']

    f1 = file.filename

    extension=f1.split(".")[-1]
    
    if extension =="docx":
       
        resume = docx2txt.process(file)
        
    elif extension =="pdf":
       
        pdf_reader = pdf.PdfFileReader(file)

        pages = pdf_reader.getNumPages()
        resume = ''
        for i in range(pages):
            page = pdf_reader.getPage(i)
            resm = page.extractText()
            resume = resume+resm
    
    elif extension =="txt":
        resume = ''
        for i in file:
            resume = resume+str(i)
        
 
        #resume = open(f1).read()

    doc = nlp(resume)
    result = []

    for ent in doc.ents:
        result.append(str(ent.label_.upper())+"   --    " +str(ent.text))
        
    #     #print(f'{ent.label_.upper():{30}} - {ent.text}')
    
    return render_template('result.html', results=result)

if __name__ == "__main__":
    app.run(debug=True)
