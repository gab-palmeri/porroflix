# Porroflix -  Media Server

This repository provides a **Docker configuration** for my home media server.

All services are orchestrated via `docker-compose`.

## Containers Overview

| Container       | Default Access              | Description                                                             |
|-----------------|-----------------------------|-------------------------------------------------------------------------|
| Jellyfin        | http://host_ip:8096          | Media streaming server                                                  |
| Jellyseerr      | http://host_ip:5055          | Request interface for movies and TV shows                               |
| Bazarr          | http://host_ip:6767          | Subtitle management                                                     |
| Radarr          | http://host_ip:7878          | Movie management                                                        |
| Sonarr          | http://host_ip:8989          | TV series management                                                    |
| Prowlarr        | http://host_ip:9696          | Indexer manager for the *Arr stack                                      |
| qBittorrent     | Internal (via VPN)          | Torrent client (traffic routed through VPN if enabled)                 |
| vpn-qBittorrent | http://host_ip:8080          | VPN gateway container used by qBittorrent                               |


## Configuration

1. **Copy the example `.env` file** and modify the values according to your setup:

    ```bash
    cp .env.example .env
    ````

2. **Update the following variables:**
  
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

## Removing the VPN

If you don't want to use a VPN follow these steps:

1. Copy the **networks** and **labels** properties from **vpn-qbittorrent**
2. Paste them in **qbittorrent**
3. Remove the **network_mode** and **depends_on** properties from **qbittorrent**
4. Change the **depends_on** property values in **radarr** and **sonarr** from **vpn-qbittorrent** to **qbittorrent**

## License

This repository is provided as-is for personal/home use.
