#!/bin/bash
# REDMYTHOS CLAW 🦀 — One Command Installer for Termux
# Run: bash install.sh

set -e

RED='\033[0;31m'
WHITE='\033[1;37m'
DIM='\033[2m'
NC='\033[0m' # No Color

echo -e "${RED}"
echo " ██████╗ ██╗      █████╗ ███████╗███████╗██╗    ██╗██╗███╗   ██╗ ██████╗ "
echo "██╔════╝ ██║     ██╔══██╗██╔════╝██╔════╝██║    ██║██║████╗  ██║██╔════╝ "
echo "██║  ███╗██║     ███████║███████╗███████╗██║ █╗ ██║██║██╔██╗ ██║██║  ███╗"
echo "██║   ██║██║     ██╔══██║╚════██║╚════██║██║███╗██║██║██║╚██╗██║██║   ██║"
echo "╚██████╔╝███████╗██║  ██║███████║███████║╚███╔███╔╝██║██║ ╚████║╚██████╔╝"
echo " ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ "
echo -e "${WHITE}REDMYTHOS CLAW 🦀 Installer${NC}"
echo -e "${DIM}Refined by Mir mahmood khan${NC}"
echo ""

echo -e "${DIM}[1/5] Updating packages...${NC}"
pkg update -y 2>/dev/null || true

echo -e "${DIM}[2/5] Installing system dependencies...${NC}"
pkg install -y python python-pip git curl 2>/dev/null || true

echo -e "${DIM}[3/5] Installing Python dependencies...${NC}"
pip install -r requirements.txt --break-system-packages --quiet

echo -e "${DIM}[4/5] Setting up ~/.redmythos/ structure...${NC}"
python3 -c "from config.setup import ensure_setup; ensure_setup()"

echo -e "${DIM}[5/5] Making executable...${NC}"
chmod +x main.py

# Create launcher script
cat > ~/.local/bin/redmythosclaw << 'EOF'
#!/bin/bash
REDMYTHOS_DIR="$HOME/redmythos-claw"
if [ -d "$REDMYTHOS_DIR" ]; then
    cd "$REDMYTHOS_DIR"
    python3 main.py "$@"
else
    echo "❌ REDMYTHOS CLAW not found at $REDMYTHOS_DIR"
fi
EOF

mkdir -p ~/.local/bin
chmod +x ~/.local/bin/redmythosclaw 2>/dev/null || true



echo ""
echo -e "${RED}✅ REDMYTHOS CLAW installed!${NC}"
echo ""
echo -e "${WHITE}Next steps:${NC}"
echo -e "  1. Add your Gemini API key:"
echo -e "     ${DIM}nano ~/.redmythos/config.json${NC}"
echo -e "     Get free key: https://aistudio.google.com/apikey"
echo ""
echo -e "  2. Start REDMYTHOS CLAW:"
echo -e "     ${RED}python3 main.py${NC}"
echo ""
echo -e "  3. Switch modes:"
echo -e "     ${DIM}/mode active_mode${NC}"
echo -e "     ${DIM}/mode building_mode${NC}"
echo -e "     ${DIM}/mode new_mode${NC}"
echo ""
echo -e "  4. Add custom modes:"
echo -e "     ${DIM}Drop any .md file in ~/.redmythos/modes/${NC}"
echo ""
echo -e "${RED}🦀 Happy Hacking!${NC}"
