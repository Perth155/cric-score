#!/bin/bash

installdir="/usr/local/bin/cricscore_bin/"
exedir="/usr/local/bin/"

if [ "$EUID" -ne 0 ];then
	echo "Installer needs to be run as root."
	exit 1
fi

echo "Downloading requirements."
{
	sudo pip3 install -r requirements.txt
}||{
	echo "Installation Failed! Check if pip is installed."
	exit 1
}

sudo mkdir -p $installdir

sudo cat > $installdir"uninstaller.sh" <<- "EOF"
#!/bin/bash
read -p "Do you want to permanently remove cricscore?[Y/n](default:n)" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
	sudo rm /usr/local/bin/cricscore
	sudo rm /usr/local/bin/cricscore_uninstall
	sudo rm -rf /usr/local/bin/cricscore_bin
	echo "Uninstallation finished."
fi
EOF

sudo chmod -R a+x $installdir"uninstaller.sh"
sudo cp ./src/*.py $installdir
mv $installdir"cricscore.py" $installdir"cricscore"
sudo chmod -R a+x $installdir"cricscore"
sudo ln -sf $installdir"cricscore" $exedir"cricscore"
sudo ln -sf $installdir"uninstaller.sh" $exedir"cricscore_uninstall"
echo "Installation finished."
