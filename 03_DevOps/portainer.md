# portainer

## Оглавление

- [portainer](#portainer)
  - [Оглавление](#оглавление)
  - [portainer install](#portainer-install)


## portainer install 

docker-compose.yml
``` yml
services:
 
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    hostname: portainer
    restart: unless-stopped
    environment:
      TZ: "Europe/Moscow"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./portainer_data:/data
    ports:
      - "9000:9000"
```

start container:
```bash
sudo docker compose up -d
```


http://89.169.167.203:9000/

http://flairbim.com:9000/#!/home