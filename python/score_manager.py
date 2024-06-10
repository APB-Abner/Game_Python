import json
import os

SCORE_FILE = './scores.json'

def save_score(score):
    if not os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'w') as file:
            json.dump([], file)
    
    with open(SCORE_FILE, 'r') as file:
        scores = json.load(file)
    
    scores.append(score)
    
    with open(SCORE_FILE, 'w') as file:
        json.dump(scores, file)

def get_high_score():
    if not os.path.exists(SCORE_FILE):
        return 0
    
    with open(SCORE_FILE, 'r') as file:
        scores = json.load(file)
    
    if not scores:
        return 0
    
    return max(scores)

def display_scores():
    if not os.path.exists(SCORE_FILE):
        return "No scores available"
    
    with open(SCORE_FILE, 'r') as file:
        scores = json.load(file)
    
    if not scores:
        return "No scores available"
    
    scores.sort(reverse=True)
    top_scores = scores[:5]
    return "\n".join([f"{i+1}. {score}" for i, score in enumerate(top_scores)])
