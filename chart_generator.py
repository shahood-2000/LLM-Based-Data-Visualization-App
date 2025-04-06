import plotly.express as px
import pandas as pd

def generate_chart(df, instructions):
    # Safety: If instructions are missing or invalid
    if not instructions or not isinstance(instructions, dict):
        return px.scatter(
            x=[0], y=[0],
            title="❌ Sorry, couldn't generate chart. Try rephrasing your prompt."
        )

    chart_type = instructions.get("chart_type", "bar").lower()
    x = instructions.get("x")
    y = instructions.get("y")

    # Safety: If x or y is missing or invalid
    if not x or not y or x not in df.columns or y not in df.columns:
        return px.scatter(
            x=[0], y=[0],
            title="❌ Invalid column names returned by LLM. Try rephrasing your prompt."
        )

    # Chart generation
    if chart_type == "bar":
        return px.bar(df, x=x, y=y, title=f"Bar Chart: {y} by {x}")
    elif chart_type == "line":
        return px.line(df, x=x, y=y, title=f"Line Chart: {y} by {x}")
    elif chart_type == "scatter":
        return px.scatter(df, x=x, y=y, title=f"Scatter Plot: {y} by {x}")
    elif chart_type == "pie":
        return px.pie(df, names=x, values=y, title=f"Pie Chart: {y} by {x}")
    elif chart_type == "histogram":
        return px.histogram(df, x=x, y=y, title=f"Histogram: {y} by {x}")
    elif chart_type == "area":
        return px.area(df, x=x, y=y, title=f"Area Chart: {y} by {x}")
    elif chart_type == "box":
        return px.box(df, x=x, y=y, title=f"Box Plot: {y} by {x}")
    else:
        return px.bar(df, x=x, y=y, title=f"Fallback Chart: {y} by {x} (unknown type '{chart_type}')")
