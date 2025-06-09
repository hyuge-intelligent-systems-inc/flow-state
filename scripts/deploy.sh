
#!/bin/bash

# FlowState Deployment Script
# Supports progressive complexity deployment with privacy-first architecture
# Usage: ./deploy.sh [environment] [complexity_level] [options]

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Default values
ENVIRONMENT=""
COMPLEXITY_LEVEL="essential"
DRY_RUN=false
VERBOSE=false
SKIP_TESTS=false
SKIP_SECURITY_SCAN=false
BACKUP_BEFORE_DEPLOY=true
ROLLBACK_ON_FAILURE=true

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

log_success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

log_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# Help function
show_help() {
    cat << EOF
FlowState Deployment Script

Usage: $0 [ENVIRONMENT] [COMPLEXITY_LEVEL] [OPTIONS]

ENVIRONMENTS:
    development     - Local development deployment
    staging         - Staging environment
    production      - Production environment

COMPLEXITY_LEVELS:
    essential       - Layer 0: Basic time tracking only (default)
    enhanced        - Layer 1: Enhanced UI and basic analytics
    advanced        - Layer 2: Full AI features and team collaboration

OPTIONS:
    --dry-run       - Show what would be deployed without actually deploying
    --verbose       - Enable verbose output
    --skip-tests    - Skip running tests before deployment
    --skip-security - Skip security scans
    --no-backup     - Skip creating backup before deployment
    --no-rollback   - Don't rollback on deployment failure
    --help          - Show this help message

EXAMPLES:
    $0 staging essential                    # Deploy essential layer to staging
    $0 production enhanced --dry-run        # Dry run enhanced layer to production
    $0 development advanced --verbose       # Deploy full features to development

ENVIRONMENT VARIABLES:
    DOCKER_REGISTRY     - Docker registry URL (default: flowstate.azurecr.io)
    KUBE_CONTEXT        - Kubernetes context to use
    SLACK_WEBHOOK_URL   - Slack webhook for deployment notifications
    BACKUP_RETENTION    - Days to retain backups (default: 30)
EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            development|staging|production)
                ENVIRONMENT="$1"
                shift
                ;;
            essential|enhanced|advanced)
                COMPLEXITY_LEVEL="$1"
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                set -x
                shift
                ;;
            --skip-tests)
                SKIP_TESTS=true
                shift
                ;;
            --skip-security)
                SKIP_SECURITY_SCAN=true
                shift
                ;;
            --no-backup)
                BACKUP_BEFORE_DEPLOY=false
                shift
                ;;
            --no-rollback)
                ROLLBACK_ON_FAILURE=false
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

    if [[ -z "$ENVIRONMENT" ]]; then
        log_error "Environment is required"
        show_help
        exit 1
    fi
}

# Validate environment and prerequisites
validate_environment() {
    log "Validating deployment environment..."

    # Check required tools
    local required_tools=("docker" "kubectl" "helm" "jq")
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            log_error "$tool is required but not installed"
            exit 1
        fi
    done

    # Check environment-specific requirements
    case $ENVIRONMENT in
        production)
            if [[ -z "${KUBE_CONTEXT:-}" ]]; then
                log_error "KUBE_CONTEXT environment variable is required for production deployment"
                exit 1
            fi
            if [[ "$COMPLEXITY_LEVEL" == "advanced" ]] && [[ -z "${AI_SERVICE_KEY:-}" ]]; then
                log_error "AI_SERVICE_KEY is required for advanced complexity level"
                exit 1
            fi
            ;;
        staging)
            # Staging validations
            ;;
        development)
            # Development validations
            ;;
    esac

    # Validate Docker registry access
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi

    log_success "Environment validation completed"
}

# Load configuration based on environment and complexity
load_config() {
    log "Loading configuration for $ENVIRONMENT environment with $COMPLEXITY_LEVEL complexity..."

    # Source environment-specific configuration
    local config_file="$PROJECT_ROOT/config/${ENVIRONMENT}.sh"
    if [[ -f "$config_file" ]]; then
        source "$config_file"
    else
        log_error "Configuration file not found: $config_file"
        exit 1
    fi

    # Set complexity-specific features
    case $COMPLEXITY_LEVEL in
        essential)
            export ENABLE_AI_FEATURES=false
            export ENABLE_TEAM_FEATURES=false
            export ENABLE_ADVANCED_ANALYTICS=false
            export UI_COMPLEXITY_LEVEL=0
            ;;
        enhanced)
            export ENABLE_AI_FEATURES=false
            export ENABLE_TEAM_FEATURES=true
            export ENABLE_ADVANCED_ANALYTICS=true
            export UI_COMPLEXITY_LEVEL=1
            ;;
        advanced)
            export ENABLE_AI_FEATURES=true
            export ENABLE_TEAM_FEATURES=true
            export ENABLE_ADVANCED_ANALYTICS=true
            export UI_COMPLEXITY_LEVEL=2
            ;;
    esac

    # Set deployment-specific variables
    export DEPLOYMENT_TIMESTAMP="$TIMESTAMP"
    export DOCKER_TAG="${DOCKER_TAG:-$TIMESTAMP}"
    export NAMESPACE="${NAMESPACE:-flowstate-$ENVIRONMENT}"

    log_success "Configuration loaded successfully"
}

# Run tests based on complexity level
run_tests() {
    if [[ "$SKIP_TESTS" == "true" ]]; then
        log_warning "Skipping tests as requested"
        return 0
    fi

    log "Running tests for $COMPLEXITY_LEVEL complexity level..."

    cd "$PROJECT_ROOT"

    # Always run core tests
    log "Running core functionality tests..."
    npm test -- --testPathPattern="core|time-tracking" --coverage

    case $COMPLEXITY_LEVEL in
        enhanced|advanced)
            log "Running enhanced feature tests..."
            npm test -- --testPathPattern="analytics|team" --coverage
            ;;
    esac

    case $COMPLEXITY_LEVEL in
        advanced)
            log "Running AI feature tests..."
            npm test -- --testPathPattern="ai|ml|insights" --coverage
            ;;
    esac

    # Integration tests for staging and production
    if [[ "$ENVIRONMENT" != "development" ]]; then
        log "Running integration tests..."
        npm run test:integration
    fi

    # Performance tests for production
    if [[ "$ENVIRONMENT" == "production" ]]; then
        log "Running performance tests..."
        npm run test:performance
    fi

    log_success "All tests passed"
}

# Security scanning
run_security_scan() {
    if [[ "$SKIP_SECURITY_SCAN" == "true" ]]; then
        log_warning "Skipping security scan as requested"
        return 0
    fi

    log "Running security scans..."

    # Dependency vulnerability scan
    log "Scanning dependencies for vulnerabilities..."
    npm audit --audit-level=moderate

    # Docker image security scan
    log "Scanning Docker images..."
    if command -v trivy &> /dev/null; then
        trivy image --severity HIGH,CRITICAL "flowstate-app:$DOCKER_TAG"
    else
        log_warning "Trivy not found, skipping container security scan"
    fi

    # Static code analysis
    if [[ -f "$PROJECT_ROOT/.eslintrc.js" ]]; then
        log "Running static code analysis..."
        npm run lint:security
    fi

    log_success "Security scans completed"
}

# Build Docker images based on complexity level
build_images() {
    log "Building Docker images for $COMPLEXITY_LEVEL complexity..."

    cd "$PROJECT_ROOT"

    # Build base image with essential features
    log "Building base application image..."
    docker build \
        --tag "flowstate-app:$DOCKER_TAG" \
        --build-arg COMPLEXITY_LEVEL="$COMPLEXITY_LEVEL" \
        --build-arg BUILD_TIMESTAMP="$TIMESTAMP" \
        --build-arg ENABLE_AI_FEATURES="$ENABLE_AI_FEATURES" \
        --build-arg ENABLE_TEAM_FEATURES="$ENABLE_TEAM_FEATURES" \
        --file Dockerfile \
        .

    # Build AI services image only for advanced complexity
    if [[ "$COMPLEXITY_LEVEL" == "advanced" ]]; then
        log "Building AI services image..."
        docker build \
            --tag "flowstate-ai:$DOCKER_TAG" \
            --build-arg BUILD_TIMESTAMP="$TIMESTAMP" \
            --file docker/Dockerfile.ai \
            .
    fi

    # Build analytics image for enhanced and advanced
    if [[ "$COMPLEXITY_LEVEL" == "enhanced" || "$COMPLEXITY_LEVEL" == "advanced" ]]; then
        log "Building analytics services image..."
        docker build \
            --tag "flowstate-analytics:$DOCKER_TAG" \
            --build-arg BUILD_TIMESTAMP="$TIMESTAMP" \
            --file docker/Dockerfile.analytics \
            .
    fi

    log_success "Docker images built successfully"
}

# Push images to registry
push_images() {
    if [[ "$DRY_RUN" == "true" ]]; then
        log "DRY RUN: Would push images to registry"
        return 0
    fi

    log "Pushing images to registry..."

    local registry="${DOCKER_REGISTRY:-flowstate.azurecr.io}"

    # Tag and push base image
    docker tag "flowstate-app:$DOCKER_TAG" "$registry/flowstate-app:$DOCKER_TAG"
    docker push "$registry/flowstate-app:$DOCKER_TAG"

    # Push complexity-specific images
    case $COMPLEXITY_LEVEL in
        advanced)
            docker tag "flowstate-ai:$DOCKER_TAG" "$registry/flowstate-ai:$DOCKER_TAG"
            docker push "$registry/flowstate-ai:$DOCKER_TAG"
            ;&  # fallthrough
        enhanced)
            docker tag "flowstate-analytics:$DOCKER_TAG" "$registry/flowstate-analytics:$DOCKER_TAG"
            docker push "$registry/flowstate-analytics:$DOCKER_TAG"
            ;;
    esac

    log_success "Images pushed to registry"
}

# Create backup before deployment
create_backup() {
    if [[ "$BACKUP_BEFORE_DEPLOY" == "false" ]]; then
        log_warning "Skipping backup as requested"
        return 0
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        log "DRY RUN: Would create backup"
        return 0
    fi

    log "Creating backup before deployment..."

    local backup_name="flowstate-$ENVIRONMENT-$TIMESTAMP"

    # Database backup
    log "Creating database backup..."
    kubectl exec -n "$NAMESPACE" deployment/postgres -- \
        pg_dump -U postgres flowstate > "backup-$backup_name.sql"

    # Configuration backup
    log "Creating configuration backup..."
    kubectl get configmaps,secrets -n "$NAMESPACE" -o yaml > "config-backup-$backup_name.yaml"

    # Upload to backup storage
    if [[ -n "${BACKUP_STORAGE_URL:-}" ]]; then
        log "Uploading backup to storage..."
        # Implementation depends on storage provider (S3, Azure Blob, etc.)
    fi

    log_success "Backup created: $backup_name"
    export BACKUP_NAME="$backup_name"
}

# Deploy using Helm charts
deploy_with_helm() {
    if [[ "$DRY_RUN" == "true" ]]; then
        log "DRY RUN: Would deploy with Helm"
        helm upgrade --install flowstate ./helm/flowstate \
            --namespace "$NAMESPACE" \
            --create-namespace \
            --values "helm/values-$ENVIRONMENT.yaml" \
            --set "image.tag=$DOCKER_TAG" \
            --set "complexity.level=$COMPLEXITY_LEVEL" \
            --set "features.ai=$ENABLE_AI_FEATURES" \
            --set "features.team=$ENABLE_TEAM_FEATURES" \
            --set "features.analytics=$ENABLE_ADVANCED_ANALYTICS" \
            --dry-run \
            --debug
        return 0
    fi

    log "Deploying with Helm..."

    # Set Kubernetes context for production
    if [[ "$ENVIRONMENT" == "production" && -n "${KUBE_CONTEXT:-}" ]]; then
        kubectl config use-context "$KUBE_CONTEXT"
    fi

    # Deploy with complexity-specific values
    helm upgrade --install flowstate ./helm/flowstate \
        --namespace "$NAMESPACE" \
        --create-namespace \
        --values "helm/values-$ENVIRONMENT.yaml" \
        --values "helm/values-$COMPLEXITY_LEVEL.yaml" \
        --set "image.tag=$DOCKER_TAG" \
        --set "deployment.timestamp=$TIMESTAMP" \
        --set "complexity.level=$COMPLEXITY_LEVEL" \
        --set "features.ai=$ENABLE_AI_FEATURES" \
        --set "features.team=$ENABLE_TEAM_FEATURES" \
        --set "features.analytics=$ENABLE_ADVANCED_ANALYTICS" \
        --timeout 600s \
        --wait

    log_success "Helm deployment completed"
}

# Health checks and deployment verification
verify_deployment() {
    if [[ "$DRY_RUN" == "true" ]]; then
        log "DRY RUN: Would verify deployment"
        return 0
    fi

    log "Verifying deployment health..."

    # Wait for pods to be ready
    log "Waiting for pods to be ready..."
    kubectl wait --for=condition=ready pod \
        -l app=flowstate \
        -n "$NAMESPACE" \
        --timeout=300s

    # Check service endpoints
    log "Checking service endpoints..."
    local service_url
    service_url=$(kubectl get service flowstate -n "$NAMESPACE" -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    
    if [[ -n "$service_url" ]]; then
        # Health check
        local max_attempts=30
        local attempt=1
        
        while [[ $attempt -le $max_attempts ]]; do
            if curl -f -s "http://$service_url/health" > /dev/null; then
                log_success "Health check passed"
                break
            fi
            
            if [[ $attempt -eq $max_attempts ]]; then
                log_error "Health check failed after $max_attempts attempts"
                return 1
            fi
            
            log "Health check attempt $attempt/$max_attempts failed, retrying..."
            sleep 10
            ((attempt++))
        done

        # Feature-specific health checks
        case $COMPLEXITY_LEVEL in
            enhanced|advanced)
                log "Checking analytics service..."
                curl -f -s "http://$service_url/api/v1/analytics/health" || {
                    log_error "Analytics service health check failed"
                    return 1
                }
                ;;
        esac

        case $COMPLEXITY_LEVEL in
            advanced)
                log "Checking AI service..."
                curl -f -s "http://$service_url/api/v1/ai/health" || {
                    log_error "AI service health check failed"
                    return 1
                }
                ;;
        esac
    fi

    log_success "Deployment verification completed"
}

# Rollback on failure
rollback_deployment() {
    if [[ "$ROLLBACK_ON_FAILURE" == "false" ]]; then
        log_warning "Rollback disabled, manual intervention required"
        return 0
    fi

    log_error "Deployment failed, initiating rollback..."

    # Helm rollback
    helm rollback flowstate -n "$NAMESPACE" || {
        log_error "Helm rollback failed"
    }

    # Restore from backup if available
    if [[ -n "${BACKUP_NAME:-}" ]]; then
        log "Restoring from backup: $BACKUP_NAME"
        # Restore database
        kubectl exec -n "$NAMESPACE" deployment/postgres -- \
            psql -U postgres -d flowstate < "backup-$BACKUP_NAME.sql" || {
            log_error "Database restore failed"
        }
    fi

    log_warning "Rollback completed, please investigate the deployment failure"
}

# Send deployment notification
send_notification() {
    local status="$1"
    local message="$2"

    if [[ -n "${SLACK_WEBHOOK_URL:-}" ]]; then
        local color
        case $status in
            success) color="good" ;;
            failure) color="danger" ;;
            *) color="warning" ;;
        esac

        curl -X POST -H 'Content-type: application/json' \
            --data "{
                \"attachments\": [{
                    \"color\": \"$color\",
                    \"title\": \"FlowState Deployment - $ENVIRONMENT\",
                    \"fields\": [
                        {\"title\": \"Environment\", \"value\": \"$ENVIRONMENT\", \"short\": true},
                        {\"title\": \"Complexity\", \"value\": \"$COMPLEXITY_LEVEL\", \"short\": true},
                        {\"title\": \"Status\", \"value\": \"$status\", \"short\": true},
                        {\"title\": \"Timestamp\", \"value\": \"$TIMESTAMP\", \"short\": true}
                    ],
                    \"text\": \"$message\"
                }]
            }" \
            "$SLACK_WEBHOOK_URL" || {
            log_warning "Failed to send Slack notification"
        }
    fi
}

# Cleanup temporary files
cleanup() {
    log "Cleaning up temporary files..."
    
    # Remove temporary backup files (keep them for a few days)
    find . -name "backup-*.sql" -mtime +7 -delete 2>/dev/null || true
    find . -name "config-backup-*.yaml" -mtime +7 -delete 2>/dev/null || true
    
    # Clean up Docker build cache
    docker system prune -f --filter "until=24h" 2>/dev/null || true
}

# Main deployment function
main() {
    local start_time
    start_time=$(date +%s)

    log "Starting FlowState deployment..."
    log "Environment: $ENVIRONMENT"
    log "Complexity Level: $COMPLEXITY_LEVEL"
    log "Timestamp: $TIMESTAMP"

    # Trap for cleanup and rollback on failure
    trap 'cleanup; rollback_deployment; send_notification "failure" "Deployment failed during execution"' ERR

    validate_environment
    load_config
    run_tests
    run_security_scan
    build_images
    push_images
    create_backup
    deploy_with_helm
    verify_deployment

    # Calculate deployment time
    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))

    cleanup

    log_success "Deployment completed successfully in ${duration}s"
    send_notification "success" "Deployment completed successfully in ${duration}s"

    # Reset trap
    trap - ERR
}

# Script execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    parse_args "$@"
    main
fi
