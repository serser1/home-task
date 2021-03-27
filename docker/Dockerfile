FROM centos:7
COPY src /src
RUN yum install stress python3 -y python3-pip ;\
pip3 install pip install psycopg2-binary ;\
pip3 install -r /src/requirement.txt
ENTRYPOINT python3 /src/main.py
