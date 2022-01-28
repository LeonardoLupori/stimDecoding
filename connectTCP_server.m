function tcp = connectTCP_server(IP, port)
% tcp = connectTCP_server(IP, port)
% 
% Function for creating a server for the Psychopy client to connect

fprintf(['Starting TCP/IP server on [Address: ' IP...
    ' - Port: %u]...'], port)
tcp = tcpip(IP, port,'NetworkRole', 'server');
fprintf('Server Ready!\n')