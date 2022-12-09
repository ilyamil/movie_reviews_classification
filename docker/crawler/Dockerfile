FROM python:3.9.16-slim-bullseye
WORKDIR /app
COPY ./ .
RUN apt-get update \
    && apt-get install wget unzip zip -y
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh && \
    bash Miniconda3-py39_4.12.0-Linux-x86_64.sh && \
    rm Miniconda3-py39_4.12.0-Linux-x86_64.sh
RUN conda env -n crawler_env
RUN conda activate crawler_env && \
    python3 set_env.py && \
    conda deactivate && \
    conda activate crawler_env
RUN python3 set_env.py
CMD ["python3", "scripts/predict.py"]