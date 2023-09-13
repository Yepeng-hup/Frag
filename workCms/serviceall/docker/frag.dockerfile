FROM python:3.7-slim-buster
WORKDIR /
ADD frag.tar.gz/ .
RUN rm -rf frag.tar.gz && cd /Frag && pip install -r requirements.txt
EXPOSE 14000/tcp
COPY ss.sh /Frag
RUN chmod +x /Frag/ss.sh
CMD [ "bash", "Frag/ss.sh" ]
