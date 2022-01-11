function rampDAC (okComms, bank, wirename, returnwirename, finalvalue, pausetime, abs_step)
% Increment or Decrement DAC voltages with a pause on each step

% Get current value
updatewireouts(okComms);
currentvalue = wireoutdata(okComms, bank, returnwirename);



if (currentvalue > finalvalue)
    % Decrementing
    step = (-1) * abs_step;
else
    % Incrementing
    step = abs_step;
end

% Loop to get to final value
pause on
for voltage = currentvalue:step:finalvalue

    wireindata(okComms,bank,wirename,voltage);
    updatewireins(okComms);


    progDAC(okComms,bank,'ProgResetDAC');
    VHV_Ret = wireoutdata(okComms, bank, returnwirename)
    pause(pausetime)
end
pause off


end

