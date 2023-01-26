
dname = uigetdir('C:\');
filename=uigetfile;
fileid=fopen(filename);
tempdata=fread(fileid);
fclose(fileid);
yrange=tempdata(1); %ROI size (no of lines)
gexp=tempdata(2); %Global or rolling shutter
data_dim=size(tempdata(35+yrange*10*4*(1-gexp):end));

data_size=data_dim(1)*data_dim(2);
blocks=data_size/(9600*yrange/240);
tempdata=reshape(tempdata(4+start+yrange*10*4*(1-gexp):end),data_size/blocks,blocks);

frames=blocks;
fdata=yrange*320;
n=1;
for l=1:blocks,
sum_frame=zeros(yrange,320,'uint8');
incr=1:yrange*40*n;
a=de2bi(tempdata(incr,l),8);
frame = reshape(a.',1,[]);
for i=1:n,
        sum_frame=rot90(reshape(frame(1+(i-1)*fdata:fdata+(i-1)*fdata),320,yrange));
end
colormap('gray');
imwrite(logical(sum_frame),[num2str(dname),'\image_',num2str(l),'.tif'],'Compression','none');
disp(['bit plane ', num2str(l) ,' completed']);
end;
clear tempdata
h = msgbox('Data Conversion Complete');