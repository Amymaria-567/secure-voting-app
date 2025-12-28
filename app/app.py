from flask import Flask, render_template, redirect
import redis
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

votes = Counter('votes_total', 'Total votes', ['type'])

@app.route('/')
def index():
    cats = redis_client.get('cats') or 0
    dogs = redis_client.get('dogs') or 0
    return render_template('index.html', cats=cats, dogs=dogs)

@app.route('/vote/<animal>')
def vote(animal):
    if animal in ['cats', 'dogs']:
        redis_client.incr(animal)
        votes.labels(type=animal).inc()
    return redirect('/')

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
