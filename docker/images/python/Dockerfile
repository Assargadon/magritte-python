ARG PYTHON_VERSION
FROM python:$PYTHON_VERSION

ARG APP_CODE_PATH_CONTAINER
WORKDIR $APP_CODE_PATH_CONTAINER

RUN apk add git

COPY requirements.txt /magritte-phyton-pakage/
RUN pip install -r /magritte-phyton-pakage/requirements.txt

# Uncomment to run script on container start. Please note the only single CMD command is allowed
#CMD ["python", "dynamic-model.py"]

# Useful to interactive run scripts in the tty
CMD ["tail", "-f", "/dev/null"]

