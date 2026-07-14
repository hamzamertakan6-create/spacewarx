[app]
title = SpaceWarx
package.name = spacewarx
package.domain = com.spacewarx.game
source.dir = .
source.include_exts = py,png,ttf,json,atlas,wav
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 1
icon.filename = %(source.dir)s/assets/icon.png

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
