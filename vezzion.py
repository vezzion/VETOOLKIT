#!/usr/bin/env python3
"""
VEZZION SECURITY TOOLKIT v3.0
Advanced Ethical Hacking Framework
For Educational & Authorized Use Only
"""

import socket
import sys
import threading
import subprocess
import os
import hashlib
import time
import re
import random
import signal
from datetime import datetime

# ==================== COLORS ====================
class C:
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    PURPLE  = '\033[95m'
    CYAN    = '\033[96m'
    WHITE   = '\033[97m'
    BOLD    = '\033[1m'
    DIM     = '\033[2m'
    RESET   = '\033[0m'
    BG_CYAN = '\033[46m'
    BLACK   = '\033[30m'

# ==================== HELPERS ====================
def clear():
    os.system('clear')

def banner(title, color=C.CYAN):
    w = 66
    print(f"\n{color}{C.BOLD}╔{'═'*w}╗")
    print(f"║{title.center(w)}║")
    print(f"╚{'═'*w}╝{C.RESET}\n")

def info(msg):   print(f"{C.CYAN}[*]{C.RESET} {msg}")
def success(msg):print(f"{C.GREEN}[+]{C.RESET} {msg}")
def error(msg):  print(f"{C.RED}[-]{C.RESET} {msg}")
def warn(msg):   print(f"{C.YELLOW}[!]{C.RESET} {msg}")
def ask(msg):    return input(f"{C.YELLOW}[?]{C.RESET} {msg}").strip()

def divider(color=C.DIM):
    print(f"{color}{'─'*68}{C.RESET}")

# ==================== MAIN BANNER ====================
def print_banner():
    clear()
    print(f"{C.CYAN}{C.BOLD}")
    print(r"  ██╗   ██╗███████╗███████╗███████╗██╗ ██████╗ ███╗   ██╗")
    print(r"  ██║   ██║██╔════╝╚══███╔╝╚══███╔╝██║██╔═══██╗████╗  ██║")
    print(r"  ██║   ██║█████╗    ███╔╝   ███╔╝ ██║██║   ██║██╔██╗ ██║")
    print(r"  ╚██╗ ██╔╝██╔══╝   ███╔╝   ███╔╝  ██║██║   ██║██║╚██╗██║")
    print(r"   ╚████╔╝ ███████╗███████╗███████╗██║╚██████╔╝██║ ╚████║")
    print(r"    ╚═══╝  ╚══════╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝")
    print(f"{C.RESET}")
    print(f"  {C.DIM}{'─'*56}{C.RESET}")
    print(f"  {C.WHITE}  Advanced Ethical Hacking Toolkit  {C.YELLOW}v3.0 Titan{C.RESET}")
    print(f"  {C.DIM}  Authorized & Educational Use Only{C.RESET}")
    print(f"  {C.DIM}{'─'*56}{C.RESET}\n")

# ==================== MENU ====================
def print_menu():
    print(f"{C.BOLD}{C.CYAN}  ┌─────────────────────────────────────────────────────┐{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}  │                    MAIN  MENU                       │{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}  ├──────┬──────────────────────┬───────────────────────┤{C.RESET}")

    modules = [
        ("01", "Network Scanner",     "Port scan + OS detect + banners"),
        ("02", "Hash Cracker",        "MD5 / SHA1 / SHA256 dictionary"),
        ("03", "Subdomain Finder",    "DNS enumeration & discovery"),
        ("04", "Password Generator",  "Entropy-based secure passwords"),
        ("05", "Whois Lookup",        "Domain information gathering"),
        ("06", "DNS Recon",           "A, MX, NS, TXT record enum"),
        ("07", "Wordlist Generator",  "Custom mutation wordlists"),
        ("08", "MAC Changer",         "Spoof interface MAC address"),
        ("09", "Banner Grabber",      "Service version fingerprinting"),
        ("10", "Live Host Monitor",   "Real-time network host detection"),
        ("99", "About",               "Toolkit information"),
        ("00", "Exit",                "Quit Vezzion"),
    ]

    for num, name, desc in modules:
        color = C.RED if num == "00" else C.YELLOW
        print(f"{C.CYAN}  │  {color}{C.BOLD}{num}{C.RESET}{C.CYAN}  │ {C.WHITE}{name:<22}{C.RESET}{C.DIM}{desc:<23}{C.CYAN}│{C.RESET}")

    print(f"{C.BOLD}{C.CYAN}  └──────┴──────────────────────┴───────────────────────┘{C.RESET}\n")

# ==================== 01: NETWORK SCANNER ====================
def scan_port(ip, port, results):
    try:
        s = socket.socket()
        s.settimeout(0.3)
        if s.connect_ex((ip, port)) == 0:
            try:
                s.send(b"\r\n")
                b = s.recv(256).decode(errors='ignore').strip()[:50]
            except:
                b = ""
            results.append((port, b))
        s.close()
    except:
        pass

def os_guess(ip):
    try:
        r = subprocess.run(['ping','-c','1','-W','1',ip], capture_output=True, timeout=2)
        m = re.search(r'ttl=(\d+)', r.stdout.decode(), re.I)
        if m:
            t = int(m.group(1))
            if t <= 64:  return "Linux / Unix"
            if t <= 128: return "Windows"
            return "Solaris / AIX"
    except: pass
    return "Unknown"

SERVICE = {21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",
           110:"POP3",143:"IMAP",443:"HTTPS",445:"SMB",3306:"MySQL",
           3389:"RDP",5432:"Postgres",5900:"VNC",8080:"HTTP-Alt",8443:"HTTPS-Alt"}

def network_scanner():
    clear(); banner("  ADVANCED NETWORK SCANNER  ")
    target = ask("Target IP or domain: ")
    if not re.match(r'^\d+\.\d+\.\d+\.\d+$', target):
        try:
            resolved = socket.gethostbyname(target)
            success(f"Resolved → {resolved}")
            target = resolved
        except:
            error("Cannot resolve domain"); return

    print(f"\n  {C.CYAN}[1]{C.RESET} Top 20 ports   {C.CYAN}[2]{C.RESET} 1–1000   {C.CYAN}[3]{C.RESET} Custom range")
    c = ask("Scan type: ")
    if   c == '1': ports = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,3306,3389,5432,5900,8080]
    elif c == '2': ports = list(range(1, 1001))
    else:
        s = int(ask("Start port: ")); e = int(ask("End port: "))
        ports = list(range(s, e+1))

    info(f"Scanning {C.BOLD}{target}{C.RESET} — {len(ports)} ports\n")
    results = []; threads = []; t0 = time.time()

    for p in ports:
        t = threading.Thread(target=scan_port, args=(target, p, results))
        threads.append(t); t.start()
        if len(threads) >= 150:
            for x in threads: x.join()
            threads = []
    for x in threads: x.join()

    elapsed = time.time() - t0
    divider()
    print(f"  {C.BOLD}Target:{C.RESET}  {target}")
    print(f"  {C.BOLD}OS:    {C.RESET}  {os_guess(target)}")
    print(f"  {C.BOLD}Time:  {C.RESET}  {elapsed:.2f}s")
    print(f"  {C.BOLD}Open:  {C.RESET}  {C.GREEN}{len(results)} ports{C.RESET}")
    divider()
    if results:
        print(f"\n  {C.BOLD}{'PORT':<8}{'SERVICE':<14}BANNER{C.RESET}")
        print(f"  {'─'*60}")
        for port, ban in sorted(results):
            svc = SERVICE.get(port, "Unknown")
            print(f"  {C.GREEN}{port:<8}{C.RESET}{C.CYAN}{svc:<14}{C.RESET}{C.DIM}{ban}{C.RESET}")
    else:
        warn("No open ports found in range")
    input(f"\n  {C.DIM}Press Enter to return...{C.RESET}")

# ==================== 02: HASH CRACKER ====================
def hash_cracker():
    clear(); banner("  HASH CRACKER  ", C.PURPLE)
    h = ask("Enter hash: ")
    ht = {32:"MD5", 40:"SHA1", 64:"SHA256"}.get(len(h), "Unknown")
    info(f"Detected: {C.BOLD}{ht}{C.RESET}")

    wl = ask("Wordlist path (or 'rockyou'): ")
    if wl == 'rockyou': wl = "/usr/share/wordlists/rockyou.txt"

    info("Starting attack...\n")
    found = None; tried = 0; t0 = time.time()

    def check(word):
        if ht == "MD5":    return hashlib.md5(word.encode()).hexdigest() == h
        if ht == "SHA1":   return hashlib.sha1(word.encode()).hexdigest() == h
        if ht == "SHA256": return hashlib.sha256(word.encode()).hexdigest() == h
        return False

    try:
        if os.path.exists(wl):
            with open(wl, 'r', errors='ignore') as f:
                for line in f:
                    w = line.strip(); tried += 1
                    if tried % 50000 == 0:
                        print(f"  {C.DIM}Tried {tried:,} words...{C.RESET}", end='\r')
                    if check(w): found = w; break
        else:
            warn("Wordlist not found — using built-in list")
            for w in ["password","123456","admin","letmein","welcome","root","toor","qwerty"]:
                tried += 1
                if check(w): found = w; break
    except KeyboardInterrupt:
        warn("Interrupted")

    divider()
    if found: success(f"Password found: {C.BOLD}{C.GREEN}{found}{C.RESET}")
    else:     error("Not found in wordlist")
    print(f"  Tried {tried:,} words in {time.time()-t0:.2f}s")
    input(f"\n  {C.DIM}Press Enter to return...{C.RESET}")

# ==================== 03: SUBDOMAIN FINDER ====================
def subdomain_finder():
    clear(); banner("  SUBDOMAIN FINDER  ", C.BLUE)
    domain = ask("Domain (e.g. example.com): ")

    subs = ["www","mail","ftp","smtp","pop","ns1","ns2","ns3","webmail","cpanel",
            "m","imap","test","admin","blog","dev","vpn","api","cdn","app",
            "forum","news","beta","shop","secure","demo","portal","media",
            "static","docs","wiki","mobile","support","auth","login","dashboard"]

    info(f"Checking {len(subs)} subdomains on {C.BOLD}{domain}{C.RESET}\n")
    found = []

    for s in subs:
        full = f"{s}.{domain}"
        try:
            ip = socket.gethostbyname(full)
            found.append((full, ip))
            success(f"{C.BOLD}{full:<35}{C.RESET} → {C.GREEN}{ip}{C.RESET}")
        except:
            print(f"  {C.DIM}✗ {full}{C.RESET}", end='\r')

    divider()
    print(f"\n  Found {C.GREEN}{C.BOLD}{len(found)}{C.RESET} subdomains")
    input(f"\n  {C.DIM}Press Enter to return...{C.RESET}")

# ==================== 04: PASSWORD GENERATOR ====================
def password_generator():
    clear(); banner("  PASSWORD GENERATOR  ", C.YELLOW)
    length  = int(ask("Length (8-64): ") or "16")
    upper   = ask("Uppercase? (y/n): ").lower() == 'y'
    lower   = ask("Lowercase? (y/n): ").lower() == 'y'
    digits  = ask("Digits?    (y/n): ").lower() == 'y'
    special = ask("Symbols?   (y/n): ").lower() == 'y'
    count   = int(ask("How many?  (1-20): ") or "5")

    chars = ""
    if upper:   chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if lower:   chars += "abcdefghijklmnopqrstuvwxyz"
    if digits:  chars += "0123456789"
    if special: chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not chars: chars = "abcdefghijklmnopqrstuvwxyz0123456789"

    print()
    for i in range(count):
        pw = ''.join(random.choice(chars) for _ in range(length))
        entropy = len(chars).bit_length() * length
        if   entropy >= 100: lvl = f"{C.GREEN}Very Strong{C.RESET}"
        elif entropy >= 80:  lvl = f"{C.CYAN}Strong{C.RESET}"
        elif entropy >= 60:  lvl = f"{C.YELLOW}Medium{C.RESET}"
        else:                lvl = f"{C.RED}Weak{C.RESET}"
        print(f"  {C.DIM}{i+1:>2}.{C.RESET} {C.BOLD}{pw}{C.RESET}  {C.DIM}[{entropy}bits — {lvl}{C.DIM}]{C.RESET}")

    input(f"\n  {C.DIM}Press Enter to return...{C.RESET}")

# ==================== 05: WHOIS LOOKUP ====================
def whois_lookup():
    clear(); banner("  WHOIS LOOKUP  ", C.PURPLE)
    domain = ask("Domain: ")
    try:
        r = subprocess.run(['whois', domain], capture_output=True, text=True, timeout=10)
        print(f"\n{C.CYAN}{r.stdout[:2500]}{C.RESET}")
    except:
        error("whois failed — is it installed?")
    input(f"\n  {C.DIM}Press Enter to return...{C.RESET}")

# ==================== 06: DNS RECON ====================
def dns_recon():
    clear(); banner("  DNS RECON  ", C.CYAN)
    domain = ask("Domain: ")
    for rt in ['A','AAAA','MX','NS','TXT','CNAME','SOA']:
        try:
            r = subprocess.run(['dig','+short',rt,domain], capture_output=True, text=True, timeout=5)
            if r.stdout.strip():
                print(f"\n  {C.BOLD}{C.GREEN}{rt} Records:{C.RESET}")
                for line in r.stdout.strip().split('\n'):
                    print(f"    {C.CYAN}{line}{C.RESET}")
        except: pass
    input(f"\n  {C.DIM}Press Enter to return...{C.RESET}")

# ==================== 07: WORDLIST GENERATOR ====================
def wordlist_generator():
    clear(); banner("  WORDLIST GENERATOR  ", C.YELLOW)
    base = ask("Base word: ")
    out  = ask("Output file (wordlist.txt): ") or "wordlist.txt"

    leet = {'a':'@','e':'3','i':'1','o':'0','s':'$','t':'7','g':'9'}
    suffixes = ["","1","123","1234","!","@","2024","2025","#","admin","root","_1","_123"]

    words = set()
    words.update([base, base.lower(), base.upper(), base.capitalize()])
    lw = ''.join(leet.get(c,c) for c in base.lower())
    words.add(lw); words.add(lw.capitalize())

    for s in suffixes:
        words.add(base + s)
        words.add(base.capitalize() + s)
        words.add(s + base)

    with open(out,'w') as f:
        for w in sorted(words): f.write(w+'\n')

    success(f"Generated {C.BOLD}{len(words)}{C.RESET} words → {C.CYAN}{out}{C.RESET}")
    input(f"\n  {C.DIM}Press Enter to return...{C.RESET}")

# ==================== 08: MAC CHANGER ====================
def mac_changer():
    clear(); banner("  MAC CHANGER  ", C.RED)
    warn("Requires root privileges\n")
    iface = ask("Interface (eth0/wlan0): ")
    mac   = ask("New MAC or 'random': ")
    if mac == 'random':
        mac = ':'.join(f'{random.randint(0,255):02x}' for _ in range(6))
        info(f"Generated MAC: {C.BOLD}{mac}{C.RESET}")
    for cmd in [f"ip link set {iface} down",
                f"ip link set {iface} address {mac}",
                f"ip link set {iface} up"]:
        subprocess.run(cmd, shell=True)
    success(f"MAC changed to {C.BOLD}{mac}{C.RESET}")
    input(f"\n  {C.DIM}Press Enter to return...{C.RESET}")

# ==================== 09: BANNER GRABBER ====================
def banner_grabber():
    clear(); banner("  BANNER GRABBER  ", C.CYAN)
    target = ask("Target IP: ")
    port   = int(ask("Port: "))
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect((target, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        b = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        success("Banner grabbed:\n")
        print(f"  {C.CYAN}{b}{C.RESET}")
    except Exception as e:
        error(f"Failed: {e}")
    input(f"\n  {C.DIM}Press Enter to return...{C.RESET}")

# ==================== 10: LIVE MONITOR ====================
def live_monitor():
    clear(); banner("  LIVE HOST MONITOR  ", C.GREEN)
    warn("Press Ctrl+C to stop\n")
    net  = ask("Network prefix (e.g. 192.168.1): ")
    seen = set()
    info(f"Monitoring {net}.0/24 ...\n")
    try:
        while True:
            for i in range(1, 255):
                ip = f"{net}.{i}"
                r  = subprocess.run(['ping','-c','1','-W','1',ip],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if r.returncode == 0 and ip not in seen:
                    seen.add(ip)
                    ts = datetime.now().strftime("%H:%M:%S")
                    success(f"[{ts}] {C.BOLD}{ip}{C.RESET} is {C.GREEN}ALIVE{C.RESET}")
            time.sleep(5)
    except KeyboardInterrupt:
        warn(f"Stopped — {len(seen)} unique hosts detected")
    input(f"\n  {C.DIM}Press Enter to return...{C.RESET}")

# ==================== ABOUT ====================
def about():
    clear(); banner("  ABOUT VEZZION  ", C.PURPLE)
    print(f"  {C.BOLD}Name:{C.RESET}     Vezzion Security Toolkit")
    print(f"  {C.BOLD}Version:{C.RESET}  3.0 — Titan Edition")
    print(f"  {C.BOLD}Modules:{C.RESET}  10 security testing modules")
    print(f"  {C.BOLD}Purpose:{C.RESET}  Educational penetration testing\n")
    divider(C.YELLOW)
    warn("Only use on systems you OWN or have WRITTEN permission to test.")
    warn("Unauthorized access is illegal under CFAA and international law.")
    divider(C.YELLOW)
    input(f"\n  {C.DIM}Press Enter to return...{C.RESET}")

# ==================== MAIN ====================
def main():
    signal.signal(signal.SIGINT, lambda s,f: (print(f"\n{C.YELLOW}  Goodbye!{C.RESET}"), sys.exit(0)))

    dispatch = {
        '1':  network_scanner,  '01': network_scanner,
        '2':  hash_cracker,     '02': hash_cracker,
        '3':  subdomain_finder, '03': subdomain_finder,
        '4':  password_generator,'04':password_generator,
        '5':  whois_lookup,     '05': whois_lookup,
        '6':  dns_recon,        '06': dns_recon,
        '7':  wordlist_generator,'07':wordlist_generator,
        '8':  mac_changer,      '08': mac_changer,
        '9':  banner_grabber,   '09': banner_grabber,
        '10': live_monitor,
        '99': about,
    }

    while True:
        print_banner()
        print_menu()
        choice = input(f"  {C.YELLOW}┌─[{C.CYAN}VEZZION{C.YELLOW}@{C.CYAN}TITAN{C.YELLOW}]\n  └──▶ {C.RESET}").strip()

        if choice in ('0', '00'):
            print(f"\n  {C.GREEN}Stay ethical. Goodbye.{C.RESET}\n")
            sys.exit(0)
        elif choice in dispatch:
            dispatch[choice]()
        else:
            warn("Invalid option"); time.sleep(0.8)

if __name__ == "__main__":
    main()
