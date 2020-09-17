from flask import Flask, escape, request, render_template

from support.regression import nyse_reg

app = Flask(__name__)

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Its the End of time',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'I guess it is not',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route('/')
@app.route('/home')
def hello():
    return render_template("home.html", posts = posts, title = "Home")

@app.route('/nyse', methods=["POST", "GET"])
def nyse():
    if request.method == "POST":
        nyse_data = []
        nyse_data.append(request.form["company_symbol"])
        nyse_data.append(request.form["open_val"])
        nyse_data.append(request.form["high_val"])
        nyse_data.append(request.form["low_val"])

        prediction, dataframe = nyse_reg(nyse_data)

        # prediction = {"prediction" : prediction}

        return render_template("predictions.html", posts=prediction, data = dataframe.to_html())
    else:
        return render_template("nyse.html")

@app.route('/about')
def about():
    return render_template("about.html", title = "Home")

if __name__ == '__main__':
    app.run(debug=True)