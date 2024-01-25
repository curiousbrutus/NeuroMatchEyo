# klima/app.py
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from klima import fetch_and_process_data, create_interactive_chart, create_tooltip_data
#from klima import get_temperature_data, plot_temperature

app = FastAPI()

# Set up Jinja2Templates for rendering HTML templates
templates = Jinja2Templates(directory="templates")

temperature_data = fetch_and_process_data()


# Create the interactive chart
chart = create_interactive_chart(temperature_data)

@app.get("/")
def read_root(request):
    
    return templates.TemplateResponse("klima.html", {"request": request})


@app.get("/plot_antartica.json")
def read_root():
    
    chart = create_interactive_chart()

    return chart.to_json()

@app.get("/tooltip_data/{year}")
def read_tooltip_data(year: int):
    # Serve tooltip data for a specific year
    tooltip_data = create_tooltip_data(temperature_data, year)
    return {"tooltip_data": tooltip_data}

def main():

    uvicorn.run(app, host="127.0.0.1", port=5000)

if __name__ == "__main__":

    main()

