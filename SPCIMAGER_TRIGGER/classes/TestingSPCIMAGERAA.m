%% SPCIMAGERAA Class Def Documentation
%
% Author: Neale Dutton
%
% Date Created: 28th Sept 2013
%
% This is a document describing all the possible MATLAB functions for
% running the SPCIMAGER_AA sensor.
%

clc
clear all


%% MATLAB Handle
% Handle for testing sensors
s = SPCIMAGERAA();


%% Set Voltages Supplies and Biasses
% Set voltages ready for connection to the sensor.


%% Sensor Connection
% Connect to Sensor:
s.SensorConnect;


%% Clock Routing
% The two time gates 'A' and 'B'

% Clock Routing for A
s.SetTimeGateInput('Bin A','ExtClk')
s.SetTimeGateInput('Bin A','OptClk','High')
s.SetTimeGateInput('Bin A','OptClk','Low')
s.SetTimeGateInput('Bin A','PulseGen')

% Clock Routing for B
s.SetTimeGateInput('Bin B','ExtClk')
s.SetTimeGateInput('Bin B','OptClk','High')
s.SetTimeGateInput('Bin B','OptClk','Low')
s.SetTimeGateInput('Bin B','PulseGen')

% Test Pad Routing
s.SetTestPad ('Bin A','Enable')
% Sets s.BinAOutput = 'Enabled';

s.SetTestPad ('Bin B','Enable')
% Sets s.BinBOutput = 'Enabled';

s.SetTestPad ('Bin A','Disable')
% Sets s.BinAOutput = 'Disabled';

s.SetTestPad ('Bin B','Disable')
% Sets s.BinBOutput = 'Disabled';


%% Video Timing
% s.SetRegionOfInterest (RowMin, RowMax, ColMin, ColMax)

% Dark ASPC Row:
RowMin = 0;
RowMax = 240;
ColMin = 0;
ColMax = 0;
s.SetRegionOfInterest (RowMin, RowMax, ColMin, ColMax);
% Pixels Selected is set to 'Dark SPC Row'
s.PixelsActive

% ASPC Rows:
RowMin = 1;
RowMax = 240;
s.SetRegionOfInterest (RowMin, RowMax, ColMin, ColMax);
% Pixels Selected is set to 'SPC'
s.PixelsActive

% TAC Rows:
RowMin = 241;
RowMax = 248;
s.SetRegionOfInterest (RowMin, RowMax, ColMin, ColMax);
% Pixels Selected is set to 'SPC'
s.PixelsActive

% TAC Rows:
RowMin = 249;
RowMax = 255;
s.SetRegionOfInterest (RowMin, RowMax, ColMin, ColMax);
% Pixels Selected is set to 'SPC'
s.PixelsActive

% -------------------------------------------------------------------------
% SetSensorMode

s.SetSensorMode('Idle')
s.SetSensorMode('Single Shot')
s.SetSensorMode('Continuous')
s.SetSensorMode('Off')

% -------------------------------------------------------------------------

% Take a picture!
%ColMin = 1;
%ColMax = 320;
%RowMin = 1;
%RowMax = 240;
%s.SetRegionOfInterest (RowMin, RowMax, ColMin, ColMax);

%[imageCaptured width height] = s.CaptureImage;
%imtool(imageCaptured, [0 4095]);

% -------------------------------------------------------------------------




% Disconnect
s.SensorDisconnect;

s.SetSensorMode('Off')

% Tidy Up
disp('Destroying Sensor Object');
delete(s); % Clears memory
clear s;   % Clear instance