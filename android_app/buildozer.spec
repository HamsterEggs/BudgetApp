[app]
title = Budget App
package.name = budgetappandroid
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,svg,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
android.permissions = 
android.api = 33
android.ndk = 25b
# (For full builds run on Linux/WSL or use CI) 

[buildozer]
log_level = 2
warn_on_root = 1
