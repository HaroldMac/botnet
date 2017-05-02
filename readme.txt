Botnet program in python for CPSC 526 Network security Systems.

Harold MacDonald
Partner Justin Currie Leslie


To run bot program, in terminal type:

./bot.py <host> <port #> <channel> <secret phase>

eg.
[hmacdona@zone44-ed as5]$ ./bot.py 199.116.235.44 12399 chancpsc526 violetsareblue

to run control, in terminal type:

./control.py <host> <port #> <channel> <secret phase>


example run of Control 

[hmacdona@zone44-ed as5]$ ./control.py 199.116.235.44 12399 chancpsc526 violetsareblue
Connecting to: 199.116.235.44
connected to server
command: status
Found 0 bots: 
command: violetsareblue
command: status
Found 1 bots: billyBotThorneton 
command: attack localhost 9999
total: 0 successful, 1 unsuccessful
failed billyBotThorneton
command: attack localhost 9999
total: 1 successful, 0 unsuccessful
successful billyBotThorneton
command: status
Found 1 bots: billyBotThorneton 
command: violetsareblue
command: status
Found 2 bots: EmmaBotson billyBotThorneton 
command: shutdown
Total bots shutdown: 2
Shutting down: EmmaBotson
Shutting down: billyBotThorneton

