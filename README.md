# Media Server with Jellyfin, *Arr Stack, and Tailscale

This repository provides a **Docker configuration** for a complete home media server, including:

- **Jellyfin** for media streaming
- **Jellyseerr** for content request management
- **Bazarr** for subtitles
- ***Arr Stack** (Radarr, Sonarr, Prowlarr) for automated movie and TV series management
- **qBittorrent** as a torrent client
- **Tailscale + tsbridge** for securely exposing services via Funnel or private network

All services are orchestrated via `docker-compose` and connected to Tailscale through `tsbridge`.

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

---

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

* You can enable or disable Funnel access for each service by adjusting the `tsbridge.service.funnel_enabled` label in `docker-compose.yml`.

## License

This repository is provided as-is for personal/home use.
