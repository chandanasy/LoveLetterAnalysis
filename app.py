#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, session, redirect, url_for
import pandas as pd
import re

app = Flask(__name__)
app.secret_key = 'dc2e779cd350a73054d804e150d4546c'  # Needed for session management

df = pd.read_csv("evan_letters_main_letters.csv")

def clean_text(text):
    # Remove HTML tags
    cleaned = re.sub(r'<[^>]*>', '', text)
    # Remove unwanted characters, preserving periods, commas, single quotes, and spaces
    cleaned = re.sub(r"[^a-zA-Z0-9\s.,']", '', cleaned)
    # Replace sequences of whitespace with a single space
    cleaned = re.sub(r'\s+', ' ', cleaned)
    # Add a space after periods if missing
    cleaned = re.sub(r'\.(?=[a-zA-Z])', '. ', cleaned)
    # Add a space after commas if missing
    cleaned = re.sub(r'\,(?=[a-zA-Z])', ', ', cleaned)
    # Remove '\xa0' characters, backslashes, and trim whitespace
    cleaned = cleaned.replace('\xa0', ' ').replace('\\', '').strip()
    return cleaned

# Ensure all data in 'letter' column is treated as string
df['letter'] = df['letter'].astype(str)

# Then apply the cleaning function
df['cleaned_letter'] = df['letter'].apply(clean_text)

@app.route('/')
def home():
    session['index'] = 0  # Initialize or reset the session index
    return redirect(url_for('letter'))  # Redirect to the first letter

@app.route('/letter')
def letter():
    # Check if the index is within the bounds of the dataframe
    if 'index' in session and session['index'] < len(df):
        # Fetch the letter at the current index
        current_letter = df.iloc[session['index']]['cleaned_letter']
        session['index'] += 1  # Increment the index for the next letter
        return render_template('letter.html', letter=current_letter)
    else:
        return "No more letters, or session not started. <a href='/'>Start Over</a>"

@app.route('/quit')
def quit():
    return "You have quit the application."

if __name__ == '__main__':
    app.run(debug=True)



