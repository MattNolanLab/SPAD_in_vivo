function array = flatten (largeArray)
%Flatten data array

    % Flatten histogram
    s = size(largeArray);
    array = zeros((s(1)*s(2)),1);
    index = 0;
    for y=1:s(2)
        for x =1:s(1)
            index = index + 1;
            array(index) = largeArray(x,y);
        end
    end
    
end

