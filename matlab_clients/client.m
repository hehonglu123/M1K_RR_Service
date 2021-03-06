m1k_obj=RobotRaconteur.ConnectService('rr+tcp://localhost:11111?service=m1k');

%set mode for each channel
m1k_obj.setmode('A','SVMI');
m1k_obj.setmode('B','HI_Z');
periodvalue=100;
% m1k_obj.wave('A', 'sine', 0, 5, periodvalue, -(periodvalue / 4), 0.5);


t = 0:1/1e3:1;
y = 5.*double(chirp(t,0,1,50,'quadratic'));
m1k_obj.write('A',y');


samples=m1k_obj.read(int16(1000));
posixtime(datetime)-samples.timestamp
plot(samples.data(1:4:end))



% % streaming
% try
%     m1k_obj.StartStreaming();
% catch 
% end
% y=zeros(periodvalue);
% timestamp_seconds=0;
% timestamp_nano=0;
% % connnect to wire
% samples_wire=m1k_obj.samples.Connect();
% % plot
% h=plot(y,'YDataSource','y');
% while true
%     timestamp=samples_wire.LastValueReceivedTime;    
%     if timestamp_seconds==timestamp.seconds && timestamp_nano== timestamp.nanoseconds
%             continue
%     else
%         timestamp_seconds=timestamp.seconds;
%         timestamp_nano= timestamp.nanoseconds;
%         y=circshift(y,1);
%         sample=samples_wire.InValue;
%         y(1)=sample(1);
%         refreshdata(h,'caller') 
%         drawnow
%     end
% end
% 
% % stop streaming
% m1k_obj.StopStreaming();



