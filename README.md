# Digantara-Assignment
Modules Imported
•	numpy as np: A library for efficient numerical computation.
•	pandas as pd: A library for data manipulation and analysis.
•	joblib: A library for parallel computing.
•	pyproj: A library for geospatial projections.
•	sgp4: A library for satellite orbit propagation.
•	datetime: A module for working with dates and times.
•	os: A module for interacting with the operating system.

**Functions**
read_tle_data(file_path)

•	Reads a file containing TLE (Two-Line Element) data for satellites.
•	Returns a list of dictionaries, where each dictionary represents a satellite with its name, TLE lines, and a satellite object.
calculate_satellite_positions(satellites)
•	Calculates the positions of a list of satellites over a 24-hour period.
•	Returns a list of lists, where each inner list contains the positions of a satellite at 1-minute intervals.

ecef2lla(pos)

•	Converts a position from ECEF (Earth-Centered, Earth-Fixed) coordinates to LLA (Latitude, Longitude, Altitude) coordinates.
•	Returns a tuple containing the latitude, longitude, and altitude.

convert_to_lla(positions)

•	Converts a list of positions from ECEF coordinates to LLA coordinates.
•	Returns a list of tuples, where each tuple contains the time, latitude, longitude, altitude, and velocity components.

filter_region(A, region)

•	Filters a list of positions to only include those within a specified rectangular region.
•	Returns a list of filtered positions.

prompt_for_region()

•	Prompts the user to enter the coordinates of a rectangular region.
•	Returns a tuple containing the minimum and maximum latitude and longitude values.

**Main Script**

•	Reads TLE data from a file.
•	Calculates the positions of the satellites over a 24-hour period and one minute time interval
•	Converts the positions to LLA coordinates.
•	Prompts the user to enter a rectangular region.
•	Filters the positions to only include those within the specified region.
•	Creates a Pandas DataFrame from the filtered data and prints the first few rows.

