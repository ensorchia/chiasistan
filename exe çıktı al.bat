@echo off
echo chiasistan derleniyor...
pip install -r kutuphaneler.txt
pip install pyinstaller
pyinstaller --onefile --icon=NONE --name chiasistan chiasistan.py
echo Derleme tamamlandı!
echo chiasistan.exe dist klasöründe oluşturuldu.
pause 