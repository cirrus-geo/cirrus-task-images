ARG BASEIMAGE=lambci/lambda:build-python3.7
FROM ${BASEIMAGE}

COPY  requirements.txt /build/

RUN \
    pip install --upgrade pip; \
    pip install -r /build/requirements.txt

COPY run.py /work/run

ENV PATH="/work:${PATH}"

WORKDIR /work
