### **songcn**

**SONG** stands for **S**tellar **O**bservations **N**etwork **G**roup.

This package, **songcn**, is designed for the [**SONG-China**](http://song.bao.ac.cn/) project.

The affliated **song** package is the SONG-China project data processing pipeline.
The affliated **twodspec** is to provide basic operations for raw 2D spectral data.


## structures


**song**

- *extract.py* \
    ??
- *song.py*\
    song image collection management
- *thar.py*\
    ThAr wavelength calibration module for SONG.
    Loads templates.

**twodspec**

- *aperture.py* \
    the aperture class
- *calibration.py*\
    wavelength calibration module    
- *ccd.py*\
    basic CCD operations
- *extract.py*\
    spectral extraction module
- *scatter.py*\
    scattered-light substraction module
- *trace*\
    trace aperture


## acknowledgements

*SmoothingSpline* is from https://github.com/wafo-project/pywafo
