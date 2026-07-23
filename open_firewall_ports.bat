@echo off
echo Opening firewall ports for Android emulator...
netsh advfirewall firewall add rule name="AI-App Vite 5173" dir=in action=allow protocol=TCP localport=5173
netsh advfirewall firewall add rule name="AI-App API 8000" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="AI-App ComfyUI 8188" dir=in action=allow protocol=TCP localport=8188
echo Done! Now tap Retry in the emulator.
pause
