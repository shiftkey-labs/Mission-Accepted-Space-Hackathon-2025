#!/bin/bash

# SatelLocator Development Server Starter
# This script ensures you're using the correct Node version

echo "🛰️  SatelLocator - Starting Development Server"
echo ""

# Check if nvm is available
if command -v nvm &> /dev/null; then
    echo "✓ nvm detected"
    echo "→ Switching to Node 20..."
    nvm use 20
    echo ""
else
    echo "⚠️  nvm not found - checking Node version..."
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 20 ]; then
        echo "❌ Node version $NODE_VERSION detected"
        echo "   Next.js 16 requires Node.js >=20.9.0"
        echo ""
        echo "Please upgrade Node.js:"
        echo "  - Install nvm: https://github.com/nvm-sh/nvm"
        echo "  - Or download Node 20+: https://nodejs.org/"
        exit 1
    fi
    echo "✓ Node version compatible"
    echo ""
fi

# Start the dev server
echo "🚀 Starting Next.js development server..."
echo "   Open http://localhost:3000 in your browser"
echo ""
echo "   Press Ctrl+C to stop"
echo ""

npm run dev

