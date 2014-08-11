#!/usr/bin/env bash
set -e

[ -z "$CHAG_DIR" ] && CHAG_DIR="/usr/local/bin"
[ -z "$CHAG_VERSION" ] && CHAG_VERSION="master"

CHAG_SOURCE="https://raw.githubusercontent.com/mtdowling/chag/$CHAG_VERSION/chag"

echo "=> Downloading chag to '$CHAG_DIR'"
curl -sS "$CHAG_SOURCE" -o "$CHAG_DIR/chag" || {
  echo >&2 "Failed to download '$CHAG_SOURCE'"
  return 1
}

echo "=> Setting executable permissions on $CHAG_DIR/chag"
chmod +x "$CHAG_DIR/chag" || {
  echo >&2 "Failed setting executable permission on $CHAG_DIR/chag"
  return 1
}

echo "chag is ready to use!"
