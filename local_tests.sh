#!/bin/bash
raco pkg update --all

LOGLEVEL=info
MAJOR=5
MINOR=2
TEAM=team23
racket -O "$LOGLEVEL"@fest -W none -l software-construction-admin -- -M $MAJOR -m $MINOR -n "$TEAM"