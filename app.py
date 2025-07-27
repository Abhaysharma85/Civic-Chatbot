from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
import json
import os
from functools import wraps
import secrets
from rapidfuzz import fuzz, process
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')

FAQ_FILE = 'faqs.json'

# Use a secure random secret key for session management
app.secret_key = secrets.token_hex(32)
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

def load_faqs():
    # Load FAQs as a list of sections, each with a name and faqs array
    if not os.path.exists(FAQ_FILE):
        with open(FAQ_FILE, 'w') as f:
            json.dump([], f)
    with open(FAQ_FILE, 'r') as f:
        return json.load(f)

def save_faqs(faqs):
    # Save FAQs as a list of sections
    with open(FAQ_FILE, 'w') as f:
        json.dump(faqs, f, indent=2)

def find_answer(question, sections, threshold=70):
    # Gather all questions and their answers with section info
    candidates = []
    for section in sections:
        for faq in section.get('faqs', []):
            candidates.append((faq['question'], faq['answer']))
    # Use rapidfuzz to find the best match
    if not candidates:
        return "Sorry, I don't know the answer to that."
    questions = [q for q, a in candidates]
    # Find the best match
    match, score, idx = process.extractOne(question, questions, scorer=fuzz.token_sort_ratio)
    if score >= threshold:
        return candidates[idx][1]
    return "Sorry, I don't know the answer to that."

def gemini_flash_response(user_input):
    api_key = os.environ.get("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    # Prepend instruction to the user input
    prompt = (
        "Please answer the following question in a single paragraph of about 40 to 50 words, "
        "and then provide a concise list of the most important steps related to the answer. "
        "\nQuestion: " + user_input
    )
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    resp = requests.post(url, headers=headers, json=data)
    if resp.ok:
        result = resp.json()
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return str(result)
    else:
        return f"Error from Gemini API: {resp.text}"

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['question']
    sections = load_faqs()
    answer = find_answer(user_input, sections)
    # If FAQ has a real answer, return it
    if answer != "Sorry, I don't know the answer to that.":
        return jsonify({'answer': answer})
    # If not, check for card-related keywords
    keywords = ['aadhaar', 'adhar', 'pan card', 'voter card']
    user_input_lower = user_input.lower()
    if any(keyword in user_input_lower for keyword in keywords):
        gemini_answer = gemini_flash_response(user_input)
        return jsonify({'answer': gemini_answer})
    # Otherwise, return the default FAQ not found response
    return jsonify({'answer': answer})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash('Incorrect password. Try again.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    # Redirect to homepage after logout
    return redirect(url_for('index'))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@admin_required
def admin():
    sections = load_faqs()
    # Pass sections to the template
    return render_template('admin.html', sections=sections)

@app.route('/admin/add', methods=['POST'])
@admin_required
def add_faq():
    # Add a new FAQ to a section
    section_name = request.form['section']
    question = request.form['question']
    answer = request.form['answer']
    sections = load_faqs()
    for section in sections:
        if section['section'] == section_name:
            section['faqs'].append({'question': question, 'answer': answer})
            break
    else:
        # If section doesn't exist, create it
        sections.append({'section': section_name, 'faqs': [{'question': question, 'answer': answer}]})
    save_faqs(sections)
    return redirect(url_for('admin'))

@app.route('/admin/delete/<section>/<int:faq_id>', methods=['POST'])
@admin_required
def delete_faq(section, faq_id):
    sections = load_faqs()
    for sec in sections:
        if sec['section'] == section:
            if 0 <= faq_id < len(sec['faqs']):
                sec['faqs'].pop(faq_id)
                save_faqs(sections)
            break
    return redirect(url_for('admin'))

@app.route('/admin/edit/<section>/<int:faq_id>', methods=['POST'])
@admin_required
def edit_faq(section, faq_id):
    sections = load_faqs()
    for sec in sections:
        if sec['section'] == section:
            if 0 <= faq_id < len(sec['faqs']):
                sec['faqs'][faq_id]['question'] = request.form['question']
                sec['faqs'][faq_id]['answer'] = request.form['answer']
                save_faqs(sections)
            break
    return redirect(url_for('admin'))

@app.route('/sections')
def get_sections():
    sections = load_faqs()
    # Only return section names and questions (not answers)
    return jsonify([
        {
            'section': section['section'],
            'faqs': [{'question': faq['question']} for faq in section.get('faqs', [])]
        }
        for section in sections
    ])

@app.route('/questions')
def questions():
    sections = load_faqs()
    return render_template('questions.html', sections=sections)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        # Here you could add logic to store or send the message
        flash('Thank you for contacting us! We have received your message.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True) 