import os
import subprocess as sb
import sys

if len(sys.argv)==1:

	print	'\n- CRISPR-SURF Docker Container -\n\t- use `SURF_count` to count sgRNAs from FASTQ\n\t- - use `SURF_deconvolution` to perform deconvolution analysis\n\t- use `SURF_webapp` to start the web application\n'
	sys.exit(1)

if sys.argv[1]=='SURF_count':
	sb.call(["/opt/conda/bin/python", "/SURF/SURF_count.py"]+ sys.argv[2:])
elif sys.argv[1]=='SURF_deconvolution':
	sb.call(["/opt/conda/bin/python", "/SURF/SURF_deconvolution.py"]+ sys.argv[2:])
elif sys.argv[1]=='SURF_webapp':
	sb.call(["/bin/bash", "-c", "/SURF/start_server_docker.sh"])
else:
	print	'\n- CRISPR-SURF Docker Container -\n\t- use `SURF` to use the command line\n\t- use `SURF_webapp` to start the web application\n'
