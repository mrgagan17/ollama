import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib3

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BangaloreMetroAPI:
    def __init__(self):
        self.base_url = "https://english.bmrc.co.in"
        self.session = requests.Session()
        self.cache = {}
        self.cache_time = {}
        self.headers = {
            'User-Agent': 'BangaloreMetroBot/1.0'
        }
        self.valid_lines = ['purple', 'green']

    def _fetch_page(self, url, cache_key):
        """Internal method to fetch and cache pages"""
        # Check cache (valid for 1 hour)
        if cache_key in self.cache and (datetime.now() - self.cache_time.get(cache_key, datetime.min)).seconds < 3600:
            return self.cache[cache_key]
            
        try:
            response = self.session.get(url, headers=self.headers, verify=False, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            self.cache[cache_key] = soup
            self.cache_time[cache_key] = datetime.now()
            return soup
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def get_metro_lines(self):
        """Get all metro lines with basic info"""
        return [
            {"name": "Purple Line", "stations_count": 37},
            {"name": "Green Line", "stations_count": 24}
        ]

    def get_stations(self, line=None):
        """Get stations for a specific line"""
        if line and line.lower() not in self.valid_lines:
            return None
            
        # Try to fetch from the home page first
        soup = self._fetch_page(self.base_url, "home")
        if not soup:
            return None
            
        stations_data = {}
        
        # Try to find stations in the home page content
        sections = soup.find_all('div', class_='elementor-widget-container')
        for section in sections:
            h2 = section.find('h2')
            if h2 and ('Purple Line' in h2.text or 'Green Line' in h2.text):
                line_name = h2.text.strip()
                stations = []
                ul = section.find('ul')
                if ul:
                    stations = [li.text.strip() for li in ul.find_all('li')]
                stations_data[line_name] = stations
        
        if line:
            line_name = "Purple Line" if line.lower() == "purple" else "Green Line"
            return {line_name: stations_data.get(line_name, [])}
        
        return stations_data

    def get_timetable(self, line=None):
        """Get timetable for a specific line"""
        if line and line.lower() not in self.valid_lines:
            return None
            
        soup = self._fetch_page(f"{self.base_url}/metro-timings/", "timetable")
        if not soup:
            return None
            
        timetable = {}
        sections = soup.find_all('div', class_='elementor-widget-container')
        
        for section in sections:
            h3 = section.find('h3')
            if h3 and ('Line' in h3.text or 'Route' in h3.text):
                line_name = h3.text.strip()
                times = {}
                
                for p in section.find_all('p'):
                    text = p.text.strip()
                    if 'First Train' in text:
                        times['first_train'] = text.replace('First Train:', '').strip()
                    elif 'Last Train' in text:
                        times['last_train'] = text.replace('Last Train:', '').strip()
                
                if times:
                    timetable[line_name] = times
        
        if line:
            line_name = "Purple Line" if line.lower() == "purple" else "Green Line"
            return {line_name: timetable.get(line_name, {})}
        return timetable

    def get_fares(self):
        """Get fare information from the fares page"""
        soup = self._fetch_page(f"{self.base_url}/fares/", "fares")
        if not soup:
            return None
            
        fares = []
        table = soup.find('table')
        
        if table:
            rows = table.find_all('tr')[1:]  # Skip header
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    fares.append({
                        'from': cols[0].text.strip(),
                        'to': cols[1].text.strip(),
                        'fare': cols[2].text.strip()
                    })
        
        return fares

    def get_notifications(self):
        """Get latest notifications from the home page"""
        soup = self._fetch_page(self.base_url, "notifications")
        if not soup:
            return None
            
        notifications = []
        items = soup.select('.elementor-post__title a')
        
        for item in items[:5]:  # Get latest 5 notifications
            notifications.append({
                'title': item.text.strip(),
                'url': item['href']
            })
        
        return notifications

# Example usage
if __name__ == "__main__":
    api = BangaloreMetroAPI()
    
    print("Available Metro Lines:")
    for line in api.get_metro_lines():
        print(f"- {line['name']} ({line['stations_count']} stations)")
    
    print("\nPurple Line Stations:")
    purple_stations = api.get_stations("purple")
    if purple_stations:
        for station in purple_stations.get("Purple Line", []):
            print(f"- {station}")
    else:
        print("Could not fetch Purple Line stations")
    
    print("\nGreen Line Timetable:")
    green_timetable = api.get_timetable("green")
    if green_timetable:
        timetable = green_timetable.get("Green Line", {})
        print(f"First Train: {timetable.get('first_train', 'N/A')}")
        print(f"Last Train: {timetable.get('last_train', 'N/A')}")
    else:
        print("Could not fetch Green Line timetable")
    
    print("\nSample Fares:")
    fares = api.get_fares()
    if fares:
        for fare in fares[:3]:  # Show first 3 fares
            print(f"{fare['from']} to {fare['to']}: ₹{fare['fare']}")
    else:
        print("Could not fetch fare information")
    
    print("\nLatest Notifications:")
    notifications = api.get_notifications()
    if notifications:
        for notice in notifications:
            print(f"- {notice['title']}")
            print(f"  More info: {notice['url']}")
    else:
        print("Could not fetch notifications")