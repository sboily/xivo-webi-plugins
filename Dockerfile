from python:2.7
MAINTAINER Sylvain Boily "sboily@avencall.com"

RUN apt-get -yq update \
   && apt-get -yqq dist-upgrade \
    && apt-get -yq autoremove

ADD . /usr/src/xivo-webi-plugins
WORKDIR /usr/src/xivo-webi-plugins
RUN pip install -r requirements.txt
RUN python setup.py install
WORKDIR /root

EXPOSE 9502

CMD xivo-webi -fd --user root
