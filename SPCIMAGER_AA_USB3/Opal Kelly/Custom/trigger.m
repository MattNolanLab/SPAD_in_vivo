function trigger (okComms, bank, ProgResetDACName)
% Toggle trigger

bankindex = 0;

l = length(bank);

for x = 1:l
   
    if(strcmp(ProgResetDACName, bank(x).name))
        bankindex = x;
        break
    end
end

% Check bank index was set
if (bankindex == 0)
   
    disp('Error : No wire by that name exists')
    
else

    addr = uint16(hex2dec(bank(bankindex).addr));
    bit = bank(bankindex).bit;
    % Trigger bit zero for programme / bit one for reset
    activatetriggerin(okComms, addr, bit);

end



end
