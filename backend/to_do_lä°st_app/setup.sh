#!/bin/bash

echo "🚀 Backend Maven Setup Script"
echo "============================="

# Check Java version
JAVA_VERSION=$(java -version 2>&1 | head -1)
echo "✓ Java version: $JAVA_VERSION"

# Check Maven
MVN_VERSION=$(mvn -v | head -1)
echo "✓ Maven version: $MVN_VERSION"

# Install dependencies
echo ""
echo "📦 Installing Maven dependencies..."
mvn clean install

# Create directory structure
echo ""
echo "📁 Creating directory structure..."
mkdir -p src/main/java/com/example
mkdir -p src/main/resources
mkdir -p src/test/java/com/example
mkdir -p target

echo "✓ Directories created"

# Initialize git
if [ ! -d ".git" ]; then
  git init
  git add .
  git commit -m "Initial backend setup"
fi

echo ""
echo "✅ Backend setup complete!"
echo ""
echo "Next steps:"
echo "  mvn clean compile - Compile the project"
echo "  mvn spring-boot:run - Run the application"
echo "  mvn test          - Run tests"
