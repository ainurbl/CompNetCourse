import PySimpleGUI as Gui
import scapy.all as scapy

import util

util.init()


def get_hosts(ip_with_mask):
    return [(host_info[1].psrc, host_info[1].hwsrc) for host_info in
            scapy.srp(scapy.Ether(dst=util.DST_MAC) / scapy.ARP(pdst=ip_with_mask), timeout=5)[0]]


first_launch = True
hosts = get_hosts(f'{util.NETWORK_IP}/24')

window = Gui.Window('Find all computers in network', [
    [Gui.Output(size=(100, 20))],
    [Gui.Submit('Begin', size=(10, 2)),
     Gui.ProgressBar(len(hosts), size=(55, 5), key='progress')],
])

while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if event == 'Begin' and first_launch:
        print(f'{"IP address":30}{"MAC address":30}{"Host name":30}')
        print('Current PC:')
        print(f'{util.MY_IP:30}{util.MY_MAC:30}{util.MY_HOST_NAME:30}')
        print('Network:')
        i = 1
        for (ip, mac) in hosts:
            print(f'{ip:30}{mac:30}{util.get_host_name(ip):30}')
            window['progress'].UpdateBar(i)
            i += 1
        first_launch = False
window.close()
