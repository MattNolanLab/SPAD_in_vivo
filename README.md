# SPAD_in_vivo
Apply SPAD sensor and photometry system to imaging GEVI in vivo
## SPCIMAGER_AA_USB3
This is to run a MATLAB based GUI to control the Opal Kelly FPGA for SPAD imaging and saving data.

Running /GUI/DigitalDemo_fast.m will start the GUI, which will provide a live mode imaging and cab save the imaging data as a .bin file.

I already added a few lines to save a .csv format timestamp (Yifang).

"fixed_aggtwo_mask.m" is the code to analyse the .bin file, and generate total photon counts for each frame.
