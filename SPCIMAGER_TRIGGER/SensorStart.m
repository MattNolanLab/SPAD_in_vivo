%% Sensor GUI
    if (exist('s') == 0) 
	
		clc
		clear all
    
		disp('SPCIMAGERAA Sensor')
		disp(' ')
        
		%s = SPCIMAGERAA('C:\SPAD\SPCIMAGER_AA_USB3\triggered SPAD\SPCIMAGER_TOP.bit'); 
        s = SPCIMAGERAA('C:\SPAD\SPCIMAGER_AA_USB3\triggered SPAD\SPCIMAGER_TOP_trigger2.bit');
        %s = SPCIMAGERAA('C:\Users\ttian\Desktop\SPCIMAGER_AA_USB3\SPCIMAGER_TOP_80ms_buffer.bit');
        %s = SPCIMAGERAA('C:\SPAD\SPCIMAGER_AA_USB3\triggered SPAD\SPCIMAGER_TOP_160ms.bit');
        %s.SetResetTime(20,100);
	else
	
		disp(' * WARNING: Already connected to sensor!')
		
	end