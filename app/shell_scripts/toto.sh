#!/usr/bin/env bash

# including demo-magic

. ./app/demo-magic.sh

# speed (defined by the user)

TYPE_SPEED=10
                    
# This should also be defined by the user...maybe later.

DEMO_PROMPT="${GREEN}➜ ${CYAN}\W "

# Clearing the prompt

clear

# The commands go here

pe "echo 'Hello world'"

# The end (shows a prompt at the end)

p ""
