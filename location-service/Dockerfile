# Stage 1 - deps

FROM python:3.12-slim AS deps
WORKDIR /app
COPY location-service/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \ 
    && pip install --no-cache-dir -r requirements.txt

# Stage 2 - runtime
FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin
COPY utils/logger.py .
COPY location-service/main.py .
ENV APP_ENV=development
EXPOSE 8000
CMD ["sh", "-c", "if [ \"$APP_ENV\" = \"production\" ]; \
  then uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4; \
  else uvicorn main:app --host 0.0.0.0 --port 8000 --reload; \
  fi"]
