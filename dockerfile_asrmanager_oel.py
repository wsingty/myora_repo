FROM  container-registry.oracle.com/os/oraclelinux:7.5

MAINTAINER    David Ingty <david.ingty@oracle.com>
COPY "jdk1.8.0_191 /javadir"
COPY "asrmanager-18.3.1-20180830031818.rpm /root"

CMD "mkdir -p /var/opt/asrmanager/configuration/"
COPY "asr.conf /var/opt/asrmanager/configuration/"







#docker build -t "oel_asrm_18.3.1:7.5" -f dockerfile .
