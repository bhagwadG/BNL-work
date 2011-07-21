#
# Example script for looking at BOSS spectra and redshift fits via Python.
#
# Written by Adam S. Bolton, University of Utah, Oct. 2009
#

# Imports:
import scipy as s
import numpy as n
import pyfits as pf
import matplotlib as mpl
mpl.use('TkAgg')
mpl.interactive(True)
from matplotlib import pyplot as p

# Set topdir:
topdir = '/astro/u/bhagwadG/work/SDSS_OLD/0310/1d'

# Pick your plate/mjd and read the data:
plate = '51990'
mjd_1 = '0310-183'
spfile = topdir + '/spSpec-' + plate + '-' + mjd_1 + '.fit'
hdulist = pf.open(spfile)
c0_1 = hdulist[0].header['COEFF0']
c1_1 = hdulist[0].header['COEFF1']
npix_1 = hdulist[0].header['NAXIS1']
wave = n.log10(10.**(c0_1 + c1_1 * n.arange(npix_1)))
bunit_1 = hdulist[0].header['BUNIT']
z_1    = hdulist[0].header['Z']
flux_1 = hdulist[0].data
hdulist.close()

plate = '51990'
mjd_2 = '0310-296'
spfile = topdir + '/spSpec-' + plate + '-' + mjd_2 + '.fit'
hdulist = pf.open(spfile)
c0_2 = hdulist[0].header['COEFF0']
c1_2 = hdulist[0].header['COEFF1']
npix_2 = hdulist[0].header['NAXIS1']
wave = n.log10(10.**(c0_2 + c1_2 * n.arange(npix_2)))
bunit_2 = hdulist[0].header['BUNIT']
z_2    = hdulist[0].header['Z']
flux_2 = hdulist[0].data
hdulist.close()

if z_1>z_2:
	numerator=z_1
	denominator=z_2
	flux_l=flux_1
	flux_s=flux_2
else:
	numerator=z_2
	denominator=z_1
	flux_l=flux_2
	flux_s=flux_s

corr=s.correlate(flux_s[0],flux_l[0],mode='same')
corr_norm_flux=corr/s.sqrt((corr*corr).sum())

median=n.median(wave)
		
ratio = n.log10((1+numerator)/(1+denominator))
peak = median-ratio

p.figure()
p.plot(wave, corr_norm_flux, 'k', color='g')
p.xlabel('Angstroms')
p.ylabel(bunit_1)
p.title("Z_1= " + str(z_1) + " and Z_2 =" + str(z_2))
p.axvline(peak,color='r')
p.savefig("/astro/u/bhagwadG/plots/correlated/"+"correlated"+"_"+mjd_1+"_"+mjd_2+".png")

additive = n.log10((1+denominator)/(1+numerator))

p.figure()
p.plot(wave, flux_s[0], 'k', color='g')
p.xlabel('Angstroms')
p.ylabel(bunit_1)
p.plot(wave+additive, flux_l[0], 'k', color='b')
p.title("Z_1= " + str(z_1) + " and Z_2 =" + str(z_2))
p.savefig("/astro/u/bhagwadG/plots/overlap/"+"overlap"+"_"+mjd_1+"_"+mjd_2+".png")

p.show()



