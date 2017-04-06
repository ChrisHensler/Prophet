for ip in $(ls -R ../../out | grep /udp-161 | cut -d "/" -f 4)
do
	hydra -P password_list.txt $ip snmp | tee out/$ip.snmp.results 
	wait

done
