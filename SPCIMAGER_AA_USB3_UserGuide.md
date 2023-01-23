# SPCMAGER_AA_USB3 User Guide
The SPAD imager works with a customised PCB, a FPGA board (Opal Kelly XEM6310) and a SPAD sensor chip. The fully assembled board would be like this:
![image](https://user-images.githubusercontent.com/77569999/195673623-381bc49c-a8e5-44e4-af3c-d6e432e4647f.png)

Opal Kelly XEM6310 is at the end of life, so you cannot buy this board, but XEM7310 would also be compatible. We're also developing new PCB for more functions.

https://docs.opalkelly.com/xem6310/

Before running the software, you may need to download and install the FrontPanel USB driver, it’s also in the GitHub folder.

https://pins.opalkelly.com/downloads

The first time you run the GUI. MATLAB may give some errors and ask you to install some packages, like “MinGW-w64” and “image processing package”, please follow the instructions and install them. 

# Two different recording mode
This is a MATLAB based GUI that will support using the SPAD imager. Running the sensor would download a "SPCIMAGER_TOP.bit" file to the FPGA. There’re different versions of ".bit" files, the're for different recording mode. You can change the mode by changing the .bit file in the "SensorStart.m".

(1) The "SPCIMAGER_TOP.bit" can record the data when you click "Capture & Save data > start" on the GUI. This is the most common used mode. 

(2) The "SPCIMAGER_TOP_trigger.bit" will allow a triggered mode recording, meaning that when you click the "Capture & Save data > start" button, the recording won't start until a 3V voltage is delivered to a pin on the PCB. This mode is usually used for synchronising the optical recording with other recordings, e.g. ephys, behavior camera. The pin to deliver the trigger signal is OPTCLK_FPGA2 in the PCB design file, or JP92 middle pin on the PCB (for old version PCB used in Tian et al 2022, it's JP86 middle pin), a Ground pin (JP43 AGND) should also be connected to ground in triggered mode.

# Run the GUI and record data with contnuous mode.

Run the file "SPICIMAGERAA/GUI/DigitalDemo_fast.m", a GUI will show:
![image](https://user-images.githubusercontent.com/77569999/195642183-8dc5d321-bd32-4892-8395-189abd6f5f0e.png)

1. Click "Sensor on" button to connect the SPCImager, this is where the .bit file is downloaded to the FPGA.
2. Use Live View > Start button to start a live mode. "Aggregation" means you can sum up multiple frames (bit-planes) to get a better image. With 1 here, you can only get very pixelated live images. With more aggregated frames, you can get better images:

![image](https://user-images.githubusercontent.com/77569999/195670112-2808e1f4-45e8-44b6-9216-db99361723b4.png)

3. "Capture background" is a function where you can remove a certain amount of background noise. First, choose the aggregation and trun off all the light source and click this button, the image will freeze and then become live again, means the background is captured. Then, turn on the light source and you could get live images with a better quality. It doesn't work very well for aggregation higher than 2048. For in-vivo or ex-vivo imaging under a microscope, aggregation up to 1024 is enough to get a good image.  

![image](https://user-images.githubusercontent.com/77569999/195669557-6805f0f6-f70c-4cf3-92b0-d7bebc59d837.png)

4. "Capture & Save data" is used to record and save data, here "block" means how many blocks you want to save, one block will be saved as one binary file, e.g., if you choose 3, you will get three files named as "spc_data1.bin","spc_data2.bin","spc_data3.bin", you could also change the file names on the GUI. "bit plane/block" means how many bit planes in each block. Since our sensor is running at 9938.4Hz, 10000 bit planes is about 1 second. Then each .bin file you save is the data for 1 second recording. After selecting recording parameters, click "start", the recording will start and .bin data will be saved.

5. The "Brightness" box on the right can be changed to get a brighter live image. 

# Trouble shooting
1. The live-mode images may have grids like this:
![image](https://user-images.githubusercontent.com/77569999/214115271-d432c324-39ad-4d0d-96fa-b41c5a664831.png)
This is because the three potentiometers on the board (in the red circle) are not adjusted correctly. This can be easily fixed by adjusting the screw while live-mode imaging to find a sweet spot without any grids. 
![image](https://user-images.githubusercontent.com/77569999/214116149-dd98fd39-70cd-4796-996f-14fdb9206508.png)
