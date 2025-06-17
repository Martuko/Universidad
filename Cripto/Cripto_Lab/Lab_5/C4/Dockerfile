# ssh_lab/C4/Dockerfile (servirá como C4 y como S1)
FROM ubuntu:22.04

RUN apt update && \
    apt install -y openssh-client openssh-server net-tools iproute2 && \
    mkdir /var/run/sshd

# Crear usuario "prueba" con contraseña "prueba"
RUN useradd -m prueba && echo "prueba:prueba" | chpasswd

# Permitir autenticación por contraseña
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
