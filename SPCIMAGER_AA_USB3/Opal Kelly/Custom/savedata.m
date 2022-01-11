%% Save results
    %SaveLocation = '';
    %SaveFilename = '';
    
    if exist(SaveLocation,'dir') ~= 7
        mkdir(SaveLocation)
    end
    
    f = strcat(SaveLocation,SaveFilename,'.mat');
    save(f,'saveData');
    disp(' * File Saved.')