cat > sample3.sh << 'EOF'
#!/bin/bash
cat /etc/shadow 2>/dev/null       # sensitive-file-read
cat ~/.ssh/id_rsa 2>/dev/null     # ssh-key-access
sh -c "echo hi"                   # shell-spawn
curl -s hackclub.com > /dev/null   # network-connect
rm -f /tmp/testfile.txt           # temp-file-delete
EOF