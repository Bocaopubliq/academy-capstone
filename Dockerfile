FROM public.ecr.aws/datamindedacademy/capstone:v3.4.1-hadoop-3.3.6-v1
WORKDIR /Bo
COPY requirements.txt /Bo/
USER root
RUN pip install -r /Bo/requirements.txt
COPY src /Bo/src



ENV AWS_ACCESS_KEY_ID=''
ENV AWS_SECRET_ACCESS_KEY=''
ENV AWS_DEFAULT_REGION=''
ENV AWS_DEFAULT_OUTPUT=''


CMD ["python3","/Bo/src/main.py"]
