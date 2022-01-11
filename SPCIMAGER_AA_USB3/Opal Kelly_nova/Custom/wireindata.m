function wireindata (okComms, bank, wirename, data )
% Parse register bank to get addr, size and starting bit from the bank
% Get data from that wireout and pass back

bankindex = 0;

l = length(bank);

for x = 1:l
   
    if(strcmp(wirename, bank(x).name))
        bankindex = x;
        break
    end
end

% Check bank index was set
if (bankindex == 0)
   
    disp(['Error : No wire by that name exists - ' wirename])
    
else

    % If setting a data value to a bit not at zero then need to parse it
    % bit by bit.
    bit = bank(bankindex).bit;
    addr = uint16(hex2dec(bank(bankindex).addr));
   
    banksize = bank(bankindex).size;    
    sz = 2 ^ (banksize) - 1;
    mask = uint32(bitshift(sz,bit));
    d = bitshift(data,bit);
    setwireinvalue(okComms, addr, d, mask);
    updatewireins(okComms);
    
    % Write to log
    %sprintf('- Setting wirein %s to %d', wirename, data)
    
end




end