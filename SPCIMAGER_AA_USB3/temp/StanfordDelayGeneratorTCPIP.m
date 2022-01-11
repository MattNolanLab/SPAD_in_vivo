classdef StanfordDelayGeneratorTCPIP < handle
    %
    % edit: Luca Parmesan 08/11/2013
    
    %% Properties
    properties %(Access = private)
        EdgeA = '';
        EdgeB = '';
        EdgeC = '';
        EdgeD = '';
        EdgeE = '';
        EdgeF = '';
        EdgeG = '';
        EdgeH = '';
        DelayGen_Model = '';
        COMPort = '';
        psuObj;
        serialCOM;
    end
    %% Public Methods
    methods
        % Constructor
        function obj = StanfordDelayGeneratorTCPIP( PortName )
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
                        fprintf(1,'GPIB is not yet supported. If you have the time please write the interface!')
                    elseif strncmpi('TCPIP', PortName,3)
                        obj.connectTCPIP('192.168.0.2')
                    else
                        fprintf(1, '\nWarning: No Comms channel connected\n');
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
            
            disp('Delay Generator Disconnected')
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
                    chan_lut = 0;
            end
        end
        
        function SetDelay ( obj,chan,delay )
            chan_lut = obj.getChanNo(chan);
            delayStr = ['DLAY ' num2str(chan_lut),',0,',num2str(delay)];
            fprintf(obj.serialCOM, delayStr);
            dispStr = ['DISP 11,' num2str(chan_lut)];
            fprintf(obj.serialCOM, dispStr);
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
            delayStr = ['LPOL ' num2str(chan_lut),',',num2str(pol)];
            fprintf(obj.serialCOM, delayStr);
        end
        
        function SetTrigger ( obj,trig_in )
            trig = lower(trig_in);
            switch(trig)
                case 'int'
                    t = 0;
                case 'extrising'
                    t = 1;
                case 'extfalling'
                    t = 2;
                case 'ssrising'
                    t = 3;
                case 'ssfalling'
                    t = 4;
                case 'ss'
                    t = 5;
                case 'line'
                    t = 5;
                otherwise
                    t = 1;
            end
            
            dispStr = ['TSRC ' num2str(t)];
            fprintf(obj.serialCOM, dispStr);
            
        end
        
        function displayOn ( obj )
            % DISPLAYON enable the display
            fprintf(obj.serialCOM, 'DISPlay on');
        end
        
        function displayOff ( obj )
            % DISPLAYOFF disable the display
            fprintf(obj.serialCOM, 'DISPlay off');
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
            cmd = ['DISP:TEXT:CLEar'];
            fprintf ( obj.serialCOM, cmd );
        end
        
        function setOutputOn (obj)
            %setScreen allows the user to write to the power supply screen
            cmd = ['OUTPut ON'];
            fprintf ( obj.serialCOM, cmd );
        end
        
        function setOutputOff (obj)
            %setScreen allows the user to write to the power supply screen
            cmd = ['OUTPut OFF'];
            fprintf ( obj.serialCOM, cmd );
        end
        
        % -----------------------------------------------------------------
        function directWrite( obj, inputString )
            % DIRECTWRITE allows to write a string over the serial port.
            % USE IT ONLY FOR DEBUG
            fprintf ( obj.serialCOM, inputString );
        end
        
        function clearErrors ( obj )
            fprintf(obj.serialCOM, '*CLS');
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
                fprintf(1, '\nPort name must be string\n');
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