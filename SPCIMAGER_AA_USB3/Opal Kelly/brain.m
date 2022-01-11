pathname='C:\Users\igyongy2\Desktop\CSS\Devices\SPCIMAGER_AA_USB3\Opal Kelly\2018_11_30_17_46_13\';
files = dir(pathname);
lresp=zeros(1000,100);
for i = 1:100,
filename=files(2+i).name;
fileid=fopen([pathname filename]);
%tempdata=uint8(fread(fileid));
tempdata=fread(fileid);
fclose(fileid);
ti=tempdata(1); 
yrange=tempdata(2);
gexp=tempdata(3);
data_dim=size(tempdata(4+yrange*10*8*(1-gexp)*(ti==1):end));
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
    lresp(l,i)=mean(double(frame));

end;
    plot(lresp(:,i))
    drawnow;
%lresp((lresp(:,i)>0.14),i)=mean(lresp(:,i));
disp(['file ', num2str(i) ,' completed']);
clear tempdata
end;
plot([0.1:0.1:100].',mean(lresp(:,:),2))
ylabel('Average pixel value');
xlabel('Time (ms)');