import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import io
import threading

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1e3a8a')
        
        # API key
        self.api_key = "feb100953bc685f15c7d4666656e21d3"
        
        # Data storage
        self.countries = []
        self.cities = []
        self.selected_country = None
        
        # Weather icons mapping
        self.weather_icons = {
            "01d": "🌞", "01n": "🌙", "02d": "⛅", "02n": "☁️",
            "03d": "☁️", "03n": "☁️", "04d": "☁️", "04n": "☁️",
            "09d": "🌧️", "09n": "🌧️", "10d": "🌦️", "10n": "🌧️",
            "11d": "⛈️", "11n": "⛈️", "13d": "❄️", "13n": "❄️",
            "50d": "🌫️", "50n": "🌫️"
        }
        
        self.setup_ui()
        self.load_countries()
        
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1e3a8a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Global Weather App", 
                              font=('Arial', 24, 'bold'), 
                              bg='#1e3a8a', fg='white')
        title_label.pack(pady=(0, 30))
        
        # Search container - using grid for better alignment
        search_container = tk.Frame(main_frame, bg='#1e3a8a')
        search_container.pack(pady=(0, 20))
        
        # Country search section
        country_section = tk.Frame(search_container, bg='#1e3a8a')
        country_section.grid(row=0, column=0, padx=(0, 20), sticky='n')
        
        country_label = tk.Label(country_section, text="Select Country", 
                                font=('Arial', 12, 'bold'), 
                                bg='#1e3a8a', fg='white')
        country_label.pack(anchor='w', pady=(0, 5))
        
        # Country search frame
        self.country_search_frame = tk.Frame(country_section, bg='#1e3a8a')
        self.country_search_frame.pack()
        
        self.country_var = tk.StringVar()
        self.country_entry = tk.Entry(self.country_search_frame, textvariable=self.country_var,
                                     font=('Arial', 14), width=25, relief=tk.FLAT, 
                                     bd=0, highlightthickness=2, highlightcolor='#3b82f6')
        self.country_entry.pack(ipady=8)
        self.country_entry.bind('<KeyRelease>', self.on_country_key_release)
        self.country_entry.bind('<FocusIn>', self.on_country_focus_in)
        self.country_entry.bind('<Button-1>', self.on_country_click)
        
        # City search section
        city_section = tk.Frame(search_container, bg='#1e3a8a')
        city_section.grid(row=0, column=1, padx=(0, 20), sticky='n')
        
        city_label = tk.Label(city_section, text="Select City", 
                             font=('Arial', 12, 'bold'), 
                             bg='#1e3a8a', fg='white')
        city_label.pack(anchor='w', pady=(0, 5))
        
        # City search frame
        self.city_search_frame = tk.Frame(city_section, bg='#1e3a8a')
        self.city_search_frame.pack()
        
        self.city_var = tk.StringVar()
        self.city_entry = tk.Entry(self.city_search_frame, textvariable=self.city_var,
                                  font=('Arial', 14), width=25, relief=tk.FLAT,
                                  bd=0, highlightthickness=2, highlightcolor='#3b82f6',
                                  state='disabled')
        self.city_entry.pack(ipady=8)
        self.city_entry.bind('<KeyRelease>', self.on_city_key_release)
        self.city_entry.bind('<FocusIn>', self.on_city_focus_in)
        self.city_entry.bind('<Button-1>', self.on_city_click)
        self.city_entry.bind('<Return>', self.search_weather)
        
        # Search button
        button_section = tk.Frame(search_container, bg='#1e3a8a')
        button_section.grid(row=0, column=2, sticky='n')
        
        # Add invisible label to align with other sections
        invisible_label = tk.Label(button_section, text="", 
                                  font=('Arial', 12, 'bold'), 
                                  bg='#1e3a8a', fg='#1e3a8a')
        invisible_label.pack(anchor='w', pady=(0, 0))
        
        search_btn = tk.Button(button_section, text="Get Weather", 
                              command=self.search_weather,
                              font=('Arial', 14, 'bold'), bg='#3b82f6', fg='white',
                              relief=tk.FLAT, padx=30, cursor='hand2',
                              activebackground='#2563eb')
        search_btn.pack(ipady=8)
        
        # Create dropdown 
        self.create_dropdown_windows()
        
        # Weather display frame
        self.weather_frame = tk.Frame(main_frame, bg='#1e3a8a')
        self.weather_frame.pack(fill=tk.BOTH, expand=True, pady=30)
        
        # Current weather frame
        self.current_frame = tk.Frame(self.weather_frame, bg='#3b82f6', relief=tk.RAISED, bd=2)
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Loading countries...",
                                    font=('Arial', 11), bg='#1e3a8a', fg='#94a3b8')
        self.status_label.pack(pady=(15, 0))
        
        # Hide dropdowns initially
        self.country_dropdown_visible = False
        self.city_dropdown_visible = False
        
        # Bind root click to hide dropdowns
        self.root.bind('<Button-1>', self.on_root_click)
        
    def create_dropdown_windows(self):
        """Create dropdown windows as overlays"""
        # Country dropdown
        self.country_dropdown_window = tk.Toplevel(self.root)
        self.country_dropdown_window.withdraw()  # Hide initially
        self.country_dropdown_window.wm_overrideredirect(True)
        self.country_dropdown_window.configure(bg='white')
        
        self.country_dropdown = tk.Listbox(self.country_dropdown_window, 
                                          font=('Arial', 11), height=6, width=25,
                                          relief=tk.FLAT, bd=1, highlightthickness=1,
                                          bg='white', fg='black', selectbackground='#e5e7eb',
                                          highlightcolor='#3b82f6')
        self.country_dropdown.pack(fill=tk.BOTH, expand=True)
        self.country_dropdown.bind('<Button-1>', self.on_country_select)
        self.country_dropdown.bind('<Double-Button-1>', self.on_country_select)
        
        # City dropdown
        self.city_dropdown_window = tk.Toplevel(self.root)
        self.city_dropdown_window.withdraw()  # Hide initially
        self.city_dropdown_window.wm_overrideredirect(True)
        self.city_dropdown_window.configure(bg='white')
        
        self.city_dropdown = tk.Listbox(self.city_dropdown_window, 
                                       font=('Arial', 11), height=6, width=25,
                                       relief=tk.FLAT, bd=1, highlightthickness=1,
                                       bg='white', fg='black', selectbackground='#e5e7eb',
                                       highlightcolor='#3b82f6')
        self.city_dropdown.pack(fill=tk.BOTH, expand=True)
        self.city_dropdown.bind('<Button-1>', self.on_city_select)
        self.city_dropdown.bind('<Double-Button-1>', self.on_city_select)
        
    def position_dropdown_window(self, dropdown_window, entry_widget):
        """Position dropdown window below the entry widget"""
        entry_widget.update_idletasks()
        x = entry_widget.winfo_rootx()
        y = entry_widget.winfo_rooty() + entry_widget.winfo_height() + 2
        dropdown_window.geometry(f"+{x}+{y}")
        
    def on_root_click(self, event):
        """Hide dropdowns when clicking outside of them"""
        # Get the widget that was clicked
        clicked_widget = event.widget
        
        # Check if click is outside country dropdown area
        if (self.country_dropdown_visible and 
            clicked_widget not in [self.country_entry, self.country_dropdown]):
            self.hide_country_dropdown()
        
        # Check if click is outside city dropdown area
        if (self.city_dropdown_visible and 
            clicked_widget not in [self.city_entry, self.city_dropdown]):
            self.hide_city_dropdown()
    
    def on_country_click(self, event):
        """Show country dropdown when entry is clicked"""
        if self.countries:
            self.on_country_key_release(None)
        
    def on_city_click(self, event):
        """Show city dropdown when entry is clicked"""
        if self.cities:
            self.on_city_key_release(None)
        
    def load_countries(self):
        """Load countries from API in background thread"""
        threading.Thread(target=self.fetch_countries, daemon=True).start()
    
    def fetch_countries(self):
        """Fetch countries from API"""
        try:
            response = requests.get("https://countriesnow.space/api/v0.1/countries/positions", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.countries = sorted([country['name'] for country in data['data']])
                self.root.after(0, self.on_countries_loaded)
            else:
                self.root.after(0, self.on_countries_error, "Failed to load countries")
        except requests.RequestException as e:
            self.root.after(0, self.on_countries_error, f"Network error: {str(e)}")
        except Exception as e:
            self.root.after(0, self.on_countries_error, f"Error loading countries: {str(e)}")
    
    def on_countries_loaded(self):
        """Called when countries are successfully loaded"""
        self.status_label.config(text="Select a country and city to get weather information")
    
    def on_countries_error(self, error_msg):
        """Called when there's an error loading countries"""
        self.status_label.config(text=f"Error: {error_msg}")
        messagebox.showerror("Error", f"Failed to load countries: {error_msg}")
    
    def on_country_key_release(self, event):
        """Handle country search input"""
        query = self.country_var.get().lower()
        if len(query) >= 1:
            suggestions = [country for country in self.countries if query in country.lower()][:8]
            if suggestions:
                self.update_country_dropdown(suggestions)
            else:
                self.hide_country_dropdown()
        else:
            # Show all countries if query is empty
            self.update_country_dropdown(self.countries[:8])
    
    def on_country_focus_in(self, event):
        """Show country dropdown when entry gets focus"""
        if self.countries:
            self.on_country_key_release(None)
    
    def update_country_dropdown(self, suggestions):
        """Update country dropdown with suggestions"""
        self.country_dropdown.delete(0, tk.END)
        for suggestion in suggestions:
            self.country_dropdown.insert(tk.END, suggestion)
        
        if suggestions and not self.country_dropdown_visible:
            self.position_dropdown_window(self.country_dropdown_window, self.country_entry)
            self.country_dropdown_window.deiconify()
            self.country_dropdown_visible = True
    
    def hide_country_dropdown(self):
        """Hide country dropdown"""
        if self.country_dropdown_visible:
            self.country_dropdown_window.withdraw()
            self.country_dropdown_visible = False
    
    def on_country_select(self, event):
        """Handle country selection"""
        # Use after_idle to ensure the selection is processed
        self.root.after_idle(self._process_country_selection)
    
    def _process_country_selection(self):
        """Process country selection after idle"""
        selection = self.country_dropdown.curselection()
        if selection:
            selected_country = self.country_dropdown.get(selection[0])
            self.country_var.set(selected_country)
            self.selected_country = selected_country
            self.hide_country_dropdown()
            
            # Enable city search and load cities
            self.city_entry.config(state='normal')
            self.city_var.set("")
            self.status_label.config(text=f"Loading cities for {selected_country}...")
            threading.Thread(target=self.fetch_cities, args=(selected_country,), daemon=True).start()
    
    def fetch_cities(self, country):
        """Fetch cities for a specific country"""
        try:
            response = requests.post("https://countriesnow.space/api/v0.1/countries/cities", 
                                   json={"country": country}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                cities = sorted(data.get('data', []))
                self.root.after(0, self.on_cities_loaded, cities)
            else:
                self.root.after(0, self.on_cities_error, "Failed to load cities")
        except requests.RequestException as e:
            self.root.after(0, self.on_cities_error, f"Network error: {str(e)}")
        except Exception as e:
            self.root.after(0, self.on_cities_error, f"Error loading cities: {str(e)}")
    
    def on_cities_loaded(self, cities):
        """Called when cities are successfully loaded"""
        self.cities = cities
        self.status_label.config(text=f"Loaded {len(cities)} cities. Select a city to get weather.")
    
    def on_cities_error(self, error_msg):
        """Called when there's an error loading cities"""
        self.status_label.config(text=f"Error: {error_msg}")
        messagebox.showerror("Error", f"Failed to load cities: {error_msg}")
    
    def on_city_key_release(self, event):
        """Handle city search input"""
        query = self.city_var.get().lower()
        if len(query) >= 1 and self.cities:
            suggestions = [city for city in self.cities if query in city.lower()][:8]
            if suggestions:
                self.update_city_dropdown(suggestions)
            else:
                self.hide_city_dropdown()
        else:
            # Show all cities if query is empty
            if self.cities:
                self.update_city_dropdown(self.cities[:8])
    
    def on_city_focus_in(self, event):
        """Show city dropdown when entry gets focus"""
        if self.cities:
            self.on_city_key_release(None)
    
    def update_city_dropdown(self, suggestions):
        """Update city dropdown with suggestions"""
        self.city_dropdown.delete(0, tk.END)
        for suggestion in suggestions:
            self.city_dropdown.insert(tk.END, suggestion)
        
        if suggestions and not self.city_dropdown_visible:
            self.position_dropdown_window(self.city_dropdown_window, self.city_entry)
            self.city_dropdown_window.deiconify()
            self.city_dropdown_visible = True
    
    def hide_city_dropdown(self):
        """Hide city dropdown"""
        if self.city_dropdown_visible:
            self.city_dropdown_window.withdraw()
            self.city_dropdown_visible = False
    
    def on_city_select(self, event):
        """Handle city selection"""
        # Use after_idle to ensure the selection is processed
        self.root.after_idle(self._process_city_selection)
    
    def _process_city_selection(self):
        """Process city selection after idle"""
        selection = self.city_dropdown.curselection()
        if selection:
            selected_city = self.city_dropdown.get(selection[0])
            self.city_var.set(selected_city)
            self.hide_city_dropdown()
            # Automatically search for weather
            self.search_weather()
    
    def search_weather(self, event=None):
        """Search for weather data"""
        country = self.country_var.get().strip()
        city = self.city_var.get().strip()
        
        if not country:
            messagebox.showwarning("Warning", "Please select a country first!")
            return
        
        if not city:
            messagebox.showwarning("Warning", "Please select a city!")
            return
        
        self.status_label.config(text="Fetching weather data...")
        self.hide_city_dropdown()
        
        # Run API call in separate thread
        threading.Thread(target=self.fetch_weather, args=(city,), daemon=True).start()
    
    def fetch_weather(self, city):
        """Fetch weather data from API"""
        try:
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            current_response = requests.get(current_url, timeout=10)
            current_data = current_response.json()
            
            if current_response.status_code == 200:
                self.root.after(0, self.display_weather, current_data)
            else:
                error_msg = current_data.get('message', 'City not found')
                self.root.after(0, self.show_error, error_msg)
                
        except requests.RequestException:
            self.root.after(0, self.show_error, "Network error. Please check your internet connection.")
        except Exception as e:
            self.root.after(0, self.show_error, f"An error occurred: {str(e)}")
    
    def display_weather(self, current_data):
        """Display weather data in the UI"""
        # Clear previous weather display
        for widget in self.current_frame.winfo_children():
            widget.destroy()
        
        # Display current weather
        self.display_current_weather(current_data)
        
        # Pack frame
        self.current_frame.pack(fill=tk.X, pady=(0, 20), padx=20)
        
        self.status_label.config(text="Weather data loaded successfully!")
    
    def display_current_weather(self, data):
        """Display current weather information"""
        city_name = data['name']
        country = data['sys']['country']
        temp = round(data['main']['temp'])
        feels_like = round(data['main']['feels_like'])
        humidity = data['main']['humidity']
        description = data['weather'][0]['description'].title()
        icon_code = data['weather'][0]['icon']
        wind_speed = data['wind']['speed']
        pressure = data['main']['pressure']
        
        # Weather icon
        icon = self.weather_icons.get(icon_code, "🌤️")
        
        # City and country header
        header_frame = tk.Frame(self.current_frame, bg='#3b82f6')
        header_frame.pack(fill=tk.X, pady=(15, 10))
        
        city_label = tk.Label(header_frame, text=f"{city_name}, {country}",
                             font=('Arial', 22, 'bold'), bg='#3b82f6', fg='white')
        city_label.pack()
        
        date_label = tk.Label(header_frame, text=datetime.now().strftime("%A, %B %d, %Y"),
                             font=('Arial', 12), bg='#3b82f6', fg='#cbd5e1')
        date_label.pack(pady=(5, 0))
        
        # Main weather display
        main_weather_frame = tk.Frame(self.current_frame, bg='#3b82f6')
        main_weather_frame.pack(pady=20)
        
        # Weather icon
        icon_label = tk.Label(main_weather_frame, text=icon, 
                             font=('Arial', 70), bg='#3b82f6')
        icon_label.pack(side=tk.LEFT, padx=(0, 30))
        
        # Temperature info
        temp_info_frame = tk.Frame(main_weather_frame, bg='#3b82f6')
        temp_info_frame.pack(side=tk.LEFT)
        
        temp_label = tk.Label(temp_info_frame, text=f"{temp}°C",
                             font=('Arial', 52, 'bold'), bg='#3b82f6', fg='white')
        temp_label.pack()
        
        feels_like_label = tk.Label(temp_info_frame, text=f"Feels like {feels_like}°C",
                                   font=('Arial', 14), bg='#3b82f6', fg='#cbd5e1')
        feels_like_label.pack()
        
        desc_label = tk.Label(temp_info_frame, text=description,
                             font=('Arial', 16), bg='#3b82f6', fg='white')
        desc_label.pack(pady=(10, 0))
        
        # Weather details
        details_frame = tk.Frame(self.current_frame, bg='#3b82f6')
        details_frame.pack(pady=(10, 20))
        
        humidity_label = tk.Label(details_frame, text=f"💧 Humidity: {humidity}%",
                                 font=('Arial', 14), bg='#3b82f6', fg='#cbd5e1')
        humidity_label.pack(side=tk.LEFT, padx=(0, 30))
        
        wind_label = tk.Label(details_frame, text=f"🌪️ Wind: {wind_speed} m/s",
                             font=('Arial', 14), bg='#3b82f6', fg='#cbd5e1')
        wind_label.pack(side=tk.LEFT, padx=(0, 30))
        
        pressure_label = tk.Label(details_frame, text=f"📊 Pressure: {pressure} hPa",
                                 font=('Arial', 14), bg='#3b82f6', fg='#cbd5e1')
        pressure_label.pack(side=tk.LEFT)
    
    def show_error(self, message):
        """Show error message"""
        self.status_label.config(text=f"Error: {message}")
        messagebox.showerror("Error", message)

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()