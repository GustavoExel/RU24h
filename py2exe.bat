pyinstaller --noconsole --icon=icon.ico --onefile RU24h.py
rm RU24h.spec
rm -r build
mv dist/RU24h.exe .
rm -r dist