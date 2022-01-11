if(exist('chipstart') == 0)
    clear
      clc
else
    if (chipstart == 1)
        error('CHIP ALREADY ON!')
        return
    else
        clear
        clc
    end
end