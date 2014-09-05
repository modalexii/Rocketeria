#!/bin/bash

environment_parent="/home/kyle/Git/modalexii/Rocketeria/dotBiz"

prod_specific_files=(
	# relative to $environment_parent
	"prod/app.yaml"
	"prod/cron.yaml"
	"prod/get_env.py"
	"prod/static/image/header-text.png"
	"prod/static/robots.txt"
	"prod/appengine_config.py"
	"prod/templates/html/footer.html"
)

read -p "[!] This will destroy all prod files. You sure about this? [yN] " -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo -e "\t[-] ok, your funeral..."
else
	echo -e "\t[!] aborting..."
	sleep 1
	exit
fi

sleep 2

cd $environment_parent

echo "[+] backing up prod-specific files"
echo -e "\t[+] making temporary directory"
mkdir /tmp/.rocketeria_prod_import

for f in ${prod_specific_files[*]}
do
	echo -e "\t[+] making backup copy of $f"
	if [ ! -d "$f" ]
	then
		mkdir -p /tmp/.rocketeria_prod_import/$(dirname "$f")
	fi
	cp -r "$f" "/tmp/.rocketeria_prod_import/$f"
done

echo "[+] obliterating prod environment"
rm -rf prod/

echo "[+] duplicating development environment"
cp -r dev prod

echo "[+] restoring prod-specific files"
for f in ${prod_specific_files[*]}
do
	echo -e "\t[+] restoring $f"
	cp -r "/tmp/.rocketeria_prod_import/$f" "$f"
done

echo "[+] removing temporary directory"
rm -rf /tmp/.rocketeria_prod_import

echo "[+] done"
