# mistral_engine.py (improved prompt engineering + Replicate API)
import os
import json
import replicate

def query_llm(prompt, df):
    columns = df.columns.tolist()

    full_prompt = f"""
You are a smart data visualization assistant.

Given the user's request: \"{prompt}\"
And the available dataset columns: {columns}

You must generate a JSON configuration ONLY in the following format:
{{
    "x": "column_name",
    "y": "column_name",
    "chart_type": "bar" / "line" / "scatter" / "pie" / "histogram" / "area" / "box",
    "summary": "One-sentence interpretation of the chart"
}}

Respond ONLY with JSON. Do not include explanations, commentary, or Markdown.
"""

    try:
        replicate_token = os.getenv("REPLICATE_API_TOKEN")
        os.environ["REPLICATE_API_TOKEN"] = replicate_token

        output = replicate.run(
            "mistralai/mistral-7b-instruct-v0.1",
            input={"prompt": full_prompt, "temperature": 0.3}
        )

        if isinstance(output, list):
            output = "".join(output)

        # Extract and validate JSON
        start = output.index("{")
        end = output.rindex("}") + 1
        json_str = output[start:end]
        parsed = json.loads(json_str)

        instructions = {
            "x": parsed.get("x"),
            "y": parsed.get("y"),
            "chart_type": parsed.get("chart_type", "bar")
        }
        summary = parsed.get("summary", "")
        return instructions, summary

    except Exception as e:
        print("Replicate LLM error:", e)
        return None, "Sorry, the model didn't return valid chart instructions. Try rephrasing your prompt."
