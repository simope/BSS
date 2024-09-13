import pandas as pd
import argparse
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, GCRS
from astropy.visualization import astropy_mpl_style

def main():
    parser = argparse.ArgumentParser(description='Process celestial data and transform coordinates.')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file with celestial data.')
    parser.add_argument('--lat', type=float, default=51.4769, help='Latitude in decimal degrees of the observation point in degrees.')
    parser.add_argument('--long', type=float, default=0, help='Longitude in decimal degrees of the observation point in degrees.')
    parser.add_argument('--alt_min', type=float, default=0, help='Minimum altitude visibility in degrees from observation point.')
    parser.add_argument('--alt_max', type=float, default=90, help='Maximum altitude visibility in degrees from observation point.')
    parser.add_argument('--timezone', type=str, default='0', help='Timezone of observation point, defined relative to UTC. Input as \'+X\' or \'-X\'.')
    parser.add_argument('--plot', action='store_true', help='If this option is used, a plot will be displayed.')
    args = parser.parse_args()
    
    # Check validity of timezone
    try:
        utcoffset = int(args.timezone)
    except:
        raise ValueError("Please enter a valid timezone, integer number preceded by minus or plus sign.")

    if utcoffset < -12 or utcoffset > 14:
        raise ValueError("Please enter a valid timezone, between -12 and +14.")

    # Read the CSV file
    cheops_data = pd.read_csv(args.csv_file)

    # Define station location on Earth
    station = EarthLocation(lat=args.lat*u.deg, lon=args.long*u.deg)

    # Preset Altitude and Azimuth columns
    cheops_data['Alt'] = None
    cheops_data['Az'] = None
    cheops_data['Local time'] = None
    cheops_data['visible'] = None

    # Transform from GCRS to the local AltAz frame
    # for each entry of the file
    for index, row in cheops_data.iterrows():
        RA = row['RA (GCRS) [deg]']
        Dec = row['Dec (GCRS) [deg]']
        dist = row['Distance (GCRS) [km]']
        time = Time(row['Time (iso)'], scale='utc')

        cheops_GCRS = GCRS(ra=RA*u.deg, dec=Dec*u.deg, distance=dist*u.km, obstime=time) # Input data
        AltAz_frame = AltAz(location=station, obstime=time) # Reference frame of the station
        cheops_AltAz = cheops_GCRS.transform_to(AltAz_frame) # Transform from GCRS to Station frame of ref

        # Save the obtained coords and local time
        cheops_data.at[index, 'Local time'] = str(time + utcoffset*u.hour)
        cheops_data.at[index, 'Alt'] = cheops_AltAz.alt.degree
        cheops_data.at[index, 'Az'] = cheops_AltAz.az.degree

        # Check if the satellite is visible by comparing Altitudes
        if cheops_AltAz.alt.degree > args.alt_min and cheops_AltAz.alt.degree < args.alt_max:
            cheops_data.at[index, 'visible'] = 'Yes' # Assuming good weather conditions of course
        else:
            cheops_data.at[index, 'visible'] = 'No'

    cheops_data.to_csv('Object_visibility.csv') # Save the csv file with the results

    if args.plot: # Display plots if --plot is True
        visible = cheops_data[cheops_data['visible']=='Yes']
        visible['Local time'] = pd.to_datetime(visible['Local time'])
        not_visible = cheops_data[cheops_data['visible']=='No']
        not_visible['Local time'] = pd.to_datetime(not_visible['Local time'])
        
        plt.style.use(astropy_mpl_style)
        plt.figure()
        plt.scatter(visible['Local time'], visible['Alt'], color='g')
        plt.scatter(not_visible['Local time'], not_visible['Alt'], color='r')
        plt.xticks(rotation='vertical')
        plt.show()

if __name__ == '__main__':
    main()
