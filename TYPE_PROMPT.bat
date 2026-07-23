@echo off
set ADB=C:\Users\Shaik Sameena\AppData\Local\Android\Sdk\platform-tools\adb.exe

echo Tapping the text field...
"%ADB%" shell input tap 553 927

ping 127.0.0.1 -n 2 >nul

echo Clearing existing text...
"%ADB%" shell input keyevent KEYCODE_CTRL_A
"%ADB%" shell input keyevent KEYCODE_DEL

echo Typing prompt...
"%ADB%" shell input text "a%srunning%scar"

ping 127.0.0.1 -n 2 >nul

echo Tapping Generate button...
"%ADB%" shell input tap 553 1224

echo Done! Generation started.
pause
