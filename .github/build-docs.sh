#!/bin/sh

# Try to use nvm to set Node.js version if available
if [ -f "$HOME/.nvm/nvm.sh" ]; then
  . "$HOME/.nvm/nvm.sh"
  nvm install 20
  nvm use 20
fi

cd docs && npm install && npm run build
