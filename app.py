from flask import Flask, render_template, redirect, request, flash, session
from surveys import satisfaction_survey
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')  # Get secret key from environment variable

responses = []

@app.route('/')
def index():
    return render_template("base.html")

@app.route('/questions/<int:qid>', methods=['GET', 'POST'])
def question(qid):
    if len(responses) != qid:
        # Trying to access questions out of order
        flash("Please answer the questions in order!", "error")
        return redirect(f'/questions/{len(responses)}')
    
    if qid >= len(satisfaction_survey.questions):
        # They've answered all the questions
        flash("Survey complete! Thank you for your responses.", "success")
        return redirect('/complete')
        
    if request.method == 'POST':
        answer = request.form['answer']
        responses.append(answer)
        return redirect(f'/questions/{len(responses)}')
        
    question = satisfaction_survey.questions[qid]
    return render_template("question.html", question=question, question_num=qid)

@app.route('/complete')
def complete():
    return render_template("complete.html")

if __name__ == '__main__':
    app.run(debug=True)