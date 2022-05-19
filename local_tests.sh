#!/bin/bash
raco pkg update --all

LOGLEVEL=info
MAJOR=8
MINOR=1
TEAM=team23
racket -O "$LOGLEVEL"@fest -W none -l software-construction-admin -- -M $MAJOR -m $MINOR -n "$TEAM"