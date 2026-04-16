FROM alpine:3.22 AS python-builder

RUN apk add --no-cache python3 py3-pip

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --no-cache-dir \
    trafilatura \
    requests \
    beautifulsoup4 \
    lxml_html_clean

FROM n8nio/n8n:latest

USER root

# Copiar runtime de Python con rutas explícitas (los globs no copian dirs correctamente)
COPY --from=python-builder /usr/bin/python3    /usr/bin/python3
COPY --from=python-builder /usr/bin/python3.12 /usr/bin/python3.12
COPY --from=python-builder /usr/lib/python3.12           /usr/lib/python3.12
COPY --from=python-builder /usr/lib/libpython3.12.so.1.0 /usr/lib/libpython3.12.so.1.0
COPY --from=python-builder /usr/lib/libpython3.so        /usr/lib/libpython3.so
COPY --from=python-builder /opt/venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

USER node
