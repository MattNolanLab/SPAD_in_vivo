clc
clear all
close all

curdir = 'C:\Users\igyongy2\desktop\temp\'; % Make sure there is a trailing \

file = [curdir 'ProcessedData\edge'];
%%
mkdir([curdir 'ProcessedData'])

n=100;
fig1 = figure('Units','pixels','Position',[100 100 320 240]);
colormap(gray);
contrast = [0 n];
set(gca,'Position',[0 0 1 1])


writerObj2 = VideoWriter([file num2str(n) '.avi']);
writerObj2.FrameRate = 20;
open(writerObj2);


for k=1:88,
    
    k
    %load(['fall_edge_normaledge' num2str(21-k) '.mat'])
    load(['ultimasshedge' num2str(k) '.mat'])    
    tempdata=tempdata(33:end);

    
    % Total Frames
    frames=100;
    
    % Summing Up
    l=1;
    
    imagestream1 = zeros(2400*frames,1);
    i = 1;
    %for x=1:4:length(tempdata(:,l))
    for x=1:4:4*length(imagestream1)
        imagestream1(i) = bitshift(uint32(tempdata(x+3,l)),24)+bitshift(uint32(tempdata(x+2,l)),16)+bitshift(uint32(tempdata(x+1,l)),8) + uint32(tempdata(x,l));
        i = i + 1;
    end
    
    imagestream1=double(imagestream1);
        
    sum_frame=zeros(1,76800);

    incr=0:2400*n-1;
    a=de2bi(imagestream1(1+incr),32); %declare
    frame = reshape(a.',1,[]);
    for i=1:n,
        sum_frame=sum_frame+frame(1+(i-1)*76800:76800+(i-1)*76800);
    end
    
    re_frame=rot90(reshape(sum_frame,320,240));
    %com_frame(:,k)=re_frame(:,166);
    com_frame(:,k)=sum(re_frame(:,:),2);
    
    if k==1,
        save_frame=com_frame;
    end;
    %com_frame(:,k)=re_frame(:,166)./save_frame;
    
    %com_frame(:,k)=sum(re_frame(:,:),2)./save_frame;
    
    imagesc(fliplr(com_frame));
    
    %imagesc(re_frame);
    
    %frame = frame(1:76800);
    %colormap('default');
    %imagesc(rot90(medfilt2(reshape(sum_frame>10,320,240),[1 1]),3),[0 1]);
    
    
    set(gca, 'XTick', []);
    %box off
    %%M(k)=getframe(gcf);%-26
    
    gf = getframe(gcf);
    %        imwrite(gf.cdata,['frame' num2str(k) '.tiff'])
    writeVideo(writerObj2,gf)
end;
close(writerObj2)
