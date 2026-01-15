#!/usr/bin/env make
# Makefile for Zigbee2MQTT Device Converter Development

.PHONY: help check-converters test-converter validate-syntax lint-yaml clean info

# Default target
help: ## Show this help message
	@echo "Zigbee2MQTT Device Converter Development"
	@echo "======================================="
	@echo ""
	@echo "Available targets:"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

check-converters: ## Validate syntax of all converter files
	@echo "🔍 Checking Zigbee converter syntax..."
	@for file in relay-2-types/*.mjs; do \
		echo "Checking $$file..."; \
		node -c "$$file" && echo "✅ $$file: Valid syntax" || echo "❌ $$file: Syntax error"; \
	done

test-converter: ## Test specific converter file (use CONVERTER=filename)
	@if [ -z "$(CONVERTER)" ]; then \
		echo "❌ Please specify a converter file: make test-converter CONVERTER=2-gang-switch-converter.mjs"; \
		exit 1; \
	fi
	@if [ ! -f "relay-2-types/$(CONVERTER)" ]; then \
		echo "❌ Converter file relay-2-types/$(CONVERTER) not found"; \
		exit 1; \
	fi
	@echo "🧪 Testing converter: $(CONVERTER)"
	@node -c "relay-2-types/$(CONVERTER)" && echo "✅ $(CONVERTER): Valid syntax" || echo "❌ $(CONVERTER): Syntax error"

validate-syntax: check-converters ## Alias for check-converters

lint-yaml: ## Lint YAML files in .github directory
	@echo "📝 Linting YAML files..."
	@if command -v yamllint >/dev/null 2>&1; then \
		yamllint .github/ || echo "⚠️  yamllint not found - skipping YAML validation"; \
	else \
		echo "⚠️  yamllint not found - install with: pip install yamllint"; \
	fi

list-converters: ## List all available converter files
	@echo "📋 Available Zigbee Converters:"
	@echo "=============================="
	@for file in relay-2-types/*.mjs; do \
		basename="$$(basename $$file)"; \
		echo "  📄 $$basename"; \
		if head -n 20 "$$file" | grep -q "description.*:"; then \
			description=$$(head -n 20 "$$file" | grep "description.*:" | cut -d'"' -f4 | head -n 1); \
			echo "      📝 $$description"; \
		fi; \
		echo ""; \
	done

show-converter: ## Show details of specific converter (use CONVERTER=filename)
	@if [ -z "$(CONVERTER)" ]; then \
		echo "❌ Please specify a converter file: make show-converter CONVERTER=2-gang-switch-converter.mjs"; \
		exit 1; \
	fi
	@if [ ! -f "relay-2-types/$(CONVERTER)" ]; then \
		echo "❌ Converter file relay-2-types/$(CONVERTER) not found"; \
		exit 1; \
	fi
	@echo "📄 Converter Details: $(CONVERTER)"
	@echo "=================================="
	@echo ""
	@echo "🔍 Fingerprint Information:"
	@grep -A 5 "fingerprint:" "relay-2-types/$(CONVERTER)" || echo "  No fingerprint found"
	@echo ""
	@echo "🏷️  Model Information:"
	@grep "model:" "relay-2-types/$(CONVERTER)" || echo "  No model found"
	@grep "vendor:" "relay-2-types/$(CONVERTER)" || echo "  No vendor found"
	@grep "description:" "relay-2-types/$(CONVERTER)" || echo "  No description found"

clean: ## Clean up temporary files
	@echo "🧹 Cleaning up..."
	@find . -type f -name "*.tmp" -delete
	@find . -type f -name "*.bak" -delete
	@echo "✅ Cleanup completed!"

info: ## Show repository and development environment info
	@echo "ℹ️  Zigbee Converter Development Info"
	@echo "==================================="
	@echo "Repository: $(shell git remote get-url origin 2>/dev/null || echo 'Not a git repository')"
	@echo "Branch: $(shell git branch --show-current 2>/dev/null || echo 'Not a git repository')"
	@echo "Node.js: $(shell node --version 2>/dev/null || echo 'Node.js not found')"
	@echo "Converters: $(shell ls relay-2-types/*.mjs 2>/dev/null | wc -l | tr -d ' ') files"
	@echo ""
	@echo "📁 Repository Structure:"
	@tree -L 2 . 2>/dev/null || ls -la

# Development workflow targets
dev-workflow: ## Show recommended development workflow
	@echo "🔄 Recommended Development Workflow"
	@echo "=================================="
	@echo ""
	@echo "1. Check existing converters:"
	@echo "   make list-converters"
	@echo ""
	@echo "2. Validate converter syntax:"
	@echo "   make check-converters"
	@echo ""
	@echo "3. Test specific converter:"
	@echo "   make test-converter CONVERTER=filename.mjs"
	@echo ""
	@echo "4. Show converter details:"
	@echo "   make show-converter CONVERTER=filename.mjs"
	@echo ""
	@echo "5. Integration with Zigbee2MQTT:"
	@echo "   - Copy converter to Zigbee2MQTT external_converters/"
	@echo "   - Restart Zigbee2MQTT to load new converter"
	@echo "   - Check logs for device recognition"

# Quick commands for common tasks
quick-check: ## Quick syntax check of all converters
	@for file in relay-2-types/*.mjs; do node -c "$$file" > /dev/null 2>&1 && echo "✅ $$(basename $$file)" || echo "❌ $$(basename $$file)"; done

# Installation helper for Zigbee2MQTT integration
install-help: ## Show installation instructions for Zigbee2MQTT
	@echo "📦 Zigbee2MQTT Installation Instructions"
	@echo "========================================"
	@echo ""
	@echo "1. Locate your Zigbee2MQTT installation:"
	@echo "   - Docker: /app/external_converters/"
	@echo "   - Manual: zigbee2mqtt/external_converters/"
	@echo ""
	@echo "2. Copy converter files:"
	@echo "   cp relay-2-types/*.mjs /path/to/zigbee2mqtt/external_converters/"
	@echo ""
	@echo "3. Update configuration.yaml:"
	@echo "   external_converters:"
	@echo "     - filename.mjs"
	@echo ""
	@echo "4. Restart Zigbee2MQTT and check logs for:"
	@echo "   [INFO] Loaded external converter filename.mjs"
