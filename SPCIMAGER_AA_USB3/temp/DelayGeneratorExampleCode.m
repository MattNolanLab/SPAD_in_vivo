%% Example code for the Stanford Delay Generator
% N Dutton 11th August

%Raw TCP/IP Object:
% dg = tcpip('192.168.0.2',5025)
% fopen(dg); % Open comms
% 
% fprintf(dg,'*RST'); % Reset box
% 
% fprintf(dg,'REMT') % Set Remote control
% fprintf(dg,'DLAY 2,0,10e-6') % Set 10us delay on edge A from edge T0
% %fscanf(dg,'EMAC?') % Do some kind of query
% fprintf(dg,'*OPC'); % Update comms
% fclose(dg); % Close comms
% clear dg % Clear object

% O/O Object
dg = StanfordDelayGeneratorTCPIP('TCPIP');

% See all options
dg

% Reset Delay Gen
% dg.reset;

% Set External Rising Edge Trigger
dg.SetTrigger('ExtRising')

% Two other options:
%dg.SetTrigger('ExtFalling')
%dg.SetTrigger('Internal')

%Set Negative Polarity on AB
dg.SetPolarity('AB','Negative')

%Set Positive Polarity on CD
dg.SetPolarity('CD','Positive')

% Set Delays on A and B
% dly = 55e-9;
 dly = 135e-9;
pw = 25e-9;

dg.SetDelay('A',dly)
dg.SetDelay('B',dly+pw)
dg.SetDelay('C',dly)
dg.SetDelay('D',dly+pw)

% Get Delay from Channel A
%dg.GetDelay('A')

% Disconnect Object
%clear dg