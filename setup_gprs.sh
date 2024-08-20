#!/bin/bash

# Update and install PPP
echo "Updating package list and installing ppp..."
sudo apt-get update
sudo apt-get install -y ppp

# Create chat script
echo "Creating chat script..."
sudo tee /etc/chatscripts/gprs-connect-chat > /dev/null <<EOL
ABORT "BUSY"
ABORT "NO CARRIER"
ABORT "ERROR"
ABORT "NO DIALTONE"
ABORT "Invalid Login"
ABORT "Login incorrect"
"" AT
OK ATH
OK ATE1
OK AT+CPIN?
OK AT+CGATT?
OK AT+SAPBR=3,1,"CONTYPE","GPRS"
OK AT+SAPBR=3,1,"APN","YOUR_APN"
OK AT+SAPBR=1,1
OK ATD*99#
CONNECT ""
EOL

# Create peers file
echo "Creating peers file..."
sudo tee /etc/ppp/peers/gprs > /dev/null <<EOL
/dev/ttyAMA0 115200
connect '/usr/sbin/chat -v -f /etc/chatscripts/gprs-connect-chat'
debug
nodetach
ms-dns 8.8.8.8
ms-dns 8.8.4.4
noauth
ipcp-accept-local
ipcp-accept-remote
persist
noipdefault
usepeerdns
defaultroute
replacedefaultroute
EOL

# Set proper permissions
echo "Setting permissions for chat script and peers file..."
sudo chmod 755 /etc/chatscripts/gprs-connect-chat
sudo chmod 755 /etc/ppp/peers/gprs

echo "Setup complete. You can now use pon and poff to manage your PPP connection."

