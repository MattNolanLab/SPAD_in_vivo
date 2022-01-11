classdef SPCIMAGERAA < handle
    %SPCIMAGER class describes all properties and methods of the
    %SPCIMAGER_AA obj
    %   Date Created: 27th Sept 2013
    %   Author: Neale Dutton
    
    %% Public Properties
    properties 
        
        FPNCorrection = zeros(240,320);
        FPNCorrectionMask = ones(240,320);
        
        % ---------------------
        % System Settings
        ClockFreq = 50E6; % 5 Mhz Clock Frequency by default.
        DigClockFreq = 50E6; % 5 Mhz Clock Frequency by default.
        % ---------------------
        % Pulse Generators

        BinAPos1 = 0;
        BinAPos2 = 10;
        
        BinBPos1 = 0;
        BinBPos2 = 10;
        
        BinADAC = 15; % DAC Drive Setting
        BinBDAC = 15; % DAC Drive Setting
 
        % ---------------------
        % Video Timing

    end  
    
    %% Protected Methods
    % The following properties are set by class methods:
    properties (SetAccess = protected)
        
        okComms = [];
        bank = [];
        
        % ---------------------
        % Power Supplies default values:
		VDDE = 3.3; % External VDDE
		
        V1V2 = 1.2; % GO1 Logic
        V3V3 = 3.3; % GO2 Logic, Disable Buffer, Output Op Amps
        V3V6 = 3.6; % Time Gate & Reset Buffer VDD
        V2V7 = 2.7; % Pixel Array VDD
        VDDOPAMP = 3.3;
        ADCPWR = 3.3;
        VREF = 1.0;
        
        VHV = 15.5; % Main Array
        VHV2 = 13.0; % Test Pixels
        
        ExposureTime = 1;
        ExposureMode = 0;
        
        NoOfExposures = 1;
        PixelBit = 1;
        
        % ---------------------
        % Bias Voltages
        VG = 3.3;
        VS = 0.1;
        VQ = 1;
        
        DAC5 = 0; % Spare
        DAC6 = 0; % Spare
        
        % Current Biases:
        IBIAS1 = 3; % 2.72V into a 270K res = 10uA, JP47
        IBIAS2 = 1.1; % 2.72V into a 270K res = 10uA, JP68
        
        % ---------------------
        % Pulse Generators
        
        % To set either Bin A or Bin B, use SetTestPads method
        BinAOutput = 'Disabled'; % Other option is 'Enabled'
        BinBOutput = 'Disabled'; % Other option is 'Enabled'
        
        BinAInputSel = 'PulseGen'; % Other options are 'OptClk' or 'ExtClk'
        BinBInputSel = 'PulseGen'; % Other options are 'OptClk' or 'ExtClk'
        
        OptClkOffsetSel = 'Low'; % Other option is high.
        
        % ---------------------
        % Video Timing
        % 'Dark SPC Row'
        % 'SPC'
        % 'TAC'
        % 'CP'
        PixelsActive = 'SPC';
        
        % Row 0 = Dark Row
        % Row 1 to 239 = SPC Imager
        % Row 240 to 247 = TAC Pixels
        % Row 248 to 255 = CP Pixels
        RowMin = 1;
        RowMax = 240;
        
        ColMin = 0;
        ColMax = 319;
        
        OutputMode = 'Analogue'; %Other option is single bit 'Digital'
        CaptureMode = 'Single'; % Other option is 'Continuous'
        
        CDS = 'On'; % CDS is Always On in this object
        Crowbar = 'On'; 
        
        GlobalReset = 'Off';
        
        DigitalTOFAmbientRejection = 'Off';
        
        RollingResetTime = 100;
        GlobalResetTime = 20;
        
        ColumnScanOutTime = 59; %COLUMN_CYCLES_CROWBAR
        ADC_Signal_Sample_Start = 27; %ADC_SIGNALS_START
        ADC_Crowbar_Sample_Start = 54;%ADC_CROWBAR_SAMPLE_START

        CDSTime = 30;
        
        % -----------------------------------------------------------------
        SensorStatus = 'Disconnected';  % Other allowed value is 'Connected'
        
        SensorMode = 'Off';
        % Other Values:
        % - Idle
        % - Sinlgle Shot
        % - Streaming
        
        % -----------------------------------------------------------------
        
        % Uncomment the sensor revision you have plugged in.
        %SensorRevision = 'SPCIMAGER_AA';
        SensorRevision = 'SPCIMAGER_AB';
        %SensorRevision = 'TACIMAGER_AA';
        
    end
    
    % The following properties are constant
    properties (SetAccess = private)
        
 
    end
    
    %% Events
    events
        ROIUpdate
    end
    
    %% Public Methods
    methods     
        % -----------------------------------------------------------------
        
        function obj = SPCIMAGERAA(ok_bitfile)
            

            [okComms bank] = ok_header_func(ok_bitfile);
            obj.SensorConnect(okComms, bank);
            
            %checkROI registers the addlistener to programme the OK and
            % update the handle statuobj.
            obj.checkROI(obj);
            
        end
        
        function delete ( obj )
            obj.SensorReset();
            obj.SensorDisconnect();
            
            ok_footer_func(obj.okComms);
            clear obj
        end
        % -----------------------------------------------------------------
        
        function SensorConnect (obj, okComms, bank)
            
            % Check obj not already connected.
            
            if(strcmp(obj.SensorStatus,'Connected'))
                disp(' *** WARNING: Sensor already connected!');
                return
            end
            
			obj.SensorStatus = 'Connected';  % Other allowed value is 'Disconnected'
            obj.SensorMode = 'Idle';
            
            
            % Attach OkComms and bank to object
            obj.okComms = okComms;
            obj.bank = bank;
            
            
           f = wireoutdata(obj.okComms,obj.bank, 'FIRMWARE_REVISION');
           disp([' * Firmware Revision: ' num2str(f)]);
         
           % Reset Chip 
           wireindata(obj.okComms,obj.bank,'SPCIMAGER_CHIP_RESET',1);
           
           % Ramp up operating voltages
		   obj.SensorStartUpVoltages (0.00) % Pause time between each ramp step
                       
           % Reset Off
           wireindata(obj.okComms,obj.bank,'SPCIMAGER_CHIP_RESET',0);


%            pause on
%            pause(1)
%            pause off
%            wireindata(obj.okComms,obj.bank,'SPCIMAGER_CHIP_RESET',1);
%            pause on
%            pause(1)
%            pause off
%            wireindata(obj.okComms,obj.bank,'SPCIMAGER_CHIP_RESET',0);           
                     
           % Set CDS correctly
           obj.SetCrowbar('On');
           
           % Set Up Digital Exposure Mode and PixelBit
           obj.SetExposures(1,1);
           
           % Power Up ADCs
           wireindata(obj.okComms,obj.bank,'ADC_PU',1);
		   
           % Programme Shift Register
           obj.SetTimeGateInput ('Bin A', 'ExtClk');
           obj.SetTimeGateInput ('Bin B', 'ExtClk');
           obj.SetExposureTime(obj.ExposureTime);
           
           obj.SetExposureMode(0);

           % Set ROI (RowMin, RowMax, ColMin, ColMax)
           obj.SetRegionOfInterest (obj.RowMin, obj.RowMax, obj.ColMin, obj.ColMax);
           
           % Set Pixel Reset Time in clock cycles (rolling_reset_time per row, global_reset_time)
           obj.SetResetTime(obj.RollingResetTime, obj.GlobalResetTime);
           
           % Set Analogue Column Scan Out Times
           obj.SetColumnScanOutTime (obj.ColumnScanOutTime, obj.ADC_Signal_Sample_Start, obj.ADC_Crowbar_Sample_Start);
           
           % Set CDS Timing
           obj.SetCDSTime (obj.CDSTime);
           
           %Set Dig TOF Ambient Rejection
           obj.SetDigitalTOFAmbientRejection(obj.DigitalTOFAmbientRejection);
           
           % Reset Output FIFO Just In Case!
           trigger(obj.okComms,obj.bank,'ADC_FIFO_RST');
           
           % Set Pulse Gen
           %obj.SetPulseGen(BinAPos1, BinAPos2, BinADAC, BinBPos1, BinBPos2, BinBDAC)
           
           % Sensor Revision Set
           obj.SetSensorRevision(obj.SensorRevision);
           
           % Set SensorStatus = 'Connected'
           disp(' * Connected to Sensor');
           
           %disp(' * Calibrating Sensor');
           %obj.SensorCalibrateResetLevel(1);
           
%            wireindata(obj.okComms,obj.bank,'SPCIMAGER_CHIP_RESET',0);
% %            pause on;
% %            pause(1)
% %            pause off;
% 
%            progDAC (obj.okComms, obj.bank, 'ProgResetDAC')
           trigger(obj.okComms,obj.bank,'PROG_CTRL_SR');
           
           disp(' * Ready for operation.');

        end
        
        % -----------------------------------------------------------------
        
        function ConnectCheck (obj)
            
            % Check obj not already connected.        
            if(strcmp(obj.SensorStatus,'Disconnected'))
                disp(' *** ERROR: Sensor not connected.');
                error('Sensor not connected.')
                return
            end
            
        end
        
        % -----------------------------------------------------------------        
        
        function SensorReset (obj)
            
            obj.ConnectCheck;
            
            % Pulse RSTN
            wireindata(obj.okComms,obj.bank,'SPCIMAGER_CHIP_RESET',1);           
            wireindata(obj.okComms,obj.bank,'SPCIMAGER_CHIP_RESET',0);
            
            disp(' * INFO: Sensor Reset - MATLAB Status will not match Sensor Status');
            
            obj.SensorMode = 'Idle';
        
        end
        
        % -----------------------------------------------------------------
        
        function SensorDisconnect (obj)
            
            % Check obj not already connected.
            if(strcmp(obj.SensorStatus,'Disconnected'))
                disp(' *** WARNING: Sensor already disconnected!');
                return
            end
            
            % Pulse RSTN low
			
            % Turn off operating voltages
            obj.SensorSwitchOffVoltages(0.01);
			
            % Set SensorStatus = 'Disconnected'
            disp(' * Disconnected from Sensor');
           obj.SensorStatus = 'Disconnected';  % Other allowed value is 'Connected'
           
           obj.SensorMode = 'Off';
        
        end
 
         % -----------------------------------------------------------------        
        
        function SetSensorRevision (obj, SensorRev_in)
            
            SensorRev_in_lower = lower(SensorRev_in);
            set = 1;
            
            if(strcmp(SensorRev_in_lower,'spcimager_aa'))
              SensorRev = 'SPCIMAGER_AA';
              set = 1;
            elseif(strcmp(SensorRev_in_lower,'spcimager_ab'))
              SensorRev = 'SPCIMAGER_AB';
              set = 0;
            elseif(strcmp(SensorRev_in_lower,'tacimager_aa'))
              SensorRev = 'TACIMAGER_AA';
              set = 0;
            else
               error(' Sensor Revision Not Regonised!')
            end
            
            obj.SensorRevision = SensorRev;
            
            % Pulse RSTN
            wireindata(obj.okComms,obj.bank,'SPCIMAGER_AA_TRUE_FALSE',set);           
            disp([' * Sensor Revision - ' SensorRev ' is selected by MATLAB.']);

        end       
        
        % -----------------------------------------------------------------
        % Initialise and Calibrate Reset Level
        
         function SensorCalibrateResetLevel (obj, imgs)
            
             oldVS = obj.VS;
             oldVG = obj.VG;
             oldExpTime = obj.ExposureTime;
             obj.SetVoltage('VS',0.2);
             obj.SetVoltage('VG',0);

             obj.SetExposureTime(0);
            disp(' * Capturing reset levels...');
            obj.SetExposureMode(8);

             
             
             for img = 1:imgs
                 if (img==1)
                     cumImg = obj.CaptureImage;
                 else
                     cumImg = cumImg + obj.CaptureImage;
                 end
             end
             
             cumImg = cumImg ./imgs;
             obj.FPNCorrection = cumImg - 8192;
             
             disp(' * Finished capture. Reset levels saved in object.FPNCorrection');
             obj.SetExposureMode(0);
             obj.SetVoltage('VS',oldVS);
             obj.SetVoltage('VG',oldVG);
             obj.SetExposureTime(oldExpTime);
        end
        
        
        % -----------------------------------------------------------------
        % Sensor Set Functions
        
        function  SetSensorMode (obj, status)
        
            switch status
                case 'Off'
                    
                    if(strcmp(obj.SensorStatus,'Connected'))
                        disp(' * ERROR: To disconnect use the SensorDisconnect function.');
                        disp(' *        SensorMode set to Idle');
                        obj.SensorMode = 'Idle';
                    else
                        obj.SensorMode = 'Off';
                        % Set Firmware Mode
                    end

                case 'Idle'
                    
                    obj.SensorMode = 'Idle';
                    % Set Firmware Mode
                    
                case 'Single Shot'
                    
                     obj.SensorMode = 'Single Shot';
                     % Set Firmware Mode

                case 'Continuous'
                    
                      obj.SensorMode = 'Continuous';
                      % Set Firmware Mode
                               
                otherwise
                    disp(' *** ERROR: Sensor status not must be Off, Idle, Single Shot, or Streaming.');
                    error('Sensor status input incorrect.')
                
            end
        
            returnMode = obj.SensorMode;
            
        end

        % -----------------------------------------------------------------
        
        function  SetGlobalReset (obj, status_in)
            
            status = lower(status_in);
            switch status
                case 'off'
                    
                wireindata(obj.okComms,obj.bank,'DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE',0);
                disp(' * Global reset for analogue exposures is off.');
                obj.GlobalReset = 'Off';
                
                case 'on'
                    
                wireindata(obj.okComms,obj.bank,'DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE',1);
                disp(' * Global reset for analogue exposures is on.');
                obj.GlobalReset = 'On';
                
                otherwise
                    disp(' *** ERROR: GlobalReset must be ON or OFF');
                    error('Sensor status input incorrect.')
                
            end

        end

        % -----------------------------------------------------------------
        
        function  SetResetTime (obj, rolling_reset_time, global_reset_time)
            
            
                if(rolling_reset_time < 16)
                    rolling_reset_time_set = 16;
                    disp(' * Info: Minimum CDS RST Timing is 16.');
                else
                    rolling_reset_time_set = rolling_reset_time;
                end
                
                if(global_reset_time < 3)
                    disp(' * Info: Minimum Global RST Timing is 3.');
                    global_reset_time_set = 3;
                else
                    global_reset_time_set = global_reset_time;
                end
                
                obj.RollingResetTime = rolling_reset_time_set;
                obj.GlobalResetTime = global_reset_time_set;
                
                wireindata(obj.okComms,obj.bank,'ROLLING_RESET_CYCLES',rolling_reset_time_set);
                wireindata(obj.okComms,obj.bank,'GLOBAL_RESET_CYCLES',global_reset_time_set);
                disp(' * Reset times are set.');
              
        end 
        
         % -----------------------------------------------------------------
         
        function  SetCDSTime (obj, cds_time)
            
                if(cds_time < 16)
                    cds_time_set = 16;
                    disp(' * Info: Minimum CDS Timing is 16.');
                else
                    cds_time_set = cds_time;
                end

                obj.CDSTime = cds_time_set;
                
                wireindata(obj.okComms,obj.bank,'CDS_BLK_AND_SIG_CYCLES',cds_time_set);
                disp(' * CDS Blk and Sig times are set.');
              
        end 
                % -----------------------------------------------------------------
        
        function  SetColumnScanOutTime (obj, ColumnScanOutTime_in, ADC_Signal_Sample_Start_in, ADC_Crowbar_Sample_Start_in)
            
            
                if(ColumnScanOutTime_in <= 30)
                    ColumnScanOutTime_set = 30;
                else
                    ColumnScanOutTime_set = ColumnScanOutTime_in;
                end
                
                if(ADC_Signal_Sample_Start_in <= 7)
                    ADC_Signal_Sample_Start_set = 3;
                else
                    ADC_Signal_Sample_Start_set = ADC_Signal_Sample_Start_in;
                end
                
                if(ADC_Crowbar_Sample_Start_in <= 15)
                    ADC_Crowbar_Sample_Start_set = 15;
                else
                    ADC_Crowbar_Sample_Start_set = ADC_Crowbar_Sample_Start_in;
                end
                                
                obj.ColumnScanOutTime = ColumnScanOutTime_set;
                obj.ADC_Signal_Sample_Start = ADC_Signal_Sample_Start_set;
                obj.ADC_Crowbar_Sample_Start = ADC_Crowbar_Sample_Start_set;
                
                wireindata(obj.okComms,obj.bank,'COLUMN_CYCLES_CROWBAR',obj.ColumnScanOutTime);
                wireindata(obj.okComms,obj.bank,'ADC_SIGNALS_START',obj.ADC_Signal_Sample_Start);
                wireindata(obj.okComms,obj.bank,'ADC_CROWBAR_SAMPLE_START',obj.ADC_Crowbar_Sample_Start);
                disp(' * Column scan out times are set.');
              
        end 
        
        % -----------------------------------------------------------------
        
        function SetDigitalTOFAmbientRejection(obj, status)
        
            if(strcmpi(status,'on'))
                obj.DigitalTOFAmbientRejection = 'On';
                wireindata(obj.okComms,obj.bank,'DIGITAL_TOF_AMBIENT_REJECTION_ENABLE',1);
                disp(' * Digital TOF Ambient Rejection Enabled.');
            elseif(strcmpi(status,'off'))
                obj.DigitalTOFAmbientRejection = 'Off';
                wireindata(obj.okComms,obj.bank,'DIGITAL_TOF_AMBIENT_REJECTION_ENABLE',0);
                disp(' * Digital TOF Ambient Rejection Disabled.');
            else
                disp(' * Error: Digital TOF Ambient Rejection status must be on or off.');
            end
            
        end
        % -----------------------------------------------------------------
        
        function [voltageSet] = SetVoltage (obj, voltageName_in, voltageValue)
            
            obj.ConnectCheck;
			
            voltageName = upper(voltageName_in);
            
			switch voltageName
                case 'DAC5'
                    obj.DAC5 = voltageValue;
                case 'DAC6'
                    obj.DAC6 = voltageValue;
				case 'VDDE'
					obj.VDDE = voltageValue;
				case 'V1V2'
					obj.V1V2 = voltageValue;
				case 'V3V3'
					obj.V3V3 = voltageValue;
                case 'VDDOPAMP'
					obj.VDDOPAMP = voltageValue;
				case 'V3V6'
					obj.V3V6 = voltageValue;
				case 'V2V7'
					obj.V2V7 = voltageValue;
				case 'VHV'
					obj.VHV = voltageValue;
				case 'VHV2'
					obj.VHV2 = voltageValue;
				case 'VG'
					obj.VG = voltageValue;
				case 'VS'
					obj.VS = voltageValue;
				case 'VQ'
					obj.VQ = voltageValue;
				case 'VREF'
					obj.VREF = voltageValue;	
                case 'IBIAS1'
					obj.IBIAS1 = voltageValue;
                case 'IBIAS2'
					obj.IBIAS2 = voltageValue;
                case 'ADCPWR'
					obj.ADCPWR = voltageValue;
				otherwise
					disp(' * ERROR: No Voltage Existobj. Check input.');
					return
			
            end
            
           voltageSet = 0;
           
            % Conversion for VHV and VHV2 and the remainder
           switch voltageName
				case 'VHV'
                    voltageSet =   uint16(voltageValue * (1000/7.4));
				case 'VHV2'
                    voltageSet =   uint16(voltageValue * (1000/7.4));
               otherwise
                   voltageSet =  uint16(voltageValue * (1000));
           end
            
            % Wire In 
            wireindata(obj.okComms,obj.bank,voltageName,voltageSet);
            % Prog DAC
            progDAC (obj.okComms, obj.bank, 'ProgResetDAC');
			
        end
        
        % -----------------------------------------------------------------
        
        function SetTestPad (obj, testpad, status)
            
            obj.ConnectCheck;
            ltp = lower(testpad);
            if(strcmp(ltp,'bin a'))
                tp = 'A';
            elseif (strcmp(ltp,'bin b'))
                tp = 'B';
            else
                disp(' * ERROR: testpad variable must equal Bin A or Bin B.');
                return
            end
            
            lst = lower(status);
            if(strcmp(lst,'enable'))
                st = 1;
            elseif (strcmp(lst,'disable'))
                st = 0;
            else
                disp(' * ERROR: status variable must equal Enable or Disable.');
                return
            end
            % Set test pads on or off
            % BinAOutput = 'Disable'; % Other option is 'Enable'
            % BinBOutput = 'Disable'; % Other option is 'Enable'
            

            %BinAOutput = 'Disable'; % Other option is 'Enable'
            
            % ENAOUT_PAD_EN
            % ENBOUT_PAD_EN
            
            % Trigger shift register write
            if (st == 1)
                disp([' * Test Pad for Bin ' tp ' is now enabled.']);
                
                if(strcmp(ltp,'bin a'))
                    obj.BinAOutput = 'Enabled';
                    wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINA_OUT_ENABLE',1);
                else
                    obj.BinBOutput = 'Enabled';
                    wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINB_OUT_ENABLE',1);
                end
                
            else
               disp([' * Test Pad for Bin ' tp ' is now disabled.']); 
               
                if(strcmp(ltp,'bin a'))
                    obj.BinAOutput = 'Disabled';
                    wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINA_OUT_ENABLE',0);
                else
                    obj.BinBOutput = 'Disabled';
                    wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINB_OUT_ENABLE',0);
                end
               
            end
            
            %BinAOutput = 'Disabled'; % Other option is 'Enabled'
            %BinBOutput = 'Disabled'; % Other option is 'Enabled'
            
            trigger(obj.okComms,obj.bank,'PROG_CTRL_SR');
            
        end
        
        % -----------------------------------------------------------------
        
        function SetTimeGateInput (obj, bin, input, offset_sel)
        %%     SetTimeGateInput (bin, input, offset_sel)
        % bin = 'Bin A' or 'Bin B'
        % input = 'PulseGen' or 'OptClk' or 'ExtClk'
        % offset_sel = 'High' or 'Low'
            obj.ConnectCheck;
            
            ltp = lower(bin);
            if(strcmp(ltp,'bin a'))
                tp = 'a';
            elseif (strcmp(ltp,'bin b'))
                tp = 'b';
            else
                disp(' * ERROR: Time gate Bin variable must equal Bin A or Bin B.');
                return
            end
            
            lst = lower(input);
            if(strcmp(lst,'pulsegen'))
                lt_sel = 0;
                ip_sel = 0;
                os_sel = 0;
            elseif (strcmp(lst,'optclk'))
                lt_sel = 1;
                ip_sel = 0;
                
                %        OptClkOffsetSel = 'Low'; % Other option is high.
                loff = lower(offset_sel);
                if(strcmp(loff,'low'))
                    os_sel = 0;
                elseif(strcmp(loff,'high'))
                    os_sel = 1;
                else
                    disp(' * ERROR: Offset_Sel variable must equal High or Low.');
                    return    
                end
                
            elseif (strcmp(lst,'extclk'))
                lt_sel = 0;
                ip_sel = 1;
                os_sel = 0;
            else
                disp(' * ERROR: Input variable must equal PulseGen, OptClk or ExtClk.');
                return
            end

            % Write optclk offset sel = os_sel
            
            % Bin A
            if(strcmp(tp,'a'))
                 
                % Write for BinA_LT_SEL, BinB_LT_SEL and BinA_InputSel, BinB_InputSel
                % BinA_LT_SEL, lt_sel
                % BinA_InputSel, ip_sel
                % Trigger shift register write
                
                if(strcmp(lst,'pulsegen'))
                    disp(' * Bin A Time Gate set to External Clock through Pulse Gen.');
                    wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINA_DELAYGEN_LT_SEL',0);
                    wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINA_INPUTSEL',0);
                    obj.BinAInputSel = 'PulseGen';
                elseif (strcmp(lst,'optclk'))
                    disp(' * Bin A Time Gate set to Optical Clock through Pulse Gen.');
                    wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINA_DELAYGEN_LT_SEL',1);
                    obj.BinAInputSel = 'OptClk';
                    if(os_sel)
                        disp(' * Optical Clock offset set high.');
                        wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINA_DELAYGEN_OFFSET_SEL',1);
                    else
                        disp(' * Optical Clock offset set low.');
                        wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINA_DELAYGEN_OFFSET_SEL',0);
                    end
                    
                else     
                    disp(' * Bin A Time Gate set to External Clock. Pulse Gen is bypassed.'); 
                    wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINA_INPUTSEL',1);
                    obj.BinAInputSel = 'ExtClk';
                end
              
             % Bin B   
             else             
                 
                % Write for BinA_LT_SEL, BinB_LT_SEL and BinA_InputSel, BinB_InputSel
                % BinB_LT_SEL, lt_sel
                % BinB_InputSel, ip_sel
                % Trigger shift register write
                
                if(strcmp(lst,'pulsegen'))
                    disp(' * Bin B Time Gate set to External Clock through Pulse Gen.');
                    wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINB_DELAYGEN_LT_SEL',0);
                    wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINB_INPUTSEL',0);
                    obj.BinBInputSel = 'PulseGen';
                elseif (strcmp(lst,'optclk'))
                    disp(' * Bin B Time Gate set to Optical Clock through Pulse Gen.');   
                    wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINB_DELAYGEN_LT_SEL',1);
                    obj.BinBInputSel = 'OptClk';
                    if(os_sel)
                        disp(' * Optical Clock offset set high.');
                        wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINB_DELAYGEN_OFFSET_SEL',1);
                    else
                        disp(' * Optical Clock offset set low.');
                        wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINB_DELAYGEN_OFFSET_SEL',0);
                    end
                    
                else     
                    disp(' * Bin B Time Gate set to External Clock. Pulse Gen is bypassed.');
                    wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINB_INPUTSEL',1);
                    obj.BinBInputSel = 'ExtClk';
                end
                
                
                
            end
            trigger(obj.okComms,obj.bank,'PROG_CTRL_SR');
        end
                
        % -----------------------------------------------------------------
        
        function SetRegionOfInterest (obj, RowMin, RowMax, ColMin, ColMax)
        %%Set Region of Interset     (RowMin, RowMax, ColMin, ColMax)
            obj.ConnectCheck;
            
            % Check Region of interest is in bounds
            if((RowMin > RowMax)||(ColMin > ColMax))
                disp('*** Error: Region of interest (ROI) must be set as RowMin, RowMax, ColMin, ColMax.');
                disp('***        ROI kept at previous values:');
                return
            end
            
            %Set obj Row/Col Min and Max
            obj.RowMin = RowMin;
            obj.RowMax = RowMax;
            
            obj.ColMin = ColMin;
            obj.ColMax = ColMax;
            
            wireindata(obj.okComms,obj.bank,'ROI_FIRST_ROW',RowMin);
            wireindata(obj.okComms,obj.bank,'ROI_FIRST_COL',ColMin);
            wireindata(obj.okComms,obj.bank,'ROI_LAST_ROW',RowMax);
            wireindata(obj.okComms,obj.bank,'ROI_LAST_COL',ColMax);            
            
            % Update handle status and programme Opal Kelly
            notify(obj,'ROIUpdate');
                        
        end
        
        % -----------------------------------------------------------------
        
        function [ActualExposureTime SPI_EXP_TIME ] = SetExposureTime (obj, timeInMicroSecs)
        %%  SetExposureTime  [ActualExposureTime SPI_EXP_TIME ] = SetExposureTime ( timeInMicroSecs)
            if (obj.ExposureMode == 3 || obj.ExposureMode == 6)
                clockfreq =  obj.DigClockFreq;
            else
                clockfreq =  obj.ClockFreq;
            end
           periodInMicroSecs = 1E6 * 1/clockfreq;
     
           % Time Codes
           minExposure = 0;
           maxExposure = (2^32)-20;
           
           inputTimeCode = round( (timeInMicroSecs / periodInMicroSecs));
           
           if(inputTimeCode < minExposure)
                
               inputTimeCode = minExposure;
               disp(' * WARNING: Min Exposure is 1 clock cycle. 0 Clock Cycles sets exposure with time gate disabled.')
               disp('            For lower exposure times use the on-chip pulse generators. ')
               
           elseif (inputTimeCode > maxExposure)
                   
               inputTimeCode = maxExposure;
              disp(' * WARNING: Max Exposure exceeded.')
           end
           
           % Old firmware
           %wireindata(obj.okComms,obj.bank,'EXPOSURE_TIME',inputTimeCode);
           inputTimeCode_LSB = bitand(uint32(65535), uint32(inputTimeCode));
           wireindata(obj.okComms,obj.bank,'EXPOSURE_TIME_LSB',inputTimeCode_LSB);
           inputTimeCode_MSB = uint16(bitshift(inputTimeCode,-16));
           wireindata(obj.okComms,obj.bank,'EXPOSURE_TIME_MSB',inputTimeCode_MSB);
           
           %Check data written:
           lsb_ret = wireoutdata(obj.okComms,obj.bank, 'EXPOSURE_TIME_LSB');
           msb_ret = wireoutdata(obj.okComms,obj.bank, 'EXPOSURE_TIME_MSB');
           
           if((inputTimeCode_MSB == msb_ret) && (inputTimeCode_LSB == lsb_ret))
          
                SPI_EXP_TIME = inputTimeCode;
                ActualExposureTime = (inputTimeCode) * periodInMicroSecs;
           
                
                obj.ExposureTime = ActualExposureTime;
                
           else
               
               SPI_EXP_TIME = inputTimeCode;
               ActualExposureTime = (inputTimeCode) * periodInMicroSecs;
               obj.ExposureTime = ActualExposureTime;
               
%                disp(['***********************************************']);
%                disp([' * FPGA WRITE ERROR: Exposure failed to write.']);
%                disp(['                     Sensor Object NOT updated.']);
%                disp(['***********************************************']);
           end
%           disp([' * Exposure set to ' num2str(ActualExposureTime) ' micro secs.']);
        end
        
        function [] = SetExposureMode (obj, Mode)
           obj.ExposureMode = Mode;
           wireindata(obj.okComms,obj.bank,'EXPOSURE_MODE',Mode);
           if(Mode == 7 || Mode == 6 || Mode == 3)
                obj.OutputMode = 'Digital';   
           else
                obj.OutputMode = 'Analogue';
           end
           disp([' * Mode set to ' num2str(Mode) ' - ' obj.OutputMode ' Readout Mode.']);

        end
        
        function [] = SetExposures (obj, NoOfExposures, PixelBit)
            wireindata(obj.okComms,obj.bank,'NO_OF_EXPOSURES',NoOfExposures);
            wireindata(obj.okComms,obj.bank,'DIGITAL_READOUT_PIXEL_BIT',PixelBit);
            obj.PixelBit = PixelBit;
            obj.NoOfExposures = NoOfExposures;
        end

        % -----------------------------------------------------------------
        
        function [] = SetCrowbar (obj, Status)
            if(strcmp(lower(Status),'on'))
                obj.Crowbar = 'On';
                wireindata(obj.okComms,obj.bank,'CDS_CROWBAR_DISABLE',0);
            else
                obj.Crowbar = 'Off';
                wireindata(obj.okComms,obj.bank,'CDS_CROWBAR_DISABLE',1);
            end
        end
        
        
        function [] = SetLED (obj, number)

                wireindata(obj.okComms,obj.bank,'OK_LEDs',number);

        end
        
        % -----------------------------------------------------------------
        
        function [ActualExposureTimeA ActualExposureTimeB] = SetPulseGen(obj, BinAPos1, BinAPos2, BinADAC, BinBPos1, BinBPos2, BinBDAC)
            
            wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINA_DELAYGEN_POS1', BinAPos1);
            wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINA_DELAYGEN_POS2', BinAPos2);
            wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINB_DELAYGEN_POS1', BinBPos2); % Keep this as Pos 2 in MATLAB
            wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINB_DELAYGEN_POS2', BinBPos1); % Keep this as Pos 1 in MATLAB
            wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINA_DELAYGEN_DAC', BinADAC);
            wireindata(obj.okComms,obj.bank,'SPCIMAGER_SPI_BINB_DELAYGEN_DAC', BinBDAC);            
            trigger(obj.okComms,obj.bank,'PROG_CTRL_SR');
            
            obj.BinAPos1 = BinAPos1;
            obj.BinAPos2 = BinAPos2;
        
            obj.BinBPos1 = BinBPos1;
            obj.BinBPos2 = BinBPos2;
        
            obj.BinADAC = BinADAC; % DAC Drive Setting
            obj.BinBDAC = BinBDAC; % DAC Drive Setting
            
            % Return exposure values
            ActualExposureTimeA = 0;
            ActualExposureTimeB = 0;
            
        end
        
        % -----------------------------------------------------------------
        % Image Capture Functions:
        
        % SINGLE_BIT_FIFO_OUT

        
        function [imageCaptured imagestream width height] = CaptureImage (obj)
           
            obj.ConnectCheck;
            
            % Check and then Set mode
            if (strcmp(obj.SensorMode, 'Single Shot') == 0)

                obj.SensorMode = 'Single Shot';
                
            end
            
            %disp(' * Capturing single frame.');
            
            % Reconstruct an image out of the image stream

            trigger(obj.okComms,obj.bank,'ADC_FIFO_RST');
            trigger(obj.okComms,obj.bank,'EXPOSURE_START_TRIGGER');

            
            %%
            
            height = obj.RowMax - obj.RowMin + 1;   
            width = obj.ColMax - obj.ColMin + 1;
            imagestream = zeros(1,width*height);
            imagestream  =  pipeoutdata(obj.okComms,obj.bank,'ADC_FIFO_OUT',width*height);
            max(imagestream);
            imageCaptured = rot90(reshape(imagestream,320,240));
            
%             if(strmatch(obj.OutputMode,'Analogue') == 1)
%                 imageCaptured = imageCaptured - obj.FPNCorrection;
%             end
        end
        
        % -----------------------------------------------------------------
        
        function [imageComposite] = GetSingleImage (obj)
           
            imageComposite = zeros(240,320);


           obj.SetRegionOfInterest (1, 240, 0, 319);
           [imageCaptured imagestream width height] = obj.CaptureImage;
            
            % FPN Correction is off
            imageComposite = imageCaptured;
            %imageComposite = imageCaptured - obj.FPNCorrection;
            
        end
        
        % Debug and Trial Functions
        function [imageCaptured] = GetTempImage (obj)

            obj.ConnectCheck;
            imagestream  =  blockpipeoutdata(obj.okComms,obj.bank,'ADC_FIFO_OUT',76800);% Read from FIFO
            imageCaptured = rot90(reshape(imagestream,320,240));
            
        end
        
        function [imagestream] = GetTempImageStream (obj)

            obj.ConnectCheck;
            imagestream  =  blockpipeoutdata(obj.okComms,obj.bank,'ADC_FIFO_OUT',76800);% Read from FIFO
            
        end
        % -----------------------------------------------------------------
        % Measurement Functions
        
        function [dcrMap] = MeasureDCR(obj, NumOfExposures, ExposureTimeInMicroSecs, VHV, VQ, VG, VS)
        %% Function to measure the DCR of the SPC Imager Sensor
        
        % Set Exposure Time
        obj.SetRegionOfInterest (0, 239, 0, 319);
        [exptime temp] = obj.SetExposureTime(ExposureTimeInMicroSecs);
        wireindata(obj.okComms,obj.bank,'DIGITAL_READOUT_PIXEL_BIT',1);
        wireindata(obj.okComms,obj.bank,'NO_OF_EXPOSURES',65535);        
        obj.SetExposureMode(6);
        
        % Set Voltages
        obj.SetVoltage('VHV',VHV);
        obj.SetVoltage('VQ', VQ);
        obj.SetVoltage('VG',VG);
        obj.SetVoltage('VS',VS);
        obj.SetVoltage('VREF',obj.VREF); 
        
        % Threshold DN for one count
        %thresh = 3000;
        
        countmap = zeros(240,320);
        
        for ep = 1:NumOfExposures
            
            datamap = obj.CaptureImage;

            % Convert datamap to known count values

            countmap = countmap + datamap;
            
        end
        
        % Normalise the dcr to one second
        normFactor = 1 / (65535 * NumOfExposures * exptime * 1E-6 );
        dcrMap = countmap .* normFactor;
        %dcrMap = countmap;
            
        end
        
        function [countmap] = GetDigitalImage(obj, NumOfExposures, ExposureTimeInMicroSecs, VHV, VQ, VG, VS, VREF)
        %% Function to measure the DCR of the SPC Imager Sensor
        
        % Set Exposure Time
        [exptime temp] = obj.SetExposureTime(ExposureTimeInMicroSecs);
        
        % Set Voltages
        obj.SetVoltage('VHV',VHV);
        obj.SetVoltage('VQ', VQ);
        obj.SetVoltage('VG',VG);
        obj.SetVoltage('VS',VS);
        obj.SetVoltage('VREF',VREF);
        
        obj.SetExposureMode(3);
        
        % Threshold DN for one count
        %thresh = 3000;
        
        countmap = zeros(240,320);

        obj.SetRegionOfInterest (1, 240, 0, 319);
        height = obj.RowMax - obj.RowMin + 1;
        width = obj.ColMax - obj.ColMin + 1;
           
        imagestream = zeros(1,width*height);
 
        trigger(obj.okComms,obj.bank,'ADC_FIFO_RST');
        trigger(obj.okComms,obj.bank,'EXPOSURE_START_TRIGGER');
 
        imagestream  = blockpipeoutdata(obj.okComms,obj.bank,'ADC_FIFO_OUT',width*height);% Read from FIFO
        
        x = 1;
        y = 1;
        
        for dn = 1:size(imagestream,2)
            str = dec2bin(imagestream(dn),16);
            for bit = 1:16
                countmap(x,y) = str2num(str(bit)) + countmap(x,y);

                if(y >= height) 
                   y = 1;
                   if(x >= width)
                       x = 1;
                   else
                    x = x + 1;
                   end
                else    
                   y = y + 1;
                end
                
            end
            
        end
        
        obj.SetExposureMode(0);    
        end
        
        % -----------------------------------------------------------------
        
        function [dcrMap] = TakeAJotImage(obj, NumOfExposures, ExposureTimeInMicroSecs, VHV, VQ, VG, VS)
        %% Function to measure the DCR of the SPC Imager Sensor
        
        % Set Exposure Time
        [exptime temp] = obj.SetExposureTime(ExposureTimeInMicroSecs);
        
        % Set Voltages
        obj.SetVoltage('VHV',VHV);
        obj.SetVoltage('VQ', VQ);
        obj.SetVoltage('VG',VG);
        obj.SetVoltage('VS',VS);
        
        % Threshold DN for one count
        %thresh = 3000;
        
        countmap = zeros(240,320);
        
        for ep = 1:NumOfExposures
            
            datamap = obj.GetSingleImage;

            % Threshold DN for one count
            thresh = 8192 + 100; % 8192 is the mid-point and allow for the outliers in offset
            
            
            % Convert datamap to known count values
            for x = 1:size(datamap,2)
                for y = 1:size(datamap,1)
                    
                    dn = datamap(y,x);
                    
                    % Threshold currently for one count
                    if (dn > thresh)
                        countmap(y,x) = countmap(y,x) + 1;
                    end
                    
                end
            end
            
        end
        
        % Normalise the dcr to one second
        normFactor = 1 / (NumOfExposures);
        dcrMap = countmap * normFactor;
        %dcrMap = countmap;
            
        end
        % -----------------------------------------------------------------
        
        function [imageFPNCorrection PPFPN_array imageVoltage avgImg FPNsigma] = MeasureFPN(obj, measureOrVerify, imageToolOpen, fftOpen, noOfExposures, crowbar, imageWidth, imageHeight)
        %% MeasureFPN - Function to measure the fixed pattern noise of the sensor.
        % measureOrVerify:  0 = verify, 1 = measure
        % imageToolOpen:  0 = do not open image tool, 1 = open image tool
            
            obj.SetExposureTime(0);
            obj.SetExposureMode(0);        
            wireindata(obj.okComms,obj.bank,'DIGITAL_READOUT_PIXEL_BIT',1);
            wireindata(obj.okComms,obj.bank,'NO_OF_EXPOSURES',1);
        
            % Exposure Modes
            % 0 = Regular Single Frame Exposure

            % 7 = Exposure Timing: Enable Low, Disbale High
            %     CDS Timing:  Normal
            %wireindata(s.okComms,s.bank,'EXPOSURE_MODE',7);

            % 8 = Exposure Timing: Normal
            %     CDS Timing:  CDSRST High during CDSSIG and CDSBLK
            %wireindata(s.okComms,s.bank,'EXPOSURE_MODE',8);

            % 15 = Exposure Timing: Enable Low, Disbale High
            %     CDS Timing:  CDSRST High during CDSSIG and CDSBLK
            %wireindata(s.okComms,s.bank,'EXPOSURE_MODE',15);
            
            % Crowbar Selection
            if(crowbar == 1)
                wireindata(obj.okComms,obj.bank,'CDS_CROWBAR_DISABLE',0);
            else
                wireindata(obj.okComms,obj.bank,'CDS_CROWBAR_DISABLE',1);
            end
            
            % -----------------------------------
            % Clear current FPN Correction
            if (measureOrVerify == 1)
                obj.FPNCorrectionMask = ones(imageHeight,imageWidth);
                obj.FPNCorrection = zeros(imageHeight,imageWidth);
            end

            disp('-----------------------------------------------')
            if (measureOrVerify == 1)
                disp(' * Starting FPN Measurement')
            else
                disp(' * Starting FPN Verification')
            end
            disp('-----------------------------------------------')



            testImg = zeros(noOfExposures,imageHeight,imageWidth);
            for exposure = 1:noOfExposures

                testImg(exposure, : , : ) = obj.GetSingleImage;
            end


            % Calculate average image
            avgImg = zeros(imageHeight,imageWidth);
            cumlativeImg = zeros(1,imageHeight,imageWidth);
            for exposure = 1:noOfExposures

                cumlativeImg = cumlativeImg(1, : , : ) + testImg(exposure, : , : );

            end

            for w = 1:imageWidth
                for h = 1:imageHeight
                
                     avgImg(h,w) = cumlativeImg(1,h,w) / noOfExposures;
                     
                end
            end
 
            % Calculate total FPN - is this really needed?
            FPN_data = reshape(avgImg,1,prod(size(avgImg)));
            FPNsigma = ConvertADCCodeToVoltage(8192+std(FPN_data),1);
            FPNsigmaFS = std(FPN_data)/8192;
            % Calculate VFPN and Scythe Data
            VFPN_data = zeros(imageWidth,1);

            for w = 1:imageWidth
                coldata = []; % Clear col data to no length
                tempcolindex = 1;
                for h = 1:imageHeight  
                    
                    if((obj.FPNCorrectionMask(h,w) == 1)) % Scythe data
                        
                        coldata(1,tempcolindex) = avgImg(h,w);


                    end
                    
                end
                % Calc VPFN data
                VFPN_data(w,1) = mean(coldata);
            end

            VFPNsigma = ConvertADCCodeToVoltage(8192+std(VFPN_data),1);
            VFPNsigmaFS = std(VFPN_data)/8192;

                  % Calculate VFPN and Scythe Data
            HFPN_data = zeros(imageHeight,1);

            for h = 1:imageHeight
                rowdata = []; % Clear col data to no length
                temprowindex = 1;
                for w = 1:imageWidth
                    
                    if((obj.FPNCorrectionMask(h,w) == 1)) % Scythe data
                        
                        rowdata(1,temprowindex) = avgImg(h,w);


                    end
                    
                end
                % Calc VPFN data
                HFPN_data(h,1) = mean(rowdata);
            end

            HFPNsigma = ConvertADCCodeToVoltage(8192+std(HFPN_data),1);
            HFPNsigmaFS = std(HFPN_data)/8192;
            
            % Calculate PPFPN correction matrix
            PPFPN_array = zeros(240,320);
            
            % Calculate PPFPN sigma
            temppixelindex = 1;
            PPFPN_data = [];           
            for w = 1:imageWidth            
                for h = 1:imageHeight  
                    
                    if((obj.FPNCorrectionMask(h,w) == 1)) % Scythe data
                        PPFPN_array(h,w) = avgImg(h,w) - VFPN_data(w,1);
                        PPFPN_data(1,temppixelindex) = avgImg(h,w) - VFPN_data(w,1);
                        temppixelindex = temppixelindex + 1; 
                    end
                    
                end
            end
            
            %PPFPN_data = reshape(PPFPN_array,1,prod(size(PPFPN_array)));
            PPFPNsigma = ConvertADCCodeToVoltage(8192+std(PPFPN_data),1);
            PPFPNsigmaFS = std(PPFPN_data)/8192;
            
            MaskSigma = std(PPFPN_data);
            MaskMean = mean(PPFPN_data);
            
            imageVoltage = ConvertADCCodeToVoltage( avgImg,1 );
            
            if (imageToolOpen == 1)
                imtool(imageVoltage)
            end
            
            if (measureOrVerify == 1)
                obj.FPNCorrection = PPFPN_array;
                imageFPNCorrection = obj.FPNCorrection;
                
                % Calculate scythe mask for image
                MaskThreshold = 5 * MaskSigma;
                deadpixels = 0;
                for w = 1:imageWidth            
                    for h = 1:imageHeight                
                        if((PPFPN_array(h,w) <= MaskMean + MaskThreshold) && (PPFPN_array(h,w) >= MaskMean - MaskThreshold))
                            obj.FPNCorrectionMask(h,w) == 1; % Keep Data
                        else
                            obj.FPNCorrectionMask(h,w) == 0; % Mask Data
                            deadpixels = deadpixels+1;
                        end
                    end
                end
                
                disp([' * Dead Pixels: ' num2str(deadpixels)]); 
                
                if (imageToolOpen == 1)
                    
                    figMask = figure;
                    imagesc(obj.FPNCorrectionMask);
                    
                    imtool(obj.FPNCorrection);
                end
                
                    if(fftOpen == 1)
                     % Show 2D FFT
                     hfft2d = vision.FFT;
                     hgs = vision.GeometricScaler('SizeMethod', 'Number of output rows and columns', 'Size', [240 320]);
                     x1 = step(hgs,imageFPNCorrection);
                     y = step(hfft2d, x1);
                     y1 = fftshift(double(y));
                     fig = figure;
                     imshow(log(max(abs(y1), 1e-6)),[]);
                     colormap(jet(64));
                     clear hfft2d;
                     clear hgs;
                    end
                     
                
            else
                imageFPNCorrection = avgImg;
                if (imageToolOpen == 1)
                    
                    % Show FPN
                    imtool(imageFPNCorrection);
                end   
                if(fftOpen == 1)
                    % Show 2D FFT
                     hfft2d = vision.FFT;
                     hgs = vision.GeometricScaler('SizeMethod', 'Number of output rows and columns', 'Size', [240 320]);
                     x1 = step(hgs,imageFPNCorrection);
                     y = step(hfft2d, x1);
                     y1 = fftshift(double(y));
                     fig = figure;
                     imshow(log(max(abs(y1), 1e-6)),[]);
                     colormap(jet(64));
                     
                     clear hfft2d;
                     clear hgs;
                end
                     
                
            end
            
            disp('-----------------------------------------------')
            if (measureOrVerify == 1)
                disp(' * Finished FPN Measurement')
            else
                disp(' * Finished FPN Verification')
            end
            
            disp([' * PPFPN 1 Sigma = ' num2str(PPFPNsigma) 'mV'])
            disp([' * VFPN 1 Sigma = ' num2str(VFPNsigma) 'mV'])
            disp([' * HFPN 1 Sigma = ' num2str(HFPNsigma) 'mV'])
            disp([' * All FPN 1 Sigma = ' num2str(FPNsigma) 'mV'])
            
            disp([' * PPFPN 1 Sigma = ' num2str(100*PPFPNsigmaFS) '%'])
            disp([' * VFPN 1 Sigma = ' num2str(100*VFPNsigmaFS) '%'])
            disp([' * HFPN 1 Sigma = ' num2str(100*HFPNsigmaFS) '%'])
            disp([' * All FPN 1 Sigma = ' num2str(100*FPNsigmaFS) '%'])
            disp('-----------------------------------------------')

            obj.SetExposureMode(0);
            
        end    
        
    end % Methods
    
    
    % -----------------------------------------------------------------
    % Private Methods        
    
    methods (Access = private)
        	
		function SensorStartUpVoltages (obj, pausetime)
		% Start Up Sequence for Sensor
		
        disp(' * Starting Up Power Supplies and Bias Voltages - In Progress');
        
		% Temporary value for VHV to hold on during sequence
		vhv_hold = 3.6;
		
		% ---------------------
        % Get Sensor final values to ramp up to.
		VDDEfinal = obj.VDDE;
        VDDOPAMPfinal = obj.VDDOPAMP;
        VREFfinal = obj.VREF;
        V1V2final = obj.V1V2;
        V3V3final = obj.V3V3;
        V3V6final = obj.V3V6;
        V2V7final = obj.V2V7;
        VHVfinal = obj.VHV;
        VHV2final = obj.VHV2;
        
		obj.SetVoltage ('ADCPWR', obj.ADCPWR);

        % Bias Voltages
        VGfinal = obj.VG;
        VSfinal = obj.VS;
        VQfinal = obj.VQ;
		
		% Calc max out of VHV1 and VHV2
		if (VHVfinal > VHV2final)
			VHVmax = VHVfinal;
		else
			VHVmax = VHV2final;
		end
		
		% Calc max out of VBIASes	
		if(VGfinal >= VSfinal)
			if(VGfinal >= VQfinal)
				VBIASmax = VGfinal;
			else
				VBIASmax = VQfinal;
			end
		else
			if(VSfinal >= VQfinal)
				VBIASmax = VSfinal;
			else
				VBIASmax = VQfinal;
			end
		end
		
		% ---------------------
		% Clear all voltages for initial setup
		
		obj.SetVoltage ('VDDE', 0);
		obj.SetVoltage ('V1V2', 0);
		obj.SetVoltage ('V3V3', 0);
		obj.SetVoltage ('V3V6', 0);
		obj.SetVoltage ('V2V7', 0);
		obj.SetVoltage ('VHV', 0);
		obj.SetVoltage ('VHV2', 0);
		obj.SetVoltage ('VQ', 0);
		obj.SetVoltage ('VS', 0);
		obj.SetVoltage ('VG', 0);
		obj.SetVoltage ('VREF', 0);
		obj.SetVoltage ('VDDOPAMP', 0);
        
		% ---------------------
		% Sequence:
		% - VHV above 3V3
		% - all internal voltages ramp up together
		% - VDDE ramps up
		% - Ramp VHV to operating voltage.
		% - Turn on Vg, Vs, Vq
		
		pause on;
		
		% 1 - VHV above 3V3
        
        % All voltage loops are written with steps of '1' not steps of
        % '0.1' as the for loop doesn't handle steps of '0.1' properly.
        % There are occasional errorobj.
        
		for mv = 0:1:(vhv_hold*10)
            vhv_cur = mv /10;
			obj.SetVoltage ('VHV', vhv_cur);
			obj.SetVoltage ('VHV2', vhv_cur);
			pause(pausetime);
			
		end
		
		% 2 - Internal voltages ramp up
		for mv = 0:1:36
    
            v_int = mv / 10;
		
			if (v_int <= V1V2final) 
				obj.SetVoltage ('V1V2',v_int);
			end
			
			if (v_int <= V3V3final) 
				obj.SetVoltage ('V3V3',v_int);
			end		

			if (v_int <= V2V7final) 
				obj.SetVoltage ('V2V7',v_int);
			end			

			if (v_int <= V3V6final) 
				obj.SetVoltage ('V3V6',v_int);
            end
            
			if (v_int <= VDDOPAMPfinal) 
				obj.SetVoltage ('VDDOPAMP',v_int);
            end	
            
			pause(pausetime);
			
		end
		
		% 3 - VDDE ramps up
		for mv = 0:1:(VDDEfinal*10)
            v_int = mv / 10;
			obj.SetVoltage ('VDDE',v_int);
			pause(pausetime);
		end
		
		% 4 - VHVs to operating voltage

		
		% 5 - Vq, Vg, Vs
		for mv = 0:1:(VBIASmax*10)
            v_int = mv / 10;
			if (v_int <= VQfinal) 
				obj.SetVoltage ('VQ',v_int);
			end			

			if (v_int <= VSfinal) 
				obj.SetVoltage ('VS',v_int);
			end

			if (v_int <= VGfinal) 
				obj.SetVoltage ('VG',v_int);
			end			
		
        end
        
        obj.SetVoltage ('VREF', VREFfinal);
        obj.SetVoltage('IBIAS2',obj.IBIAS2);
        obj.SetVoltage('IBIAS1',obj.IBIAS1);
        
        
        for mv = (10*vhv_hold):1:(10*VHVmax)
            v_int = mv /10;
		
			if (v_int <= VHVfinal) 
				obj.SetVoltage ('VHV',v_int);
			end	
			
			if (v_int <= VHV2final) 
				obj.SetVoltage ('VHV2',v_int);
			end	

			pause(pausetime);			
		
		end
				
		pause off;
        
        disp(' * Starting Up Power Supplies and Bias Voltages - Complete');

		end
		
		% -----------------------------------------------------------------
		
		function SensorSwitchOffVoltages(obj, pausetime)
            
        disp(' * Switching Off Power Supplies and Bias Voltages - In Progress');
		
				% Temporary value for VHV to hold on during sequence
		vhv_hold = 3.6;
		
		% ---------------------
        % Get Sensor current values to ramp from.
		VDDEcur = obj.VDDE;
        V1V2cur = obj.V1V2;
        V3V3cur = obj.V3V3;
        V3V6cur = obj.V3V6;
        V2V7cur = obj.V2V7;
        VHVcur = obj.VHV;
        VHV2cur = obj.VHV2;

        % Bias Voltages
        VGcur = obj.VG;
        VScur = obj.VS;
        VQcur = obj.VQ;
		
		% ---------------------
		% Sequence:
		% - Turn off Vg, Vs, Vq
		% - Ramp VHV down from operating voltage.
		% - VDDE ramps down
		% - all internal voltages ramp down together
		% - VHV ramps below 3V3

        % ADC Off
        obj.SetVoltage ('ADCPWR', 0);
        
		% 5 - Vq,Vs,Vg
		obj.SetVoltage ('VQ', 0);
		obj.SetVoltage ('VS', 0);
		obj.SetVoltage ('VG', 0);
		
		% 4 - VHV to holding voltage
        if(VHVcur > vhv_hold)
		for v_int = VHVcur:0.1:vhv_hold
			if (v_int <= VHV1final) 
				obj.SetVoltage ('VHV',v_int);
			end	
			pause(pausetime);			
        end
        end
		
        if(VHV2cur > vhv_hold)
		for v_int = VHV2cur:0.1:vhv_hold
			if (v_int <= VHV2final) 
				obj.SetVoltage ('VHV2',v_int);
			end	
			pause(pausetime);			
		end
        end
        
		%3 - VDDE
		obj.SetVoltage ('VDDE',0);
		
		%2 - Internal Voltages
        obj.SetVoltage ('VREF', 0);
		obj.SetVoltage ('VDDOPAMP', 0);
		obj.SetVoltage ('V3V3', 0);
		obj.SetVoltage ('V3V6', 0);
		obj.SetVoltage ('V2V7', 0);
		obj.SetVoltage ('V1V2', 0);
        obj.SetVoltage('IBIAS2',0)
        obj.SetVoltage('IBIAS1',0)
		
		%1 - Ramp Down VHV
		obj.SetVoltage ('VHV',0);
		obj.SetVoltage ('VHV2',0);
        
        disp(' * Switching On Power Supplies and Bias Voltages - Complete');
		
		end
		
		% -----------------------------------------------------------------
		
        function updateROIStatus (obj)
                % 'Dark SPC Row'
                % 'SPC'
                % 'TAC'
                % 'CP'
                %PixelsActive = 'SPC';
                
                if (obj.RowMin == 0)
                    obj.PixelsActive = 'Dark SPC Row';
                    %disp([' * Sensor SPC pixels are activated.']);
                elseif (obj.RowMin >= 1 && obj.RowMax <= 239)
                    obj.PixelsActive = 'SPC';
                elseif (obj.RowMin >= 240 && obj.RowMax <= 247)
                    obj.PixelsActive = 'TAC';
                elseif (obj.RowMin >= 248 && obj.RowMax <= 255)
                    obj.PixelsActive = 'CP';
                else
                    obj.PixelsActive = 'SPC';
                end
                
                %disp([' * Sensor ' obj.PixelsActive ' pixels are activated.']);
                
                %Programme Opal Kelly here
            end
        
    end
	
	
    
    % -----------------------------------------------------------------
    % Static / Private Methods     
    
    
    methods (Static,Access = private)
           
        function checkROI(obj)
            addlistener(obj,'ROIUpdate',...
                @(src,evnt)obj.updateROIStatus);
        end
        
        
    end
    
end

