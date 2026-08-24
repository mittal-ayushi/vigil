# VIGIL 

VIGIL is a tool that watches a program while it runs and tells you if it does something sketchy, eg : reading password files, touching ssh keys, opening a shell, or connecting to some network. 

It uses strace to peek at all the syscalls (basically every request a program makes to the operating system, eg : open this file, connect to this ip etc) then it checks each one against some rules . If a rule matches then it logs an alert... If you turn on enforce mode and the rule is a dangerous one, it'll kill the program right there..

It also tracks bursts so if the same bad thing keeps happening again and again in a short time, it will flag that as a burst instead of just spamming individual multiple alerts. 

## What it can catch

The stuff it looks for right now : 

* reading /etc/shadow or /etc/passwd (basically password files) 

* opening your ssh keys

* spawning a shell like /bin/sh or /bin/bash

* deleting files from /tmp 

* dns lookups and outgoing network connections 

You can add your own rules yourself, because they just like in a simple list inside main.c , each rule has a name, the syscall to watch for, a bit of text to match in the args and whether it should be enforced (kill the program) or just log it. 

# Two ways to run it 

1) Through website (its easier and more visual) 

2) Through terminal (more raw but with more control) 

## Website way 

Demo Link: 

1) start the python server, this is what connects the website to the actual vigil program. 

RUN : 'python3 server.py' 

this needs flask and flask_cors already installed, and it needs the compiled main program sitting next to it 

2) Open index.html in your browser

3) Pick enforce or monitor mode using buttons 

4) upload a script (you can use MAINSAMPLE.sh from this repo to see it clearly or any one of the sample script)

5) Click scan script, it will take some time (around 2 minutes) to run and watch the script. 

6) You will see live feed showing every alert and burst as they happen, plus totla counts at top. 

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

You need strace installed on your machine for any of this to work since thats what VIGIL runs on in reality.