from mcp.server import MCPServer
import requests


mcp= MCPServer("Weather")

@mcp.tool()
def getweatherdata(city: str):
    url="https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric"
    }
    
    response = requests.get(url, params)
    
    if response.status_code !=200:
        return f"Unable to fetch data from weather api"
    
    return response.json()

if __name__ == "__main__":
    mcp.run()
