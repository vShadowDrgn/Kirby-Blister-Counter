## Design decisions:

- We use docker instead of podman, because we need access to the gpio device. This is also possible with podman, but it requires sudo permissions, which makes setting up setup auto-start with podman harder.

## Installation

Boot the Raspberry Pi with the SD-Card and log in via SSH.

### Preparing the Raspberry Pi

1. Open the config by running "sudo raspi-config".
2. In the "System Options", change Password and Hostname.
3. In the "Performance Options", set the GPU Memory to 32 MB.
4. In the "Advanced Options", expand the filesystem.

6. Run `sudo apt update`.
7. Run `sudo apt upgrade`.
8. Run `sudo rpi-update`.
9. Run `sudo reboot`.

### Install Git

```bash
sudo apt install git
```

# Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh | sudo sh get-docker.sh
sudo groupadd docker | sudo usermod -aG docker $USER
```

You may need to logout and login again for the permissions to be updated.

### Git clone the project

```bash
git clone https://github.com/vShadowDrgn/Kirby-Blister-Counter.git
cd Kirby-Blister-Counter
```

### Move the database

```bash
sudo mkdir -p /opt/kirbycounter
sudo mv database.db /opt/kirbycounter/database.db
sudo chown -R 1000:1000 /opt/kirbycounter
```

You can also put your database backup there.

### Build the docker image and create the container

NOTE: We need sudo because we need access to the gpio device.

```bash
sudo docker build --no-cache -t kirbycounter .
```
```bash
sudo docker create --name kirbycounter --restart=always --network=host --device /dev/gpiochip0:/dev/gpiochip0 -v /opt/kirbycounter/database.db:/app/database.db kirbycounter:latest
```

### Run the docker container

```bash
sudo docker start kirbycounter
```
