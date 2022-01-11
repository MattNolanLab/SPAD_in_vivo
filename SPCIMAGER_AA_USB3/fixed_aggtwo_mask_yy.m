clear all
%addpath('Inpaint_nans')
blocksize=10000;%10000 blocks per seconds

summ_frame=zeros(240,320,'uint32');
no_background=1; % I modified--YIFANG,  original=0
no_signal=1;
noise_cancel=0;% original ==0
disp(['000 yifang']) ;
%% save background, only useful for triggered data
background=double(summ_frame)/(blocksize*no_background); 
%% create new folder for output image(not used)
% foldername = 'new20211013';        %I modified here--YIFANG
% mkdir(foldername)
% outputFileName= [foldername,'\output'];
%% 
in=1;
%background=0;%%yifang
no_signal=1;
bw_frame=zeros(1,blocksize*no_signal);

% for triggered sample
xxrange=125:200;
yyrange=71:131;

%for continuous sample cell_1
% xxrange=10:300;
% yyrange=10:220;

% % for continuous sample cell_2
% xxrange=239:282;
% yyrange=8:65;

% %for testing
% xxrange=1:240;
% yyrange=1:320;

bmask=zeros(240,320);
bmask(yyrange,xxrange)=1; %set mask to ROI

disp(['333 yifang']);

%cd 'C:\SPAD\SPADData\20220101\11_pink_TTL_18mA_1s'
cd 'C:\SPAD\SPADData\triggered_SPAD\real_data'
for co = 1:1;
   filename=['spc_data1.bin']; 
   %filename=['C:\SPAD\SPADData\continuous_SPAD\real_data\spc_data3.bin'];
   

    bcapture=0;
    summ=1;%adjust if necessary
    
    fileid=fopen(filename);
    tempdata=fread(fileid);
    fclose(fileid);
    ti=tempdata(1);%index of the exp
    yrange=tempdata(2);%240 or user defined
    gexp=tempdata(3);% global shutter or not
    data_dim=size(tempdata(4+yrange*10*8*(1-gexp)*(ti==1):end));
    %if it is not global shutter fisrt 19200 byte not count?
    
    data_size=data_dim(1)*data_dim(2);
    blocks=data_size/(9600*yrange/240); %blocksize, should equal to blocksize?
    tempdata=reshape(tempdata(4+yrange*10*8*(1-gexp)*(ti==1):end),data_size/blocks,blocks);
    
    fdata=yrange*320;
    n=1;
    kk=1;
    
    for cc=1:blocksize/summ,
        summ_frame=zeros(yrange,320,'uint32');
        
        for l=1+(cc-1)*summ:cc*summ,
            
            incr=0+(kk-1)*yrange*40:yrange*40*n-1+(kk-1)*yrange*40;
            a=de2bi(tempdata(1+incr,l),8);
            frame = reshape(a.',1,[]);
            for i=1:n,
                l_frame=frame(1+(i-1)*fdata:fdata+(i-1)*fdata);
                c_frame=uint32(rot90(reshape(l_frame,320,yrange)));
                bw_frame(in)=sum(c_frame(logical(bmask)),'all');
                in=in+1;
%                 imagesc(c_frame); % I uncomment here---YIFANG  
%                 drawnow;  % I uncomment here---YIFANG
                summ_frame=summ_frame+c_frame;
                
            end
        end;
        fpimage=double(summ_frame)/summ;
        cimage=log((1-background)./(1-fpimage));
        %cimage1=log((1-background)./(1-fpimage));
        if noise_cancel == 0
        cimage=fpimage-background*0;
        else
        cimage2=cimage;
        backk=background;
        backk(backk>0.2)=NaN;
        backk=-1*log((1 - backk));
        backkk=mean(backk(~isnan(backk)));
        cimage=(cimage+backkk);
        
        cimage(find(background>0.2))=NaN; %interpolate over outliers
        %cimage(find(cimage>0.2))=NaN;
        %cimage(find(cimage<0.01))=NaN;
        cimage=inpaint_nans(cimage,4); % I commented here--YIFANG
        end;
        
        cimage=uint16(cimage*summ);  % I commented this---YIFANG      
        % %to generate images
        %imwrite(cimage,[outputFileName,'_',num2str(co),'_',num2str(cc),'.tif'],'Compression','none');
        %imwrite(background,[outputFileName,'_',num2str(co),'_',num2str(cc),'.tif'],'Compression','none');
        cc;
        co;
        colormap('gray');
        
    end;
end;
%ROI

trace=bw_frame;
max_count=sum(bmask,'all');
trace_comp=-max_count*log(1-trace/max_count);

%keyboard;
trace_ref=reshape(trace,[blocksize,no_signal]);
%trace_av=mean(trace_ref,2);
figure;
plot(trace_ref);
%plot(trace_av);
a_meanCount=mean(trace_ref)
% y=lowpass(trace_av,1000,10000);
% plot(y);

% TO SAVE THE trace_ref file
save_mat_name = ['trace_ref.mat'];
save_csv_name = ['trace_ref.csv'];
csvwrite(save_csv_name, trace_ref)
save(save_mat_name,'trace_ref');
