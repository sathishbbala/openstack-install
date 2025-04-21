
Install Openstack on a single VirtualBox VM 
===========================================
This README file has the installation steps to install openstack and deploy an app on the openstack instance provisioned. Multiple instances can be set up to deploy the application with changes to the Security Groups and Configuration files. This repository contains all files needed to install and to deploy an application on the openstack instance


A. Start a Ubuntu VM using VirtualBox with the following specifications and set up port forwarding rules. 
CPU - 4
Memory - 12G
Disk size - 60G
Network Adapter - NAT

Port Forwarding: 
<laptop-ip> Port 22/80/8080 -> 10.0.2.15 port 22/80/8080

B. Once the OS installation is completed, verify the interface, internet access, routing on the VM. 
**DO NOT run “sudo apt update && sudo apt upgrade” after the OS installation is successful**. This is not needed as openstack installation will update the packages as per the installation requirements. 
```

openstack@openstack:~$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:bf:7a:bf brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 metric 100 brd 10.0.2.255 scope global dynamic enp0s3
       valid_lft 86157sec preferred_lft 86157sec
    inet6 fd00::a00:27ff:febf:7abf/64 scope global dynamic mngtmpaddr noprefixroute
       valid_lft 86158sec preferred_lft 14158sec
    inet6 fe80::a00:27ff:febf:7abf/64 scope link
       valid_lft forever preferred_lft forever

openstack@openstack:~$ ip route
default via 10.0.2.2 dev enp0s3 proto dhcp src 10.0.2.15 metric 100
10.0.2.0/24 dev enp0s3 proto kernel scope link src 10.0.2.15 metric 100
10.0.2.2 dev enp0s3 proto dhcp scope link src 10.0.2.15 metric 100
10.0.2.3 dev enp0s3 proto dhcp scope link src 10.0.2.15 metric 100

openstack@openstack:~$ sudo iptables -t nat -L -n -v
[sudo] password for openstack:
Chain PREROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
```


C. Set up passwordless sudo for the openstack user (or the user that was created as part of the installation)
```
openstack@openstack:~$ cat /etc/sudoers.d/openstack
openstack ALL = (ALL) NOPASSWD: ALL

openstack@openstack:~$ sudo -l
Matching Defaults entries for openstack on openstack:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User openstack may run the following commands on openstack:
    (ALL : ALL) ALL
    (ALL) NOPASSWD: ALL
```

D. Setup the timezone using the timedatectl command
```
openstack@openstack:~$ timedatectl set-timezone Asia/Kolkata
==== AUTHENTICATING FOR org.freedesktop.timedate1.set-timezone ===
Authentication is required to set the system timezone.
Authenticating as:  (openstack)
Password:
==== AUTHENTICATION COMPLETE ===
openstack@openstack:~$ date
Wed Apr 16 04:04:57 PM IST 2025
openstack@openstack:~$ timedatectl
               Local time: Wed 2025-04-16 16:05:02 IST
           Universal time: Wed 2025-04-16 10:35:02 UTC
                 RTC time: Wed 2025-04-16 10:35:02
                Time zone: Asia/Kolkata (IST, +0530)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

E. Install openstack using devstack - Clone the devstack git repository 
```
openstack@openstack:~$ git clone https://opendev.org/openstack/devstack.git -b stable/2023.2
Cloning into 'devstack'...
remote: Enumerating objects: 51669, done.
remote: Counting objects: 100% (31301/31301), done.
remote: Compressing objects: 100% (10565/10565), done.
remote: Total 51669 (delta 30536), reused 20736 (delta 20736), pack-reused 20368
Receiving objects: 100% (51669/51669), 9.70 MiB | 2.48 MiB/s, done.
Resolving deltas: 100% (36683/36683), done.
```

F. Install openstack after creating the local.conf file in the devstack directory by running ./stack.sh. Look for the following message in the install log files to confirm the installation completed successfully. 
```
Installatoncompleted

This is your host IP address: 10.0.2.15
This is your host IPv6 address: fd00::a00:27ff:febf:7abf
Horizon is now available at http://10.0.2.15/dashboard
Keystone is serving at http://10.0.2.15/identity/
The default users are: admin and demo
The password: admin_123

Services are running under systemd unit files.
For more information see:
https://docs.openstack.org/devstack/latest/systemd.html

DevStack Version: 2023.2
Change: daa3ed62d38daadecfecccc022655deb65e81141 Update glance image size limit 2025-02-13 11:37:41 +0000
OS Version: Ubuntu 22.04 jammy
```

G. Check the openstack installation by logging into the horizon dashboard using admin/admin_123 as the credentials 

H. Check the openstack CLI using the following commands: 
```
openstack@openstack:~/devstack$ source ~/devstack/openrc admin admin
WARNING: setting legacy OS_TENANT_NAME to support cli tools.
openstack@openstack:~/devstack$ openstack network list
+--------------------------------------+---------+----------------------------------------------------------------------------+
| ID                                   | Name    | Subnets                                                                    |
+--------------------------------------+---------+----------------------------------------------------------------------------+
| 8570dc4d-ffb9-4769-af9c-432f8ecb9ad8 | public  | a9ce6785-2f33-4139-9eae-4c2c7e92363a, d385ce45-5d0a-408c-9c91-f87d39e04402 |
| 8cf92e46-6e2b-410a-9585-77e49f1a733f | private | 93f2a87a-3211-4be0-aa4a-25e73d34bacd, dc496aed-051a-48ae-b356-10d7434b8871 |
| baab45f1-77ad-4987-8dc9-d082666a76a3 | shared  | 831c9685-aedf-4634-b133-1094079606e2                                       |
+--------------------------------------+---------+----------------------------------------------------------------------------+
```

I. Ensure the mtu is set to 1400 across all networks. Openstack installation uses 1500 as the standard for MTU which sometimes can cause mismatch between networks leading to network packet drops or loss. 
```
sudo ip link set dev enp0s3 mtu 1400
sudo ip link set br-ex mtu 1400

Use the “ip addr show <device-name>"  to verify if the mtu is changed to 1400

-- set the mtu to 1400 for the public and private network created in openstack
openstack network set --mtu 1400 8570dc4d-ffb9-4769-af9c-432f8ecb9ad8
openstack network set --mtu 1400 8cf92e46-6e2b-410a-9585-77e49f1a733f

Use the openstack network show <network-id> to verify if the mtu is changed to 1400
```


J. Configure openstack 
Create custom flavor m1.custom from the horizon dashboard. (2vCPU/2GB Memory/3GB Root disk). 
```
openstack@openstack:~/devstack$ openstack flavor list
+--------------------------------------+-----------+-------+------+-----------+-------+-----------+
| ID                                   | Name      |   RAM | Disk | Ephemeral | VCPUs | Is Public |
+--------------------------------------+-----------+-------+------+-----------+-------+-----------+
| 1                                    | m1.tiny   |   512 |    1 |         0 |     1 | True      |
| 2                                    | m1.small  |  2048 |   20 |         0 |     1 | True      |
| 3                                    | m1.medium |  4096 |   40 |         0 |     2 | True      |
| 4                                    | m1.large  |  8192 |   80 |         0 |     4 | True      |
| 42                                   | m1.nano   |   128 |    1 |         0 |     1 | True      |
| 5                                    | m1.xlarge | 16384 |  160 |         0 |     8 | True      |
| 84                                   | m1.micro  |   192 |    1 |         0 |     1 | True      |
| c1                                   | cirros256 |   256 |    1 |         0 |     1 | True      |
| d1                                   | ds512M    |   512 |    5 |         0 |     1 | True      |
| d2                                   | ds1G      |  1024 |   10 |         0 |     1 | True      |
| d3                                   | ds2G      |  2048 |   10 |         0 |     2 | True      |
| d4                                   | ds4G      |  4096 |   20 |         0 |     4 | True      |
| e0253ea3-58c5-4202-b131-4fdb7d981dd1 | m1.custom |  2048 |    3 |         0 |     2 | True      |
+--------------------------------------+-----------+-------+------+-----------+-------+-----------+
```

K. Upload the debian generic cloud image into glance. 
```
wget https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-genericcloud-amd64.qcow2
openstack image create "Debian" --file debian-11-genericcloud-amd64.qcow2 --disk-format qcow2 --container-format bare --public
```

L. Add ssh, http, and TCP/8080 ingress rules in the default security group using the horizon dashboard.
```
openstack@openstack:~/devstack$ openstack security group rule list | egrep '22:|80:|8080:'
| 29f288b2-0b92-49da-b4fd-01ea34278a51 | tcp         | IPv4      | 0.0.0.0/0 | 80:80      | ingress   | None                                 | None                 | 930d3197-a2f1-41df-b4ab-85321027c025 |
| b8047bc3-d0f2-4c00-bcca-4885a4200d39 | tcp         | IPv4      | 0.0.0.0/0 | 8080:8080  | ingress   | None                                 | None                 | 930d3197-a2f1-41df-b4ab-85321027c025 |
| ccd3d3a0-47e7-4fef-9638-685dc5125ca2 | tcp         | IPv4      | 0.0.0.0/0 | 22:22      | ingress   | None                                 | None                 | 930d3197-a2f1-41df-b4ab-85321027c025 |
```

M. Create a key pair “DemoKeyPair” that will be used when provisioning an openstack instance. Use the Horizon dashboard to create the keypair. Download the private key and store it in the .ssh directory under devstack user as "demokeypair.pem". Use chnod to set the file permissions to 0400 for the private key. 
```
openstack@openstack:~/.ssh$ pwd
/home/openstack/.ssh
openstack@openstack:~/.ssh$ ls -al demokeypair.pem
-r-------- 1 openstack openstack 1675 Apr 16 17:05 demokeypair.pem
openstack@openstack:~/.ssh$ openstack keypair list
+-------------+-------------------------------------------------+------+
| Name        | Fingerprint                                     | Type |
+-------------+-------------------------------------------------+------+
| DemoKeyPair | 91:f6:2d:ed:99:fd:2e:af:7c:77:f5:23:b0:92:51:a9 | ssh  |
+-------------+-------------------------------------------------+------+
```

N. Provision a openstack instance using debian image and associate a floating IP address to the instance using the horizon dashboard.
```
openstack@openstack:~/.ssh$ openstack server list
+--------------------------------------+---------+--------+----------------------------------------------------------------------+--------+-----------+
| ID                                   | Name    | Status | Networks                                                             | Image  | Flavor    |
+--------------------------------------+---------+--------+----------------------------------------------------------------------+--------+-----------+
| b75d6b11-54eb-40c1-be74-af6075b267cb | webtier | ACTIVE | private=10.0.0.22, 172.24.4.67, fdef:2562:56c8:0:f816:3eff:fec2:b662 | Ubuntu | m1.custom |
+--------------------------------------+---------+--------+----------------------------------------------------------------------+--------+-----------+
```

O.Check the ssh port is open and accessible on the webtier instance from the devstack host using nc command
```
openstack@openstack:~/.ssh$ nc -vz 172.24.4.67 22
Connection to 172.24.4.67 22 port [tcp/ssh] succeeded!
```

P. SSH to the openstack instance and Ensure that the name resolution is working correctly on the openstack instance running Debian. 
```
sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
sudo bash -c 'echo "nameserver 1.1.1.1" >> /etc/resolv.conf'
Verify if the name resolution is working correctly using the following commands: 
ping -c1 www.google.com
curl -I http://example.com
curl -I https://www.example.com
```

Q. Set up port forwarding on the devstack host so the http requests to <devstack-host>:8080 is forwarded to <webtier-floating-ip>:8080. 
```
sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 172.24.4.67:8080
sudo iptables -t nat -A POSTROUTING -p tcp -d 172.24.4.67 --dport 8080 -j MASQUERADE
172.24.4.67 - Floating IP of the openstack instance (in my case) 
```


R. Deploy the application 
Install the nginx, flask, and sqlite3 as the debian generic cloud image does not have the required software using the sudo command. 
```
sudo apt update
sudo apt install nginx
sudo apt install -y python3 python3-pip sqlite3
pip3 install Flask
```

S. create the sqlite database using the following commands 
```
sqlite3 students.db
CREATE TABLE students(id integer primary key autoincrement, first_name varchar(20), last_name varchar(20), email_address varchar(40), phone_number varchar(12));
```

T. Download and copy the scripts from github repo to the openstack instance. Create a directory "crud_app" under devstack and copy all the files from the github repository. 
```
sudo cp -p crud-app /etc/nginx/sites-available/crud-app
sudo ln -s /etc/nginx/sites-available/crud-app /etc/nginx/sites-enabled/
sudo nginx -t 
sudo systemctl restart nginx
mkdir templates && mv *.html templates/. 
```

T. Start the application using the following command: 
```
debian@webtier:~/crud_app$ python3 app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 749-044-597
```

U. Access the application at the URL: 
```
http://<laptop-ip>:8080
```




