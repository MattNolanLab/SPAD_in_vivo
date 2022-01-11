
clear all

SensorStart
vrefrange=0.5:0.1:1.5;
for t=1:11,
    
exps =200;%2020*10;
%exps = 2;
y1=1;
y2=240;
s.SetVoltage('VG',3.3);
s.SetVoltage('VS',0.1);
s.SetVoltage('VHV',15.5);
s.SetVoltage('VREF',vrefrange(t));%1.3 1
s.SetVoltage('IBIAS2',1.1);%1.3 1.1
%s.SetSensorRevision ('SPCIMAGER_AA');

s.SetVoltage('V3V3',3.3); %3.3
s.SetVoltage('V3V6',3.6); %3.6
s.SetVoltage('V5_SET',3.5);
s.SetVoltage('V2V7',2.7); % can be changed by 2.7+/- 0.2V

s.SetVoltage('VHV2',13);
s.SetVoltage('VQ',0.4);
s.SetExposureTime(1);
s.SetExposureMode(6);%6
s.SetResetTime(20,100);%20,100
%s.SetExposures(1,1);
wireindata(s.okComms,s.bank,'DEBUG_FORCE_GLOBAL_RESET_FOR_ANA_EXPOSURE',0);
% trigger(s.okComms,s.bank,'EXPOSURE_START_TRIGGER');
s.SetExposures(exps,1);
s.SetRegionOfInterest (y1, y2, 0, 319);

trigger(s.okComms, s.bank, 'PROG_CTRL_SR');
trigger(s.okComms,s.bank,'ADC_FIFO_RST');
trigger(s.okComms,s.bank,'EXPOSURE_START_TRIGGER');

yrange=(y2-y1)+1;
fdata=yrange*320;

frames=exps;%1600
blocks=1;%20;%16
n=100;%200;
kk=1;
tempdata=zeros(32+4*yrange*10*frames,blocks,'uint8');

%tempdata=zeros(4*2400*frames,1,'uint8');

% img_dump  =  pipeoutdata(s.okComms,s.bank,'ADC_FIFO_OUT',76800);
% imagesc(rot90(reshape(img_dump,320,240)));
% error

%load background.mat - 20us exp
%load 1mmpsglycerol20us_003.mat
% Asum=zeros(yrange,320,'uint32');
% pause on
% pause(2)
%timeout(s.okComms,10)
for l=1:blocks,
tic
%exacttime=clock;
tempdata(:,l) =  readfromblockpipeout(s.okComms, 163,32, 32+yrange*10*frames*4);
%tempdata(:,l) =  readfrompipeout(s.okComms, 163,2400*frames*4);
%tempdata =  readfromblockpipeout(s.okComms, 163,32, 2400*frames*4);
toc
end;
% load('image.mat');
% %tempdata(:,1)=image;
% tempdata=image.';
% 
% tempdata=reshape(tempdata,1600000/1000,1000);
% n=1;
% blocks=1000;
%----
tempdata=tempdata(33:end);
% % data_dim=size(tempdata);
% % data_size=data_dim(1)*data_dim(2);
% % blocks=data_size/(9600*yrange/240);
% % tempdata=reshape(tempdata,data_size/blocks,blocks);

for l=1:blocks,
pipevalue_adj = zeros(yrange*10*frames,1,'uint32');
i = 1;
for x=1:4:length(tempdata(:,l))
    pipevalue_adj(i) = bitshift(uint32(tempdata(x+3,l)),24)+bitshift(uint32(tempdata(x+2,l)),16)+bitshift(uint32(tempdata(x+1,l)),8) + uint32(tempdata(x,l));
    i = i + 1;
end
sum_frame=zeros(1,fdata,'uint32');
incr=0+(kk-1)*yrange*10:yrange*10*n-1+(kk-1)*yrange*10;
a=de2bi(pipevalue_adj(1+incr),32); %declare
frame = reshape(a.',1,[]);
for i=1:n,
      sum_frame=sum_frame+frame(1+(i-1)*fdata:fdata+(i-1)*fdata);
end
colormap('gray');

A=rot90(reshape(sum_frame,320,yrange));
%A(240,:)=100*A(240,:);
%A=reshape(sum_frame,320,yrange);
%A=[A(end,:);A(1:end-1,:)];

%Asum=Asum+A;
imagesc(A,[0 n]);
bitsum(t)=sum(sum(A))
%imagesc(Asum);
axis equal;
%imagesc(medfilt2(rot90(reshape(sum_frame,320,yrange))),[0 n]);
M(l)=getframe(gcf);
disp(['block ', num2str(l) ,' completed']);
end;
%---- 

end;
SensorStop
% figure;
% % plot(vrefrange,bitsum)
% % hold on
% tic
% %save('delfile.mat','-v7.3','tempdata')
% %save('delfile.mat','tempdata')
% savefast delfile.mat tempdata
% toc


