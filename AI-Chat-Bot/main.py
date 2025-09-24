from flask import Flask, render_template, url_for, request
import ollama

app = Flask(__name__)

conversation = []
@app.route("/",methods=["GET","POST"])
def index():
    with open("instructions.txt") as instr:
        sys_ = instr.read()

    ollama.create(model="Kevin", from_="llama3.2",system = sys_,
                  parameters={"temperature": 0.1})
    
    answer = ''

    if request.method == "POST":
        qn = request.form["textInput"]
        if qn not in ('bye','') : 
            answer = ollama.generate(model="Kevin", prompt=qn)
            conversation.append({"type": "client", "content": qn})
            conversation.append({"type": "bot", "content": answer.response})

            if answer != '':
                return render_template("index.html",answer = answer.response, convo=conversation)

            else:
                return render_template("index.html",answer = answer, convo=conversation)
        elif qn == 'bye':
            ollama.delete('Kevin')
            return """
<p style='text-align: center; font-size: 20px;'>Good bye, it was nice chatting with you!<br>
<a href='/'>Return home</a></p>
"""
        
    return render_template("index.html",answer = '', convo='')



if __name__ == "__main__":
    app.run(debug=True)
