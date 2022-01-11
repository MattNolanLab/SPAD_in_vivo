
load ('C:\SPAD\SPADData\triggered_SPAD\real_data\trace_ref.mat');

% trace_temp = reshape(trace_ref,20,[]); %20 is bin size and you can change it.
% trace_binned=mean(trace_temp,1);
% trace_binned=transpose(trace_binned);% this is to transpose the result array, you can use it if you need
trace_binned = transpose(mean(reshape(trace_ref,20,[]),1));
plot(trace_binned);


% trace_raw=trace_ref;
% trace_binned_1 = calculate_bin_mean(trace_raw,20);
% 
% function trace_binned = calculate_bin_mean (trace_raw,bin_window)
% trace_temp=reshape(trace_raw,bin_window,[]); % reshape the trace to a M*binsize array
% trace_binned=mean(trace_temp,1); % mean the array for each column
% trace_binned=transpose(trace_binned);%transpose
% end



