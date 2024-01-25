# klima/app.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import datetime
from klima import fetch_and_process_data, create_interactive_chart, create_tooltip_data
#from klima import get_temperature_data, plot_temperature

app = FastAPI()

# Set up Jinja2Templates for rendering HTML templates
templates = Jinja2Templates(directory="templates")

chart = None

@app.get("/")
def read_root(request: Request):
    global chart

    if chart is None:
        chart = create_interactive_chart()

    return templates.TemplateResponse("klima.html", {"request": request})

@app.get("/plot_global.json")
def read_chart():
    global chart

    # Check if chart is None or empty
    if chart is None or chart.empty:
        print("Error: Invalid or empty chart.")
        return {"error": "Invalid or empty chart"}

    return chart.to_json()


@app.get("/tooltip_data/{year}")
def read_tooltip_data(year: int):
    # Serve tooltip data for a specific year
    tooltip_data = create_tooltip_data(year)
    return {"tooltip_data": tooltip_data}

def main():

    uvicorn.run(app, host="127.0.0.1", port=5000)

if __name__ == "__main__":

    main()

