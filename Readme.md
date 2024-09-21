# CQIL-Demo

## Introduction

This is a preliminary demo repository for interactively [CQIL](https://github.com/Photooon/CQIL) demonstration. The demo is built based on Vue and Django (with websocket). We are working to make it easier to use. Please excuse the current simplicity of the project.

## Quick Usage

Launch vue ui to open the front-end in hot compilation mode:
```bash
cd front-end
vue ui
```

Make sure you have prepared the base model and cqil model correctly under `server/models`. For example `server/models/Qwen1.5-14B` and `server/models/cqil-qwen1.5b-14b`. The server will place cqil model on gpu0 and base model on gpu1.

Run server:
```bash
python manage.py runserver [PORT]
```