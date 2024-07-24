# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "YOUR_PEARSONAL_KEY"
)

def process(question):
    completion = client.chat.completions.create(
    model="meta/llama3-70b-instruct",
    messages=[{"role":"user","content":question}],
    temperature=0.5,
    top_p=1,
    max_tokens=1024,
    stream=True
    )

    ans = ""

    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            ans += chunk.choices[0].delta.content  

    return ans

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_string = data.get('string')
    output_string = process(input_string)

    return jsonify({'prediction': output_string})
    
    
if __name__ == '__main__':
    app.run(debug=True)
