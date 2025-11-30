# st_supabase_docker

Objective
---------

This repo demonstrates a minimal Streamlit app talking to a PostgREST (Supabase-style) API backed by PostgreSQL using Docker Compose. It's intended for local testing and learning how the UI and API interact.

Quick start
-----------

Prerequisites
- Docker and Docker Compose (v2: `docker compose`) installed

Start the app (recommended)

```bash
cd /path/to/st_supabase_docker
docker compose up --build
```

Open the Streamlit UI:

```
http://localhost:8501
```

Services started
- `supabase-db` — PostgreSQL (initialized with `init.sql`)
- `supabase-api` — PostgREST REST API exposing the DB (container port `3000`)
- `streamlit-app` — Streamlit UI (host port `8501`)

Environment variables
- `SUPABASE_URL`: base URL for the API (inside Docker should be `http://supabase:3000`)
- `SUPABASE_KEY`: API key passed as `apikey` header to PostgREST

Use the `environment:` section in `docker-compose.yml` to configure these values for the `streamlit` service.

Usage
- Add Item — create a new item (name + description)
- View Items — list and delete items

Commands
- Start (foreground):

```bash
docker compose up --build
```

- Start (detached):

```bash
docker compose up -d
```

- Stop (keep DB data):

```bash
docker compose down
```

- Reset DB (remove DB volume so `init.sql` runs fresh):

```bash
docker compose down -v
```

Local development without Docker

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export SUPABASE_URL=http://<host-or-ip>:3000
export SUPABASE_KEY=<your-api-key>
streamlit run app.py
```

Troubleshooting
- 401 Unauthorized: check `SUPABASE_KEY` and PostgREST configuration (or use `apikey` header)
- App cannot reach API from container: use service host `http://supabase:3000` not `0.0.0.0` or `localhost`
- DB init errors: remove the volume and restart (`docker compose down -v`)

Files of interest
- `app.py` — Streamlit UI and tiny REST client
- `docker-compose.yml` — orchestrates services and env vars
- `init.sql` — DB initialization
- `Dockerfile` — Streamlit image
- `requirements.txt` — Python deps

If you'd like I can also add a smoke-test script, a small `Makefile`, or a `start.sh` helper.

## Explanation of files

- `app.py` — Streamlit application; contains the UI and the minimal REST client that talks to PostgREST (`/items` endpoints).
- `Dockerfile` — Builds the Streamlit container image used by the `streamlit` service.
- `docker-compose.yml` — Orchestrates three services: Postgres DB (`db`), PostgREST API (`supabase` / `supabase-api`) and the `streamlit` app. Also sets runtime environment variables for the Streamlit container.
- `init.sql` — Database initialization script executed when the DB volume is created: creates the `items` table, RLS policies used for development, and grants for the `anon` role.
- `requirements.txt` — Python dependency list used to build the Streamlit image (`streamlit`, `requests`, `python-dotenv`).
- `.env.example` — Template showing the environment variables the app expects (copy to `.env` for local use).
- `.env` — Local environment file (used for reference). Note: this repository may include a `.env` for convenience but the container uses values from `docker-compose.yml` at runtime.
- `README.md` — This documentation and usage guide.
- `LICENSE` — Project license.

