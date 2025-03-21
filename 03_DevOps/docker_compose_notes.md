
# docker notes

## Оглавление

- [docker notes](#docker-notes)
  - [Оглавление](#оглавление)
  - [docker install](#docker-install)
  - [docker commands](#docker-commands)


## docker install 

Step 1:
Update the APT Package Index
First, update the existing list of packages:

``` bash
sudo apt-get update
```

Step 2:
Install Required Packages
Install the necessary packages for allowing apt to use repositories over HTTPS:
``` bash
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

Step 3:
Add Docker’s Official GPG Key
Add Docker’s official GPG key to your system:
``` bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
Step 4:
Set Up the Docker APT Repository
Add the Docker APT repository to your system:
``` bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
Step 5:
Update the APT Package Index Again
Update the package index again to include the Docker packages from the newly added repository:
``` bash
sudo apt-get update
```
Step 6:
Install Docker Engine, CLI, and Containered
Install the latest version of Docker Engine, Docker CLI, and containered:
``` bash
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```



## docker commands  


start all containers
```bash
sudo docker compose up -d
```

force recreate container
```bash
sudo docker compose up --build --force-recreate --no-deps -d <container_name>
```