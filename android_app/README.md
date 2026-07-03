# Android APK build instructions

This folder contains a Kivy-based scaffold of the Budget App suitable for packaging to Android.

Prerequisites
- Linux environment (Ubuntu) or WSL2 with Android SDK/NDK installed, or use a CI runner with Buildozer.
- Install `buildozer` (https://github.com/kivy/buildozer) and required Android SDK/NDK toolchains.

Quick build (on Linux/WSL):
```bash
sudo apt update && sudo apt install -y python3-pip python3-venv git
python3 -m pip install --user buildozer
python3 -m pip install --user kivy
cd android_app
buildozer init    # will create buildozer.spec if needed
# edit buildozer.spec if required, then:
buildozer android debug
# resulting APK will be in bin/
```

Notes
- Building an APK requires Linux-based toolchain; Windows native Buildozer is not supported. Use WSL2 or a Linux VM.
- The Kivy scaffold focuses on core data entry and SQLite persistence. Some desktop features (Tkinter UI, exact theming, pie charts) are omitted — they can be added with Kivy widgets or by including additional Python libraries (be aware of binary dependencies).
