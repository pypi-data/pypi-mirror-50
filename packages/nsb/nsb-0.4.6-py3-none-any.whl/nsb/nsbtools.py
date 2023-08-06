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
import time
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import ephem
from operator import itemgetter


def writeToDataFile(filename, values):
    '''
    Very simple Function to write (append) some values to a file
    '''
    f = open(filename, 'a')
    f.write(values)
    f.close()


def plotMaps(image, title):
    #print('Please close Plot Window to proceed (terminate)...')
    plt.figure()
    vmin, vmax = np.nanmin(image), np.minimum(4 * np.nanmedian(image), np.nanmax(image))
    plt.imshow(image, cmap=cm.viridis, vmin=vmin, vmax=vmax)
    plt.colorbar()
    plt.gca().get_xaxis().set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.title(title)
    plt.draw()


def plotObsTime(model):

    plt.figure()
    separation = np.nan_to_num(model.separation)
    bright = np.nan_to_num(model.bright)
    bright = bright[separation > 0]

    # keeps number of steps between 11 and 101
    steps = np.min([101, np.max([11, model.threshold])])
    model.brightness_range = np.linspace(0, model.threshold, steps)

    hours = []
    if model.verbose: print(
        "total Observation Time gain of source %s during moontime\n max nsb\tgain total hours\t(hours per year)" % (
        model.source.name))
    for limit in model.brightness_range:
        h = np.sum(bright < limit) / (60 / model.timeresolution)
        hours.append(h)
        if model.verbose: print(
            "%.2f nLb,\t(%.2f hours),\t(%.2f hours/year)" % (limit, h, 365 * h / (model.time_end - model.time_start)))

    plt.plot(model.brightness_range, 365 * np.array(hours) / (model.time_end - model.time_start),
             label=model.source.name)
    plt.legend()
    ax = plt.gca()
    plt.title("Observation Time Gain with Moonlight")
    ax.set_xlabel('max allowed Brightness')
    ax.set_ylabel('Moonlight Observation Time [h/year]')
    plt.draw()


def plotTimespan(model):
    # verbose timing output
    if model.verbose:
        all_times = model.sunset + model.sunrise + model.sourceset + model.sourcerise + model.moonset + model.moonrise
        all_times = sorted(all_times, key=itemgetter(0))
        sun_down = False
        for i in range(len(all_times)):
            if "Sunset" in all_times[i][1]:
                sun_down = True
            if sun_down:
                if i > 0 and not ("Sunset" in all_times[i][1]):
                    print("\t\t\t%.2f hours" % ((all_times[i][0] - all_times[i - 1][0]) * 24))
                print(all_times[i][1])
            if "Sunrise" in all_times[i][1]:
                sun_down = False
                print()

    plt.rcParams['figure.figsize'] = 16, 12
    # fig, (sub1, sub2, sub3) = plt.subplots(3, 1, sharex=True)
    fig, (sub1, sub2) = plt.subplots(2, 1, sharex=True)
    plt.subplots_adjust(bottom=0.5)

    # source alt colorcoded
    co = []
    for value in model.sourcealt:
        co.append(np.interp(value, [0.0, 90.0], [0.0, 1.0]))

    if len(model.timestamps) <= 50:
        labels = ['      %s' % ephem.Date(t + model.time_start) for t in model.timestamps]
        plt.xticks(model.timestamps, labels, rotation=90)
    elif len(model.timestamps) > 50 and (model.time_end - model.time_start) < 15:
        ticks = []
        labels = []
        t = 0
        while t < (model.time_end - model.time_start):
            t += 0.25
            ticks.append(t)
            labels.append("      " + str(ephem.Date(t + model.time_start)))
        plt.xticks(ticks, labels, rotation=90)

    elif (model.time_end - model.time_start) < 50:
        ticks = []
        labels = []
        t = 0
        while t < (model.time_end - model.time_start):
            t += 1
            ticks.append(t)
            labels.append("      " + str(ephem.Date(t + model.time_start)))
        plt.xticks(ticks, labels, rotation=90)

    else:
        plt.xlabel('Days since %s' % model.time_start)

    sub1.minorticks_on()
    sub2.minorticks_on()

    sub1.set_title('estimated sky-brightness for position of source "%s"' % model.source.name)
    # sub1.scatter(model.timestamps, model.bright, s=1, c=co, label='brightness')
    sub1.scatter(model.timestamps, model.bright, s=1, label='brightness')
    sub1.set_ylim((10, 10000))
    sub1.set_yscale("log", nonposy='clip')
    sub1.set_xlim(left=0, right=model.time_end - model.time_start)
    sub1.axhline(y=150, alpha=0.7, color='green', ls='--', linewidth=1)
    sub1.axhline(y=500, alpha=0.7, color='orange', ls='--', linewidth=1)
    sub1.axhline(y=1000, alpha=0.7, color='red', ls='--', linewidth=1)
    sub1.set_ylabel('Brightness')

    sub2.plot(model.timestamps, model.moonphase, label='moon phase')
    sub2.plot(model.timestamps, model.separation, label='separation')
    sub2.plot(model.timestamps, model.moonalt, label='moon alt')
    sub2.plot(model.timestamps, model.sourcealt, label='source alt')
    sub2.set_xlim(left=0, right=model.time_end - model.time_start)
    sub2.axhspan(80, 100, facecolor='grey', alpha=0.2)
    sub2.axhline(y=0, linewidth=0.2, color='black')
    sub2.set_ylabel('Alt, Sep [deg]\nPhase [%]')

    # put the orange and grey bands for dayligt and moonlight
    for i in range(0, len(model.sunrise)):
        sub1.axvspan(model.sunrise[i][0], model.sunset[i][0], facecolor='orange', alpha=0.1)
        sub2.axvspan(model.sunrise[i][0], model.sunset[i][0], facecolor='orange', alpha=0.1)

    for i in range(0, len(model.moonrise)):
        sub1.axvspan(model.moonrise[i][0], model.moonset[i][0], facecolor='grey', alpha=0.1)
        sub2.axvspan(model.moonrise[i][0], model.moonset[i][0], facecolor='grey', alpha=0.1)

    sub1.legend(loc='upper right')
    sub2.legend(loc='upper right')

    # Pad margins so that markers don't get clipped by the axes
    # plt.margins(0.2)
    fig.tight_layout()
    plt.tight_layout()
    plt.draw()
    fname = "%s_%s_-_%s.pdf" % (model.source.name, model.time_start, model.time_end)
    fname = fname.replace(" ", "_").replace("/", "-")

    # plt.savefig("star_baselines/" + fname, papertype="a4", dpi=300)

    plt.draw()


def makeDateString(date):

    d = date.tuple()
    date_string = ''
    for x in d:
        if float(x) < 1:
            x = 0
        if len(str(int(x))) > 1:
            date_string += str(int(x))
        elif len(str(int(x))) == 1:
            date_string += '0' + str((x))
    return date_string

def makeDate(datestring, timestring):
    if datestring in ['today', 'heute']:
        year = time.strftime("%Y")
        month = time.strftime("%m")
        day = time.strftime("%d")
    else:
        year = datestring[0:4]
        month = datestring[5:7]
        day = datestring[8:]

    if timestring in ['now', 'jetzt']:
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")
    else:
        hour = timestring[0:2]
        minute = timestring[3:5]
        second = timestring[6:]

    return "" + str(year) + "/" + str(month) + "/" + str(day) + " " \
                + str(hour) + ":" + str(minute) + ":" + str(second)


def nLbMag(B):
    '''
    nanoLambert to Magnitude conversion
    '''
    return -2.5 * math.log10(1.0 / np.pi * 0.00001 * B / 108400.0)


def MagnLb(M):
    '''
    Magnitude to nanoLambert conversion
    '''
    return np.pi * 100000 * 108400 * 10**(-0.4 * M)


def greatCircle(Zen, phi, Zen2, phi2):
    '''
    Calculates the great Circle Distance of two pairs of spheric coordinates
    Works for GPS Coordinates as well as for Zen / Az (not ALT !)
    '''
    if math.isclose(Zen, Zen2) and math.isclose(phi, phi2):
        return 0
    else:
        return math.acos(math.sin(np.pi / 2. - Zen) * math.sin(np.pi / 2. - Zen2) +
                         math.cos(np.pi / 2. - Zen) * math.cos(np.pi / 2. - Zen2) * math.cos(phi - phi2))



def X(Z):
    if Z <= math.pi/2:
        return 0.4 + 0.6 * (1 - 0.96 * (math.sin(Z))**2)**(-0.5)
    else:
        return 0.4 + 0.6 * (1 - 0.96 * 1)**(-0.5)


def f(rho):
    r = math.degrees(rho)
    A = 5.2313
    B = 0.9351
    F = 5.9014
    return 10**A * (B + (math.cos(rho))**2) + 10**(F - r / 40)


def I_moon(moon_alpha):
    a = math.degrees(moon_alpha)
    return 10**(-0.4 * (3.84 + 0.026 * math.fabs(a) + 4 * 10**(-9) * a**4))


def B_sky(Zen, phi, B_zero, k):
    """
    Krisciunas et. al Sky-only-Model
    Brightness of the Sky at certain position without moon
    """
    if Zen < np.pi / 2:
        return B_zero * X(Zen) * 10**(-0.4 * k * (X(Zen) - 1))
    else:
        return 0


def B_moon(Zen, phi, Zen_moon, phi_moon, k, moon_alpha, moon_horizon=-4.0):
    """
    Krisciunas et. al Moon-Model
    only valid for moon above horizon. it gives values for negative moon alt,
    but they have no physical meaning.
    --> so in that case better return 0
    """
    Zm = Zen_moon + float(np.deg2rad(moon_horizon))
    if Zm < np.pi / 2:
        rho = greatCircle(Zen, phi, Zm, phi_moon)
        #return f(rho) * I_moon(moon_alpha) * 10 ** (-0.4 * k * X(Zm)) * (1 - 10 ** (-0.4 * k * X(Zen))) - B_sky(Zen, phi, 67.5, k)
        return f(rho) * I_moon(moon_alpha) * (1 - 10 ** (-0.4 * k * X(Zen))) * (10 ** (-0.4 * k * X(Zm)) - 10 ** (-0.4 * k * X(np.pi / 2)))
    else:
        return 0

