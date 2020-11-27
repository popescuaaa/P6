ARG BASE_IMAGE=python:3.6.12-alpine3.12

FROM ${BASE_IMAGE}

ARG BUILD_DIR=.
ARG USER=loadbalancer
ARG HOME=/home/${USER}
ARG REQUIREMENTS_FILE=requirements.txt

USER root

RUN adduser ${USER} --disabled-password

COPY --chown=loadbalancer:loadbalancer ${BUILD_DIR} ${HOME}

RUN chown -R ${USER} ${HOME} \
    && chmod +x -R ${HOME}

USER ${USER}

WORKDIR ${HOME}

RUN pip install --no-warn-script-location -r ${REQUIREMENTS_FILE}

CMD ["sh", "run.sh"]