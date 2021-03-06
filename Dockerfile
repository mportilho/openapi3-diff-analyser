# ---- Base python ----
FROM python:3.9.5 AS base
# Create app directory
WORKDIR /app

# ---- Dependencies ----
FROM base AS dependencies
COPY app/requirements.txt ./
# install app dependencies
RUN pip install -r requirements.txt

# ---- Copy Files/Build ----
FROM dependencies AS build
WORKDIR /app
COPY . /app
# Build / Compile if required

# --- Release with Default Image ----
FROM python:3.9.5 AS release
# Create app directory
WORKDIR /app

# Install app dependencies
COPY --from=dependencies /app/requirements.txt ./
COPY --from=dependencies /root/.cache /root/.cache
RUN pip install -r requirements.txt

ARG SERVER_PORT=5000
ENV SERVER_PORT=${SERVER_PORT}

COPY --from=build /app/ ./
CMD python main.py --server=${SERVER_PORT}