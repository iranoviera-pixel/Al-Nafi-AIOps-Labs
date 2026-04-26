#!/bin/bash

# Define routes (destination gateway)
declare -A ROUTES=(
  ["192.168.2.0/24"]="192.168.1.1"
  ["10.0.0.0/8"]="192.168.1.2"
)

# Add routes if they don't exist
for DEST in "${!ROUTES[@]}"; do
  GATEWAY="${ROUTES[$DEST]}"
  if ! ip route show | grep -q "$DEST"; then
    echo "Adding route: $DEST via $GATEWAY"
    sudo ip route add "$DEST" via "$GATEWAY"
  else
    echo "Route $DEST already exists."
  fi
done

# Verify
echo "Current routes:"
ip route show


