import os
import sys
import requests
import subprocess
import shutil
import time
import json
from colorama import init, Fore, Style
from tqdm import tqdm
import winreg
import psutil
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print(Fore.RED + "Bu uygulama yönetici izni gerektiriyor!" + Style.RESET_ALL)
    print(Fore.YELLOW + "Lütfen uygulamayı yönetici olarak çalıştırın." + Style.RESET_ALL)
    input("Devam etmek için bir tuşa basın...")
    sys.exit(1)

init(autoreset=True)

class ChiaSistan:
    def __init__(self):
        self.versiyon = "1.0.2"
        self.github_repo = "https://raw.githubusercontent.com/ensorchia/chiasistan/main/version.json"
        self.kategoriler = {
            "1": "Tarayıcılar",
            "2": "Oyun Başlatıcılar",
            "3": "Yazılım Araçları",
            "4": "Sistem Araçları"
        }
        
        self.uygulamalar = {
            "1": {
                "1": {"isim": "Google Chrome", "url": "https://dl.google.com/chrome/install/latest/chrome_installer.exe"},
                "2": {"isim": "Brave", "url": "https://laptop-updates.brave.com/latest/winx64"},
                "3": {"isim": "Opera GX", "url": "https://download.opera.com/download/get/?id=62612&location=415&nothanks=yes&sub=marine"},
                "4": {"isim": "Firefox", "url": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=tr"}
            },
            "2": {
                "1": {"isim": "Steam", "url": "https://cdn.cloudflare.steamstatic.com/client/installer/SteamSetup.exe"},
                "2": {"isim": "Epic Games", "url": "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi"},
                "3": {"isim": "EA App", "url": "https://origin-a.akamaihd.net/EA-Desktop-Client-Download/installer-releases/EAappInstaller.exe"},
                "4": {"isim": "Ubisoft Connect", "url": "https://ubistatic3-a.akamaihd.net/orbit/launcher_installer/UbisoftConnectInstaller.exe"}
            },
            "3": {
                "1": {"isim": "Visual Studio Code", "url": "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64"},
                "2": {"isim": "Visual Studio 2022", "url": "https://aka.ms/vs/17/release/vs_community.exe"}
            },
            "4": {
                "1": {"isim": "Microsoft Edge Kaldırıcı", "fonksiyon": self.edge_kaldir},
                "2": {"isim": "Bilgisayari Hızlandır", "fonksiyon": self.pc_optimize},
                "3": {"isim": "Driver Güncelle", "fonksiyon": self.driver_guncelle}
            }
        }

    def ekrani_temizle(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def baslik_yazdir(self):
        self.ekrani_temizle()
        print(Fore.CYAN + """
 
   _____ _    _ _____           _____ _____  _____ _______       _   _ 
  / ____| |  | |_   _|   /\    / ____|_   _|/ ____|__   __|/\   | \ | |
 | |    | |__| | | |    /  \  | (___   | | | (___    | |  /  \  |  \| |
 | |    |  __  | | |   / /\ \  \___ \  | |  \___ \   | | / /\ \ | . ` |
 | |____| |  | |_| |_ / ____ \ ____) |_| |_ ____) |  | |/ ____ \| |\  |
  \_____|_|  |_|_____/_/    \_\_____/|_____|_____/   |_/_/    \_\_| \_|
                                                                       
                                                                       

        """ + Style.RESET_ALL)
        print(Fore.YELLOW + "Bilgisayar Asistanı ve Uygulama Yükleyici" + Style.RESET_ALL)
        print("=" * 50)

    def dosya_indir(self, url, dosya_adi):
        try:
            response = requests.get(url, stream=True)
            toplam_boyut = int(response.headers.get('content-length', 0))
            
            with open(dosya_adi, 'wb') as dosya, tqdm(
                desc=dosya_adi,
                total=toplam_boyut,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    boyut = dosya.write(data)
                    bar.update(boyut)
            return True
        except Exception as e:
            print(Fore.RED + f"Hata: {str(e)}" + Style.RESET_ALL)
            return False

    def uygulama_kur(self, url, isim):
        print(Fore.GREEN + f"\n{isim} indiriliyor..." + Style.RESET_ALL)
        dosya_adi = f"{isim.replace(' ', '_')}.exe"
        
        if self.dosya_indir(url, dosya_adi):
            print(Fore.GREEN + f"\n{isim} kuruluyor..." + Style.RESET_ALL)
            subprocess.run([dosya_adi], shell=True)
            os.remove(dosya_adi)
            print(Fore.GREEN + f"\n{isim} başarıyla kuruldu!" + Style.RESET_ALL)
            time.sleep(1)
        else:
            print(Fore.RED + f"\n{isim} kurulumu başarısız oldu!" + Style.RESET_ALL)
            time.sleep(1)

    def edge_kaldir(self):
        try:
            print(Fore.YELLOW + "\nMicrosoft Edge kaldırılıyor..." + Style.RESET_ALL)
            subprocess.run(['powershell', 'Get-AppxPackage *Microsoft.MicrosoftEdge* | Remove-AppxPackage'], shell=True)
            print(Fore.GREEN + "Microsoft Edge başarıyla kaldırıldı!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Hata: {str(e)}" + Style.RESET_ALL)

    def pc_optimize(self):
        try:
            print(Fore.YELLOW + "\nBilgisayar optimize ediliyor..." + Style.RESET_ALL)
            
          
            temp_dir = os.environ.get('TEMP')
            for item in os.listdir(temp_dir):
                try:
                    path = os.path.join(temp_dir, item)
                    if os.path.isfile(path):
                        os.unlink(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
                except Exception:
                    continue
            
        
            subprocess.run(['cleanmgr', '/sagerun:1'], shell=True)
            
            print(Fore.GREEN + "Bilgisayar başarıyla optimize edildi!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Hata: {str(e)}" + Style.RESET_ALL)

    def driver_guncelle(self):
        try:
            print(Fore.YELLOW + "\nDriver güncellemeleri kontrol ediliyor..." + Style.RESET_ALL)
            subprocess.run(['pnputil', '/scan-devices'], shell=True)
            print(Fore.GREEN + "Driver güncellemeleri kontrol edildi!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Hata: {str(e)}" + Style.RESET_ALL)

    def guncelleme_kontrol(self):
        try:
            print(Fore.YELLOW + "\nGüncellemeler kontrol ediliyor..." + Style.RESET_ALL)
            response = requests.get(self.github_repo)
            if response.status_code == 200:
                son_versiyon = response.json().get('version')
                if son_versiyon != self.versiyon:
                    print(Fore.GREEN + f"Yeni güncelleme bulundu! Versiyon: {son_versiyon}" + Style.RESET_ALL)
                    print(Fore.YELLOW + "Uygulama güncelleniyor..." + Style.RESET_ALL)
                    self.uygulamayi_guncelle()
                else:
                    print(Fore.GREEN + "Uygulama güncel!" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Güncelleme kontrolü sırasında hata: {str(e)}" + Style.RESET_ALL)

    def uygulamayi_guncelle(self):
        print("Güncelleme başlatılıyor...")
        updater_path = os.path.join(os.path.dirname(sys.executable), "updater.exe")
        os.startfile(updater_path)
        sys.exit(0)

    def menu_goster(self):
        self.guncelleme_kontrol()
        while True:
            self.baslik_yazdir()
            print("\nKategoriler:")
            for key, value in self.kategoriler.items():
                print(f"{key}. {value}")
            
            print("\n0. Çıkış")
            secim = input("\nKategori seçin (0-4): ")
            
            if secim == "0":
                break
            elif secim in self.kategoriler:
                self.kategori_goster(secim)
            else:
                print(Fore.RED + "Geçersiz seçim!" + Style.RESET_ALL)
                time.sleep(1)

    def kategori_goster(self, kategori):
        while True:
            self.baslik_yazdir()
            print(f"\n{self.kategoriler[kategori]} Kategorisi:")
            
            for key, value in self.uygulamalar[kategori].items():
                print(f"{key}. {value['isim']}")
            
            print("\n0. Geri")
            secim = input("\nUygulama seçin: ")
            
            if secim == "0":
                break
            elif secim in self.uygulamalar[kategori]:
                uygulama = self.uygulamalar[kategori][secim]
                if 'url' in uygulama:
                    self.uygulama_kur(uygulama['url'], uygulama['isim'])
                elif 'fonksiyon' in uygulama:
                    uygulama['fonksiyon']()
            else:
                print(Fore.RED + "Geçersiz seçim!" + Style.RESET_ALL)
                time.sleep(1)

if __name__ == "__main__":
    uygulama = ChiaSistan()
    uygulama.menu_goster() 
