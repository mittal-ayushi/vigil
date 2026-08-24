#this sample can be used to clearly show the difference between enforce and monitor mode

echo "starting test"

# should get killed here if enforcement is on
cat /etc/shadow >/dev/null 2>&1

cat ~/.ssh/id_rsa >/dev/null 2>&1
/bin/sh -c 'echo child shell ran' >/dev/null 2>&1
touch /tmp/demo_scratch
rm -f /tmp/demo_scratch
(exec 3<>/dev/tcp/93.184.216.34/80) 2>/dev/null

echo "end"