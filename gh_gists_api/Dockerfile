FROM python:3.11-alpine
WORKDIR /app
RUN addgroup gists_g && adduser --disabled-password gists_u -G gists_g
COPY --chown=gists_u:gists_g . /app
USER gists_u
RUN dos2unix /app/tests/*.py && \
    pip install --no-cache-dir -r requirements.txt
CMD ["python", "gists.py"]
