function pipedata = blockpipeoutdata (okComms, bank, pipename, bsize, psize)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
bankindex = 0;
pipedata = -1;

if ~exist('psize', 'var') | isempty(psize), psize = bsize; end

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
    
    pipevalue =  readfromblockpipeout(okComms, addr, 32, bsize*2, bsize*2);
    
    pipevalue_adj = zeros((bsize),1);
    
    i = 1;
    for x=1:2:length(pipevalue)
        pipevalue_adj(i) = bitshift(uint16(pipevalue(x+1)),8) + uint16(pipevalue(x));
        i = i + 1;
    end
    
    pipedata = pipevalue_adj;
end
end

