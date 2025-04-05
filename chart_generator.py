# chart_generator.py
import plotly.express as px

def generate_chart(df, instructions):
    chart_type = instructions.get("chart_type")
    x = instructions.get("x")
    y = instructions.get("y")

    if not x or not y:
        raise ValueError("Missing x or y axis in chart instructions")

    try:
        if chart_type == "bar":
            fig = px.bar(df, x=x, y=y, title=f"Bar Chart: {y} vs {x}")
        elif chart_type == "line":
            fig = px.line(df, x=x, y=y, title=f"Line Chart: {y} over {x}")
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x, y=y, title=f"Scatter Plot: {y} vs {x}")
        elif chart_type == "pie":
            fig = px.pie(df, names=x, values=y, title=f"Pie Chart: {y} by {x}")
        else:
            raise ValueError("Unsupported chart type")

        return fig

    except Exception as e:
        raise ValueError(f"Failed to generate chart: {str(e)}")
