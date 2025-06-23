#!/bin/bash
gunicorn -b 0.0.0.0:${PORT:-5000} app:app
