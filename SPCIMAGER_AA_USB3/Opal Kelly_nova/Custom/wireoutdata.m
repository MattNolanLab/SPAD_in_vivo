function data = wireoutdata (okComms, bank, wirename )
% Parse register bank to get addr, size and starting bit from the bank
% Get data from that wireout and pass back

bankindex = 0;
data = -1;

l = length(bank);

for x = 1:l
   
    if(strcmp(wirename, bank(x).name))
        bankindex = x;
        break
    end
end

% Check bank index was set
if (bankindex == 0)
   
    disp('Error : No wire by that name exists')
    
else
    
    updatewireouts(okComms);
    
    addr = uint16(hex2dec(bank(bankindex).addr));
    readvalue = getwireoutvalue(okComms, addr);
    bs = bank(bankindex).bit * (-1);
    data = bitshift(readvalue,bs);
    
    % Write to log
    %sprintf('- Wireout %s is value %d', wirename, data)

end

end

