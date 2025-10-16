from flask import Flask, render_template, request, flash, redirect, url_for
from lib.schema import QDetails
from lib import db
from lib.validate import screener_check, complete_check
from csv import reader


app = Flask(__name__)
app.secret_key = 'secret secret secret'
app.jinja_env.filters['zip'] = zip

data = open("datamap.csv", "r")
variables = next(reader(data, delimiter=','))

record_data = {}
for i in variables:
    record_data[i] = None


record_data["status"] = 1
checker = 'valid'
@app.route('/')
def home():
    return render_template("home.html")

age = ''
@app.route('/q1', methods=["GET", "POST"])
def q1():
    global age, record_data, checker
    q_text = QDetails()
    q_text.get_xml("qre.xml", "Q1")
    if request.method == 'POST':
        age = request.form["q1"]
        if age.isnumeric():
            age = int(age)
            if age in range(18, 100):
                record_data["q1"] = age
                checker = complete_check("q1", record_data)
                if checker == 'valid':
                    f_message = 'You are ' + str(age) + ' years-old'
                    flash(f_message)
                    return redirect(url_for('q2'))
                elif checker == 'invalid':
                    return "Invalid data not submitted to database!"
                else:
                    pass
            else:
                record_data["status"] = 2
                record_data["q1"] = age
                checker = screener_check('q1', record_data)
                if checker == 'valid':
                    db.add_record(record_data)
                elif checker == 'invalid':
                    return "Invalid data not submitted to database!"
                else:
                    pass
                checker = 'valid'
                for i in variables:
                    record_data[i] = None
                record_data["status"] = 1
                return render_template("screener_msg.html")
        else:
            flash("Invalid input, please type valid age number!")
    return render_template("q1.html", q_text=q_text.qtext, age=age)




@app.route("/q2", methods=['GET','POST'])
def q2():
    global record_data
    qndet = QDetails()
    qndet.get_xml("qre.xml", "Q2")

    if request.method == 'POST':
        q2_ = request.form['Q2_radio']
        record_data["q2"] = int(q2_)
        checker = complete_check("q2", record_data)
        if checker == 'valid':
            f_message = 'your choice is ' + str(q2_)
            flash(f_message)
            return redirect(url_for('q3'))
        elif checker == 'invalid':
            return "Invalid data not submitted to database! " + "Q2: " + str(record_data["q2"]) + "Checker: " + checker + "Status: " + str(record_data["status"])
        else:
            pass
    return render_template("q2.html", q_text=qndet.qtext, q_options=qndet.options, q_id=qndet.option_ids, zip=zip)



q3data = []
@app.route("/q3", methods=['GET','POST'])
def q3():
    global q3data, record_data, checker
    qndet = QDetails()
    qndet.get_xml("qre.xml", "Q3")
    q3opt_temp = qndet.options
    q3opts = []
    for i in q3opt_temp:
        i = i.split(" ")
        q3opts.append(i[0])
    q3data = [0 for x in range(len(q3opt_temp))]
    if request.method == 'POST':
        q3_ = request.form.getlist('Q3_multi')
        for i in q3_:
            if "None" in q3_ and len(q3_) > 1:
                flash("You've selected conflicting items, please try again!")
                return redirect(url_for('q3'))
            elif "None" in q3_ and len(q3_) == 1:
                q3data[-1] = 1
                record_data["status"] = 2
                q3map = ["Q3_0_1", "Q3_0_2", "Q3_0_3", "Q3_0_4", "Q3_0_5", "Q3_0_6", "Q3_0_7", "Q3_0_99"]
                for x, y in zip(q3map, q3data):
                    record_data[x] = y
                checker = screener_check('Q3_0_99', record_data)
                if checker == 'valid':
                    db.add_record(record_data)
                elif checker == 'invalid':
                    return "Invalid data not submitted to database!"
                else:
                    pass
                checker = 'valid'
                for i in variables:
                    record_data[i] = None
                return render_template("screener_msg.html")
            elif i in q3opts and i != "None":
                q3data[q3opts.index(i)] = 1
            else:
                pass
        record_data["status"] = 1
        q3map = ["Q3_0_1", "Q3_0_2", "Q3_0_3", "Q3_0_4", "Q3_0_5", "Q3_0_6", "Q3_0_7", "Q3_0_99"]
        for x, y in zip(q3map, q3data):
            record_data[x] = y
        flash(q3data)
        checker = complete_check("q3",record_data)
        if checker == "valid":
            if q3data[-2] == 1:
                return redirect(url_for('q3_1'))
            else:
                return redirect(url_for('q3_2'))
        elif checker == 'invalid':
            return "Invalid data not submitted to database!"
        else:
            pass
    q3data.clear()
    return render_template("q3.html", q_text=qndet.qtext, q_options=qndet.options)


q3_1_ = ''
@app.route("/q3_1", methods=['GET', 'POST'])
def q3_1():
    global record_data, q3_1_
    qndet = QDetails()
    qndet.get_xml("qre.xml", "Q3.1")
    if request.method == 'POST':
        q3_1_ = request.form['Q3_1t']
        if q3_1_ in ['', ' ', '  ']:
            flash("Please do not leave the field empty!")
            return redirect(url_for('q3_1'))
        else:
            checker = complete_check("q3_1", record_data)
            if checker == "valid":
                record_data["Q3_1"] = q3_1_
                flash(q3_1_)
                return redirect(url_for('q3_2'))
            elif checker == 'invalid':
                return "Invalid data not submitted to database!"
            else:
                pass
    q3_1_ = ''

    return render_template("q3_1.html", q_text=qndet.qtext)



@app.route("/q3_2", methods=['GET','POST'])
def q3_2():
    global q3data, record_data, checker
    qndet = QDetails()
    qndet.get_xml("qre.xml", "Q3.2")
    opts_ = qndet.options
    q3_2_ = []
    q3_2data_all = [None for x in q3data[:-1]]
    q32map = ["Q3_2_1", "Q3_2_2", "Q3_2_3", "Q3_2_4", "Q3_2_5", "Q3_2_6", "Q3_2_7"]

    for i in range(len(q3data)):
        if q3data[i] == 1:
            q3_2_.append(opts_[i])
        else:
            pass

    if request.method == "POST":
        q3_2data = request.form.getlist("Q3_2")
        q3_2data = [int(x) for x in q3_2data]

        for i, j in zip(q3_2_, q3_2data):
            q3_2data_all[opts_.index(i)] = j
        for x, y in zip(q32map, q3_2data_all):
            record_data[x] = y
        checker = complete_check("q3_2", record_data)
        if checker == 'valid':
            db.add_record(record_data)
        elif checker == 'invalid':
            return "Invalid data not submitted to database!"
        else:
            pass
        for i in variables:
            record_data[i] = None
        record_data["status"] = 1
        return render_template("complete_msg.html")
    return render_template("q3_2.html", q_text=qndet.qtext, q_options=q3_2_)
data.close()

if __name__ == '__main__':
    app.run(debug=True)
