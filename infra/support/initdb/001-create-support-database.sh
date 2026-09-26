#!/bin/sh
set -eu

# Executado automaticamente pelo entrypoint somente em um cluster vazio.
exec /opt/koddahub-support/scripts/bootstrap-existing.sh
