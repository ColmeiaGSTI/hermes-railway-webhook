FROM nousresearch/hermes-agent:latest

# Webhook-only TCP keepalive adjustment.
COPY patch_telegram.py /tmp/patch_telegram.py
RUN python /tmp/patch_telegram.py && rm /tmp/patch_telegram.py
