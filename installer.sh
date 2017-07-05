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
sudo rm /usr/local/bin/cricscore
sudo rm /usr/local/bin/cricscore_uninstall
sudo rm -rf /usr/local/bin/cricscore_bin
echo "Uninstallation finished."
EOF

sudo chmod -R a+x $installdir"uninstaller.sh"
sudo cp {./src/*.py,./src/cricscore} $installdir
sudo chmod -R a+x $installdir"cricscore"
sudo ln -sf $installdir"cricscore" $exedir"cricscore"
sudo ln -sf $installdir"uninstaller.sh" $exedir"cricscore_uninstall"
echo "Installation finished."
