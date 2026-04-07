Instructions to run monitoring program:

pip install -r requirements.txt

(make sure ssh server is installed to test ssh authentication alerts)

python train.py

sudo /home/ewadlei/syslogml-env/bin/python monitor.py

To test sudo authentication run commands with sudo ls with incorrect passwords. 
shh fakeuser@localhost multiple times to get alerts for ssh connections

sudo systemctl restart ssh to test Service Restart detection 

Can also run normal commands (ls, cd, pwd) to show no alerts show
