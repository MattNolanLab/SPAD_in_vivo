function pipedata = pipeoutdata (okComms, bank, pipename, blocksize)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
bankindex = 0;
pipedata = -1;

l = length(bank);

for x = 1:l
   
    if(strcmp(pipename, bank(x).name))
        bankindex = x;
        break
    end
end

% Check bank index was set
if (bankindex == 0)
   
    disp('Error : No pipe by that name exists')
    
else

    addr = uint16(hex2dec(bank(bankindex).addr));
    
    pipevalue = readfromblockpipeout(okComms, addr,32, blocksize*4);
    
    %pipevalue = readfromblockpipeout(okComms, addr, 16*2, blocksize*4, blocksize/8);
   
    %pipevalue = readfrompipeout(okComms, addr, blocksize*4, blocksize*4);
    
    pipevalue_adj = zeros(blocksize,1,'uint32');
    
    %pipedata=pipevalue;
    i = 1;
    for x=1:4:length(pipevalue)
        pipevalue_adj(i) = bitshift(uint32(pipevalue(x+3)),24)+bitshift(uint32(pipevalue(x+2)),16)+bitshift(uint32(pipevalue(x+1)),8) + uint32(pipevalue(x));
        i = i + 1;
    end
    
    pipedata = pipevalue_adj;

    
end
end

