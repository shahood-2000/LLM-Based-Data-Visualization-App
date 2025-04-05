# mistral_engine.py
import json
import requests

def query_llm(prompt, df):
    columns = df.columns.tolist()

    full_prompt = f"""
You are a data visualization assistant.

Given this prompt from the user: \"{prompt}\"
And the following dataset columns: {columns}

Return only a JSON like this:
{{
    "x": "column_name",
    "y": "column_name",
    "chart_type": "bar" / "line" / "scatter" / "pie",
    "summary": "Short explanation of what the chart shows"
}}
Only respond with valid JSON — no extra comments or explanation.
"""

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama2",
            "prompt": full_prompt,
            "stream": False
        })

        result = response.json()
        output = result["response"]

        # Extract JSON from model output
        start = output.index("{")
        end = output.rindex("}") + 1
        json_str = output[start:end]
        parsed = json.loads(json_str)

        instructions = {
            "x": parsed.get("x"),
            "y": parsed.get("y"),
            "chart_type": parsed.get("chart_type")
        }

        summary = parsed.get("summary", "")
        return instructions, summary

    except Exception as e:
        print("LLM parsing error:", e)
        return None, "Sorry, I couldn't understand the instructions. Try rephrasing your prompt."
