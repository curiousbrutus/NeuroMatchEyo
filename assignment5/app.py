"""
strompris fastapi app entrypoint
"""
import datetime
import os
from typing import List, Optional
import altair as alt
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pathlib import Path
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
docs_templates = Jinja2Templates(directory="docs/_build/html")

app.mount("/_static", StaticFiles(directory=Path(__file__).parent.absolute()/"docs/_build/html/_static"), name="_static")


# `GET /` should render the `strompris.html` template
# with inputs:
# - request
# - location_codes: location code dict
# - today: current date

@app.get("/")
def read_root(
    request: Request,
    location_codes: dict = LOCATION_CODES,
    today: datetime.date = datetime.date.today(),
):
    return templates.TemplateResponse("strompris.html", {
        "request": request,
        "location_codes": location_codes,
        "today": today,
    })

# GET /plot_prices.json should take inputs:
# - locations (list from Query)
# - end (date)
# - days (int, default=7)
# all inputs should be optional
# return should be a vega-lite JSON chart (alt.Chart.to_dict())
# produced by `plot_prices`
# (task 5.6: return chart stacked with plot_daily_prices)

"""
# alternative solution
@app.get("/plot_prices.json")
async def read_plot_prices():
    try:
        df = fetch_prices()  # You might need to pass the required parameters
        chart = plot_prices(df)
        chart_dict = chart.to_dict()

        return JSONResponse(content=chart_dict)
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An error occurred: {e}")
        # Return an error response
        return JSONResponse(content={"error": f"Internal Server Error: {e}"}, status_code=500)


"""

@app.get("/plot_prices.json")
def read_plot_prices(
    locations: Optional[List[str]] = Query(None),
    end: Optional[datetime.date] = None,
    days: int = 7,
):
    df = fetch_prices(end_date=end, days=days, locations=locations)
    chart = plot_prices(df)
    return chart.to_dict()
    

# Task 5.6 (bonus):
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date

@app.get("/activity")
def read_activity(
    request: Request,
    location_codes: dict = LOCATION_CODES,
    activities: dict = ACTIVITIES,
    today: datetime.date = datetime.date.today(),
):
    return templates.TemplateResponse("activity.html", {
        "request": request,
        "location_codes": location_codes,
        "activities": activities,
        "today": today,
    })
...

# Task 5.6:
# `GET /plot_activity.json` should return vega-lite chart JSON (alt.Chart.to_dict())
# from `plot_activity_prices`
# with inputs:
# - location (single, default=NO1)
# - activity (str, default=shower)
# - minutes (int, default=10)
@app.get("/plot_activity.json")
def read_plot_activity(
    location: str = "NO1",
    activity: str = "shower",
    minutes: int = 10,
):
    df = fetch_day_prices(location=location)
    chart = plot_activity_prices(df, activity=activity, minutes=minutes)
    return chart.to_dict()


# mount your docs directory as static files at `/help`
@app.get("/help", include_in_schema=False)

def read_help(request: Request):
    return docs_templates.TemplateResponse("strompris.html", {"request": request})


def main():
    """Launches the application on port 5000 with uvicorn"""
    # use uvicorn to launch your application on port 5000
    ...


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)#debug=True)

    #main()
