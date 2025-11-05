from flask import Flask, request, render_template
import os
from RAGlib import loadDoc, splitDoc, vector_db, retriever, create_chain

app = Flask(__name__)
@app.route('/',methods=["GET","POST"])
def main():
    if request.method == "POST":
        f = request.files['documents']
        f.save('static/files/'+f.filename)
    all_files = os.listdir('static/files')
    return render_template("index.html",all_files = all_files,fNum = len(all_files))

@app.route('/rag',methods=["GET","POST"])
def rag():
    result = None
    if request.method == "POST":
        selectedFile = request.form.get("file")
        question = request.form.get("question")
        # load file
        doc = loadDoc(str(selectedFile))
        # split file
        all_splits = splitDoc(doc)
        # add to vector db
        vDB = vector_db(all_splits)
        # build retriever
        golden_retriever = retriever(vDB)
        # build chain
        myChain = create_chain(golden_retriever)
        result = myChain.invoke(input = question)
    all_files = os.listdir('static/files')
    return render_template("rag.html",all_files = all_files,
                           fNum = len(all_files), result = result)

if __name__ == "__main__":
    app.run(debug=True)
