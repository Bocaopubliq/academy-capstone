FROM gitpod/workspace-full

ENV DEBIAN_FRONTEND=noninteractive
ENV SPARK_LOCAL_IP=0.0.0.0

USER root
# Install apt packages and clean up cached files
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Install the AWS CLI and clean up tmp files
RUN wget https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -O ./awscliv2.zip && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf ./aws awscliv2.zip

USER gitpod
EXPOSE 3000
EXPOSE 8080
EXPOSE 4040
WORKDIR /Bo
COPY requirements.txt /Bo/requirements.txt
RUN pip install pip --upgrade && pip install -r requirements.txt
COPY src src

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG AWS_DEFAULT_OUTPUT

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
ENV AWS_DEFAULT_OUTPUT=$AWS_DEFAULT_OUTPUT

ENTRYPOINT ["/bash/bin"]
CMD ["python3","src/main.py"]