function varargout = DigitalDemo_fast(varargin)
% DigitalDemo_fast MATLAB code for DigitalDemo_fast.fig
%      DigitalDemo_fast, by itself, creates a new DigitalDemo_fast or raises the existing
%      singleton*.
%
%      H = DigitalDemo_fast returns the handle to a new DigitalDemo_fast or the handle to
%      the existing singleton*.
%
%      DigitalDemo_fast('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in DigitalDemo_fast.M with the given input arguments.
%
%      DigitalDemo_fast('Property','Value',...) creates a new DigitalDemo_fast or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before DigitalDemo_fast_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to DigitalDemo_fast_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help DigitalDemo_fast

% Last Modified by GUIDE v2.5 09-Sep-2015 15:35:12

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @DigitalDemo_fast_OpeningFcn, ...
    'gui_OutputFcn',  @DigitalDemo_fast_OutputFcn, ...
    'gui_LayoutFcn',  [] , ...
    'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before DigitalDemo_fast is made visible.
function DigitalDemo_fast_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to DigitalDemo_fast (see VARARGIN)

% Choose default command line output for DigitalDemo_fast
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes DigitalDemo_fast wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = DigitalDemo_fast_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% % hObject    handle to pushbutton1 (see GCBO)
% % eventdata  reserved - to be defined in a future version of MATLAB
% % handles    structure with handles and user data (see GUIDATA)
% imageCaptured = grabImage(hObject, eventdata, handles);
% %assignin('base','imageCaptured',imageCaptured);
% clear imageCaptured;
%
% function [imageCaptured] = grabImage(hObject, eventdata, handles)
% Setup

axes(handles.axes1);
h = text(0,-3,'Live Mode...','fontsize',10);
drawnow;
pause on
% framm=uint32(zeros(240,320));
while 1,
    
    g_back=evalin('base','g_back');
   % evalin('base','wireindata(s.okComms,s.bank,''DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE'',0)'); %forced gs
%     
    gexp=1;
    exptime=evalin('base','exptime');
    ttime=exptime + 0.32*(1-gexp);
    concat = ['s.SetExposureTime(' num2str(ttime) ');'];
    evalin('base',concat);
    if g_back == 1,
        n=evalin('base','n');
        
        %     concat = ['s.SetExposures(' num2str(n+2-gexp) ',1)'];
        concat = ['s.SetExposures(' num2str(n) ',1)'];
        evalin('base',concat);
        % y1=evalin('base','y1');
        % y2=evalin('base','y2');
        % yrange=(y2-y1)+1;
        %
        % concat = ['s.SetRegionOfInterest(' num2str(y1) ',' num2str(y2) ',0,319)'];
        concat = ['s.SetRegionOfInterest(1,240,0,319)'];
        evalin('base',concat);
        evalin('base','trigger(s.okComms, s.bank, ''ADC_FIFO_RST'')');
        evalin('base','trigger(s.okComms, s.bank, ''EXPOSURE_START_TRIGGER'')');
        
        % tempdata = readfromblockpipeout(evalin('base','s.okComms'),162,32,yrange*320*4);
        % pipevalue_adj = zeros(yrange*320,1,'uint16');
        
        tempdata = readfromblockpipeout(evalin('base','s.okComms'),162,32,240*320*4);
        pipevalue_adj = zeros(240*320,1,'uint16');
        i = 1;
        for x=1:4:length(tempdata)%33
            pipevalue_adj(i) = bitshift(uint32(tempdata(x+1)),8) + uint32(tempdata(x));
            i = i + 1;
        end
        sum_frame=pipevalue_adj;
        
        b_frame=sum_frame;
        assignin('base', 'b_frame', b_frame);
        assignin('base', 'g_back', 0);
        assignin('base', 'b_saved', 1);
    else
        n=evalin('base','n');
        
        concat = ['s.SetExposures(' num2str(n) ',1)'];
        evalin('base',concat);
        y1=evalin('base','y1');
        y2=evalin('base','y2');
        %         yrange=(y2-y1)+1;
        %
        %         concat = ['s.SetRegionOfInterest(' num2str(y1) ',' num2str(y2) ',0,319)'];
        concat = ['s.SetRegionOfInterest(1,240/y1,0,319)'];
        evalin('base',concat);
                
        evalin('base','wireindata(s.okComms,s.bank,''SPCIMAGER_CHIP_RESET'',1)');       
        pause(2e-4*n);
        evalin('base','wireindata(s.okComms,s.bank,''SPCIMAGER_CHIP_RESET'',0)');      
        evalin('base','trigger(s.okComms, s.bank, ''PROG_CTRL_SR'')');
%        pause(1);
        evalin('base','trigger(s.okComms, s.bank, ''ADC_FIFO_RST'')');
        evalin('base','trigger(s.okComms, s.bank, ''EXPOSURE_START_TRIGGER'')');
        
        tempdata = readfromblockpipeout(evalin('base','s.okComms'),162,32,(240/y1)*320*4);
        pipevalue_adj = zeros((240/y1)*320,1,'uint16');
        i = 1;
        for x=1:4:length(tempdata)%33
            pipevalue_adj(i) = bitshift(uint32(tempdata(x+1)),8) + uint32(tempdata(x));
            i = i + 1;
        end
        sum_frame=pipevalue_adj;
        
      colormap('default');
        
        b_saved=evalin('base','b_saved');
        
        if b_saved==1,
            b_frame=evalin('base','b_frame');
            %         imageCaptured=rot90(reshape(max(sum_frame-b_frame,0),320,yrange),1);
            %             rb=reshape(b_frame,320,240);
            %             imageCaptured=max(rot90(reshape(sum_frame,320,yrange)-rb(:,y1:y2),1),0);
            imageCaptured=rot90(reshape(max(sum_frame-b_frame,0),320,240),1);
        else
            imageCaptured=rot90(reshape(max(sum_frame,0),320,240/y1),1);
        end;
        %std(imagestream)
        
        %low = 0;
%         if n>1,
%         background=evalin('base','bframeee');
%   %      assignin('base', 'imageCaptured', imageCaptured);
%         imageCaptured=double(imageCaptured);
%         imageCaptured(background>100)=NaN;
%         imageCaptured=uint16(inpaint_nans(imageCaptured,4));
%         end
%         
        colormap('default');
        
        %contrast = [low high];
        %imagesc(imageCaptured, contrast)
        bright=evalin('base','bright');
        stop=evalin('base','stop');
        if stop ==1,
            assignin('base', 'stop', 0);
            break;
        end;
%         framm=framm+uint32(imageCaptured);
%         imagesc(framm);
        
        %imagesc(1,y1+2*0,fliplr(fliplr(imageCaptured(y1+2*0:y2,:))),[0 n/bright]);
        % %     x=['Total DC: ' num2str(sum(imageCaptured(:)))];
        % %     %x = sprintf(' %2d',name);
        % %     text(0,-3,x,'fontsize',10);
        %     %imagesc(1,1,imageCaptured)
        imagesc(1,1,imageCaptured);
        axis([0 320 0 240]);
        %h = text(0,-3,['Live Mode...'],'fontsize',10);
            h = text(0,-3,['Live Mode...', num2str(log10(1024*-log(1-median(single(imageCaptured(:)))/1024)))],'fontsize',10);%median
            %h = text(0,-3,'Live Mode...','fontsize',10);
        drawnow;
        
        axes(handles.axes3);
        histogram(double(imageCaptured),'Normalization','probability');
        
        xlim([0 n/bright]);
        drawnow;
        axes(handles.axes1);
        assignin('base', 'tempframe', imageCaptured);
        
        %    dnoise=median(imageCaptured(:));
        % %   dnoise=mean(imageCaptured(:)/(n*0.1e-6));
        % %    median(imageCaptured(:));
        %     concat = ['dnoise(' num2str(ti) ')=' num2str(dnoise) ';'];
        %     evalin('base',concat);
        % %    assignin('base', 'noise', imageCaptured(:));
        % % %    toc
% %         assignin('base', 'tempframe', framm);
        %evalin('base','framm=tempframe+framm');
    end;
end;
delete(h)
clear imageCaptured;


% --- Executes on button press in setup_button.
function df=setup_button_Callback(hObject, eventdata, handles)
% hObject    handle to setup_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

if(evalin('base','exist(''s'')') == 1)
    evalin('base','SensorStop');
    clear all;
    evalin('base','SensorStart');
else
    clear all;
    evalin('base','SensorStart');
end
evalin('base','SensorStart');

%     assignin('base', 'BinAPos1', 0);
%     assignin('base', 'BinAPos2', 20);%114/3 %118
%     assignin('base', 'BinBPos1', 0);
%     assignin('base', 'BinBPos2', 20);%122
%     assignin('base', 'BinADAC', 13);%13
%     assignin('base', 'BinBDAC',13);%13
%     evalin('base','s.SetPulseGen(BinAPos1, BinAPos2, BinADAC, BinBPos1, BinBPos2, BinBDAC);');
% 
%      evalin('base','s.SetTimeGateInput (''Bin A'', ''PulseGen'');');
%       evalin('base','s.SetTimeGateInput (''Bin B'', ''PulseGen'');');
% %      evalin('base','s.SetTimeGateInput (''Bin A'', ''OptClk'', ''High'');');
% %      evalin('base','s.SetTimeGateInput (''Bin B'', ''OptClk'', ''High'');');
%      evalin('base','wireindata(s.okComms,s.bank,''SPCIMAGER_SPI_BINA_INPUTSEL'',0);');
%      evalin('base','wireindata(s.okComms,s.bank,''SPCIMAGER_SPI_BINB_INPUTSEL'',0);');
%      evalin('base','wireindata(s.okComms,s.bank,''SPCIMAGER_SPI_BINA_OUT_ENABLE'',1);');
%      evalin('base','wireindata(s.okComms,s.bank,''SPCIMAGER_SPI_BINB_OUT_ENABLE'',1);');

%note: voltage settings are exposure dependent!
evalin('base','s.SetExposureMode(6);');
evalin('base','s.SetVoltage(''VG'',3.3);');%0.9,0.7 3.3!!! Try setting to 0.7V for HDR work
evalin('base','s.SetVoltage(''V3V3'',3.3);');%3.3
evalin('base','s.SetVoltage(''V2V7'',2.9);');%2.7 2.9!!!
evalin('base','s.SetVoltage(''V3V6'',3.6);');%3.6
% evalin('base','s.SetVoltage(''DAC6'',2.9);');%2.7
% evalin('base','s.SetVoltage(''DAC5'',3.6);');%3.6
evalin('base','s.SetVoltage(''VS'',0.1);'); %0.15 0.1!!!
evalin('base','s.SetVoltage(''VHV'',15.5);');%18 15.5!!!
evalin('base','s.SetVoltage(''VQ'',0.7);');%1!!
evalin('base','s.SetVoltage(''VREF'',1.2);'); %1.2 !!!
evalin('base','s.SetVoltage(''IBIAS2'',1.1);');%1.1
evalin('base','s.SetExposureTime(100.32);');
evalin('base','s.SetResetTime(20,100);');
assignin('base', 'gexp', 0); %start with rolling shutter
assignin('base', 'b_saved', 0);
assignin('base', 'g_back', 0);
assignin('base', 'exptime', 100);
assignin('base', 'bright', 1);
evalin('base','wireindata(s.okComms,s.bank,''DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE'',1)');
assignin('base', 'n', 1);
assignin('base','y1',1);
assignin('base','y2',240);
assignin('base', 'file_name', 'spc_data');
assignin('base','blocks',1);
assignin('base', 'bitplanes',1000);
assignin('base', 'stop', 0);
evalin('base','load(''bframeee'')');
%    timeout(evalin('base','s.okComms'),10);

evalin('base','wireindata(s.okComms,s.bank,''SPCIMAGER_CHIP_RESET'',1)');
pause on
pause(0.1);
evalin('base','wireindata(s.okComms,s.bank,''SPCIMAGER_CHIP_RESET'',0)');
evalin('base','trigger(s.okComms, s.bank, ''PROG_CTRL_SR'')');
%evalin('base','trigger(s.okComms, s.bank, ''PROG_CTRL_SR'')');

function df=popupmenu1_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenu1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupmenu1 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu1
contents = cellstr(get(hObject,'String'));
df = contents{get(hObject,'Value')};
assignin('base', 'n', str2double(df));
% concat = ['s.SetExposures(' df ',1)'];
% evalin('base',concat);

% --- Executes during object creation, after setting all properties.
function popupmenu1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenu1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in popupmenu5.
function popupmenu5_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenu5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupmenu5 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu5
contents = cellstr(get(hObject,'String'));
df = contents{get(hObject,'Value')};
switch df
    case 'Normal'
        evalin('base','s.SetVoltage(''VHV'',15.5);');
    case 'Low'
        evalin('base','s.SetVoltage(''VHV'',15);');
    case 'High'
        evalin('base','s.SetVoltage(''VHV'',16);');
end


% --- Executes during object creation, after setting all properties.
function popupmenu5_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenu5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
evalin('base','SensorStop');
delete(handles.figure1)

function edit1_Callback(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit1 as text
%        str2double(get(hObject,'String')) returns contents of edit1 as a double
df = str2double(get(hObject,'String'));
assignin('base', 'y1', df);

% --- Executes during object creation, after setting all properties.
function edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function edit2_Callback(hObject, eventdata, handles)
% hObject    handle to edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit2 as text
%        str2double(get(hObject,'String')) returns contents of edit2 as a double
df = str2double(get(hObject,'String'));
assignin('base', 'y2', df);

% --- Executes during object creation, after setting all properties.
function edit2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function edit3_Callback(hObject, eventdata, handles)
% hObject    handle to edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit3 as text
%        str2double(get(hObject,'String')) returns contents of edit3 as a double
df = get(hObject,'String');
assignin('base', 'file_name', df);

% --- Executes during object creation, after setting all properties.
function edit3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in popupmenu7.
function popupmenu7_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenu7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupmenu7 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu7
contents = cellstr(get(hObject,'String'));
df = contents{get(hObject,'Value')};
assignin('base', 'blocks', str2double(df));

% --- Executes during object creation, after setting all properties.
function popupmenu7_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenu7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

% --- Executes on selection change in popupmenu8.
function popupmenu8_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenu8 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns popupmenu8 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu8
contents = cellstr(get(hObject,'String'));
df = contents{get(hObject,'Value')};
assignin('base', 'bitplanes', str2double(df));

% --- Executes during object creation, after setting all properties.
function popupmenu8_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenu8 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton5.
function pushbutton5_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% % evalin('base','s.SetVoltage(''VREF'',1.4-(16-1)*0.014);');
% % %folder=[14 1386 1372];
% % 
% % % Vrange = [14.5:0.1:16.5];
% % % 
% % % for v=1:21,
% % % 
% % % evalin('base',['s.SetVoltage(''VHV'',',num2str(Vrange(v)),');']);
% % 

for v=1:40, %revise!

%Vrange = [12.6:0.2:13.4];
Vrange = [14:0.5:16];
for an=1:5,
evalin('base',['s.SetVoltage(''VHV'',',num2str(Vrange(an)),');']);
%%%%for an=1:41,
%     
Erange = logspace(log10(0.2),log10(200),20);
%Erange = logspace(log10(1),log10(1),20);
 

 
%evalin('base',['s.SetVoltage(''VHV'',',num2str(Vrange(v)),');']);
%2.54!!
%13.4!
format shortg
c = clock;
dirname=[num2str(c(1)),'_',num2str(c(2)),'_',num2str(c(3)),'_',num2str(c(4)),'_',num2str(c(5)),'_',num2str(floor(c(6)))];
%mkdir(dirname)
 
pause on;

blocks=evalin('base','blocks');
bitplanes=evalin('base','bitplanes');
file_name=evalin('base','file_name');
gexp=evalin('base','gexp');
concat = ['s.SetExposures(' num2str((blocks/blocks)*bitplanes+2*(1-gexp)) ',1)'];%1.9
evalin('base',concat)
n=num2str((blocks/blocks)*bitplanes+2*(1-gexp));

y1=evalin('base','y1');
y2=evalin('base','y2');
yrange=(y2-y1)+1;

concat = ['s.SetRegionOfInterest(' num2str(y1) ',' num2str(y2) ',0,319)'];
evalin('base',concat);

evalin('base','wireindata(s.okComms,s.bank,''DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE'',1-gexp)');

exptime=evalin('base','exptime');
ttime=exptime + 0.32*(1-gexp);
%ttime=Erange(v) + 0.32*(1-gexp);
concat = ['s.SetExposureTime(' num2str(ttime) ')'];
evalin('base',concat);

frames=bitplanes;%1600

%trigger(evalin('base','s.okComms'), evalin('base','s.bank'),'ADC_FIFO_RST');
%trigger(evalin('base','s.okComms'), evalin('base','s.bank'),'EXPOSURE_START_TRIGGER');
%pause(ttime/1e4);

for ti=1:blocks,
    tic
%      evalin('base','wireindata(s.okComms,s.bank,''SPCIMAGER_CHIP_RESET'',1)');       
%     pause(2e-4*n);
%     evalin('base','wireindata(s.okComms,s.bank,''SPCIMAGER_CHIP_RESET'',0)');      
%     evalin('base','trigger(s.okComms, s.bank, ''PROG_CTRL_SR'')');
    trigger(evalin('base','s.okComms'), evalin('base','s.bank'),'ADC_FIFO_RST');
    trigger(evalin('base','s.okComms'), evalin('base','s.bank'),'EXPOSURE_START_TRIGGER');
    %pause(ttime/1e6)
    
    
    % Grab Image
    %    tempdata = zeros(32+4*yrange*10*(frames+(1-gexp)),1,'uint8');
    %tempdata = evalin('base',['readfromblockpipeout(s.okComms, 163,16, 240*10*',num2str(frames),'*4)']);
    tempdata = readfromblockpipeout(evalin('base','s.okComms'),163,128,yrange*10*(frames+2*(ti==1)*(1-gexp))*4);

        
    %tempdata = readfromblockpipeout(evalin('base','s.okComms'),162,32,240*320*4);
    
%             pipevalue_adj = zeros(240*320,1,'uint16');
%         i = 1;
%         for x=1:4:length(tempdata)%33
%             pipevalue_adj(i) = bitshift(uint32(tempdata(x+1)),8) + uint32(tempdata(x));
%             i = i + 1;
%         end
%         sum_frame=pipevalue_adj;
%         imagesc(rot90(reshape(max(sum_frame,0),320,240),1));
       % drawnow;
    
    concat= [num2str(an) '_' num2str(v) file_name num2str(ti) '.bin'];
    %concat= [dirname '/' file_name num2str(ti) '.bin'];
    %    savefast(concat,'tempdata','yrange','gexp') %change!
    fileid = fopen(concat,'w'); %'a'
    fwrite(fileid,[ti;yrange;gexp;tempdata(:)]);
    fclose(fileid);
    %    averageTime = toc/frames
    clear tempdata
    toc
 end;
end;
keyboard;
end;
h = msgbox('Data Capture Complete');

% --- Executes on button press in pushbutton7.
function pushbutton9_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%uiopen('matlab');
[filename,pathname]=uigetfile;
fileid=fopen([pathname filename]);
%tempdata=uint8(fread(fileid));
tempdata=fread(fileid);
fclose(fileid);
ti=tempdata(1); 
yrange=tempdata(2);
gexp=tempdata(3);
data_dim=size(tempdata(4+yrange*10*8*(1-gexp)*(ti==1):end));

dname=evalin('base','dname');
data_size=data_dim(1)*data_dim(2);
blocks=data_size/(9600*yrange/240);
tempdata=reshape(tempdata(4+yrange*10*8*(1-gexp)*(ti==1):end),data_size/blocks,blocks);

%frames=blocks;
fdata=yrange*320;
n=1;
kk=1;
for l=1:blocks,
    % pipevalue_adj = zeros(yrange*10*frames,1,'uint32');
    % i = 1;
    % for x=1:4:length(tempdata(:,l))
    %     pipevalue_adj(i) = bitshift(uint32(tempdata(x+3,l)),24)+bitshift(uint32(tempdata(x+2,l)),16)+bitshift(uint32(tempdata(x+1,l)),8) + uint32(tempdata(x,l));
    %     i = i + 1;
    % end
    sum_frame=zeros(yrange,320,'uint8');
    incr=0+(kk-1)*yrange*40:yrange*40*n-1+(kk-1)*yrange*40;
    % a=de2bi(pipevalue_adj(1+incr),32); %declare
    a=de2bi(tempdata(1+incr,l),8); %declare
    frame = reshape(a.',1,[]);
    for i=1:n,
        %       c_frame = rot90(reshape(frame(1+(i-1)*fdata:fdata+(i-1)*fdata),320,yrange));
        %       sum_frame=sum_frame+c_frame;
        sum_frame=rot90(reshape(frame(1+(i-1)*fdata:fdata+(i-1)*fdata),320,yrange));
    end
    colormap('default');
    %imwrite(logical(sum_frame),[num2str(dname),'\image',num2str(ti),'_',num2str(l),'.tif'],'Compression','none');
    imwrite(uint8(sum_frame),[num2str(dname),'\image',num2str(ti),'_',num2str(l),'.tif'],'Compression','none');
    
    disp(['bit plane ', num2str(l) ,' completed']);
end;
clear tempdata
h = msgbox('Data Conversion Complete');

% --- Executes on button press in pushbutton9.
function pushbutton7_Callback(hObject, eventdata, handles)
dname = uigetdir('C:\');
assignin('base', 'dname', dname);
% hObject    handle to pushbutton9 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in togglebutton2.
function togglebutton2_Callback(hObject, eventdata, handles)
gexp=evalin('base','gexp');
assignin('base', 'gexp', 1-gexp);


% hObject    handle to togglebutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUI%DATA)

% 45ns for 63

% Hint: get(hObject,'Value') returns toggle state of togglebutton2


% --- Executes on selection change in popupmenu9.
function popupmenu9_Callback(hObject, eventdata, handles)
% hObject    handle to popupmenu9 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
contents = cellstr(get(hObject,'String'));
df = contents{get(hObject,'Value')};
assignin('base', 'bright', str2double(df));
% Hints: contents = cellstr(get(hObject,'String')) returns popupmenu9 contents as cell array
%        contents{get(hObject,'Value')} returns selected item from popupmenu9


% --- Executes during object creation, after setting all properties.
function popupmenu9_CreateFcn(hObject, eventdata, handles)
% hObject    handle to popupmenu9 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton11.
function pushbutton11_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton11 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
assignin('base', 'stop', 1);

% --- Executes on button press in pushbutton12.
function pushbutton12_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton12 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
assignin('base', 'g_back', 1);

function edit5_Callback(hObject, eventdata, handles)
% hObject    handle to edit5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit5 as text
%        str2double(get(hObject,'String')) returns contents of edit5 as a double
df = str2double(get(hObject,'String'));
assignin('base', 'exptime', df);

% --- Executes during object creation, after setting all properties.
function edit5_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
