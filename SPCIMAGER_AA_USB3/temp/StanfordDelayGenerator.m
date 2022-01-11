classdef StanfordDelayGenerator < handle
    % N Dutton August 2014
    
    %% Properties
    properties %(Access = private)
        EdgeADelay = 0;
        EdgeBDelay = 0;
        EdgeCDelay = 0;
        EdgeDDelay = 0;
        EdgeEDelay = 0;
        EdgeFDelay = 0;
        EdgeGDelay = 0;
        EdgeHDelay = 0;
        PulseT0Polarity = 'Positive';
        PulseABPolarity = 'Positive';
        PulseCDPolarity = 'Positive';
        PulseEFPolarity = 'Positive';
        PulseGHPolarity = 'Positive';
        Triggering = 'Internal';
        DelayGen_Model = '';
        COMPort = 'COM1'; % Set COM port of your RS232 adaptor that the the delay generator is connected to.
        psuObj;
        serialCOM;
        ipAddr = '192.168.0.2'; % The IP address that is set on the delay generator.
    end
    %% Public Methods
    methods
        % Constructor
        function obj = StanfordDelayGenerator( PortName )
            % StanfordDelayGenerator create the object to control the delay
            % generator Stanford DG64 on the given PORTNAME serial port.
            obj.DelayGen_Model = 'Stanford DG645';
            switch nargin
                case 0
                    fprintf(1, '\nWarning: specify PortName\n');
                otherwise
                    if strncmpi('COM', PortName,3)
                        obj.set_COMport(PortName);
                        obj.connectSerial();
                    elseif strncmpi('GPIB', PortName,4)
                        error('Error: GPIB is not yet supported. If you have the time please write the interface!')
                    elseif strncmpi('TCPIP', PortName,3)
                        obj.set_COMport(PortName);
                        obj.connectTCPIP(obj.ipAddr)
                    else
                        fprintf(1, '\n * Warning: No Comms channel connected\n');
                    end
                    obj.startup()
            end
        end
        
        % Destructor
        function delete ( obj )
            % DELETE destroy the object closing the serial connection and
            % clearing the variable, may a instrreset is required
            %obj.reset
            % put the system to local mode
            obj.remoteControlOff
            % close the connection with the power supply
            fclose(obj.serialCOM);
            % destruct the serial com
            delete(obj.serialCOM);
            clear obj.serialCOM
            
            disp(' * Delay Generator Disconnected')
        end
        
        % -----------------------------------------------------------------
        function [chan_lut] = getChanNo(obj, chan)
            switch(chan)
                case 'T0'
                    chan_lut = 0;
                case 'T1'
                    chan_lut = 1;
                case 'A'
                    chan_lut = 2;
                case 'B'
                    chan_lut = 3;
                case 'C'
                    chan_lut = 4;
                case 'D'
                    chan_lut = 5;
                case 'E'
                    chan_lut = 6;
                case 'F'
                    chan_lut = 7;
                case 'G'
                    chan_lut = 8;
                case 'H'
                    chan_lut = 9;
                case 'AB'
                    chan_lut = 1;
                case 'CD'
                    chan_lut = 2;
                case 'EF'
                    chan_lut = 3;
                case 'GH'
                    chan_lut = 4;
                otherwise
                    error(['Channel does not exist:' chan])
                    chan_lut = 99;
            end
        end
        
        function SetDelay ( obj,chan,delay )
            
            % Set the object up.
            switch(chan)
                case 'T0'

                case 'T1'
                    
                case 'A'
                    obj.EdgeADelay = delay;
                case 'B'
                    obj.EdgeBDelay = delay;
                case 'C'
                    obj.EdgeCDelay = delay;
                case 'D'
                    obj.EdgeDDelay = delay;
                case 'E'
                    obj.EdgeEDelay = delay;
                case 'F'
                    obj.EdgeFDelay = delay;
                case 'G'
                    obj.EdgeGDelay = delay;
                case 'H'
                    obj.EdgeHDelay = delay;
                otherwise
                    error(['Edge does not exist. Please enter single edge only: A,B,C,D,E,F,G,H '])
            end
        
            % Set the delay on the box.
            chan_lut = obj.getChanNo(chan);
            delayStr = ['DLAY ' num2str(chan_lut),',0,',num2str(delay)];
            fprintf(obj.serialCOM, delayStr);
            
            % Change display on the box to match the channel
            dispStr = ['DISP 11,' num2str(chan_lut)];
            fprintf(obj.serialCOM, dispStr);
            
            disp([' * Delay edge ' chan ' set.']);
        end
        
        function [out] = GetDelay ( obj,chan)
            chan_lut = obj.getChanNo(chan);
            delayStr = ['DLAY? ' num2str(chan_lut)];
            out = fscanf(obj.serialCOM, delayStr);
            dispStr = ['DISP 11,' num2str(chan_lut)];
            fprintf(obj.serialCOM, dispStr);
        end
        
        function SetPolarity ( obj,chan,pol )   
            chan_lut = obj.getChanNo(chan);
            ptl = lower(pol);
            commTxt = num2str(0);
            if(strcmp(ptl,'positive'))
                commTxt = num2str(1);
            switch(chan)
                case 'T0'
                    PulseT0Polarity = 'Positive';
                case 'AB'
                    PulseABPolarity = 'Positive';
                case 'CD'
                    PulseCDPolarity = 'Positive';
                case 'EF'
                    PulseEFPolarity = 'Positive';
                case 'GH'
                    PulseGHPolarity = 'Positive';
                otherwise
                    error(['Polarity must be set on either T0,AB,CD,EF, or GH only. Invalid channel:' chan])
                    chan_lut = 99;
            end
            elseif(strcmp(ptl,'negative'))
                commTxt = num2str(0);
            switch(chan)
                case 'T0'
                    PulseT0Polarity = 'Negative';
                case 'AB'
                    PulseABPolarity = 'Negative';
                case 'CD'
                    PulseCDPolarity = 'Negative';
                case 'EF'
                    PulseEFPolarity = 'Negative';
                case 'GH'
                    PulseGHPolarity = 'Negative';
                otherwise
                    error(['Polarity must be set on either T0,AB,CD,EF, or GH only. Invalid channel:' chan])
                    chan_lut = 99;
            end
            else
                error('Polarity must be positive or negative.')
            end
            
            delayStr = ['LPOL ' num2str(chan_lut),',',commTxt];
            fprintf(obj.serialCOM, delayStr);
            
            disp([' * Pulse channel ' chan ' polarity set.'];
        end
        
        function SetTrigger ( obj,trig_in )
            trig = lower(trig_in);
            switch(trig)
                case 'int'
                    t = 0;
                    obj.Triggering = 'Internal';
                case 'extrising'
                    t = 1;
                    obj.Triggering = 'External Rising';
                case 'extfalling'
                    t = 2;
                    obj.Triggering = 'External Falling';
                case 'ssrising'
                    t = 3;
                    obj.Triggering = 'Single Shot Rising';
                case 'ssfalling'
                    t = 4;
                    obj.Triggering = 'Single Shot Falling';
                case 'ss'
                    t = 5;
                    obj.Triggering = 'Single Shot';
                case 'line'
                    t = 5;
                    obj.Triggering = 'Line';
                otherwise
                    t = 1;
                    error('Triggering must be set as internal,extrising,extfalling,ssrising,ssfalling,ss or line.')
            end
            
            dispStr = ['TSRC ' num2str(t)];
            fprintf(obj.serialCOM, dispStr);
            
            disp([' * Triggering set to ' obj.Triggering]);
            
        end
        
        function displayOn ( obj )
            % DISPLAYON enable the display
           %fprintf(obj.serialCOM, 'DISPlay on');
           disp('Not yet implemented.');
        end
        
        function displayOff ( obj )
            % DISPLAYOFF disable the display
            %fprintf(obj.serialCOM, 'DISPlay off');
            disp('Not yet implemented.');
        end
        
        function remoteControlOn ( obj )
            % REMOTECONTROLON give access to remote control
            fprintf(obj.serialCOM, 'REMT');
        end
        
        function remoteControlOff ( obj )
            % REMOTECONROLOFF ends the remote control
            fprintf(obj.serialCOM, 'LCAL');
        end
        
        function reset ( obj )
            % RESET reset the delay gen
            fprintf ( obj.serialCOM, '*RST' );
        end
        
        function setScreen (obj, text)
            %setScreen allows the user to write to the power supply screen
            cmd = ['DISP:TEXT "' text '"'];
            fprintf ( obj.serialCOM, cmd );
        end
        
        function clearScreen (obj)
            %setScreen allows the user to write to the power supply screen
            %cmd = ['DISP:TEXT:CLEar'];
            %fprintf ( obj.serialCOM, cmd );
            disp('Not yet implemented.');
        end
        
        function setOutputOn (obj)
            %setScreen allows the user to write to the power supply screen
            %cmd = ['OUTPut ON'];
            %fprintf ( obj.serialCOM, cmd );
            disp('Not yet implemented.');
        end
        
        function setOutputOff (obj)
            %setScreen allows the user to write to the power supply screen
            %cmd = ['OUTPut OFF'];
            %fprintf ( obj.serialCOM, cmd );
            disp('Not yet implemented.');
        end
        
        % -----------------------------------------------------------------
        function directWrite( obj, inputString )
            % DIRECTWRITE allows to write a string over the serial port.
            % USE IT ONLY FOR DEBUG
            fprintf ( obj.serialCOM, inputString );
            disp([' * Direct Write to Delay Generator: ' inputString]);
        end
        
        function clearErrors ( obj )
            fprintf(obj.serialCOM, '*CLS');
            disp(' * Errors Cleared.')
        end
    end
    %% Private methods
    methods (Access = private)
        % -----------------------------------------------------------------
        % Set COM port
        function set_COMport ( obj, PortName )
            if ischar(PortName)
                obj.COMPort = PortName;
            else
                fprintf(1, '\n * Port name must be string\n');
            end
        end
        % -----------------------------------------------------------------
        % Connect to delayGenerator
        function connectTCPIP ( obj,port )
            % Create Serial Object
            obj.serialCOM = tcpip(port,5025);
            % Load the driver (not really necessary)
            %obj.psuObj = icdevice (obj.psuDriver, obj.serialCOM);
            % Connect to delay gen
            fopen(obj.serialCOM);
            disp(' * Stanford DG645 delay generator TCPIP connection open.')
        end
        
        % -----------------------------------------------------------------
        % Connect to delay gen over 
        function connectSerial ( obj )
            if isempty(obj.COMPort)
                fprintf(1, '\n * Error: No COM Port Specified\n');
            else
                % Create Serial Object
                obj.serialCOM = serial(obj.COMPort);
                % Load the driver (not really necessary)
                obj.psuObj = icdevice (obj.psuDriver, obj.serialCOM);
                % Connect to PSU
                fopen(obj.serialCOM);
            end
        end
        
        % -----------------------------------------------------------------
        function update ( obj )
            warning off
            fprintf ( obj.serialCOM, '*OPC?' );
            %             fprintf(1,' Waiting for messages:\n');
            %             reply = fscanf(obj.serialCOM);
            %             if strcmpi(reply,'')
            %                 reply = ' - No reply\n';
            %             end
            %             fprintf(1,reply);
            %             warning on
        end
        % -----------------------------------------------------------------
        % Start procedure, all voltages to 0
        function startup ( obj )
            obj.remoteControlOn
            obj.reset
            disp('Delay Generator Connected')
        end
        % -----------------------------------------------------------------
    end
end