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

import os

from .nsbtools import makeDate



class TheConfiguration():
    def __init__(self):
        pass

    def readStandardConfig(self):
        try:
            home = os.path.join(os.path.expanduser("~"), ".nsb/")
            self.config_filepath = os.path.join(home,'config.cfg')
            self.readConfig(self.config_filepath)
        except Exception as e:
            print('%s not found! \nWill now try to create a default one!' % self.config_filepath)
            print(e)
            self.createConfig(self.config_filepath)
            self.readConfig(self.config_filepath)

    def readConfig(self, configfile):
        self.file = open(configfile, 'r')
        self.config = {}
        try:
            for line in self.file:
                line = line.strip()
                if not line.startswith('#'):
                    self.config[line.split('=')[0].strip()] = line.split('=')[1].strip()
            t1, t2 = self.config['time'].split(' ')[0], self.config['time'].split(' ')[1]
            self.config['time'] = makeDate(t1, t2)
            # dirty check for new version of the configfile
            # if there is no mhz entry this will fail
            mhz = self.config['use_mhz']
            print('successfully opened %s' % configfile)
        except Exception as e:
            print(e)
            print('\nSomething went wrong while reading %s' % configfile)
            print('if you updated nsb to a version > 0.4.0, you have to create a new standard config')
            print('python -m nsb --create /home/$USER/.nsb/config.cfg')
            raise SystemExit
        self.file.close()

    def createConfig(self, configfile):
        with open(configfile, 'w+') as f:
            f.write("""#
# allskymaps Config File
#
# Date and Time
time = today now
#time = 2017/01/18 23:30:00
#
# Observer Location (HESS is at 16.5028 -23.27280 @ 1800.0)
Lon = 16.5028
Lat = -23.27280
elevation = 1800.
#
# dark zenith night sky brightness (units nanoLambert)
B = 77.0
#
# Extinction coefficient (units mags per air mass)
k = 0.479
#
# define output units MHz (instead of nanoLamberts)
use_mhz = False
#
# output Imagesize in Pixels (its gonna be square)
image_size = 200
#
# observation position in the sky [deg]
alt = 90.0
az  = 0.0
#
# Level of HealPixMap used for plotting gaia catalog
healpixlevel = 7
#
# Gaussian smoothing kernel [pixel]
gauss = 0.0
#
moon_above_horizon = 0.0
#
sun_below_horizon = -18.0
#
source_above_horizon = 10.0""")

        print('SUCCESS! %s with default values was saved to disc\nnow proceeding...\n' % os.path.realpath(configfile))
