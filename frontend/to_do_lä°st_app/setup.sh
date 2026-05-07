#!/bin/bash

echo "🎨 Frontend Setup Script"
echo "======================="

# Check Node.js version
NODE_VERSION=$(node -v)
echo "✓ Node.js version: $NODE_VERSION"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

# Create .env.local
echo ""
echo "🔐 Creating .env.local..."
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8080/api
NEXT_PUBLIC_APP_NAME=My App
EOF

echo "✓ .env.local created"

# Create necessary directories
echo ""
echo "📁 Creating directory structure..."
mkdir -p src/components
mkdir -p src/pages
mkdir -p src/services
mkdir -p src/hooks
mkdir -p src/types
mkdir -p src/utils
mkdir -p src/styles

echo "✓ Directories created"

# Initialize git
if [ ! -d ".git" ]; then
  git init
  git add .
  git commit -m "Initial frontend setup"
fi

echo ""
echo "✅ Frontend setup complete!"
echo ""
echo "Next steps:"
echo "  npm run dev      - Start development server"
echo "  npm run build    - Build for production"
echo "  npm run lint     - Run linter"
echo "  npm run format   - Format code"
