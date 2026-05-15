FROM python:alpine
RUN apk update --no-cache && apk upgrade --no-cache
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --chown=appuser:appgroup /app/jalali.py /app/index.html /app/
RUN pip install jdatetime
RUN chmod +x /app/jalali.py
USER appuser
ENTRYPOINT ["python", "/app/jalali.py"]
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8000/ || exit 1
