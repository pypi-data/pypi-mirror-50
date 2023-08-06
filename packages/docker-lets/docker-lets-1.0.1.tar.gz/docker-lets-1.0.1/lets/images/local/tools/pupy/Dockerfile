FROM alxchk/pupy:unstable

RUN apt-get update && \
    apt-get install -qy xz-utils wget git && \
    git clone https://github.com/n1nj4sec/pupy /tmp/pupy && \
    git -C /tmp/pupy submodule update --init --recursive && \
    rm -r /opt/pupy && \
    ln -s /tmp/pupy/pupy /opt/ && \
    wget https://github.com/n1nj4sec/pupy/releases/download/latest/payload_templates.txz -O /tmp/payload_templates.tgz && \
    tar xvf /tmp/payload_templates.tgz -C /opt/pupy/

ENTRYPOINT [ "/opt/pupy/conf/pupysh.sh" ]
