function ledTest ( okComms, pausetime )
%LED Test to flash through all LEDs

mask = uint32(hex2dec('ffffffff'));
addr = uint16(0);
pause on
for v = 0:255
    value = uint32(v);
    setwireinvalue(okComms, addr, value, mask);
    updatewireins(okComms);
    pause(pausetime)
end
pause(1)

pause off


% off
    value = uint32(0);
    setwireinvalue(okComms, addr, value, mask);
    updatewireins(okComms);

end

