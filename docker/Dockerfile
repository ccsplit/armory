FROM debian:stable-slim as base
MAINTAINER dlawson@depthsecurity.com
ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt install -y curl ca-certificates git build-essential\
      sudo nano vim p7zip-full zlib1g-dev

FROM base as go
ENV GOPATH /gobins
RUN echo "alias go_get='go get -uv'" >> ~/.bashrc
RUN curl https://dl.google.com/go/go1.14.4.linux-amd64.tar.gz -o go.tar.gz\
      && tar zxfv go.tar.gz\
      && ln -s /go/bin/* /bin/

# Install all of the tools into the $GOPATH/bin/ directory so it can be copied later
# to the final image.
RUN go get -u -v github.com/ffuf/ffuf\
      && go get -u -v github.com/OJ/gobuster\
      && go get -u -v github.com/sensepost/gowitness\
      && go get -u -v github.com/projectdiscovery/subfinder/cmd/subfinder\
      && go get -u -v github.com/hakluke/hakrawler\
      && go get -u -v github.com/anshumanbh/tko-subs
RUN cp /gobins/src/github.com/anshumanbh/tko-subs/providers-data.csv /gobins/bin/providers-data.csv


FROM base as makebuilds
WORKDIR /opt
RUN mkdir /bins
RUN git clone https://github.com/robertdavidgraham/masscan && cd masscan && make -j && cp bin/masscan /bins
RUN git clone https://github.com/rbsec/sslscan && cd sslscan && make static && cp sslscan /bins

#
#FROM base as python
#WORKDIR /opt/src
#
#CMD ["echo", "Cloning various repos"]
#RUN git clone https://github.com/joaomatosf/jexboss
#RUN touch /tmp/linkedint2
#RUN git clone https://github.com/fang0654/LinkedInt
#RUN git clone https://github.com/sullo/nikto
#RUN git clone https://github.com/m8r0wn/pymeta
#RUN git clone https://github.com/aboul3la/Sublist3r
#RUN git clone https://github.com/anshumanbh/tko-subs
#RUN git clone https://github.com/DanMcInerney/xsscrapy
#RUN git clone https://github.com/fang0654/Asnlookup
#RUN git clone https://github.com/fang0654/DomLink
#RUN git clone https://github.com/offensive-security/exploitdb
#
#
## Next couple of lines are to use custom version of ffuf until it gets updated
#WORKDIR /opt/src/jexboss
#RUN pip install -r requires.txt
#RUN ln -s /opt/src/jexboss/jexboss.py /usr/local/bin/jexboss.py
#WORKDIR /opt/src/LinkedInt
#RUN pip install thready http
#RUN chmod +x /opt/src/LinkedInt/LinkedInt.py
#RUN ln -s /opt/src/LinkedInt/LinkedInt.py /usr/local/bin/LinkedInt.py
#WORKDIR /opt/src/masscan
#RUN make -j
#RUN make install
#RUN ln -s /opt/src/nikto/program /opt/nikto
#RUN ln -s /opt/nikto/nikto.pl /usr/local/bin/nikto
#WORKDIR /opt/src/pymeta
#RUN python3 setup.py install
#RUN chmod +x pymeta.py
#
#WORKDIR /opt/src/Sublist3r
#RUN pip install -r requirements.txt
#RUN ln -s /opt/src/Sublist3r/sublist3r.py /usr/local/bin/sublist3r
#WORKDIR /opt/src/xsscrapy
#RUN pip install -r requirements.txt
#ENV PATH="${PATH}:/opt/src/xsscrapy"
#RUN chmod +x /opt/src/xsscrapy/xsscrapy.py
#RUN export PATH=$PATH:/opt/src/xsscrapy
#RUN ln -s /opt/src/Asnlookup/asnlookup.py /usr/local/bin/asnlookup.py
#RUN chmod +x /usr/local/bin/asnlookup.py
#RUN ln -s /opt/src/DomLink/domLink.py /usr/local/bin/domLink.py
#RUN chmod +x /usr/local/bin/domLink.py
#
#RUN sed -i 's/\/opt\/exploitdb/\/opt\/src\/exploitdb/g' /opt/src/exploitdb/.searchsploit_rc
#RUN cp /opt/src/exploitdb/.searchsploit_rc /root/
#RUN ln -s /opt/src/exploitdb/searchsploit /usr/local/bin/searchsploit
#
#WORKDIR /opt/src
#
## Going to increment this everytime I want to update armory.
#RUN touch /tmp/revision91
#
#
#RUN git clone https://github.com/depthsecurity/armory.git
#WORKDIR /opt/src/armory
#RUN git checkout armory2.0
#CMD ["echo", "Installing Armory"]
#RUN pip3 install django # Not sure why this doesn't work from the setup
#RUN python3 setup.py install
#RUN pip3 install jinja2 xlsxwriter
#WORKDIR /root/current


FROM base as final
COPY --from=go /go/bin/* /bin/
COPY --from=makebuilds /bins/* /bin/
RUN echo "deb-src http://deb.debian.org/debian buster main" >> /etc/apt/sources.list

CMD ["echo", "Installing Debian packages needed."]
RUN apt update && apt install -y python python3 git python3-pip python-pip libmariadb-dev-compat\
      ruby ruby-dev gem dnsrecon hydra nmap whois libnet-ssleay-perl chromium xclip
WORKDIR /src
CMD ["echo", "Cloning various repos"]
#RUN git clone https://github.com/joaomatosf/jexboss.git
#RUN touch /tmp/linkedint2
#RUN git clone https://github.com/fang0654/LinkedInt
#RUN git clone https://github.com/sullo/nikto
#RUN git clone https://github.com/m8r0wn/pymeta
#RUN git clone https://github.com/aboul3la/Sublist3r.git
#RUN git clone https://github.com/DanMcInerney/xsscrapy.git
#RUN git clone https://github.com/fang0654/Asnlookup.git
#RUN git clone https://github.com/fang0654/DomLink.git
#RUN git clone https://github.com/offensive-security/exploitdb.git

RUN gem install aquatone
