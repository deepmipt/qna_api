FROM python:3.6-stretch
WORKDIR /app
ADD . /app
ENV QNA_DATA /data
VOLUME /data
EXPOSE 80
RUN pip install -r requirements.txt
CMD ["python", "api.py"]