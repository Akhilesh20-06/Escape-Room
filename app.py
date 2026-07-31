from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
import csv


app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")



# Load questions
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as file:
        questions = json.load(file)
        print("Loaded Questions:", len(questions))
        return questions

def save_participant(username, department):
    file_exists = os.path.isfile("participants.csv")

    with open("participants.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Username", "Department"])

        writer.writerow([username, department])
# Login page
@app.route("/")
def home():
    session.clear()
    session["current_question"] = 0
    session["attempts"] = 2
    return render_template("login.html")


# Save participant information in session only
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    department = request.form["department"]

    session["username"] = username
    session["department"] = department

    # Save participant to CSV
    save_participant(username, department)

    return redirect(url_for("question"))
# Question page
@app.route("/question", methods=["GET", "POST"])
def question():

    questions = load_questions()

    current = session.get("current_question", 0)
    attempts = session.get("attempts", 2)

    if current >= len(questions):
        return redirect(url_for("success"))

    q = questions[current]
    message = ""

    if request.method == "POST":

        selected = int(request.form["option"])

        if selected == q["answer"]:

            session["current_question"] = current + 1
            session["attempts"] = 2

            if session["current_question"] >= len(questions):
                return redirect(url_for("success"))

            return redirect(url_for("question"))

        else:

            attempts -= 1
            session["attempts"] = attempts

            if attempts == 0:
                return redirect(url_for("gameover"))

            message = f"❌ Wrong Answer! {attempts} attempt(s) remaining."

    return render_template(
        "question.html",
        question=q,
        question_number=current + 1,
        total_questions=len(questions),
        attempts=attempts,
        message=message,
        username=session.get("username"),
        department=session.get("department")
    )


# Success page
@app.route("/success")
def success():
    return render_template("success.html")


# Game Over page
@app.route("/gameover")
def gameover():
    return render_template("gameover.html")


# Restart
@app.route("/restart")
def restart():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)