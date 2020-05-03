#!/usr/bin/zsh

action=$1
msg=$2
t_host='127.0.0.1'
r_host='172.17.0.1'

if [ "$action" = 'pull' ]; then
	sed -i "s/$t_host/$r_host/g" server/*.py
	git pull
	sed -i "s/$t_host/$r_host/g" server/*.py
elif [ "$action" = 'push' ]; then
	sed -i "s/$r_host/$t_host/g" server/*.py
	pipreqs --force
	git diff
	echo "\n\nCode will commit after 3s..."
	sleep 3
	git add *
	git commit -m $msg
	git push
	echo "\n\nCommit success !"
	sed -i "s/$t_host/$r_host/g" server/*.py
fi
