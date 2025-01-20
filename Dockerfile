FROM python:3.12.8-alpine3.21

# Ensures that stdout and stderr are sent straight
# to the terminal (no buffering).
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# Create venv and new user.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser --disabled-password --no-create-home django-user

# Add venv to path.
ENV PATH="/py/bin:$PATH"

USER django-user

CMD ["/bin/sh"]