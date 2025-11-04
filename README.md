# Porroflix -  Media Server

This repository provides a **Docker configuration** for my home media server.

All services are orchestrated via `docker-compose` and connected to Tailscale through `tsbridge`.

## Containers Overview

| Container       | URL                                     | Description                                                                                            |
| --------------- | ----------------------------------------| -------------------------------------------------------------------------------------------------------|
| Jellyfin        | `jellyfin.<your-ts-name>.ts.net`        | Media streaming server                                                                                 |
| Jellyseerr      | `jellyseerr.<your-ts-name>.ts.net`      | Request interface for movies/TV                                                                        |
| Bazarr          | `bazarr.<your-ts-name>.ts.net`          | Subtitle management                                                                                    |
| Radarr          | `radarr.<your-ts-name>.ts.net`          | Movie management                                                                                       |
| Sonarr          | `sonarr.<your-ts-name>.ts.net`          | TV series management                                                                                   |
| Prowlarr        | `prowlarr.<your-ts-name>.ts.net`        | Indexer manager for *Arr stack                                                                         |
| qBittorrent     | `See vpn-qBittorrent`                   | Internal Torrent client, not seen by the Tailnet                                                       |
| vpn-qBittorrent | `vpn-qbittorrent.<your-ts-name>.ts.net` | VPN gateway used by qBittorrent. All qbittorrent's traffic goes through here (WebUI, Radarr, Sonarr..) |


## Configuration

1. **Copy the example `.env` file** and modify the values according to your setup:

    ```bash
    cp .env.example .env
    ````

2. **Update the following variables:**

    _Tailscale Config_
    * `TS_OAUTH_CLIENT_ID` and `TS_OAUTH_CLIENT_SECRET`: your Tailscale OAuth credentials
  
   _Misc_
    * `PUID` / `PGID`: user and group ID for Docker file permissions  
    * `TZ`: your timezone

   _Folders_
    * `CONFIG_DIR`: path to store containers' configuration folders  
    * `DATA_DIR`: base directory for all media and torrent data  
    * `MEDIA_FOLDER`: folder name inside `DATA_DIR` for your media library  
    * `TORRENTS_FOLDER`: folder name inside `DATA_DIR` for torrent downloads

   _VPN_
    * `VPN_SERVICE_PROVIDER`: your VPN provider  
    * `VPN_TYPE`: VPN protocol (`openvpn` or `wireguard`)  
    * `VPN_USERNAME` / `VPN_PASSWORD`: VPN account credentials (if required by provider)  
    * `WIREGUARD_PRIVATE_KEY`: your WireGuard private key (if using WireGuard)  
    * `WIREGUARD_ADDRESSES`: WireGuard assigned IP address range  
    * `SERVER_COUNTRIES`: preferred VPN server locations  


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

## Removing the VPN

If you don't want to use a VPN follow these steps:

1. Copy the **networks** and **labels** properties from **vpn-qbittorrent**
2. Paste them in **qbittorrent**
3. Remove the **network_mode** and **depends_on** properties from **qbittorrent**
4. Change the **depends_on** property values in **radarr** and **sonarr** from **vpn-qbittorrent** to **qbittorrent**

## License

This repository is provided as-is for personal/home use.
