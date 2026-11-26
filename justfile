set quiet
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# List recipes
default:
    just --list
