# Determining observability of a satellite

## Overview
This Python script processes celestial data from a CSV file, transforming coordinates from the Geocentric Celestial Reference System (GCRS) to a local Altitude-Azimuth (AltAz) reference frame.
Then, depending on the specifications of the observation point, it determines if the satellite is visible or not. It finally saves the results in a new CSV file and, if requested, displays a plot of the Altitude of the satellite over time, with color changing if the latter is visible or not.

## Features

- **Coordinate Transformation** : Converts Right Ascension (RA) and Declination (Dec) from the GCRS frame to the local AltAz frame.
- **Visibility Check**: Filters data based on altitude limits to determine visibility.
- **Timezone Adjustment**: Adjusts the observation time to the local timezone of the observation point.
- **Optional Plotting**: Generates a plot showing the altitude of the object over time, with color-coding for visibility.

## Requirements

- Python 3
- Astropy
- Pandas
- Matplotlib

You can find online the instructions to install Python on your machine. Then, you can install the required packages from a terminal window with:

```
pip install pandas matplotlib astropy
```

## How to use

From a terminal window:

```
python observable.py [csv_file_path] [--lat LATITUDE] [--long LONGITUDE] [--alt_min MIN_ALTITUDE] [--alt_max MAX_ALTITUDE] [--timezone TIMEZONE] [--plot]
```

### Arguments

- csv_file_path (str): Path to the CSV file containing celestial data (required).
- --lat (float): Latitude of the observation point in decimal degrees. If not provided, the default is 51.4769 (Greenwich, UK).
- --long (float): Longitude of the observation point in decimal degrees. If not provided, the default is is 0.0 (Greenwich, UK).
- --alt_min (float): Minimum altitude visibility from the observation point, in degrees. Default is 0°.
- --alt_max (float): Maximum altitude visibility from the observation point, in degrees. Default is 90°.
- --timezone (str): Timezone offset from UTC in the format '+X' or '-X'. Default is '0' (UTC).
- --plot: If specified, the script will generate a plot showing the altitude of the object over time, with visible points in green and non-visible points in red.

# Additional material: Celestial coordinates 3D plot

The script `CelestialCoords` displays a 3D plot of the Earth with its rotation axis. It also shows the Ecliptic, Celestial Equator, some notable points and the definition of the GCRS axes.