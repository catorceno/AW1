# Despliegue en EC2

### 5.2 Comprobar
Comprobar acceso al servidor ec2:
![Hello World Prueba](hello-world-prueba.png)

- `curl http://127.0.0.1:8000/` (dentro del servidor) → respondió `Hello World!` sin problema.
- `curl http://172.31.27.1:8000/` (IP privada, desde otra sesión SSH) → rechazo inmediato (`Could not connect to server`, 0 ms). El paquete llegó a la máquina, pero como el proceso no escucha en esa interfaz, nadie lo atendió.
- Navegador a `http://13.222.125.97:8000/` → no rechazó, quedó esperando y expiró por tiempo (`ERR_CONNECTION_TIMED_OUT`). Esto es distinto al caso anterior: acá el paquete probablemente ni siquiera llegó a la instancia, lo que apunta a que el grupo de seguridad de EC2 está bloqueando el puerto 8000 desde afuera.

Por un lado, Flask escucha solo en `127.0.0.1` (loopback), no en todas las interfaces de la máquina, así que ni siquiera la IP privada responde desde otra sesión. Por otro lado, el grupo de seguridad de EC2 no tiene abierto el puerto 8000 hacia el exterior, así que aunque corrigiera el punto 1, el navegador seguiría sin poder llegar desde internet.