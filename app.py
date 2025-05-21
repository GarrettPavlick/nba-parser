from flask import Flask, request, jsonify
import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/nba", methods=["POST"])
def parse_champions():
    data = request.get_json()
    champions_text = data.get("champions", "")
    entries = [entry.strip() for entry in champions_text.split(",") if entry.strip()]
    
    results = []
    for entry in entries:
        try:
            year, team = entry.strip().split(" ", 1)
        except ValueError:
            continue  # skip malformed entries
        prompt = f"Who did the {year} {team} defeat in the NBA Finals?"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a basketball expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            loser = response['choices'][0]['message']['content'].strip()
        except Exception as e:
            loser = f"Error: {str(e)}"
        results.append({
            "Year": year,
            "Winner": team,
            "Loser": loser
        })
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
