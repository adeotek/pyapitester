# Python DevOps Tools

## Description

A collection of DevOps CLI tools written in Python

## Available tools

- `apitester` - A simple API tester where the requests are configured in a JSON file (see `configuration.sample.json` sample configuration)
- `dockerct` - Docker Containers management tool (create, update, remove)
- `utf8bom` - UTF8 file encoding converter

## Setup

### Install `venv` module

```powershell
pip3 install virtualenv
```

### Create environment

```powershell
# cd project_path
python3 -m venv env
```

### Activate environment

#### Windows

```powershell
.\env\Scripts\Activate.ps1
```

#### Linux

```bash
source env/bin/activate
```

### Upgrade `pip`

```powershell
python -m pip install --upgrade pip
```

### Deactivate environment

```powershell
deactivate
```

## Install tool from source

### For development

```powershell
python -m pip install --editable .
```

### For usage only

```powershell
python -m pip install .
```

## Publish to PyPi.org

### Prerequisite

```powershell
python -m pip install build twine
```

### Build

```powershell
python -m build
```

### Check

```powershell
twine check dist/*
```

### Upload

```powershell
twine upload dist/*
```
