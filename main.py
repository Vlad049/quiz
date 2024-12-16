from flask import Flask, render_template, redirect, request, url_for

from data import function
from database.base import create_db, Session
from database.models import Pizza


app = Flask(__name__)


@app.get("/")
def index():
    with Session() as session:
        pizzas = session.query(Pizza).all()
        return render_template("index.html", pizzas=pizzas)


@app.get("/poll/")
def poll():
    question = "Яка піцца тобі подобаєтсья найбільше"
    answers = ["Пепероні", "Класична"]
    return render_template("poll.html", question=question, answers=answers)


@app.get("/add_vote/")
def add_vote():
    vote = request.args.get("vote")
    function.write_file(vote)
    return redirect(url_for("results"))


@app.get("/results/")
def results():
    answers = function.read_file()
    return render_template("results.html", answers=answers)


if __name__ == "__main__":
    create_db()
    app.run(debug=True)