
#!/bin/bash

# FlowState Development Environment Setup Script
# Sets up complete development environment with progressive complexity support
# Usage: ./setup_dev_environment.sh [complexity_level] [options]

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Default values
COMPLEXITY_LEVEL="essential"
FORCE_REINSTALL=false
SKIP_DOCKER=false
SKIP_DATABASE=false
SKIP_AI_SETUP=false
VERBOSE=false
QUICK_SETUP=false
OFFLINE_MODE=false
DEV_TOOLS_ONLY=false

# Platform detection
OS_TYPE=""
ARCH_TYPE=""
PACKAGE_MANAGER=""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Progress tracking
declare -A setup_status
total_steps=0
completed_steps=0

# Logging functions
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

log_success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
    ((completed_steps++))
}

log_warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

log_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

log_info() {
    echo -e "${CYAN}[INFO] $1${NC}"
}

log_step() {
    echo -e "${PURPLE}[STEP $((completed_steps + 1))/$total_steps] $1${NC}"
}

# Progress bar
show_progress() {
    local progress=$((completed_steps * 100 / total_steps))
    local filled=$((progress / 2))
    local empty=$((50 - filled))
    
    printf "\r${BLUE}Progress: ["
    printf "%${filled}s" | tr ' ' '='
    printf "%${empty}s" | tr ' ' '-'
    printf "] %d%% (%d/%d)${NC}" "$progress" "$completed_steps" "$total_steps"
    
    if [[ $completed_steps -eq $total_steps ]]; then
        echo ""
    fi
}

# Help function
show_help() {
    cat << EOF
FlowState Development Environment Setup

Usage: $0 [COMPLEXITY_LEVEL] [OPTIONS]

COMPLEXITY_LEVELS:
    essential       - Layer 0: Basic time tracking development setup (default)
    enhanced        - Layer 1: Enhanced features with analytics and team tools
    advanced        - Layer 2: Full AI/ML development environment

OPTIONS:
    --force         - Force reinstall of all components
    --skip-docker   - Skip Docker and container setup
    --skip-database - Skip database setup
    --skip-ai       - Skip AI/ML development tools setup
    --verbose       - Enable verbose output
    --quick         - Quick setup with minimal components
    --offline       - Offline mode (use cached packages only)
    --dev-tools     - Install only development tools (no services)
    --help          - Show this help message

EXAMPLES:
    $0                              # Setup essential development environment
    $0 enhanced                     # Setup with analytics and team features
    $0 advanced --verbose           # Full setup with AI/ML tools and verbose output
    $0 --quick --skip-docker        # Quick setup without Docker
    $0 --dev-tools                  # Install only development tools

REQUIREMENTS:
    - macOS 10.15+, Ubuntu 18.04+, or Windows 10+ with WSL2
    - At least 8GB RAM (16GB recommended for advanced setup)
    - 10GB free disk space (20GB for advanced setup)
    - Internet connection (unless --offline mode)

ENVIRONMENT VARIABLES:
    FLOWSTATE_DEV_DB    - Development database URL override
    FLOWSTATE_AI_KEY    - AI service API key for advanced features
    DOCKER_HOST         - Docker host override
    NODE_VERSION        - Node.js version to install (default: 18)
EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            essential|enhanced|advanced)
                COMPLEXITY_LEVEL="$1"
                shift
                ;;
            --force)
                FORCE_REINSTALL=true
                shift
                ;;
            --skip-docker)
                SKIP_DOCKER=true
                shift
                ;;
            --skip-database)
                SKIP_DATABASE=true
                shift
                ;;
            --skip-ai)
                SKIP_AI_SETUP=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                set -x
                shift
                ;;
            --quick)
                QUICK_SETUP=true
                shift
                ;;
            --offline)
                OFFLINE_MODE=true
                shift
                ;;
            --dev-tools)
                DEV_TOOLS_ONLY=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Detect platform and architecture
detect_platform() {
    log_step "Detecting platform and architecture..."

    case "$(uname -s)" in
        Darwin*)
            OS_TYPE="macos"
            PACKAGE_MANAGER="brew"
            ;;
        Linux*)
            OS_TYPE="linux"
            if command -v apt-get &> /dev/null; then
                PACKAGE_MANAGER="apt"
            elif command -v yum &> /dev/null; then
                PACKAGE_MANAGER="yum"
            elif command -v pacman &> /dev/null; then
                PACKAGE_MANAGER="pacman"
            else
                log_error "Unsupported Linux distribution"
                exit 1
            fi
            ;;
        CYGWIN*|MINGW*|MSYS*)
            OS_TYPE="windows"
            PACKAGE_MANAGER="chocolatey"
            ;;
        *)
            log_error "Unsupported operating system: $(uname -s)"
            exit 1
            ;;
    esac

    case "$(uname -m)" in
        x86_64|amd64)
            ARCH_TYPE="x64"
            ;;
        arm64|aarch64)
            ARCH_TYPE="arm64"
            ;;
        *)
            log_error "Unsupported architecture: $(uname -m)"
            exit 1
            ;;
    esac

    log_success "Platform detected: $OS_TYPE ($ARCH_TYPE) with $PACKAGE_MANAGER"
}

# Check system requirements
check_requirements() {
    log_step "Checking system requirements..."

    # Check available memory
    local memory_gb=0
    case $OS_TYPE in
        macos)
            memory_gb=$(( $(sysctl -n hw.memsize) / 1024 / 1024 / 1024 ))
            ;;
        linux)
            memory_gb=$(( $(grep MemTotal /proc/meminfo | awk '{print $2}') / 1024 / 1024 ))
            ;;
        windows)
            # Windows check would need to be implemented
            memory_gb=8  # Assume minimum
            ;;
    esac

    local required_memory=8
    if [[ "$COMPLEXITY_LEVEL" == "advanced" ]]; then
        required_memory=16
    fi

    if [[ $memory_gb -lt $required_memory ]]; then
        log_warning "System has ${memory_gb}GB RAM, but ${required_memory}GB is recommended for $COMPLEXITY_LEVEL setup"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    # Check disk space
    local available_space
    available_space=$(df "$PROJECT_ROOT" | awk 'NR==2 {print $4}')
    local available_gb=$((available_space / 1024 / 1024))
    
    local required_space=10
    if [[ "$COMPLEXITY_LEVEL" == "advanced" ]]; then
        required_space=20
    fi

    if [[ $available_gb -lt $required_space ]]; then
        log_error "Insufficient disk space. Available: ${available_gb}GB, Required: ${required_space}GB"
        exit 1
    fi

    # Check internet connection (unless offline mode)
    if [[ "$OFFLINE_MODE" == "false" ]]; then
        if ! ping -c 1 google.com &> /dev/null; then
            log_warning "No internet connection detected. Some packages may not install."
            read -p "Continue with offline mode? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                OFFLINE_MODE=true
            else
                exit 1
            fi
        fi
    fi

    log_success "System requirements check completed"
}

# Install package manager if needed
install_package_manager() {
    log_step "Setting up package manager..."

    case $OS_TYPE in
        macos)
            if ! command -v brew &> /dev/null; then
                log "Installing Homebrew..."
                if [[ "$OFFLINE_MODE" == "false" ]]; then
                    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                else
                    log_error "Homebrew not found and offline mode enabled"
                    exit 1
                fi
            fi
            ;;
        linux)
            case $PACKAGE_MANAGER in
                apt)
                    sudo apt-get update
                    ;;
                yum)
                    sudo yum update -y
                    ;;
                pacman)
                    sudo pacman -Sy
                    ;;
            esac
            ;;
        windows)
            if ! command -v choco &> /dev/null; then
                log_error "Chocolatey not found. Please install Chocolatey first."
                exit 1
            fi
            ;;
    esac

    log_success "Package manager setup completed"
}

# Install development tools
install_dev_tools() {
    log_step "Installing development tools..."

    # Node.js and npm
    local node_version="${NODE_VERSION:-18}"
    if ! command -v node &> /dev/null || [[ "$FORCE_REINSTALL" == "true" ]]; then
        log "Installing Node.js $node_version..."
        
        case $OS_TYPE in
            macos)
                brew install "node@$node_version"
                ;;
            linux)
                case $PACKAGE_MANAGER in
                    apt)
                        curl -fsSL https://deb.nodesource.com/setup_${node_version}.x | sudo -E bash -
                        sudo apt-get install -y nodejs
                        ;;
                    yum)
                        curl -fsSL https://rpm.nodesource.com/setup_${node_version}.x | sudo bash -
                        sudo yum install -y nodejs
                        ;;
                    pacman)
                        sudo pacman -S nodejs npm
                        ;;
                esac
                ;;
            windows)
                choco install nodejs --version=$node_version
                ;;
        esac
    fi

    # Git
    if ! command -v git &> /dev/null; then
        log "Installing Git..."
        case $OS_TYPE in
            macos)
                brew install git
                ;;
            linux)
                case $PACKAGE_MANAGER in
                    apt)
                        sudo apt-get install -y git
                        ;;
                    yum)
                        sudo yum install -y git
                        ;;
                    pacman)
                        sudo pacman -S git
                        ;;
                esac
                ;;
            windows)
                choco install git
                ;;
        esac
    fi

    # Development utilities
    local dev_tools=("curl" "jq" "htop")
    
    if [[ "$COMPLEXITY_LEVEL" == "enhanced" || "$COMPLEXITY_LEVEL" == "advanced" ]]; then
        dev_tools+=("redis" "postgresql")
    fi

    for tool in "${dev_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            log "Installing $tool..."
            case $OS_TYPE in
                macos)
                    brew install "$tool"
                    ;;
                linux)
                    case $PACKAGE_MANAGER in
                        apt)
                            sudo apt-get install -y "$tool"
                            ;;
                        yum)
                            sudo yum install -y "$tool"
                            ;;
                        pacman)
                            sudo pacman -S "$tool"
                            ;;
                    esac
                    ;;
                windows)
                    choco install "$tool"
                    ;;
            esac
        fi
    done

    log_success "Development tools installation completed"
}

# Install Docker and container tools
install_docker() {
    if [[ "$SKIP_DOCKER" == "true" || "$DEV_TOOLS_ONLY" == "true" ]]; then
        log_warning "Skipping Docker installation"
        return 0
    fi

    log_step "Installing Docker and container tools..."

    if ! command -v docker &> /dev/null || [[ "$FORCE_REINSTALL" == "true" ]]; then
        log "Installing Docker..."
        
        case $OS_TYPE in
            macos)
                if [[ "$ARCH_TYPE" == "arm64" ]]; then
                    brew install --cask docker
                else
                    brew install --cask docker
                fi
                ;;
            linux)
                # Install Docker using official script
                if [[ "$OFFLINE_MODE" == "false" ]]; then
                    curl -fsSL https://get.docker.com -o get-docker.sh
                    sudo sh get-docker.sh
                    sudo usermod -aG docker "$USER"
                    rm get-docker.sh
                else
                    log_error "Docker installation requires internet connection"
                    exit 1
                fi
                ;;
            windows)
                choco install docker-desktop
                ;;
        esac
    fi

    # Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log "Installing Docker Compose..."
        case $OS_TYPE in
            macos|windows)
                # Usually bundled with Docker Desktop
                ;;
            linux)
                sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                sudo chmod +x /usr/local/bin/docker-compose
                ;;
        esac
    fi

    # Kubernetes tools for advanced setup
    if [[ "$COMPLEXITY_LEVEL" == "advanced" ]]; then
        if ! command -v kubectl &> /dev/null; then
            log "Installing kubectl..."
            case $OS_TYPE in
                macos)
                    brew install kubectl
                    ;;
                linux)
                    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
                    rm kubectl
                    ;;
                windows)
                    choco install kubernetes-cli
                    ;;
            esac
        fi

        if ! command -v helm &> /dev/null; then
            log "Installing Helm..."
            case $OS_TYPE in
                macos)
                    brew install helm
                    ;;
                linux)
                    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
                    ;;
                windows)
                    choco install kubernetes-helm
                    ;;
            esac
        fi
    fi

    log_success "Docker and container tools installation completed"
}

# Setup Node.js development environment
setup_nodejs_environment() {
    log_step "Setting up Node.js development environment..."

    cd "$PROJECT_ROOT"

    # Install project dependencies
    if [[ ! -d "node_modules" || "$FORCE_REINSTALL" == "true" ]]; then
        log "Installing Node.js dependencies..."
        if [[ "$OFFLINE_MODE" == "true" ]]; then
            npm install --offline
        else
            npm ci
        fi
    fi

    # Install global development tools
    local global_tools=("@vue/cli" "@angular/cli" "create-react-app" "eslint" "prettier" "nodemon")
    
    if [[ "$COMPLEXITY_LEVEL" == "enhanced" || "$COMPLEXITY_LEVEL" == "advanced" ]]; then
        global_tools+=("@storybook/cli" "webpack-cli" "typescript")
    fi

    if [[ "$COMPLEXITY_LEVEL" == "advanced" ]]; then
        global_tools+=("@tensorflow/tfjs-node" "ml5" "brain.js")
    fi

    for tool in "${global_tools[@]}"; do
        if ! npm list -g "$tool" &> /dev/null; then
            log "Installing global tool: $tool"
            npm install -g "$tool"
        fi
    done

    # Setup development scripts
    log "Setting up development scripts..."
    
    # Create .nvmrc file for Node version management
    echo "${NODE_VERSION:-18}" > .nvmrc

    # Setup pre-commit hooks
    if [[ ! -d ".git/hooks" ]]; then
        git init
    fi

    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Run tests before commit
npm run lint
npm run test:unit
EOF
    chmod +x .git/hooks/pre-commit

    log_success "Node.js environment setup completed"
}

# Setup database environment
setup_database() {
    if [[ "$SKIP_DATABASE" == "true" || "$DEV_TOOLS_ONLY" == "true" ]]; then
        log_warning "Skipping database setup"
        return 0
    fi

    log_step "Setting up database environment..."

    # PostgreSQL for development
    if [[ "$COMPLEXITY_LEVEL" == "enhanced" || "$COMPLEXITY_LEVEL" == "advanced" ]]; then
        log "Setting up PostgreSQL..."
        
        # Create development database
        local db_name="flowstate_dev"
        local db_user="flowstate_user"
        local db_password="flowstate_dev_password"
        
        case $OS_TYPE in
            macos)
                if ! brew services list | grep postgresql | grep started &> /dev/null; then
                    brew services start postgresql
                fi
                ;;
            linux)
                sudo systemctl start postgresql
                sudo systemctl enable postgresql
                ;;
        esac

        # Create database and user
        sudo -u postgres psql << EOF || log_warning "Database setup may have failed (this is normal if already exists)"
CREATE DATABASE $db_name;
CREATE USER $db_user WITH PASSWORD '$db_password';
GRANT ALL PRIVILEGES ON DATABASE $db_name TO $db_user;
EOF

        # Setup environment variables
        cat >> "$PROJECT_ROOT/.env.development" << EOF
DATABASE_URL=postgresql://$db_user:$db_password@localhost:5432/$db_name
REDIS_URL=redis://localhost:6379
EOF
    fi

    # SQLite for essential mode
    if [[ "$COMPLEXITY_LEVEL" == "essential" ]]; then
        log "Setting up SQLite for essential mode..."
        cat >> "$PROJECT_ROOT/.env.development" << EOF
DATABASE_URL=sqlite://./dev.sqlite
EOF
    fi

    # Run database migrations
    if [[ -f "package.json" ]] && npm run | grep -q "db:migrate"; then
        log "Running database migrations..."
        npm run db:migrate:dev
    fi

    log_success "Database environment setup completed"
}

# Setup AI/ML development environment
setup_ai_environment() {
    if [[ "$SKIP_AI_SETUP" == "true" || "$COMPLEXITY_LEVEL" != "advanced" || "$DEV_TOOLS_ONLY" == "true" ]]; then
        log_warning "Skipping AI/ML environment setup"
        return 0
    fi

    log_step "Setting up AI/ML development environment..."

    # Python for AI/ML development
    if ! command -v python3 &> /dev/null; then
        log "Installing Python 3..."
        case $OS_TYPE in
            macos)
                brew install python@3.9
                ;;
            linux)
                case $PACKAGE_MANAGER in
                    apt)
                        sudo apt-get install -y python3 python3-pip python3-venv
                        ;;
                    yum)
                        sudo yum install -y python3 python3-pip
                        ;;
                    pacman)
                        sudo pacman -S python python-pip
                        ;;
                esac
                ;;
            windows)
                choco install python
                ;;
        esac
    fi

    # Create Python virtual environment for AI development
    log "Setting up Python virtual environment..."
    python3 -m venv ai-env
    source ai-env/bin/activate

    # Install AI/ML dependencies
    log "Installing AI/ML Python packages..."
    pip install --upgrade pip
    pip install numpy pandas scikit-learn tensorflow torch transformers

    # Create AI development configuration
    cat >> "$PROJECT_ROOT/.env.development" << EOF
PYTHON_ENV=./ai-env/bin/python
AI_MODEL_PATH=./models
TENSORFLOW_ENV=development
EOF

    # Setup Jupyter for experimentation
    if [[ "$QUICK_SETUP" == "false" ]]; then
        log "Installing Jupyter Notebook..."
        pip install jupyter notebook jupyterlab
        
        # Create notebooks directory
        mkdir -p notebooks/experiments
        mkdir -p models/trained
        mkdir -p data/datasets
    fi

    deactivate

    log_success "AI/ML environment setup completed"
}

# Setup IDE and editor configurations
setup_ide_config() {
    log_step "Setting up IDE and editor configurations..."

    # VS Code settings
    mkdir -p .vscode
    
    cat > .vscode/settings.json << 'EOF'
{
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": true
    },
    "typescript.preferences.importModuleSpecifier": "relative",
    "files.exclude": {
        "**/node_modules": true,
        "**/dist": true,
        "**/.git": true,
        "**/coverage": true
    },
    "search.exclude": {
        "**/node_modules": true,
        "**/dist": true,
        "**/coverage": true
    }
}
EOF

    cat > .vscode/extensions.json << 'EOF'
{
    "recommendations": [
        "esbenp.prettier-vscode",
        "dbaeumer.vscode-eslint",
        "bradlc.vscode-tailwindcss",
        "ms-vscode.vscode-typescript-next",
        "ms-vscode.vscode-json",
        "formulahendry.auto-rename-tag",
        "christian-kohler.path-intellisense"
    ]
}
EOF

    # Add complexity-specific extensions
    if [[ "$COMPLEXITY_LEVEL" == "advanced" ]]; then
        cat >> .vscode/extensions.json << 'EOF'
        ,
        "ms-python.python",
        "ms-toolsai.jupyter",
        "ms-vscode.cpptools"
    ]
}
EOF
    else
        echo "    ]" >> .vscode/extensions.json
        echo "}" >> .vscode/extensions.json
    fi

    # Launch configurations
    cat > .vscode/launch.json << 'EOF'
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch Development Server",
            "type": "node",
            "request": "launch",
            "program": "${workspaceFolder}/src/server.js",
            "env": {
                "NODE_ENV": "development"
            },
            "console": "integratedTerminal"
        },
        {
            "name": "Run Tests",
            "type": "node",
            "request": "launch",
            "program": "${workspaceFolder}/node_modules/.bin/jest",
            "args": ["--runInBand"],
            "console": "integratedTerminal"
        }
    ]
}
EOF

    # EditorConfig
    cat > .editorconfig << 'EOF'
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false

[*.py]
indent_size = 4
EOF

    log_success "IDE configuration setup completed"
}

# Create development environment files
create_environment_files() {
    log_step "Creating development environment files..."

    # Create .env.development if it doesn't exist
    if [[ ! -f ".env.development" ]]; then
        cat > .env.development << EOF
# FlowState Development Environment
NODE_ENV=development
PORT=3000
HOST=localhost

# Complexity Level
COMPLEXITY_LEVEL=$COMPLEXITY_LEVEL

# Feature Flags
ENABLE_AI_FEATURES=$([ "$COMPLEXITY_LEVEL" == "advanced" ] && echo "true" || echo "false")
ENABLE_TEAM_FEATURES=$([ "$COMPLEXITY_LEVEL" != "essential" ] && echo "true" || echo "false")
ENABLE_ADVANCED_ANALYTICS=$([ "$COMPLEXITY_LEVEL" != "essential" ] && echo "true" || echo "false")

# Development Tools
DEBUG=flowstate:*
LOG_LEVEL=debug

# Security (development only)
JWT_SECRET=development_secret_key_change_in_production
SESSION_SECRET=development_session_secret

# Privacy Settings
DATA_RETENTION_DAYS=30
ENABLE_ANALYTICS=false
PRIVACY_MODE=strict

# External Services (development)
REDIS_URL=redis://localhost:6379
ELASTICSEARCH_URL=http://localhost:9200

# AI Services (if advanced)
AI_SERVICE_URL=http://localhost:8080
ML_MODEL_PATH=./models

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
EOF
    fi

    # Create .env.test
    cat > .env.test << EOF
# FlowState Test Environment
NODE_ENV=test
DATABASE_URL=sqlite://./test.sqlite
REDIS_URL=redis://localhost:6379/1

# Disable external services in tests
ENABLE_EXTERNAL_APIS=false
ENABLE_TELEMETRY=false

# Test-specific settings
TEST_TIMEOUT=10000
PARALLEL_TESTS=true
EOF

    # Create development docker-compose file
    if [[ "$SKIP_DOCKER" == "false" ]]; then
        cat > docker-compose.dev.yml << EOF
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: flowstate_dev
      POSTGRES_USER: flowstate_user
      POSTGRES_PASSWORD: flowstate_dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

EOF

        if [[ "$COMPLEXITY_LEVEL" == "advanced" ]]; then
            cat >> docker-compose.dev.yml << EOF
  elasticsearch:
    image: elasticsearch:7.14.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  jupyter:
    image: jupyter/tensorflow-notebook
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/home/jovyan/work
    environment:
      - JUPYTER_ENABLE_LAB=yes

EOF
        fi

        cat >> docker-compose.dev.yml << EOF
volumes:
  postgres_data:
  redis_data:
EOF

        if [[ "$COMPLEXITY_LEVEL" == "advanced" ]]; then
            echo "  elasticsearch_data:" >> docker-compose.dev.yml
        fi
    fi

    log_success "Environment files created"
}

# Start development services
start_dev_services() {
    if [[ "$DEV_TOOLS_ONLY" == "true" || "$SKIP_DOCKER" == "true" ]]; then
        log_warning "Skipping development services startup"
        return 0
    fi

    log_step "Starting development services..."

    # Start Docker services
    if [[ -f "docker-compose.dev.yml" ]]; then
        log "Starting Docker development services..."
        docker-compose -f docker-compose.dev.yml up -d
        
        # Wait for services to be ready
        log "Waiting for services to be ready..."
        sleep 10
        
        # Health check
        if docker-compose -f docker-compose.dev.yml ps | grep -q "Up"; then
            log_success "Development services started successfully"
        else
            log_warning "Some services may not have started correctly"
        fi
    fi

    log_success "Development services startup completed"
}

# Calculate total steps based on configuration
calculate_total_steps() {
    total_steps=8  # Base steps
    
    if [[ "$SKIP_DOCKER" == "false" && "$DEV_TOOLS_ONLY" == "false" ]]; then
        ((total_steps++))
    fi
    
    if [[ "$SKIP_DATABASE" == "false" && "$DEV_TOOLS_ONLY" == "false" ]]; then
        ((total_steps++))
    fi
    
    if [[ "$COMPLEXITY_LEVEL" == "advanced" && "$SKIP_AI_SETUP" == "false" && "$DEV_TOOLS_ONLY" == "false" ]]; then
        ((total_steps++))
    fi
    
    if [[ "$DEV_TOOLS_ONLY" == "false" ]]; then
        ((total_steps++))  # Start services
    fi
}

# Print setup summary
print_setup_summary() {
    log ""
    log "=========================================="
    log "         SETUP SUMMARY"
    log "=========================================="
    log "Complexity Level: $COMPLEXITY_LEVEL"
    log "Platform: $OS_TYPE ($ARCH_TYPE)"
    log "Package Manager: $PACKAGE_MANAGER"
    log ""
    
    log_info "Development Environment Ready!"
    log ""
    log "Available Commands:"
    log "  npm run dev          - Start development server"
    log "  npm run test         - Run tests"
    log "  npm run build        - Build for production"
    log "  npm run lint         - Run linter"
    log ""
    
    if [[ "$SKIP_DOCKER" == "false" && "$DEV_TOOLS_ONLY" == "false" ]]; then
        log "Docker Services:"
        log "  PostgreSQL:  localhost:5432"
        log "  Redis:       localhost:6379"
        
        if [[ "$COMPLEXITY_LEVEL" == "advanced" ]]; then
            log "  Elasticsearch: localhost:9200"
            log "  Jupyter:      localhost:8888"
        fi
        log ""
    fi
    
    log "Configuration Files Created:"
    log "  .env.development     - Development environment variables"
    log "  .env.test           - Test environment variables"
    log "  .vscode/            - VS Code configuration"
    log "  .editorconfig       - Editor configuration"
    
    if [[ "$SKIP_DOCKER" == "false" ]]; then
        log "  docker-compose.dev.yml - Development services"
    fi
    
    log ""
    log_success "Setup completed successfully!"
    
    if [[ "$COMPLEXITY_LEVEL" == "advanced" && "$SKIP_AI_SETUP" == "false" ]]; then
        log ""
        log_info "AI/ML Environment:"
        log "  Python virtual environment: ./ai-env"
        log "  Activate with: source ai-env/bin/activate"
        log "  Jupyter notebooks: ./notebooks"
    fi
}

# Main setup function
main() {
    local start_time
    start_time=$(date +%s)

    log "Starting FlowState development environment setup..."
    log "Complexity Level: $COMPLEXITY_LEVEL"
    log "Platform: $(uname -s) $(uname -m)"

    calculate_total_steps

    detect_platform
    show_progress

    check_requirements
    show_progress

    install_package_manager
    show_progress

    install_dev_tools
    show_progress

    install_docker
    show_progress

    setup_nodejs_environment
    show_progress

    setup_database
    show_progress

    setup_ai_environment
    show_progress

    setup_ide_config
    show_progress

    create_environment_files
    show_progress

    start_dev_services
    show_progress

    # Calculate setup time
    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))

    print_setup_summary

    log ""
    log_success "Development environment setup completed in ${duration}s"
}

# Script execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    parse_args "$@"
    main
fi
