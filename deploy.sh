#!/bin/bash

echo "🚀 QuantumQR - Quick Deployment Helper"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1: Checking if you're in the right directory...${NC}"
cd "/Users/majid/Desktop/QR Code Generator"

echo -e "${GREEN}✓ Current directory: $(pwd)${NC}"
echo ""

echo -e "${BLUE}Step 2: Checking for Git repository...${NC}"
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
    git branch -M main
    echo -e "${GREEN}✓ Git initialized${NC}"
else
    echo -e "${GREEN}✓ Git repository exists${NC}"
fi
echo ""

echo -e "${BLUE}Step 3: Adding all files to Git...${NC}"
git add .

echo ""

read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Initial commit - QuantumQR ready for deployment"
fi

git commit -m "$commit_msg"
echo -e "${GREEN}✓ Files committed${NC}"
echo ""

echo -e "${BLUE}Step 4: Ready to push to GitHub!${NC}"
echo ""
echo "Next steps:"
echo "1. Go to: https://github.com/new"
echo "2. Create a new repository called 'quantumqr'"
echo "3. Come back here and run:"
echo ""
echo "   git remote add origin https://github.com/YOUR-USERNAME/quantumqr.git"
echo "   git push -u origin main"
echo ""
echo "OR just copy-paste this:"
echo ""
echo -e "${GREEN}   git remote add origin YOUR_REPO_URL${NC}"
echo -e "${GREEN}   git push -u origin main${NC}"
echo ""
echo "Then deploy on Render.com:"
echo -e "${BLUE}   https://render.com → New Web Service → Connect GitHub${NC}"
echo ""

