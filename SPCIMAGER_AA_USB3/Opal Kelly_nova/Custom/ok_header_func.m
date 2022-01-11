%% Opal Kelly Test Comms Header
% Author: Neale Dutton
% Creation Date: 11/12/12
% Last Update: 08/08/13

% Comment: 

function [okComms bank] = ok_header_func ( OKbitfile )
%% OK Header
% Connects to the Opal Kelly

format short eng

disp('--------------------------')
disp('Opal Kelly to Matlab Comms')
disp('--------------------------')


% Load the correct register bank:
ok_register_bank;

setuperror = 0;

% Check bitfile exists:
bitfilecheck = exist(OKbitfile,'file');
if(bitfilecheck == 2)
    disp(' * Located bit file.')
else
    setuperror = 1;
    error('Error: No bit file!')
end

% The following procedure is to open communications with the Opal Kelly
% generic FPGA platform. Testing can then be started by means of a
% script or manual instructions.

% Open library and communications:

if (setuperror == 0)
    % Check library is loaded
    if ~libisloaded('okFrontPanel')
        loadlibrary('okFrontPanel', 'okFrontPanelDLL.h', 'notempdir');
    end
    
    % Open OK comms
    okComms.ptr = calllib('okFrontPanel', 'okFrontPanel_Construct');
end

if (setuperror == 0)
    % Check if any OKs are connected
    success = checkfpgaexists (okComms);
    if (success)
        disp(' * Opal Kelly FPGA is connected')
    else
        setuperror = 1;
        disp('Error: No Opal Kellys are connected')
    end
end

if (setuperror == 0)
    % Retrieve serial number of first connected device and open/programme fpga.
    % Serial Number:
    fpga = openbyserial(okComms, '');
    
    % Get Opal Kelly Device ID for logging purposes
    id = getdeviceid(okComms);
end

% Check device is open
if (setuperror == 0)
    open = isopen(okComms);
    if (open)
        disp(' * FPGA is Open')
    else
        disp('Error: Error in opening FPGA')
        setuperror = 1;
    end
end

if (setuperror == 0)
    % Configure FPGA
    if (open)
%         success = configurefpga(fpga, OKbitfile);
        success = configurefpga(okComms, OKbitfile);
        if (success)
            disp(' * FPGA Programmed Successfully')
        else
            disp('Error: Error in programming FPGA')
            setuperror = 1;
        end
    end
end

if (setuperror)
    
    % Close OK Comms
    calllib('okFrontPanel', 'okFrontPanel_Destruct', okComms.ptr);
    error('There was an error in setup. Please ensure an FPGA is pluggged in and no other programme is calling it.');
    
else
    
    
    % Default wire in mask value
    mask = uint32(hex2dec('ffffffff'));
    
    disp(' ')
    disp('--------------------------')
    disp('Testing Procedure:')
    disp('--------------------------')
    
    clear bitfilecheck;
    clear setuperror;
    clear success;
    clear sn;
    
end
end