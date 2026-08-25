# VIGIL 

VIGIL is a tool that watches a program while it runs and tells you if it does something sketchy, eg : reading password files, touching ssh keys, opening a shell, or connecting to some network. 

It uses strace to peek at all the syscalls (basically every request a program makes to the operating system, eg : open this file, connect to this ip etc) then it checks each one against some rules . If a rule matches then it logs an alert... If you turn on enforce mode and the rule is a dangerous one, it'll kill the program right there..

It also tracks bursts so if the same bad thing keeps happening again and again in a short time, it will flag that as a burst instead of just spamming individual multiple alerts.

<img width="1915" height="851" alt="vigil" src="https://github.com/user-attachments/assets/85b1e821-e01e-40d7-94b8-c23c989ba4d5" />


## What it can catch

The stuff it looks for right now : 

* reading /etc/shadow or /etc/passwd (basically password files) 

* opening your ssh keys

* spawning a shell like /bin/sh or /bin/bash

* deleting files from /tmp 

* dns lookups and outgoing network connections 

# Two ways to run it  (Use Linux/WSL)

1) Through website (its easier and more visual) 

2) Through terminal (more raw but with more control) 

## Website way 
1) Compile the program
   gcc -o main main.c -Wall -Wextra
2) start the python server, this is what connects the website to the actual vigil program.

RUN : 'python3 server.py' 

this needs flask and flask_cors already installed (pip installed flask flask-cors)

3) Open index.html in your browser

4) Pick enforce or monitor mode using buttons 

5) upload a script (you can use MAINSAMPLE.sh from this repo to see it clearly or any one of the sample script)

6) Click scan script, it will take some time (around 2 minutes) to run and watch the script. 

7) You will see live feed showing every alert and burst as they happen, plus totla counts at top. 

## Terminal method 

First compile it 

'gcc -o main main.c -Wall -Wextra' 

Then run it pointing at whatever program you wanna watch 

'./main ./sample' 

If you want enforce mode on (so it kills the program directrly when it does something bad) add -k before the target 

'./main -k ./sample1'

there is also attach mode, where instead of launching a new program VIGIL can be pointed at a already running program using its pid..

'./main -p 1234'

This will print stuff live in ur terminal, alerts as they happen, and at the end a final report showing exit status and a count of every syscall it saw. 

It also writes everything in a file named alerts.json so it can be easier to analyse. 

## Note
You need strace installed on your machine for any of thisgit to work since thats what VIGIL runs on in reality.


You need strace installed on your machine for any of this to work since thats what VIGIL runs on in reality.
