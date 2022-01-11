%% Sensor GUI
    if (exist('s') == 0) 
	
		clc
		clear all
    
		disp('SPCIMAGERAA Sensor')
		disp(' ')
        
		s = SPCIMAGERAA('C:\SPAD\SPCIMAGER_AA_USB3\SPCIMAGER_AA_USB3\SPCIMAGER_TOP.bit');
        %s.SetResetTime(20,100);
	else
	
		disp(' * WARNING: Already connected to sensor!')
		
	end