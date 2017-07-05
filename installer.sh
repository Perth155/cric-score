#!/bin/bash

if ["$EUID" -ne 0]
	then echo "Installer needs to be run as root."
	exit 1
fi

echo "Downloading requirements."
{
	sudo pip3 install -r requirements.txt
}||{
	echo "Failed! Check if pip is installed."
	exit 1
}

sudo mkdir /usr/local/bin/cricscore
chmod +x uninstaller.sh ../src/cricscore.py
sudo cp {installer.sh uninstaller.sh /src/*.py} /usr/local/bin/cricscore
sudo ln -sf /usr/local/bin/cricscore.py /usr/bin/cricscore
sudo ln -sf /usr/local/bin/uninstaller.sh /usr/bin/cricscore_uninstall
echo "Installation finished..."
