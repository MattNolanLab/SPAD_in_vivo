trigger(evalin('base','s.okComms'), evalin('base','s.bank'),'ADC_FIFO_RST');
updatetriggerouts(evalin('base','s.okComms'));
while ~istriggered(evalin('base','s.okComms'), 96, 1),
    updatetriggerouts(evalin('base','s.okComms'));
    istriggered(evalin('base','s.okComms'), 96, 1)
    
end;