clear all;
SensorStart
exps = 1000;
s.SetVoltage('VG',3.3)
s.SetVoltage('VS',0.1)
s.SetVoltage('VHV',15.5)
s.SetVoltage('VREF',1)%1.3
s.SetVoltage('IBIAS2',1.1)

s.SetVoltage('V3V3',3.3) %3.3
s.SetVoltage('V3V6',3.6) %3.6
s.SetVoltage('V5_SET',3.5)
s.SetVoltage('V2V7',2.7); % can be changed by 2.7+/- 0.2V

s.SetVoltage('VHV2',13)
s.SetVoltage('VQ',1)
s.SetExposureTime(2);
s.SetExposureMode(6);%6
s.SetResetTime(20,100);%20,100
s.SetExposures(exps,1);

trigger(s.okComms, s.bank, 'PROG_CTRL_SR');
trigger(s.okComms,s.bank,'ADC_FIFO_RST');
trigger(s.okComms,s.bank,'EXPOSURE_START_TRIGGER');

frames=16;%1600
blocks=1;%16
n=16;
kk=1;

%tempdata=zeros(4*2400*frames,blocks,'uint32');
tempdata=zeros(4*2400*frames,1,'uint32');

% img_dump  =  pipeoutdata(s.okComms,s.bank,'ADC_FIFO_OUT',76800);
% imagesc(rot90(reshape(img_dump,320,240)));
% error

for l=1:blocks,
tempdata=zeros(4*2400*frames,1,'uint32');
trigger(s.okComms,s.bank,'ADC_FIFO_RST');
trigger(s.okComms,s.bank,'EXPOSURE_START_TRIGGER');

%tempdata(:,l) =  readfromblockpipeout(s.okComms, 163,32, 2400*frames*4);
tempdata =  readfromblockpipeout(s.okComms, 163,32, 32+2400*frames*4);
% load('image.mat');
% %tempdata(:,1)=image;
% tempdata=image.';

tempdata=tempdata(33:end);

%for l=1:blocks,
pipevalue_adj = zeros(2400*frames,1,'uint32');
i = 1;
for x=1:4:length(tempdata)
    pipevalue_adj(i) = bitshift(uint32(tempdata(x+3)),24)+bitshift(uint32(tempdata(x+2)),16)+bitshift(uint32(tempdata(x+1)),8) + uint32(tempdata(x));
    i = i + 1;
end
sum_frame=zeros(1,76800,'uint32');
incr=0+(kk-1)*2400:2400*n-1+(kk-1)*2400;
a=de2bi(pipevalue_adj(1+incr),32); %declare
frame = reshape(a.',1,[]);
for i=1:n,
      sum_frame=sum_frame+frame(1+(i-1)*76800:76800+(i-1)*76800);
end
colormap('gray');
%se = strel('square',1);
%imagesc(imerode(rot90(reshape(sum_frame,320,240)),se),[0 n]);
imagesc(rot90(reshape(sum_frame,320,240)),[0 n]);
M(l)=getframe(gcf);
disp(['block ', num2str(l) ,' completed']);
end;
%end
%SensorStop

