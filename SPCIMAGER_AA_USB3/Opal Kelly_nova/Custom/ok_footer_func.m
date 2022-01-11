function [] = ok_footer_func( okComms )
    %% Close the OK Object
    %OK Footer
    % Closes connection to the connected Opal Kelly


    disp('--------------------------')
    disp('Closing Communications')
    disp('--------------------------')
    disp(' * Connection to Opal Kelly Closed.')
    calllib('okFrontPanel', 'okFrontPanel_Destruct', okComms.ptr);
    disp(' * Experiment Complete.')

end
