
#!/bin/bash

# FlowState Test Runner Script
# Comprehensive testing for progressive complexity architecture
# Usage: ./run_tests.sh [test_type] [complexity_level] [options]

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Default values
TEST_TYPE="all"
COMPLEXITY_LEVEL="all"
ENVIRONMENT="test"
VERBOSE=false
COVERAGE=true
PARALLEL=true
WATCH=false
UPDATE_SNAPSHOTS=false
FAIL_FAST=false
BAIL_ON_FIRST_FAILURE=false
OUTPUT_FORMAT="console"
GENERATE_REPORT=false

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Test result tracking
declare -A test_results
total_tests=0
passed_tests=0
failed_tests=0
skipped_tests=0

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

log_info() {
    echo -e "${CYAN}[INFO] $1${NC}"
}

log_test() {
    echo -e "${PURPLE}[TEST] $1${NC}"
}

# Help function
show_help() {
    cat << EOF
FlowState Test Runner

Usage: $0 [TEST_TYPE] [COMPLEXITY_LEVEL] [OPTIONS]

TEST_TYPES:
    all                 - Run all tests (default)
    unit                - Unit tests only
    integration         - Integration tests only
    e2e                 - End-to-end tests only
    performance         - Performance tests
    security            - Security tests
    accessibility       - Accessibility tests
    privacy             - Privacy compliance tests
    api                 - API tests
    ui                  - UI component tests
    ai                  - AI/ML model tests
    database            - Database tests
    migration           - Database migration tests

COMPLEXITY_LEVELS:
    all                 - Test all complexity levels (default)
    essential           - Layer 0: Basic time tracking
    enhanced            - Layer 1: Enhanced features and analytics
    advanced            - Layer 2: Full AI features and team collaboration

OPTIONS:
    --environment ENV   - Test environment (test, staging, production)
    --verbose           - Enable verbose output
    --no-coverage       - Skip coverage reporting
    --no-parallel       - Run tests sequentially
    --watch             - Watch mode for development
    --update-snapshots  - Update test snapshots
    --fail-fast         - Stop on first test failure
    --bail              - Exit immediately on first failure
    --format FORMAT     - Output format (console, json, junit, html)
    --report            - Generate comprehensive test report
    --help              - Show this help message

EXAMPLES:
    $0                                          # Run all tests
    $0 unit essential                          # Run unit tests for essential layer only
    $0 e2e advanced --verbose                  # Run e2e tests for advanced features with verbose output
    $0 performance --environment staging       # Run performance tests against staging
    $0 --watch unit                           # Watch mode for unit tests during development

ENVIRONMENT VARIABLES:
    TEST_DATABASE_URL   - Test database connection string
    CI                  - Set to 'true' when running in CI environment
    HEADLESS           - Set to 'true' for headless browser tests
    PARALLEL_WORKERS   - Number of parallel test workers (default: CPU cores)
EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            all|unit|integration|e2e|performance|security|accessibility|privacy|api|ui|ai|database|migration)
                TEST_TYPE="$1"
                shift
                ;;
            essential|enhanced|advanced)
                COMPLEXITY_LEVEL="$1"
                shift
                ;;
            --environment)
                ENVIRONMENT="$2"
                shift 2
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --no-coverage)
                COVERAGE=false
                shift
                ;;
            --no-parallel)
                PARALLEL=false
                shift
                ;;
            --watch)
                WATCH=true
                shift
                ;;
            --update-snapshots)
                UPDATE_SNAPSHOTS=true
                shift
                ;;
            --fail-fast)
                FAIL_FAST=true
                shift
                ;;
            --bail)
                BAIL_ON_FIRST_FAILURE=true
                shift
                ;;
            --format)
                OUTPUT_FORMAT="$2"
                shift 2
                ;;
            --report)
                GENERATE_REPORT=true
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

# Setup test environment
setup_test_environment() {
    log "Setting up test environment..."

    cd "$PROJECT_ROOT"

    # Load test environment variables
    if [[ -f ".env.test" ]]; then
        export $(grep -v '^#' .env.test | xargs)
    fi

    # Set complexity-specific environment variables
    case $COMPLEXITY_LEVEL in
        essential)
            export TEST_AI_FEATURES=false
            export TEST_TEAM_FEATURES=false
            export TEST_ADVANCED_ANALYTICS=false
            ;;
        enhanced)
            export TEST_AI_FEATURES=false
            export TEST_TEAM_FEATURES=true
            export TEST_ADVANCED_ANALYTICS=true
            ;;
        advanced)
            export TEST_AI_FEATURES=true
            export TEST_TEAM_FEATURES=true
            export TEST_ADVANCED_ANALYTICS=true
            ;;
        all)
            # Test all features for comprehensive coverage
            export TEST_AI_FEATURES=true
            export TEST_TEAM_FEATURES=true
            export TEST_ADVANCED_ANALYTICS=true
            ;;
    esac

    # CI-specific configuration
    if [[ "${CI:-false}" == "true" ]]; then
        export HEADLESS=true
        export PARALLEL_WORKERS=${PARALLEL_WORKERS:-4}
        log_info "Running in CI mode"
    else
        export PARALLEL_WORKERS=${PARALLEL_WORKERS:-$(nproc 2>/dev/null || echo 2)}
    fi

    # Create test output directories
    mkdir -p test-results/{unit,integration,e2e,performance,security,accessibility,privacy}
    mkdir -p coverage/{unit,integration,e2e}

    log_success "Test environment setup completed"
}

# Validate test prerequisites
validate_prerequisites() {
    log "Validating test prerequisites..."

    # Check Node.js and npm
    if ! command -v node &> /dev/null; then
        log_error "Node.js is required but not installed"
        exit 1
    fi

    if ! command -v npm &> /dev/null; then
        log_error "npm is required but not installed"
        exit 1
    fi

    # Install dependencies if needed
    if [[ ! -d "node_modules" ]]; then
        log "Installing dependencies..."
        npm ci
    fi

    # Check for test-specific tools based on test type
    case $TEST_TYPE in
        e2e|accessibility)
            if ! command -v playwright &> /dev/null && ! npx playwright --version &> /dev/null 2>&1; then
                log_warning "Playwright not found, installing..."
                npx playwright install
            fi
            ;;
        performance)
            if ! command -v artillery &> /dev/null && ! npx artillery --version &> /dev/null 2>&1; then
                log_warning "Artillery not found for performance testing"
            fi
            ;;
        security)
            if ! command -v snyk &> /dev/null && ! npx snyk --version &> /dev/null 2>&1; then
                log_warning "Snyk not found for security testing"
            fi
            ;;
    esac

    # Database setup for database tests
    if [[ "$TEST_TYPE" == "database" || "$TEST_TYPE" == "migration" || "$TEST_TYPE" == "all" ]]; then
        setup_test_database
    fi

    log_success "Prerequisites validation completed"
}

# Setup test database
setup_test_database() {
    log "Setting up test database..."

    # Check if test database is available
    if [[ -z "${TEST_DATABASE_URL:-}" ]]; then
        log_warning "TEST_DATABASE_URL not set, using SQLite for tests"
        export TEST_DATABASE_URL="sqlite://./test-db.sqlite"
    fi

    # Run database migrations for test database
    npm run db:migrate:test || {
        log_error "Failed to run test database migrations"
        exit 1
    }

    # Seed test data
    npm run db:seed:test || {
        log_warning "Failed to seed test database"
    }

    log_success "Test database setup completed"
}

# Build test command based on configuration
build_test_command() {
    local test_cmd="npm test"
    local jest_args=()

    # Add Jest configuration based on test type
    case $TEST_TYPE in
        unit)
            jest_args+=("--testPathPattern='(unit|spec)'" "--testPathIgnorePattern='(integration|e2e)'")
            ;;
        integration)
            jest_args+=("--testPathPattern='integration'" "--runInBand")
            ;;
        api)
            jest_args+=("--testPathPattern='api'" "--runInBand")
            ;;
        database)
            jest_args+=("--testPathPattern='database'" "--runInBand")
            ;;
        migration)
            jest_args+=("--testPathPattern='migration'" "--runInBand")
            ;;
        ui)
            jest_args+=("--testPathPattern='(component|ui)'" "--setupFilesAfterEnv='<rootDir>/test/setup/ui.js'")
            ;;
        ai)
            jest_args+=("--testPathPattern='(ai|ml)'" "--testTimeout=30000")
            ;;
    esac

    # Add complexity-level filtering
    if [[ "$COMPLEXITY_LEVEL" != "all" ]]; then
        jest_args+=("--testNamePattern='$COMPLEXITY_LEVEL'")
    fi

    # Add coverage options
    if [[ "$COVERAGE" == "true" ]]; then
        jest_args+=("--coverage" "--coverageDirectory=coverage/$TEST_TYPE")
        
        # Coverage thresholds based on complexity
        case $COMPLEXITY_LEVEL in
            essential)
                jest_args+=("--coverageThreshold='{\"global\":{\"statements\":90,\"branches\":85,\"functions\":90,\"lines\":90}}'")
                ;;
            enhanced)
                jest_args+=("--coverageThreshold='{\"global\":{\"statements\":85,\"branches\":80,\"functions\":85,\"lines\":85}}'")
                ;;
            advanced)
                jest_args+=("--coverageThreshold='{\"global\":{\"statements\":80,\"branches\":75,\"functions\":80,\"lines\":80}}'")
                ;;
        esac
    fi

    # Add parallel execution
    if [[ "$PARALLEL" == "true" ]] && [[ "$TEST_TYPE" != "integration" ]]; then
        jest_args+=("--maxWorkers=$PARALLEL_WORKERS")
    fi

    # Add watch mode
    if [[ "$WATCH" == "true" ]]; then
        jest_args+=("--watch" "--watchAll=false")
    fi

    # Add snapshot updates
    if [[ "$UPDATE_SNAPSHOTS" == "true" ]]; then
        jest_args+=("--updateSnapshot")
    fi

    # Add failure handling
    if [[ "$FAIL_FAST" == "true" ]]; then
        jest_args+=("--bail=1")
    fi

    # Add verbose output
    if [[ "$VERBOSE" == "true" ]]; then
        jest_args+=("--verbose")
    fi

    # Add output format
    case $OUTPUT_FORMAT in
        json)
            jest_args+=("--json" "--outputFile=test-results/$TEST_TYPE/results.json")
            ;;
        junit)
            jest_args+=("--reporters=default" "--reporters=jest-junit")
            export JEST_JUNIT_OUTPUT_DIR="test-results/$TEST_TYPE"
            ;;
    esac

    # Combine command and arguments
    if [[ ${#jest_args[@]} -gt 0 ]]; then
        test_cmd="$test_cmd -- ${jest_args[*]}"
    fi

    echo "$test_cmd"
}

# Run unit tests
run_unit_tests() {
    log_test "Running unit tests..."

    local cmd
    cmd=$(TEST_TYPE="unit" build_test_command)
    
    if eval "$cmd"; then
        test_results["unit"]="PASSED"
        log_success "Unit tests passed"
        return 0
    else
        test_results["unit"]="FAILED"
        log_error "Unit tests failed"
        return 1
    fi
}

# Run integration tests
run_integration_tests() {
    log_test "Running integration tests..."

    # Start test services if needed
    if command -v docker-compose &> /dev/null; then
        log "Starting test services..."
        docker-compose -f docker-compose.test.yml up -d
        
        # Wait for services to be ready
        sleep 10
    fi

    local cmd
    cmd=$(TEST_TYPE="integration" build_test_command)
    
    local result=0
    if eval "$cmd"; then
        test_results["integration"]="PASSED"
        log_success "Integration tests passed"
    else
        test_results["integration"]="FAILED"
        log_error "Integration tests failed"
        result=1
    fi

    # Cleanup test services
    if command -v docker-compose &> /dev/null; then
        docker-compose -f docker-compose.test.yml down
    fi

    return $result
}

# Run end-to-end tests
run_e2e_tests() {
    log_test "Running end-to-end tests..."

    # Filter tests based on complexity level
    local e2e_config="playwright.config.js"
    case $COMPLEXITY_LEVEL in
        essential)
            e2e_config="playwright.essential.config.js"
            ;;
        enhanced)
            e2e_config="playwright.enhanced.config.js"
            ;;
        advanced)
            e2e_config="playwright.advanced.config.js"
            ;;
    esac

    local playwright_cmd="npx playwright test"
    
    if [[ "$VERBOSE" == "true" ]]; then
        playwright_cmd="$playwright_cmd --reporter=list"
    fi

    if [[ "${HEADLESS:-true}" == "true" ]]; then
        playwright_cmd="$playwright_cmd --headed=false"
    fi

    if [[ "$PARALLEL" == "true" ]]; then
        playwright_cmd="$playwright_cmd --workers=$PARALLEL_WORKERS"
    fi

    # Add configuration file
    playwright_cmd="$playwright_cmd --config=$e2e_config"

    if eval "$playwright_cmd"; then
        test_results["e2e"]="PASSED"
        log_success "End-to-end tests passed"
        return 0
    else
        test_results["e2e"]="FAILED"
        log_error "End-to-end tests failed"
        return 1
    fi
}

# Run performance tests
run_performance_tests() {
    log_test "Running performance tests..."

    # API performance tests
    if command -v artillery &> /dev/null || npx artillery --version &> /dev/null 2>&1; then
        log "Running API performance tests..."
        
        local artillery_config="test/performance/api-load-test.yml"
        if npx artillery run "$artillery_config" --output "test-results/performance/api-results.json"; then
            log_success "API performance tests passed"
        else
            log_error "API performance tests failed"
            test_results["performance"]="FAILED"
            return 1
        fi
    fi

    # Frontend performance tests
    log "Running frontend performance tests..."
    if npm run test:performance:frontend; then
        log_success "Frontend performance tests passed"
    else
        log_error "Frontend performance tests failed"
        test_results["performance"]="FAILED"
        return 1
    fi

    # Database performance tests
    if [[ "$COMPLEXITY_LEVEL" == "advanced" || "$COMPLEXITY_LEVEL" == "all" ]]; then
        log "Running database performance tests..."
        if npm run test:performance:database; then
            log_success "Database performance tests passed"
        else
            log_error "Database performance tests failed"
            test_results["performance"]="FAILED"
            return 1
        fi
    fi

    test_results["performance"]="PASSED"
    log_success "Performance tests passed"
    return 0
}

# Run security tests
run_security_tests() {
    log_test "Running security tests..."

    local security_result=0

    # Dependency vulnerability scan
    log "Scanning dependencies for vulnerabilities..."
    if npm audit --audit-level=moderate; then
        log_success "Dependency scan passed"
    else
        log_error "Dependency vulnerabilities found"
        security_result=1
    fi

    # SAST (Static Application Security Testing)
    if command -v snyk &> /dev/null || npx snyk --version &> /dev/null 2>&1; then
        log "Running static security analysis..."
        if npx snyk test; then
            log_success "Static security analysis passed"
        else
            log_error "Static security analysis failed"
            security_result=1
        fi
    fi

    # Security-focused unit tests
    log "Running security unit tests..."
    if npm test -- --testPathPattern='security'; then
        log_success "Security unit tests passed"
    else
        log_error "Security unit tests failed"
        security_result=1
    fi

    # Privacy compliance tests
    if [[ "$COMPLEXITY_LEVEL" == "advanced" || "$COMPLEXITY_LEVEL" == "all" ]]; then
        log "Running privacy compliance tests..."
        if npm run test:privacy; then
            log_success "Privacy compliance tests passed"
        else
            log_error "Privacy compliance tests failed"
            security_result=1
        fi
    fi

    if [[ $security_result -eq 0 ]]; then
        test_results["security"]="PASSED"
        log_success "Security tests passed"
    else
        test_results["security"]="FAILED"
        log_error "Security tests failed"
    fi

    return $security_result
}

# Run accessibility tests
run_accessibility_tests() {
    log_test "Running accessibility tests..."

    # Automated accessibility testing with axe-core
    log "Running automated accessibility tests..."
    if npx playwright test --config=playwright.a11y.config.js; then
        log_success "Automated accessibility tests passed"
    else
        log_error "Automated accessibility tests failed"
        test_results["accessibility"]="FAILED"
        return 1
    fi

    # Color contrast tests
    log "Running color contrast tests..."
    if npm run test:accessibility:contrast; then
        log_success "Color contrast tests passed"
    else
        log_error "Color contrast tests failed"
        test_results["accessibility"]="FAILED"
        return 1
    fi

    # Keyboard navigation tests
    log "Running keyboard navigation tests..."
    if npm run test:accessibility:keyboard; then
        log_success "Keyboard navigation tests passed"
    else
        log_error "Keyboard navigation tests failed"
        test_results["accessibility"]="FAILED"
        return 1
    fi

    # Screen reader compatibility tests
    if [[ "$COMPLEXITY_LEVEL" == "enhanced" || "$COMPLEXITY_LEVEL" == "advanced" || "$COMPLEXITY_LEVEL" == "all" ]]; then
        log "Running screen reader compatibility tests..."
        if npm run test:accessibility:screenreader; then
            log_success "Screen reader tests passed"
        else
            log_error "Screen reader tests failed"
            test_results["accessibility"]="FAILED"
            return 1
        fi
    fi

    test_results["accessibility"]="PASSED"
    log_success "Accessibility tests passed"
    return 0
}

# Run privacy compliance tests
run_privacy_tests() {
    log_test "Running privacy compliance tests..."

    # GDPR compliance tests
    log "Running GDPR compliance tests..."
    if npm run test:privacy:gdpr; then
        log_success "GDPR compliance tests passed"
    else
        log_error "GDPR compliance tests failed"
        test_results["privacy"]="FAILED"
        return 1
    fi

    # Data encryption tests
    log "Running data encryption tests..."
    if npm run test:privacy:encryption; then
        log_success "Data encryption tests passed"
    else
        log_error "Data encryption tests failed"
        test_results["privacy"]="FAILED"
        return 1
    fi

    # User consent management tests
    log "Running consent management tests..."
    if npm run test:privacy:consent; then
        log_success "Consent management tests passed"
    else
        log_error "Consent management tests failed"
        test_results["privacy"]="FAILED"
        return 1
    fi

    # Data export/deletion tests
    log "Running data portability tests..."
    if npm run test:privacy:portability; then
        log_success "Data portability tests passed"
    else
        log_error "Data portability tests failed"
        test_results["privacy"]="FAILED"
        return 1
    fi

    test_results["privacy"]="PASSED"
    log_success "Privacy compliance tests passed"
    return 0
}

# Run AI/ML specific tests
run_ai_tests() {
    log_test "Running AI/ML tests..."

    # Model accuracy tests
    log "Running model accuracy tests..."
    if npm run test:ai:accuracy; then
        log_success "Model accuracy tests passed"
    else
        log_error "Model accuracy tests failed"
        test_results["ai"]="FAILED"
        return 1
    fi

    # Bias detection tests
    log "Running bias detection tests..."
    if npm run test:ai:bias; then
        log_success "Bias detection tests passed"
    else
        log_error "Bias detection tests failed"
        test_results["ai"]="FAILED"
        return 1
    fi

    # Privacy-preserving ML tests
    log "Running federated learning tests..."
    if npm run test:ai:federated; then
        log_success "Federated learning tests passed"
    else
        log_error "Federated learning tests failed"
        test_results["ai"]="FAILED"
        return 1
    fi

    # AI explainability tests
    log "Running AI explainability tests..."
    if npm run test:ai:explainability; then
        log_success "AI explainability tests passed"
    else
        log_error "AI explainability tests failed"
        test_results["ai"]="FAILED"
        return 1
    fi

    test_results["ai"]="PASSED"
    log_success "AI/ML tests passed"
    return 0
}

# Generate comprehensive test report
generate_test_report() {
    if [[ "$GENERATE_REPORT" != "true" ]]; then
        return 0
    fi

    log "Generating comprehensive test report..."

    local report_file="test-results/comprehensive-report-$TIMESTAMP.html"
    
    cat > "$report_file" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>FlowState Test Report - $TIMESTAMP</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f0f0f0; padding: 20px; border-radius: 5px; }
        .summary { display: flex; gap: 20px; margin: 20px 0; }
        .metric { background: #f9f9f9; padding: 15px; border-radius: 5px; flex: 1; }
        .passed { color: #28a745; }
        .failed { color: #dc3545; }
        .skipped { color: #ffc107; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>FlowState Test Report</h1>
        <p>Generated: $(date)</p>
        <p>Environment: $ENVIRONMENT</p>
        <p>Complexity Level: $COMPLEXITY_LEVEL</p>
        <p>Test Type: $TEST_TYPE</p>
    </div>
    
    <div class="summary">
        <div class="metric">
            <h3>Total Tests</h3>
            <div style="font-size: 2em;">$total_tests</div>
        </div>
        <div class="metric">
            <h3 class="passed">Passed</h3>
            <div style="font-size: 2em; color: #28a745;">$passed_tests</div>
        </div>
        <div class="metric">
            <h3 class="failed">Failed</h3>
            <div style="font-size: 2em; color: #dc3545;">$failed_tests</div>
        </div>
        <div class="metric">
            <h3 class="skipped">Skipped</h3>
            <div style="font-size: 2em; color: #ffc107;">$skipped_tests</div>
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Test Suite</th>
                <th>Status</th>
                <th>Coverage</th>
            </tr>
        </thead>
        <tbody>
EOF

    # Add test results to report
    for test_suite in "${!test_results[@]}"; do
        local status="${test_results[$test_suite]}"
        local coverage_file="coverage/$test_suite/lcov-report/index.html"
        local coverage_link=""
        
        if [[ -f "$coverage_file" ]]; then
            coverage_link="<a href='../coverage/$test_suite/lcov-report/index.html'>View Coverage</a>"
        else
            coverage_link="N/A"
        fi
        
        cat >> "$report_file" << EOF
            <tr>
                <td>$test_suite</td>
                <td class="${status,,}">$status</td>
                <td>$coverage_link</td>
            </tr>
EOF
    done

    cat >> "$report_file" << EOF
        </tbody>
    </table>
    
    <h2>Coverage Summary</h2>
    <iframe src="../coverage/lcov-report/index.html" width="100%" height="400px"></iframe>
    
</body>
</html>
EOF

    log_success "Test report generated: $report_file"
}

# Print test summary
print_test_summary() {
    log ""
    log "=========================================="
    log "             TEST SUMMARY"
    log "=========================================="
    log "Environment: $ENVIRONMENT"
    log "Complexity Level: $COMPLEXITY_LEVEL"
    log "Test Type: $TEST_TYPE"
    log ""

    for test_suite in "${!test_results[@]}"; do
        local status="${test_results[$test_suite]}"
        case $status in
            "PASSED")
                log_success "$test_suite: $status"
                ((passed_tests++))
                ;;
            "FAILED")
                log_error "$test_suite: $status"
                ((failed_tests++))
                ;;
            "SKIPPED")
                log_warning "$test_suite: $status"
                ((skipped_tests++))
                ;;
        esac
        ((total_tests++))
    done

    log ""
    log "Total: $total_tests | Passed: $passed_tests | Failed: $failed_tests | Skipped: $skipped_tests"
    
    if [[ $failed_tests -gt 0 ]]; then
        log_error "Some tests failed!"
        return 1
    else
        log_success "All tests passed!"
        return 0
    fi
}

# Main test execution function
main() {
    local start_time
    start_time=$(date +%s)

    log "Starting FlowState test execution..."
    log "Test Type: $TEST_TYPE"
    log "Complexity Level: $COMPLEXITY_LEVEL"
    log "Environment: $ENVIRONMENT"

    setup_test_environment
    validate_prerequisites

    local overall_result=0

    # Execute tests based on type
    case $TEST_TYPE in
        all)
            run_unit_tests || overall_result=1
            if [[ "$BAIL_ON_FIRST_FAILURE" == "true" && $overall_result -ne 0 ]]; then exit 1; fi
            
            run_integration_tests || overall_result=1
            if [[ "$BAIL_ON_FIRST_FAILURE" == "true" && $overall_result -ne 0 ]]; then exit 1; fi
            
            run_e2e_tests || overall_result=1
            if [[ "$BAIL_ON_FIRST_FAILURE" == "true" && $overall_result -ne 0 ]]; then exit 1; fi
            
            run_security_tests || overall_result=1
            if [[ "$BAIL_ON_FIRST_FAILURE" == "true" && $overall_result -ne 0 ]]; then exit 1; fi
            
            run_accessibility_tests || overall_result=1
            if [[ "$BAIL_ON_FIRST_FAILURE" == "true" && $overall_result -ne 0 ]]; then exit 1; fi
            
            if [[ "$COMPLEXITY_LEVEL" == "advanced" || "$COMPLEXITY_LEVEL" == "all" ]]; then
                run_ai_tests || overall_result=1
                if [[ "$BAIL_ON_FIRST_FAILURE" == "true" && $overall_result -ne 0 ]]; then exit 1; fi
                
                run_privacy_tests || overall_result=1
                if [[ "$BAIL_ON_FIRST_FAILURE" == "true" && $overall_result -ne 0 ]]; then exit 1; fi
            fi
            ;;
        unit)
            run_unit_tests || overall_result=1
            ;;
        integration)
            run_integration_tests || overall_result=1
            ;;
        e2e)
            run_e2e_tests || overall_result=1
            ;;
        performance)
            run_performance_tests || overall_result=1
            ;;
        security)
            run_security_tests || overall_result=1
            ;;
        accessibility)
            run_accessibility_tests || overall_result=1
            ;;
        privacy)
            run_privacy_tests || overall_result=1
            ;;
        ai)
            if [[ "$COMPLEXITY_LEVEL" == "essential" ]]; then
                log_warning "AI tests skipped for essential complexity level"
                test_results["ai"]="SKIPPED"
            else
                run_ai_tests || overall_result=1
            fi
            ;;
        api|database|migration|ui)
            local cmd
            cmd=$(build_test_command)
            if eval "$cmd"; then
                test_results["$TEST_TYPE"]="PASSED"
                log_success "$TEST_TYPE tests passed"
            else
                test_results["$TEST_TYPE"]="FAILED"
                log_error "$TEST_TYPE tests failed"
                overall_result=1
            fi
            ;;
    esac

    # Calculate execution time
    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))

    generate_test_report
    print_test_summary

    log ""
    log "Test execution completed in ${duration}s"

    exit $overall_result
}

# Script execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    parse_args "$@"
    main
fi
