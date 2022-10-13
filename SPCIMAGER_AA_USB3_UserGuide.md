# SPCMAGER_AA_USB3 User Guide
The SPAD imager works with a customised PCB, a FPGA board (Opal Kelly XEM6310) and a SPAD arrary. 

https://docs.opalkelly.com/xem6310/

Before running the GUI, you may need to download and install the FrontPanel USB driver, it’s also in the GitHub folder.

https://pins.opalkelly.com/downloads

The first time you run the GUI. MATLAB may give some errors and ask you to install some plug-ins, like “MinGW-w64” and “image processing package”, please follow the instructions and install them.

# Run the GUI and record data with contnuous mode.

Run the file "SPICIMAGERAA/GUI/DigitalDemo_fast.m", a GUI will show up.
![image](https://user-images.githubusercontent.com/77569999/195642183-8dc5d321-bd32-4892-8395-189abd6f5f0e.png)



# Two different recording mode
This is a MATLAB based GUI that will support using the SPAD imager. Running the sensor would download a "SPCIMAGER_TOP.bit" file to the FPGA. There’re different versions of ".bit" files. You can change the mode by changing the .bit file in the "SensorStart.m".

(1) The "SPCIMAGER_TOP.bit" can record the data when you click "record" on the GUI. 

(2) The "SPCIMAGER_TOP_trigger.bit" will allow a triggered mode recording, meaning that when you click the "record" button, the recording won't start until a 3V voltage is delivered to a pin on the PCB.
