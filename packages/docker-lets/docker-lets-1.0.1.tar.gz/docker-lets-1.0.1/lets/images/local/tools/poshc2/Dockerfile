FROM python:2
RUN curl -sSL https://raw.githubusercontent.com/nettitude/PoshC2_Python/master/Install.sh | bash
RUN sed -i "s/if not os.path.exists(directory):/if True:/g" /opt/PoshC2_Python/C2Server.py \
    && sed -i "s/os.makedirs(directory)//g" /opt/PoshC2_Python/C2Server.py
VOLUME ["/opt/PoshC2_Project"]
