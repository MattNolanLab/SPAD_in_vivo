clearvars

Erange = logspace(log10(0.2),log10(200),20);
%Output name
% load back_l.mat
% load back_n.mat

%data bit-planes
ddir1='C:\Users\igyongy2\Desktop\CSS\Devices\SPCIMAGER_AA_USB3\Opal Kelly\1_off'; %path where files reside
%ddir1='C:\Users\igyongy2\Desktop\ulens\back_n'; %path where files reside
ddir2='C:\Users\igyongy2\Desktop\CSS\Devices\SPCIMAGER_AA_USB3\Opal Kelly\450_noulens'; %path where files reside
dfile='spc_data'; %name of the files (excluding the numbering)

%desired level of aggregation

%Process background files
for an = 1:1,
    an
for co = 18:18,
    co
    %open background file
    filename=[ddir1,'/',num2str(an),'_',num2str(co), 'spc_data', '1.bin'];
    fileid=fopen(filename);
    tempdata=fread(fileid);
    fclose(fileid);
    %read file header (containing index of file, frame size, shutter type),
    %ascertain data size (no of bitplanes in file), and reshape data into a
    %convenient form
    ti=tempdata(1); %index
    yrange=tempdata(2); %frame size (number of lines)
    gexp=tempdata(3); %1 for global shutter, 0 for rolling shutter
    data_dim=size(tempdata(4+yrange*10*8*(1-gexp)*(ti==1):end));
    data_size=data_dim(1)*data_dim(2);
    blocks=data_size/(40*yrange); %no of bit-planes in file
    tempdata=reshape(tempdata(4+yrange*10*8*(1-gexp)*(ti==1):end),data_size/blocks,blocks);
    fdata=yrange*320; %number of pixels in a frame
    
    %initialise sum
%     if co==1,
%         summ_frame_odd=zeros(yrange,320,'uint16');
%         summ_frame_even=zeros(yrange,320,'uint16');
%     end;
        
    summ_frame=zeros(yrange,320,'uint16');
    %decode every bit-plane (i.e. extract binary pixel values, and turn
    %them into an appropriately sized array), and add them to the sum
    for l=1:blocks,
        incr=1:yrange*40;
        a=de2bi(tempdata(incr,l),8);
        frame = reshape(a.',1,[]);
        l_frame=frame(1:fdata);
        c_frame=uint16(rot90(reshape(l_frame,320,yrange)));
%         if mod(l,2) == 1,
       summ_frame=summ_frame+c_frame;
%         else
%             summ_frame_even=summ_frame_even+c_frame;
%         end

       
    end
    back_nl=summ_frame;
  %  disp(['Processing background...',num2str(100*co/bnum),'% complete']);
end
end
%keyboard;

out_nl=zeros(1,20);
%Process background files
for an = 20:20,
    an
for co = 15:15,
    co
    %open background file
    filename=[ddir2,'/',num2str(an),'_',num2str(co), 'spc_data', '1.bin'];
    fileid=fopen(filename);
    tempdata=fread(fileid);
    fclose(fileid);
    %read file header (containing index of file, frame size, shutter type),
    %ascertain data size (no of bitplanes in file), and reshape data into a
    %convenient form
    ti=tempdata(1); %index
    yrange=tempdata(2); %frame size (number of lines)
    gexp=tempdata(3); %1 for global shutter, 0 for rolling shutter
    data_dim=size(tempdata(4+yrange*10*8*(1-gexp)*(ti==1):end));
    data_size=data_dim(1)*data_dim(2);
    blocks=data_size/(40*yrange); %no of bit-planes in file
    tempdata=reshape(tempdata(4+yrange*10*8*(1-gexp)*(ti==1):end),data_size/blocks,blocks);
    fdata=yrange*320; %number of pixels in a frame
    
    %initialise sum
%     if co==1,
%         summ_frame_odd=zeros(yrange,320,'uint16');
%         summ_frame_even=zeros(yrange,320,'uint16');
%     end;
        
    summ_frame=zeros(yrange,320,'uint16');
    %decode every bit-plane (i.e. extract binary pixel values, and turn
    %them into an appropriately sized array), and add them to the sum
    for l=1:blocks,
        incr=1:yrange*40;
        a=de2bi(tempdata(incr,l),8);
        frame = reshape(a.',1,[]);
        l_frame=frame(1:fdata);
        c_frame=uint16(rot90(reshape(l_frame,320,yrange)));
%         if mod(l,2) == 1,
       summ_frame=summ_frame+c_frame;
%         else
%             summ_frame_even=summ_frame_even+c_frame;
%         end
       c_frame(back_nl>570)=NaN;
       cf(l)=nanmean(c_frame(:)); 

    end
    summ_frame=single(summ_frame);
    summ_frame(back_nl>570)=NaN;
    o_frame=summ_frame(:,:);
    out_nl(an,co)=nanmean(o_frame(:)); 
    out_nls(an,co)=std(cf);  
  %  disp(['Processing background...',num2str(100*co/bnum),'% complete']);
end
end


% 
%Output name
% load back_l.mat
% load back_n.mat

%data bit-planes
ddir1='C:\Users\igyongy2\Desktop\CSS\Devices\SPCIMAGER_AA_USB3\Opal Kelly\lens_loff'; %path where files reside
%ddir1='C:\Users\igyongy2\Desktop\ulens\back_n'; %path where files reside
ddir2='C:\Users\igyongy2\Desktop\CSS\Devices\SPCIMAGER_AA_USB3\Opal Kelly\450_ulens'; %path where files reside
dfile='spc_data'; %name of the files (excluding the numbering)

%desired level of aggregation

%Process background files
for an = 1:1,
    an
for co = 18:18,
    co
    %open background file
    filename=[ddir1,'/',num2str(an),'_',num2str(co), 'spc_data', '1.bin'];
    fileid=fopen(filename);
    tempdata=fread(fileid);
    fclose(fileid);
    %read file header (containing index of file, frame size, shutter type),
    %ascertain data size (no of bitplanes in file), and reshape data into a
    %convenient form
    ti=tempdata(1); %index
    yrange=tempdata(2); %frame size (number of lines)
    gexp=tempdata(3); %1 for global shutter, 0 for rolling shutter
    data_dim=size(tempdata(4+yrange*10*8*(1-gexp)*(ti==1):end));
    data_size=data_dim(1)*data_dim(2);
    blocks=data_size/(40*yrange); %no of bit-planes in file
    tempdata=reshape(tempdata(4+yrange*10*8*(1-gexp)*(ti==1):end),data_size/blocks,blocks);
    fdata=yrange*320; %number of pixels in a frame
    
    %initialise sum
%     if co==1,
%         summ_frame_odd=zeros(yrange,320,'uint16');
%         summ_frame_even=zeros(yrange,320,'uint16');
%     end;
        
    summ_frame=zeros(yrange,320,'uint16');
    %decode every bit-plane (i.e. extract binary pixel values, and turn
    %them into an appropriately sized array), and add them to the sum
    for l=1:blocks,
        incr=1:yrange*40;
        a=de2bi(tempdata(incr,l),8);
        frame = reshape(a.',1,[]);
        l_frame=frame(1:fdata);
        c_frame=uint16(rot90(reshape(l_frame,320,yrange)));
%         if mod(l,2) == 1,
       summ_frame=summ_frame+c_frame;
%         else
%             summ_frame_even=summ_frame_even+c_frame;
%         end

       
    end
    back_l=summ_frame;
  %  disp(['Processing background...',num2str(100*co/bnum),'% complete']);
end
end
%keyboard;

out_l=zeros(1,20);
%Process background files
for an = 32:32,
    an
for co = 10:10,
    co
    %open background file
    filename=[ddir2,'/',num2str(an),'_',num2str(co), 'spc_data', '1.bin'];
    fileid=fopen(filename);
    tempdata=fread(fileid);
    fclose(fileid);
    %read file header (containing index of file, frame size, shutter type),
    %ascertain data size (no of bitplanes in file), and reshape data into a
    %convenient form
    ti=tempdata(1); %index
    yrange=tempdata(2); %frame size (number of lines)
    gexp=tempdata(3); %1 for global shutter, 0 for rolling shutter
    data_dim=size(tempdata(4+yrange*10*8*(1-gexp)*(ti==1):end));
    data_size=data_dim(1)*data_dim(2);
    blocks=data_size/(40*yrange); %no of bit-planes in file
    tempdata=reshape(tempdata(4+yrange*10*8*(1-gexp)*(ti==1):end),data_size/blocks,blocks);
    fdata=yrange*320; %number of pixels in a frame
    
    %initialise sum
%     if co==1,
%         summ_frame_odd=zeros(yrange,320,'uint16');
%         summ_frame_even=zeros(yrange,320,'uint16');
%     end;
        
    summ_frame=zeros(yrange,320,'uint16');
    %decode every bit-plane (i.e. extract binary pixel values, and turn
    %them into an appropriately sized array), and add them to the sum
    for l=1:blocks,
        incr=1:yrange*40;
        a=de2bi(tempdata(incr,l),8);
        frame = reshape(a.',1,[]);
        l_frame=frame(1:fdata);
        c_frame=uint16(rot90(reshape(l_frame,320,yrange)));
%         if mod(l,2) == 1,
       summ_frame=summ_frame+c_frame;
%         else
%             summ_frame_even=summ_frame_even+c_frame;
%         end
       c_frame(back_l>500)=NaN;
       cf(l)=nanmean(c_frame(:)); 

    end
    summ_frame=single(summ_frame);
    summ_frame(back_l>500)=NaN;
    o_frame=summ_frame(:,:);
    out_l(an,co)=nanmean(o_frame(:));  
    out_ls(an,co)=std(cf);
  %  disp(['Processing background...',num2str(100*co/bnum),'% complete']);
end
end
plot(Erange,out_nl(:,6)/1000,'-*');
hold on;
plot(Erange,out_l(:,6)/1000,'-+');
legend('no ulens','ulens');
ylabel('Bit density');
xlabel('Exposure (us)');
