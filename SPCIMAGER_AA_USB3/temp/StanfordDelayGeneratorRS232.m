classdef StanfordDelayGeneratorRS232 < handle
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
        function obj = StanfordDelayGenerator( PortName )
            % StanfordDelayGenerator create the object to control the delay
            % generator Stanford DG64 on the given PORTNAME serial port.
            obj.PSU_Model = 'Stanford DG645';
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
                        fprintf(1,'Wrong Class! Select StanfordDelayGeneratorTCPIP')
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
            obj.reset
            % put the system to local mode
            obj.remoteControlOff
            % close the connection with the power supply
            fclose(obj.serialCOM);
            % destruct the serial com
            delete(obj.serialCOM);
            clear obj.serialCOM
        end
        
        % -----------------------------------------------------------------
        
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
            fprintf(obj.serialCOM, 'SYST:REM');
        end

        function remoteControlOff ( obj )
            % REMOTECONROLOFF ends the remote control
            fprintf(obj.serialCOM, 'SYST:LOC');
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
            % DIRECTWRITE allows to write a string over the seria port.
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
        % Connect to power supply
        function connectSerial ( obj )
            if isempty(obj.COMPort)
                fprintf(1, '\nNo COM Port Specified\n');
            else
                % Create Serial Object
                obj.serialCOM = serial(obj.COMPort);
                % Load the driver (not really necessary)
                %obj.psuObj = icdevice (obj.psuDriver, obj.serialCOM);
                % Connect to delay gen
                fopen(obj.serialCOM);
            end
        end

        % -----------------------------------------------------------------
        function update ( obj )
            warning off
            fprintf ( obj.serialCOM, '*OPC?' );
            fprintf(1,' Waiting for messages:\n');
            reply = fscanf(obj.serialCOM);
            if strcmpi(reply,'')
                reply = ' - No reply\n';
            end
            fprintf(1,reply);
            warning on
        end
        % -----------------------------------------------------------------        
        % Start procedure, all voltages to 0
        function startup ( obj )
            obj.remoteControlOn
            obj.reset
        end
        % -----------------------------------------------------------------
    end
end