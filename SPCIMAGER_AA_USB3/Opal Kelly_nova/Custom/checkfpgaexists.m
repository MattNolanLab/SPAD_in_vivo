function success = checkfpgaexists ( okComms )
% Check FGPA exists

num_fpga = calllib('okFrontPanel', 'okFrontPanel_GetDeviceCount', okComms.ptr);

if (num_fpga < 1)
    disp('Error: No FPGA is plugged in!')
    success = 0;
else
    success = 1;
end

end

