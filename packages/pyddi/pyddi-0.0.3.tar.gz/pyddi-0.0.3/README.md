# pyddi

### Description 

This tool is designed to identify regions in an image that require direction-dependent calibration. 
 
### Installation

Installation from source, working directory where source is checked out

    pip install .

This package is available on PYPI, allowing

    pip install pyddi

### The Technique:

This tool carries out the following steps:

1. It searches for pixels in an image/sources in the sky model with high signal-to-noise ratio.   
2. For computation purposes, pixels separated by a few beams are grouped. The position and intensity of the brightest pixel is returned for each group.  
3. Computes the local variance around pixels from 2 or sources from 1, and selects those with high local variance.   
4. If the user provides a PSF image, the PSF is correlated with each source/region. those with high correlation factor are selected.
5. Lastly, the tool writes out a Tigger model containing the source/pixel positions that made it through step 3 or 4. 

    5.1 However, a user can supply an actual sky model and the tool will cross match with above model, and tag sources in this former model as 'dE'.
  
    5.2 Or, alternatively, a user can specify whether they want their actual sky model to be used for the identification rather than pixels from an image, in which case, the sources in the sky model will be updated with tags 'dE'. 
    
    5.3 If a sky model is not supplied, source a model with positions will be returned. This model should not be used for anything except the positions.

### Implementation  

For help: pyddi  -h    

    Finds the direction subject to direction-dependent effects.  
  
    optional arguments:      
       -h, --help            show this help message and exit
       -i IMAGE, --img IMAGE    
                 Image of interest. Required.
       -p PSF_IMAGE, --psf PSF_IMAGE   
                 The psf image. Default=None.
       -c CATALOG, --cat CATALOG   
                  Sky model as LSM/txt. Default=None. Must be in Tigger  
                  format: "#format:name, ra_d, dec_d, i"   
       -fth FLUX_THRESHOLD, --flux-thresh FLUX_THRESHOLD   
                  Flux threshold. Regions in an image with flux > fth *
                  noise are considered. Default=10
       -vth VARIANCE_THRESHOLD, --variance-thresh VARIANCE_THRESHOLD   
                  Local variance threshold. Sources with varinace > vth   
                  * noise are considered. Defautl=5.   
       -vsize VARIANCE_SIZE, --var-size VARIANCE_SIZE   
                  The size of the region to compute the local variance.  
                  E.g vsize=10, gives a region of size = 10 *   
                  resolution. The resolution is in pixels. Default=10   
       -cth CORRELATION_THRESHOLD, --correlation-thresh CORRELATION_THRESHOLD   
                  Correlation threshold. Sources with correlation factor   
                  > cth are considered. Default=0.5    
       -csize CORRELATION_SIZE, --corr-size CORRELATION_SIZE   
                  The size of the region to compute correlation. see   
                  vsize. Default=5   
       -gpix GROUP_PIXELS, --group-pix GROUP_PIXELS   
                  The size of the region to group the pixels, in terms   
                  of psf-size. The psf is in degrees. e.g gpix=20, gives   
                  20xpsf. Default=20   
       -usec USE_CATALOG, --use-cat USE_CATALOG   
                  Use -cat for the identification and not only -i.    
       -o OUTPUT_PREFIX, --outpref OUTPUT_PREFIX    
                  The prefix for the output file containing directions   
                  in RA, DEC both in degrees, and peak flux of the   
                  pixels. Default=None  

Example Run:

    pyddi -i examples/kat7restored.fits -c examples/kat7restored.gaul -p examples/kat7psf.fits -vth 10 -cth 0.7 -gpix 50  -usec -o test-output 

    
  
 
 
 
 

