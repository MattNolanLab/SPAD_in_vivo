function MATLABSendMail(Person, StartTime, RunTime, Information)
% SENDMAIL :- A wrapper specifically for named user to use SendMail...

% Use: run function at the end of your Matlab simulation, or run when code
% reaches, 80%, 90%, 100% etc. Code will email you details of start time,
% finish time, run time, and the machine it was run on. 

% Extensions: the System.getProperties class is very powerful, as is the
% Matlab getenv function. For Start time, end time etc use the Matlab
% profiler (ie. tick and toc etc)

if (Person == 'Neale')
    MATLABSendMail_toNeale;
elseif (Person == 'Luca')
    MATLABSendMail_toLuca;
elseif (Person == 'Salvatore')
    MATLABSendMail_toSalvatore;
else
    disp('Error: Incorrect person idientifier in MATLAB Send Mail script');
    return
end


% Then this code will set up the preferences:
setpref('Internet','E_mail', myMail);
setpref('Internet','SMTP_Server', mySMTP);
setpref('Internet','SMTP_Username', myUsername);
setpref('Internet','SMTP_Password', myPass);

% Code to setup smtp sockets:
props = java.lang.System.getProperties;
props.setProperty('mail.smtp.auth','true');
props.setProperty('mail.smtp.socketFactory.class', ...
                  'javax.net.ssl.SSLSocketFactory');
props.setProperty('mail.smtp.socketFactory.port','465');

% Send email to my own GMail account:
if (computer == 'PCWIN')
    Machine = 'Local PC';
else
    Machine = getenv('HOSTNAME');
end

ST = ['Your MATLAB process started: ' num2str(StartTime) char(10)];
RT = [' Finished with a run time of: ' num2str(RunTime) char(10)];
Info = ['Machine: ' Machine char(10) 'Other Information: ' Information];

Subject = strcat('MATLAB Alert - Your MATLAB Process on :  ', Machine);
Message = strcat(ST,  ...
                RT, ...
                Info);
             
sendmail(myMail, Subject, Message)

disp(' * Alert mail sent.')

end