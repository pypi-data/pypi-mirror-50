#!/usr/bin/env python3
"""
allskymaps python package.

Draws Allsky Nightsky Images with stars from the GAIA catalog

    This work has made use of data from the European Space Agency (ESA)
    mission {\\it Gaia} (\\url{https://www.cosmos.esa.int/gaia}), processed by
    the {\\it Gaia} Data Processing and Analysis Consortium (DPAC,
    \\url{https://www.cosmos.esa.int/web/gaia/dpac/consortium}). Funding
    for the DPAC has been provided by national institutions, in particular
    the institutions participating in the {\\it Gaia} Multilateral Agreement.

and draws moonlight corresponding to the Model from Krisciunas et al.

   author = {{Krisciunas}, K. and {Schaefer}, B.~E.},
    title = "{A model of the brightness of moonlight}",
  journal = {\pasp},
     year = 1991,
    month = sep,
   volume = 103,
    pages = {1033-1039},
      doi = {10.1086/132921},
   adsurl = {http://adsabs.harvard.edu/abs/1991PASP..103.1033K},


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

Created and maintained by Matthias Buechele [FAU].

"""


import sys
import inspect
import ephem
import os.path
import math
import matplotlib.pyplot as plt
import astropy.io.fits as pyfits

from .help import PlatformHelp
from .input_options import ReadOptions
from .model import nsbModel
from .config import TheConfiguration
from .nsbtools import makeDateString, plotMaps, plotTimespan, plotObsTime
from .mypycat import mypycat
from .gaia import Gaia


def main():
    home = os.path.join(os.path.expanduser("~"), ".nsb/")
    if not os.path.exists(home):
        os.makedirs(home)

    Help = PlatformHelp()
    Options = ReadOptions(sys.argv)
    try:
        assert(Options.show_help == False)
    except:
        #print(inspect.stack()[0][2:4][::-1])
        # Show help and halt
        Help.show_help()
        raise SystemExit

    Help.show_title()
    conf = TheConfiguration()
    if Options.altconfset:
        conf.readConfig(Options.conf)
    else:
        conf.readStandardConfig()

    # Lets have a look what we gonna do today... 

    # try to get all the values from user input (Options)
    # if it fails, because there was no input -> use the values from Configfile.

    try:
        size = Options.imageSize
        print('* user input: Imagesize of %i pixels' % size)
    except Exception as e:
        size = int(conf.config['image_size'])
        print('* Imagesize of %i pixels from config file' % size)
    try:
        if Options.source_set:
            mpc = mypycat()
            source = mpc.get(Options.tracked_source_name)
            alt, az = 0, 0 # has to be calculated later
            print('* user input: pointing on %s' % source.name)
        else:
            alt = math.radians(Options.alt)
            az = math.radians(Options.az)
            source = None
            print('* user input: Alt/Az of %.1f|%.1f' % (math.degrees(alt), math.degrees(az)))
    except Exception as e:
        alt = math.radians(float(conf.config['alt']))
        az = math.radians(float(conf.config['az']))
        source = None
        print('* Alt/Az of %.1f|%.1f from config file' % (alt, az))
    try:
        level = Options.healpixlevel
        print('* user input: HealPixLevel of %i' % level)
    except Exception as e:
        level = int(conf.config['healpixlevel'])
        print('* HealPixLevel of %i from config file' % level)
    try:
        lat, lon = float(Options.lat), float(Options.lon)
        print('* user input location: Lat %s Lon %s' % (lat, lon))
    except Exception as e:
        lat, lon = float(conf.config['Lat']), float(conf.config['Lon'])
        print('* location from config file: Lat %s Lon %s' % (lat, lon))
    try:
        elevation = float(Options.elevation)
        print('* user input elevation: %.1f m ' % elevation)
    except Exception as e:
        elevation = float(conf.config['elevation'])
        print('* elevation from config file: %.1f m' % elevation)
    """
    try:
        B_zero = Options.B_zero
        print('* user input B_zero = %.3f' % B_zero)
    except Exception as e:
        B_zero = float(conf.config['B'])
        print('* B_zero = %.3f from config file ' % B_zero
    try:
        k = Options.extinction
        print('* user input k=%.3f' % k)
    except Exception as e:
        k = float(conf.config['k'])
        print('* Extinction from config file k=%.3f' % k)
    """
    try:
        gauss = Options.gauss
        if gauss > 0:
            print('* user input gaussian smoothing with %.1f' % gauss)
        else:
            print('* no smoothing')
    except Exception as e:
        gauss = float(conf.config['gauss'])
        if gauss > 0:
            print('* Gaussian smoothing with %.1f from config' % gauss)
        else:
            print('* no smoothing')
    try:
        use_mhz = Options.use_mhz
        if use_mhz:
            print('* user input units MHz (BE CAREFULL: THIS IS THE EXPERIMENTAL MODEL')
        else:
            print('* user input units nLb (the old model)')
    except Exception as e:
        um = conf.config['use_mhz']
        if um in ('True', 'true', '1', 'yes', 'Yes', 't', 'T'):
            use_mhz = True
        else:
            use_mhz = False
        print('* units specified in config file: use_mhz = %s' % use_mhz)
    try:
        output_dir = Options.output_dir
        print('* user specified output to: %s' % output_dir)
    except Exception as e:
        output_dir = ""
    try:
        date_and_time = ephem.Date(Options.time)
        print('* user input Date of %s' % date_and_time)
    except Exception as e:
        date_and_time = ephem.Date(conf.config['time'])
        print('* Date from config file %s' % date_and_time)

    try:
        date_and_time2 = ephem.Date(Options.time2)
        print('* user input End Date of %s' % date_and_time2)
    except Exception as e:
        date_and_time2 = date_and_time + 0.5
        if Options.obs_time or Options.trend:
            print('* NO END TIME set. Going to use start + 12 hours')

    """
    Let the Drawing begin!
    """
    gaiamap = Gaia(level=level)
    model = nsbModel(conf, gaiamap, date_and_time, date_and_time2, use_mhz=True, threshold=None,timeresolution=1, verbose=False)

    if date_and_time2 < date_and_time:
        raise SystemExit(" time_end has to be after time_start! - No Plot possible.")
    else:
        if Options.obs_time:
            model.setSource(source=source)
            if date_and_time + 360 > date_and_time2:
                input("\nDoing the max NSB Observation time gain plot makes more sense with a timespan\nof more than one year...\n[Enter] to continue anyway, ctrl+C to abort\n")
            model.threshold = Options.limit
            model.calculateTimespan()
            plotObsTime(model)
        if Options.trend:
            model.setSource(source=source)
            model.timeresolution = 15
            model.calculateTimespan()
            plotTimespan(model)

    if Options.skymap:
        print("* Moon at \talt %.2f\taz %.2f\twith a phase of %.2f %% (%.2f deg)" % (
              math.degrees(model.moon.alt), math.degrees(model.moon.az), 100 * model.moon.moon_phase,
              math.degrees(model.moon_alpha)))

        model.drawAllSky(size=size)
        if source is None:
            model.drawFOV_altaz(alt=alt, az=az, fov=5.0, size=42)
        else:
            model.drawFOV_source(source=source, fov=5.0, size=42)
        if gauss > 0:
            model.smooth_gauss(sigma=gauss)
        #model.median_filter(size=10)

    
        title = 'Allskymaps for %s\n(Lon %.4f | Lat %.4f)' % (model.observer_source.date, math.degrees(model.observer_source.lon), math.degrees(model.observer_source.lat))
        
        plotMaps(model.allskymap.data, title)
        plotMaps(model.fovmap.data, "FOV")

        median_allsky, mean_allsky, median_fov, mean_fov = model.getStatistics()
        print('Median All-Sky nsbModel: \t %.2f %s\n'
              'Mean All-Sky nsbModel: \t %.2f %s' % (median_allsky, model.units, mean_allsky, model.units))
        print('Median FOV-Sky nsbModel: \t %.2f %s\n'
              'Mean FOV-Sky nsbModel: \t %.2f %s' % (median_fov, model.units, mean_fov, model.units))


        if Options.savefits:
            hdul = pyfits.HDUList([model.allskymap, model.fovmap])
            fname = output_dir + "NSB_Model_of_"+ makeDateString(date_and_time) + ".fits"
            hdul.writeto(fname, 'exception', True)
            print("Saved output to\n%s" % fname)

    plt.show()
    print("done.\n")



if __name__ == '__main__':
    main()
