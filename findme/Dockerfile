FROM python:3.6
RUN mkdir /code
WORKDIR /code
ADD requirement.txt /code/
RUN pip install -r requirement.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends default-jre default-jdk
RUN apt-get install -y fonts-nanum
RUN ls -l /usr/share/fonts/truetype/    
RUN java -version
RUN curl -L https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh | bash
ADD . /code/
