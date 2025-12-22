import subprocess
import platform
import re
import locale


def detect_network_type_multilingual():
    system = platform.system().lower()

    if system == "windows":
        return detect_windows_network_multilingual()
    elif system == "linux":
        return detect_linux_network_multilingual()
    elif system == "darwin":  # macOS
        return detect_macos_network_multilingual()
    else:
        return "Unknown OS"


def detect_windows_network_multilingual():
    try:
        current_locale = locale.getdefaultlocale()[0] or 'en_US'

        result = subprocess.run(['ipconfig', '/all'],
                                capture_output=True, text=True, timeout=10)

        output = result.stdout

        ethernet_keywords = [
            'ethernet adapter',  # 英文
            '以太网适配器',  # 中文简体
            '乙太網路介面卡',  # 中文繁体
            'адаптер локальной сети',  # 俄语
            'carte réseau',  # 法语
            'adapter de red',  # 西班牙语
            'Netzwerkadapter',  # 德语
            'アダプター',  # 日语
            '어댑터',  # 韩语
            'adattatore di rete',  # 意大利语
            'placa de rede',  # 葡萄牙语
        ]

        wireless_keywords = [
            'wireless lan adapter',
            'wi-fi adapter',
            'wireless adapter',
            '無線ネットワークアダプター',  # 日语
            '무선 네트워크 어댑터',  # 韩语
            '適配器',  # 中文（可能指无线）
            'беспроводной адаптер',  # 俄语
            'adaptateur sans fil',  # 法语
            'adaptador inalámbrico',  # 西班牙语
            'WLAN-Adapter',  # 德语
            'adattatore wireless',  # 意大利语
            'adaptador sem fio',  # 葡萄牙语
        ]

        disconnected_status = [
            'media disconnected',
            'média desconectado',  # 葡萄牙语
            'média desconectada',  # 西班牙语
            'nicht verbunden',  # 德语
            'déconnecté',  # 法语
            'disconnesso',  # 意大利语
            'отключено',  # 俄语
            '未接続',  # 日语
            '연결되지 않음',  # 韩语
            '未连接',  # 中文
        ]

        output_lower = output.lower()

        ethernet_connected = False
        for eth_keyword in ethernet_keywords:
            if eth_keyword.lower() in output_lower:
                sections = output_lower.split('adapter')
                for section in sections:
                    if eth_keyword.lower() in section:
                        if not any(disconn in section for disconn in disconnected_status):
                            ethernet_connected = True
                            break

        wifi_connected = False
        for wifi_keyword in wireless_keywords:
            if wifi_keyword.lower() in output_lower:
                sections = output_lower.split('adapter')
                for section in sections:
                    if any(keyword.lower() in section for keyword in wireless_keywords):
                        if not any(disconn in section for disconn in disconnected_status):
                            wifi_connected = True
                            break

        return {
            'ethernet': ethernet_connected,
            'wifi': wifi_connected,
            'language': current_locale
        }
    except Exception as e:
        print(f"Windows connection detect failed: {e}")
        return None


def detect_linux_network_multilingual():
    import os

    network_info = {'ethernet': False, 'wifi': False}

    interfaces_path = '/sys/class/net/'
    if os.path.exists(interfaces_path):
        for interface in os.listdir(interfaces_path):
            if interface.startswith('lo'):
                continue

            operstate_path = f'{interfaces_path}{interface}/operstate'
            carrier_path = f'{interfaces_path}{interface}/carrier'

            is_up = False
            if os.path.exists(operstate_path):
                with open(operstate_path, 'r') as f:
                    state = f.read().strip().lower()
                    if state in ['up', 'unknown']:
                        is_up = True
            elif os.path.exists(carrier_path):
                with open(carrier_path, 'r') as f:
                    carrier = f.read().strip()
                    if carrier == '1':
                        is_up = True

            if is_up:
                ethernet_patterns = [
                    r'^eth\d+$',  # eth0, eth1...
                    r'^enp\d+s\d+$',  # enp0s3, enp1s0...
                    r'^eno\d+$',  # eno1, eno2...
                    r'^ens\d+f\d+$',  # ens3f0, ens4f1...
                    r'^em\d+$',  # em1, em2...
                    r'^p\d+p\d+$',  # p1p1, p2p1...
                ]

                wifi_patterns = [
                    r'^wlan\d+$',  # wlan0, wlan1...
                    r'^wlp\d+s\d+$',  # wlp2s0, wlp3s0...
                    r'^ra\d+$',  # ra0, ra1... (Ralink)
                    r'^ath\d+$',  # ath0, ath1... (Atheros)
                    r'^wifi\d+$',  # wifi0...
                    r'^mon\d+$',  # monitor mode
                ]

                for pattern in ethernet_patterns:
                    if re.match(pattern, interface):
                        network_info['ethernet'] = True
                        break
                else:
                    for pattern in wifi_patterns:
                        if re.match(pattern, interface):
                            network_info['wifi'] = True
                            break

    return network_info


def detect_macos_network_multilingual():
    try:
        result = subprocess.run(['networksetup', '-listallhardwareports'],
                                capture_output=True, text=True, timeout=10)

        output = result.stdout

        ethernet_keywords = [
            'ethernet', 'ethernet adapter', 'ethernet interface',
            '以太网', '乙太網路', '랜선', 'проводной',
            'cable', 'réseau filaire', 'red cableada'
        ]

        wifi_keywords = [
            'wi-fi', 'airport', 'wireless', 'wifi',
            '無線', '와이파이', 'беспроводной',
            'sans fil', 'inalámbrico', 'wireless'
        ]

        network_info = {'ethernet': False, 'wifi': False}

        lines = output.split('\n')
        for i, line in enumerate(lines):
            if 'Hardware Port:' in line or '硬件端口:' in line or '硬體連接埠:' in line:
                port_name = line.split(':', 1)[1].strip() if ':' in line else ''

                if i + 1 < len(lines) and (
                        'Device:' in lines[i + 1] or '装置:' in lines[i + 1] or '裝置:' in lines[i + 1]):
                    device = lines[i + 1].split(':', 1)[1].strip() if ':' in lines[i + 1] else ''

                    try:
                        status_result = subprocess.run(['ifconfig', device],
                                                       capture_output=True, text=True, timeout=5)

                        status_text = status_result.stdout.lower()
                        if any(active_indicator in status_text for active_indicator in
                               ['status: active', 'running', 'active', 'running', 'actif', 'activo', 'aktiv']):

                            if any(keyword.lower() in port_name.lower() for keyword in ethernet_keywords):
                                network_info['ethernet'] = True
                            elif any(keyword.lower() in port_name.lower() for keyword in wifi_keywords):
                                network_info['wifi'] = True
                    except:
                        pass

        return network_info
    except Exception as e:
        print(f"macOS connection detect failed: {e}")
        return None


if __name__ == "__main__":
    print("开始多语言网络连接检测...")
    result = detect_network_type_multilingual()

    if result and isinstance(result, dict):
        print(f"\n检测结果:")
        print(f"有线连接: {'已连接' if result.get('ethernet', False) else '未连接'}")
        print(f"无线连接: {'已连接' if result.get('wifi', False) else '未连接'}")
    else:
        print("网络检测失败或不支持的操作系统")