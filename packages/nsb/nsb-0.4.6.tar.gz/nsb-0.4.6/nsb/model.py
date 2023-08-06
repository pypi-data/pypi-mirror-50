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

import numpy as np
import astropy.io.fits as pyfits
from astropy import units as u
from astropy.coordinates import SkyCoord
import ephem
import math
from scipy.ndimage import gaussian_filter, median_filter
from tqdm import tqdm
from operator import itemgetter
import matplotlib.pyplot as plt
from . import nsbtools


class nsbModel():
    def __init__(self, conf, gaiamap, time1, time2=None, use_mhz=True, threshold=400, timeresolution=15, verbose=False):
        # create an PyEphem Observer and set the pressure to 0 -> No atmospheric corrections near the horizon
        self.observer_sun = ephem.Observer()
        #self.observer_sun.pressure = 0
        self.observer_sun.horizon = conf.config['sun_below_horizon']
        self.observer_sun.lon, self.observer_sun.lat = conf.config['Lon'], conf.config['Lat']
        self.observer_sun.elevation = float(conf.config['elevation'])

        self.observer_moon = ephem.Observer()
        #self.observer_moon.pressure = 0
        self.observer_moon.horizon = conf.config['moon_above_horizon']
        self.observer_moon.lon, self.observer_moon.lat = conf.config['Lon'], conf.config['Lat']
        self.observer_moon.elevation = float(conf.config['elevation'])

        self.observer_source = ephem.Observer()
        #self.observer_source.pressure = 0
        self.observer_source.horizon = conf.config['source_above_horizon']
        self.observer_source.lon, self.observer_source.lat = conf.config['Lon'], conf.config['Lat']
        self.observer_source.elevation = float(conf.config['elevation'])

        self.moon = ephem.Moon()
        self.sun = ephem.Sun()
        self.source = None  # will be set later if needed

        # all the other stuff
        self.verbose = verbose
        self.offset = ephem.Date('0001/01/01 00:00:00')

        self.time_start = time1
        self.time_end = time2
        self.threshold = threshold
        self.timeresolution = timeresolution
        self.use_mhz = use_mhz
        if self.use_mhz:
            self.units = 'MHz'
        else:
            self.units = 'nLb'
        self.gaiamap = gaiamap

        self.setDate(self.time_start)


    def setSource(self, source, ra_offset=0.0, dec_offset=0.0):
        if source is None:
            raise SystemExit("No source given! Check your arguments!")
        else:
            self.pointing = source.name
            if source.name.lower().strip() == 'moon':
                self.source = self.moon
            else:
                self.source = ephem.FixedBody()
                if type(source.ra) is str:
                    self.source._ra, self.source._dec = source.ra, source.dec
                else:
                    self.source._ra, self.source._dec = ephem.hours(math.radians(source.ra)), ephem.degrees(math.radians(source.dec))

                self.source._ra += np.deg2rad(ra_offset)
                self.source._dec += np.deg2rad(dec_offset)
                self.source.name = source.name
                self.setDate(self.time_start)
                self.recomputeAll()
                coord = SkyCoord(ra=self.source._ra * u.rad, dec=self.source._dec* u.rad, frame='icrs')
                self.source_lon, self.source_lat = coord.galactic.l.value, coord.galactic.b.value
                #print('* %s at \tzen %.2f\taz %.2f' % (self.source.name, math.degrees(np.pi / 2 - self.source.alt), math.degrees(self.source.az)))


    def drawAllSky(self, size=400, fov_averaging=False):
        a = np.empty((size, size))
        a.fill(np.nan)
        self.allskymap = pyfits.PrimaryHDU(a)
        self.allskymap.header['sunalt'] = (math.degrees(self.sun.alt), 'Degrees')
        self.allskymap.header['moonalt'] = (math.degrees(self.moon.alt), 'Degrees')
        self.allskymap.header['moonaz'] = (math.degrees(self.moon.az), 'Degrees')
        self.allskymap.header['moonph'] = (self.moon.moon_phase, 'Moon Phase as Fraction of illuminated Surface')
        if self.source is not None:
            self.allskymap.header['alt'] = (math.degrees(self.source.alt), 'Degrees (Pointing)')
            self.allskymap.header['az'] = (math.degrees(self.source.az), 'Degrees (Pointing)')
            self.allskymap.header['source'] = (self.pointing, 'Name of pointed source (if available)')
        #self.allskymap.header['extinc'] = (self.k, 'Extincion Coefficient used')
        self.allskymap.header['bzero'] = (0, " ")
        self.allskymap.header['lat'] = (str(self.observer_source.lat), 'Observer GPS Position')
        self.allskymap.header['lon'] = (str(self.observer_source.lon), 'Observer GPS Position')
        self.allskymap.header['elev'] = (self.observer_source.elevation, 'Observer Elevation [m above NN]')
        self.allskymap.header['units'] = (self.units)

        if fov_averaging:
            self.allskymap.data = self.getAllSky_FOV_average(size_allsky=size, size_fov=10, fov=5.0)
        else:
            self.allskymap.data = self.getAllSky(size)

    def getAllSky_FOV_average(self, size_allsky, size_fov, fov):
        data = np.empty((size_allsky, size_allsky))
        data.fill(np.nan)
        resolution = math.radians(180) / size_allsky
        offset_zen = 0
        offset_az = 0
        offset_x = 0
        offset_y = -offset_zen * (1 / resolution)
        for x in tqdm(range(size_allsky)):
            for y in range(size_allsky):
                az = (math.atan2((x - size_allsky / 2. - offset_x),
                                 (y - size_allsky / 2. - offset_y)) + offset_az)
                zen = math.hypot((x - size_allsky / 2. - offset_x),
                                 (y - size_allsky / 2. - offset_y)) * resolution
                if (zen < resolution * size_allsky / 2):
                    data[y, x] = np.nanmedian(self.getFOV_altaz(np.pi/2 - zen, az, fov=fov, size=size_fov))
        return data


    def getAllSky(self, size):
        resolution = math.radians(180) / size
        offset_zen = 0
        offset_az = 0
        offset_x = 0
        offset_y = -offset_zen * (1 / resolution)
        return self.getMapData(size, offset_x, offset_y, offset_az, offset_zen, resolution, silent=False)

    def drawFOV_source(self, source, fov=5.0, size=10, ra_offset=0.0, dec_offset=0.0):
        self.setSource(source, ra_offset=ra_offset, dec_offset=dec_offset)
        a = np.empty((size, size))
        a.fill(np.nan)
        self.fovmap = pyfits.ImageHDU(a)
        self.fovmap.data = self.getFOV_source(fov=fov, size=size)

    def drawFOV_altaz(self, alt, az, fov=5.0, size=10):
        a = np.empty((size, size))
        a.fill(np.nan)
        self.fovmap = pyfits.ImageHDU(a)
        self.fovmap.data = self.getFOV_altaz(alt, az, fov=fov, size=size)


    def getFOV_altaz(self, pointing_alt, pointing_az, fov, size):
        resolution = math.radians(fov) / size
        offset_zen = float(np.pi/2 - pointing_alt)
        offset_az = float(pointing_az)
        offset_x = 0
        offset_y = -offset_zen * (1  /resolution)
        return self.getMapData(size, offset_x, offset_y, offset_az, offset_zen, resolution, silent=True)

    def getFOV_source(self, fov, size):
        resolution = math.radians(fov) / size
        offset_zen = float(np.pi/2 - self.source.alt)
        offset_az = float(self.source.az)
        offset_x = 0
        offset_y = -offset_zen * (1  /resolution)
        return self.getMapData(size, offset_x, offset_y, offset_az, offset_zen, resolution, silent=False)


    def getMapData(self, size, offset_x, offset_y, offset_az, offset_zen, resolution, silent=True):

        sunalt = float(self.sun.alt)
        if sunalt > 0:
            sunset = self.observer_source.next_setting(self.sun)
            # print fancy red error message
            message = 5 * '#' + ' Sun still up! Next sunset at %s ' % sunset + 5 * '#'
            print('\x1b[0;30;41m' + len(message) * '#')
            print(message)
            print(len(message) * '#' + '\x1b[0m')

            return -1 * np.ones((size, size))

        elif sunalt < 0 and sunalt > math.radians(-18.0):
            # print fancy red error message
            message = 5 * '#' + ' Sunlight might have influence! sun alt= %.2f deg ' % math.degrees(sunalt) + 5 * '#'
            print('\x1b[0;30;41m' + len(message) * '#')
            print(message)
            print(len(message) * '#' + '\x1b[0m')

            return np.zeros((size, size))

        else:
            # Model drawing starts here:
            data = np.empty((size, size))
            data.fill(np.nan)
            for x in tqdm(range(size), disable=silent):
                for y in range(size):
                    az = (math.atan2((x - size / 2. - offset_x),
                                     (y - size / 2. - offset_y)) + offset_az)
                    zen = math.hypot((x - size / 2. - offset_x),
                                     (y - size / 2. - offset_y)) * resolution
                    if (zen > math.radians(90.0)):
                        continue
                    else:
                        moondist = nsbtools.greatCircle(zen, az, np.pi / 2. - self.moon.alt, self.moon.az)
                        if moondist > math.radians(5.0) and nsbtools.greatCircle(zen, az, offset_zen, offset_az) < resolution*size / 2:
                            if self.use_mhz:
                                # new model
                                data[y, x] = self.model_new(zen=zen, az=az)
                            else:
                                # old model
                                data[y, x] = self.model_old(zen=zen, az=az)
            return data

    def model_new(self, zen, az):
        ra, dec = self.observer_source.radec_of(az, math.pi / 2 - zen)
        healpixid = self.gaiamap.healpix(math.degrees(ra), math.degrees(dec))
        b1 = 0.594
        b3 = 0.126
        s = 25.851
        return s * (b1 * nsbtools.B_moon(zen, az, np.pi / 2. - self.moon.alt, self.moon.az, 0.479, self.moon_alpha)
            + b3 * nsbtools.MagnLb(self.gaiamap.getBrightness(healpixid)))

    def model_old(self, zen, az):
        ra, dec = self.observer_source.radec_of(az, math.pi / 2 - zen)
        healpixid = self.gaiamap.healpix(math.degrees(ra), math.degrees(dec))
        return (nsbtools.B_moon(zen, az, np.pi / 2. - self.moon.alt, self.moon.az, 0.479, self.moon_alpha) +
                nsbtools.B_sky(zen, az, 77.0, 0.479) +
                nsbtools.MagnLb(self.gaiamap.getBrightness(healpixid)))


    def smooth_gauss(self, sigma):
        self.allskymap.data = gaussian_filter(self.allskymap.data, sigma=sigma)

    def median_filter(self, size):
        self.allskymap.data = median_filter(self.allskymap.data, size=int(size))

    def getStatistics(self):
        median_allsky, mean_allsky = np.nanmedian(self.allskymap.data), np.nanmean(self.allskymap.data)
        median_fov, mean_fov = np.nanmedian(self.fovmap.data), np.nanmean(self.fovmap.data)
        if not np.isnan(median_allsky) and not np.isnan(mean_allsky):
            self.allskymap.header['median'] = (median_allsky, 'Median Image Brightness')
            self.allskymap.header['mean'] = (mean_allsky, 'Mean Image Brightness')
        if not np.isnan(median_fov) and not np.isnan(mean_fov):
            self.fovmap.header['median'] = (median_fov, 'Median Image Brightness')
            self.fovmap.header['mean'] = (mean_fov, 'Mean Image Brightness')
        return median_allsky, mean_allsky, median_fov, mean_fov

    def setDate(self, date):
        self.observer_source.date = date
        self.observer_moon.date = date
        self.observer_sun.date = date
        self.recomputeAll()

    def recomputeAll(self):
        if self.source is not None:
            self.source.compute(self.observer_source)
        self.moon.compute(self.observer_moon)
        self.moon_alpha = math.acos(self.moon.moon_phase * 2 - 1)
        self.sun.compute(self.observer_sun)

    def calculateTimespan_fast(self, moonallowed=True):
        self.setDate(self.time_start)
        self.bright = []
        self.moonphase = []
        self.moonalt = []
        self.sourcealt = []
        self.moonaz = []
        self.sourceaz = []
        self.separation = []

        t = self.time_start
        self.setDate(t)

        while t < self.time_end:

            if self.sun.alt > self.observer_sun.horizon:
                t = self.observer_sun.next_setting(self.sun)
                self.setDate(t)

            elif self.source.alt > self.observer_source.horizon and moonallowed:
                if self.use_mhz:
                    # new model
                    self.bright.append(self.model_new(zen=np.pi / 2 - self.source.alt, az=self.source.az))
                else:
                    # old model
                    self.bright.append(self.model_old(zen=np.pi / 2 - self.source.alt, az=self.source.az))

                self.moonphase.append(self.moon.moon_phase)
                self.moonalt.append(math.degrees(self.moon.alt))
                self.moonaz.append(math.degrees(self.moon.az))
                self.sourcealt.append(math.degrees(self.source.alt))
                self.sourceaz.append(math.degrees(self.source.az))

                self.separation.append(math.degrees(nsbtools.greatCircle(np.pi / 2. - self.source.alt,
                                                                         self.source.az,
                                                                         np.pi / 2. - self.moon.alt,
                                                                         self.moon.az)))

            elif not moonallowed and self.source.alt > self.observer_source.horizon and self.moon.alt < self.observer_moon.horizon:
                if self.use_mhz:
                    # new model
                    self.bright.append(self.model_new(zen=np.pi / 2 - self.source.alt, az=self.source.az))
                else:
                    # old model
                    self.bright.append(self.model_old(zen=np.pi / 2 - self.source.alt, az=self.source.az))
                """
                self.moonphase.append(self.moon.moon_phase)
                self.moonalt.append(math.degrees(self.moon.alt))
                self.moonaz.append(math.degrees(self.moon.az))
                self.sourcealt.append(math.degrees(self.source.alt))
                self.sourceaz.append(math.degrees(self.source.az))

                self.separation.append(math.degrees(nsbtools.greatCircle(np.pi / 2. - self.source.alt,
                                                                         self.source.az,
                                                                         np.pi / 2. - self.moon.alt,
                                                                         self.moon.az)))
                """
            else:
                pass

            t += 1.0 / (24 * (60 / self.timeresolution))
            self.setDate(t)


    def calculateTimespan(self):
        self.setDate(self.time_start)
        self.timestamps = []
        self.bright = []
        self.moonphase = []
        self.moonalt = []
        self.sourcealt = []
        self.moonaz = []
        self.sourceaz = []
        self.sunalt = []
        self.sunaz = []
        self.separation = []

        t = self.time_start
        while t < self.time_end:
            self.setDate(t)
            self.timestamps.append(t - self.time_start)
            if self.source.alt > self.observer_source.horizon and self.sun.alt < self.observer_sun.horizon:
                if self.use_mhz:
                    # new model
                    self.bright.append(self.model_new(zen=np.pi / 2 - self.source.alt, az=self.source.az))
                else:
                    # old model
                    self.bright.append(self.model_old(zen=np.pi / 2 - self.source.alt, az=self.source.az))

            else:
                self.bright.append(-1)

            self.moonphase.append(self.moon.moon_phase * 100)
            self.moonalt.append(math.degrees(self.moon.alt))
            self.moonaz.append(math.degrees(self.moon.az))
            self.sourcealt.append(math.degrees(self.source.alt))
            self.sourceaz.append(math.degrees(self.source.az))
            self.sunalt.append(math.degrees(self.sun.alt))
            self.sunaz.append(math.degrees(self.sun.az))

            if self.source.alt > self.observer_source.horizon and self.sun.alt < self.observer_sun.horizon and self.moon.alt > self.observer_moon.horizon:
                self.separation.append(math.degrees(nsbtools.greatCircle(np.pi / 2. - self.source.alt,
                                                                         self.source.az,
                                                                         np.pi / 2. - self.moon.alt,
                                                                         self.moon.az)))
            else:
                self.separation.append(-1)

            t += 1.0 / (24 * (60 / self.timeresolution))

        t = self.time_start - 1
        self.setDate(self.time_start)
        #self.recomputeAll()
        self.sunset = []
        self.sunrise = []
        while t < self.time_end:
            self.observer_sun.date = t
            sr = self.observer_sun.next_rising(self.sun)
            ss = self.observer_sun.next_setting(self.sun)

            t = ss + 0.25
            self.sunrise.append([float(sr - self.time_start), str(sr) + ' \tSunrise'])
            self.sunset.append([float(ss - self.time_start), str(ss) + ' \tSunset'])

        t = self.time_start - 1
        self.setDate(self.time_start)
        #self.recomputeAll()
        self.moonset = []
        self.moonrise = []
        while t < self.time_end:
            self.observer_moon.date = t
            mr = self.observer_moon.next_rising(self.moon)
            ms = self.observer_moon.next_setting(self.moon)
            t = ms + 0.25
            self.moonrise.append([float(mr - self.time_start), str(mr) + ' \tMoonrise'])
            self.moonset.append([float(ms - self.time_start), str(ms) + ' \tMoonset'])

        t = self.time_start
        self.setDate(self.time_start)
        #self.recomputeAll()
        self.sourceset = []
        self.sourcerise = []
        while t < self.time_end:
            self.observer_source.date = t
            sor = self.observer_source.next_rising(self.source)
            sos = self.observer_source.next_setting(self.source)
            t = sos + 0.25
            self.sourceset.append([float(sos - self.time_start), str(sos) + ' \tSet of ' + self.source.name])
            self.sourcerise.append([float(sor - self.time_start), str(sor) + ' \tRise of ' + self.source.name])
