[app]
title = Jeu de Mémoire
package.name = jeumemoire
package.domain = org.antigravity

source.dir = .
source.include_exts = py,kv,json,ttf,png,jpg

version = 1.0

requirements = python3==3.11.0,kivy==2.3.0,pydantic==2.5.0

orientation = portrait
fullscreen = 0

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33
android.arch = arm64-v8a

# Icône & splash
android.icon = data/images/logo.png
android.presplash = data/images/logo.png
android.presplash_color = #1E3A8A

[buildozer]
log_level = 2
warn_on_root = 1
