
import subprocess

DEBUG=False


def knock(host, ports):
	for port in ports:
		subprocess.call(["nmap", "-Pn", "--host_timeout", "100", "--max-retries", "0", "-p", port, host])
