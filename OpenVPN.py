import subprocess

# Install OpenVPN
subprocess.run(['sudo', 'apt-get', 'install', 'openvpn', '-y'])

# Generate server keys
subprocess.run(['sudo', 'openvpn', '--genkey', '--secret', 'server.key'])

# Configure server
server_conf = """
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh.pem
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 9.9.9.11"
keepalive 10 120
tls-auth ta.key 0
cipher AES-256-CBC
auth SHA256
user nobody
group nogroup
persist-key
persist-tun
status openvpn-status.log
verb 3
"""

with open('/etc/openvpn/server.conf', 'w') as f:
    f.write(server_conf)

# Start OpenVPN
subprocess.run(['sudo', 'systemctl', 'enable', 'openvpn.service'])
subprocess.run(['sudo', 'systemctl', 'start', 'openvpn.service'])