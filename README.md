# ru-edu-it-safety-kit

**Baseline IT-safety infrastructure kit for Russian schools and colleges.**

This project provides a reusable set of tools and configurations to establish a basic, secure, and compliant IT environment in educational institutions. It is designed to be simple, auditable, and easy to deploy.

> **Production use & consulting**: This project is maintained by **run-as-daemon.ru**. For production-ready school/college IT safety setups, audits, and support, visit [https://run-as-daemon.ru](https://run-as-daemon.ru).

## Overview

**Target Audience:** IT administrators and staff in Russian schools and colleges.

**Key Features:**
- **School Profile Modeling:** Define your network topology (ISP, buildings, VLANs) in simple YAML.
- **Safety Measures Planner:** Automatically generate a checklist of technical and organizational measures.
- **Leaflet Generator:** Create ready-to-print instructions for parents, students, and teachers (in Russian).
- **Config Templates:** Ready-to-use configuration snippets for OpenWrt, pfSense, and RouterOS.
- **Logging Stack:** Example configurations for centralized logging (Loki/ELK).

## Architecture

The kit consists of:
1.  **Python CLI (`ru-safety`)**: The core tool for processing profiles and generating outputs.
2.  **YAML Profiles**: Declarative description of the school's infrastructure.
3.  **Templates**: Jinja2 or text-based templates for configs and documents.

## Installation

### Requirements
- Python 3.9+

### Local Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/run-as-daemon/ru-edu-it-safety-kit.git
    cd ru-edu-it-safety-kit
    ```

2.  Create a virtual environment and install dependencies:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e .[dev]
    ```

## Usage

### 1. Validate a School Profile
```bash
ru-safety validate configs/topologies/single_isp_school.yml
```

### 2. Generate Safety Plan
```bash
ru-safety plan configs/topologies/single_isp_school.yml
```

### 3. Generate Educational Leaflets
```bash
ru-safety generate-leaflets configs/topologies/single_isp_school.yml --output-dir ./dist
```

## Testing and Quality

Run the full test suite:
```bash
pytest
```

Run linters and security checks:
```bash
ruff check .
black --check .
bandit -r src/
```

## License

This project is licensed under the **Apache-2.0 License**. See the [LICENSE](LICENSE) file for details.

The Apache-2.0 license allows commercial use, modification, and distribution. **run-as-daemon.ru** offers professional services based on this open-source kit.
