FROM python:latest

ADD ./ImportFile.py .
ADD ./lista_urls.txt .

RUN pip install pymongo
RUN pip install beautifulsoup4
RUN pip install json_logging
RUN pip install requests

CMD ["python", "ImportFile.py"]