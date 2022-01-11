
%% Close the OK Object
% Close OK Object
disp('--------------------------')
disp('Closing Communications')
disp('--------------------------')
disp(' * Connection to Opal Kelly Closed.')
calllib('okFrontPanel', 'okUsbFrontPanel_Destruct', okComms.ptr);
disp(' * Experiment Complete.');
RunTime = toc(ticID);

clear okComms;
clear id;
clear mask;
clear bank;
clear fpga;
clear open;