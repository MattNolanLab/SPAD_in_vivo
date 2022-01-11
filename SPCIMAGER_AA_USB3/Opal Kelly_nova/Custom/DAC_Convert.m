function DAC_Data = DAC_Convert( bank, wirename, voltage)


high_or_low = 0; % 1 for high, 0 for low

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
   
    disp('Error : No wire by that name exists')
    
else
    
    % Main code here
    if(strncmpi(bank(bankindex).name, 'VHV' , 3))
        high_or_low = 1;
    else
        high_or_low = 0;
    end
    
    if(high_or_low)
        DAC_Data = uint16(voltage * (1000/7.4));
    else
        DAC_Data = uint16(voltage * 1000);
    end
end

end

