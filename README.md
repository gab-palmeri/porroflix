# Media Server with Jellyfin, *Arr Stack, and Tailscale

This repository provides a **Docker configuration** for my home media server.

All services are orchestrated via `docker-compose` and connected to Tailscale through `tsbridge`.

## Services Overview

| Service     | URL                                      | Description                     |
| ----------- | ---------------------------------------- | ------------------------------- |
| Jellyfin    | `jellyfin.<your-ts-name>.ts.net`        | Media streaming server          |
| Jellyseerr  | `jellyseerr.<your-ts-name>.ts.net`      | Request interface for movies/TV |
| Bazarr      | `bazarr.<your-ts-name>.ts.net`          | Subtitle management             |
| Radarr      | `radarr.<your-ts-name>.ts.net`          | Movie management                |
| Sonarr      | `sonarr.<your-ts-name>.ts.net`          | TV series management            |
| Prowlarr    | `prowlarr.<your-ts-name>.ts.net`        | Indexer manager for *Arr stack  |
| qBittorrent | `qbittorrent.<your-ts-name>.ts.net`     | Torrent client                  |


## Configuration

1. **Copy the example `.env` file** and modify the values according to your setup:

    ```bash
    cp .env.example .env
    ````

2. **Update the following variables:**

* `TS_OAUTH_CLIENT_ID` and `TS_OAUTH_CLIENT_SECRET`: your Tailscale OAuth credentials
* `PUID` / `PGID`: user and group ID for Docker file permissions
* `TZ`: your timezone
* `CONFIG_DIR`: path to store containers' configuration folders
* `MEDIA_DIR`: path to your media library
* `TORRENTS_DIR`: path for torrent downloads


## Running the Stack

Start all containers:

```bash
docker compose up -d
```

Stop the stack:

```bash
docker compose down
```

Check logs:

```bash
docker compose logs -f <service_name>
```

---

## Tailscale Funnel

`funnel.py` allows you to enable or disable the Tailscale Funnel for Jellyfin and Jellyseerr without manually editing `docker-compose.yml`.

#### 1. Make the script executable

```bash
chmod +x funnel.py
```

#### 2. Create a Python virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install ruamel.yaml
```

#### 4. Usage

```bash
./funnel.py on|off
```

The script will update the `docker-compose.yml` labels and restart the **Jellyfin** and **Jellyseerr** containers.


## License

This repository is provided as-is for personal/home use.