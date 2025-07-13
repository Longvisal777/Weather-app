# Global Weather App

A comprehensive desktop weather application built with Python and Tkinter. This application allows users to search for real-time weather information for cities worldwide, featuring an intuitive interface with country and city selection dropdowns, and detailed weather displays with visual icons.

## Features

- **Global Coverage**: Access weather data for cities worldwide with comprehensive country and city databases.
- **Smart Search System**: 
  - Dynamic country selection with real-time filtering
  - City autocomplete based on selected country
  - Intuitive dropdown menus with keyboard navigation
- **Real-Time Weather Data**: Current weather conditions including temperature, humidity, wind speed, and atmospheric pressure.
- **Visual Weather Display**: 
  - Weather condition icons (sunny, cloudy, rainy, snowy, etc.)
  - Clean and modern user interface with blue gradient theme
  - Detailed weather metrics with intuitive symbols
- **Responsive Design**: User-friendly interface that adapts to different screen sizes.
- **Error Handling**: Comprehensive error handling for network issues and invalid city searches.
- **Background Processing**: Non-blocking API calls to maintain smooth user experience.

## How to Run the Source Code

This section is for users who want to run the application directly from its Python source code.

### Prerequisites

Make sure you have Python installed on your system (Python 3.x is recommended). The following libraries are required:
- `tkinter` (usually comes pre-installed with Python)
- `requests` for API calls
- `Pillow` (PIL) for image handling
- `threading` (built-in Python module)

### Installation

1. **Clone or download** the project files to your local machine.

2. **Navigate** to the project directory in your terminal or command prompt:
   ```bash
   cd your_project_directory
   ```

3. **Install the required Python libraries** using pip:
   ```bash
   pip install requests pillow
   ```
   ```bash
   pip install requests 
   ```

### Usage

1. **The application will start** with a fresh interface. The weather data will be displayed in an organized format with:
   - Current temperature and "feels like" temperature
   - Weather description and visual icon
   - Humidity, wind speed, and atmospheric pressure
   - City name, country, and current date

## How to Use the Application

1. **Select a Country**: 
   - Click on the country search field
   - Type to filter countries or scroll through the dropdown
   - Select your desired country from the list

2. **Select a City**: 
   - Once a country is selected, the city field becomes active
   - Type to search for cities or browse the dropdown
   - Select your desired city from the filtered results

3. **Get Weather Data**: 
   - Click the "Get Weather" button or press Enter in the city field
   - The application will fetch and display current weather information
   - Weather data includes temperature, conditions, humidity, wind, and pressure

4. **View Weather Information**: 
   - Current temperature with "feels like" temperature
   - Weather description with appropriate icon
   - Additional details like humidity, wind speed, and atmospheric pressure
   - Location and date information

## API Configuration

The application uses the OpenWeatherMap API. If you're running from source code, you may need to:
- Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api)
- Replace the API key in the source code if needed

## Troubleshooting

- **Network Issues**: Ensure you have an active internet connection
- **City Not Found**: Try selecting a different city or check the spelling
- **Application Won't Start**: Make sure all dependencies are installed (for source code) or run the .exe file directly
- **Slow Loading**: API responses may take a few seconds depending on your internet connection

## Technical Details

- **GUI Framework**: Tkinter
- **Weather API**: OpenWeatherMap API
- **Country/City Data**: Countries Now API
- **Programming Language**: Python 3.x
- **Threading**: Background API calls for responsive UI

