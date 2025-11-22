# 🛡️ ru-edu-it-safety-kit

![CI](https://github.com/ranas-mukminov/ru-edu-it-safety-kit/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)

🇬🇧 English | 🇷🇺 [Русская версия](README.ru.md)

Baseline IT safety infrastructure kit for Russian schools and colleges. This toolkit provides a comprehensive set of tools and configuration templates to establish secure, compliant, and maintainable IT environments in educational institutions.

**Author:** [Ranas Mukminov](https://github.com/ranas-mukminov)  
**Website:** [run-as-daemon.ru](https://run-as-daemon.ru)

## Overview

`ru-edu-it-safety-kit` is an open-source project designed specifically for IT administrators and technical staff in Russian educational institutions (schools, colleges, technical schools). It addresses the unique challenges of securing educational networks: student safety, content filtering, network segmentation, and compliance with Russian regulatory requirements.

The kit provides declarative configuration, automated safety planning, and ready-to-use documentation templates. It helps schools implement baseline security measures without requiring deep networking expertise or expensive consultants.

## Key Features

- **Declarative School Profiles:** Describe your network topology (ISPs, buildings, VLANs, roles) in simple YAML format
- **Automated Safety Planning:** Generate technical and organizational security measures based on your infrastructure profile
- **Educational Content Generator:** Create ready-to-print leaflets and guidelines for parents, students, and teachers in Russian
- **Multi-Vendor Support:** Configuration templates for OpenWrt, pfSense, and MikroTik RouterOS
- **Network Segmentation:** VLAN-based isolation for admin, teacher, student, and guest networks
- **Content Filtering:** DNS-based filtering configurations (SkyDNS, Yandex.DNS compatible)
- **Centralized Logging:** Docker-based examples for log aggregation (Loki/Grafana stack)
- **Compliance-Focused:** Aligned with Russian educational regulations and information security requirements
- **Production-Ready:** Includes CI/CD, tests, linting, and security checks

## Architecture / Components

The kit consists of three main layers:

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Tool (ru-safety)                  │
│                  Python 3.9+ / Click                     │
└─────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌──────────┐    ┌───────────┐   ┌──────────────┐
    │ Validator│    │  Measures │   │   Leaflet    │
    │          │    │  Planner  │   │  Generator   │
    └──────────┘    └───────────┘   └──────────────┘
           │               │               │
           └───────────────┴───────────────┘
                           ▼
              ┌─────────────────────────┐
              │   School Profile YAML   │
              │  (topology, VLANs, ISPs)│
              └─────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌──────────┐    ┌───────────┐   ┌──────────────┐
    │ OpenWrt  │    │  pfSense  │   │  RouterOS    │
    │ templates│    │ templates │   │  templates   │
    └──────────┘    └───────────┘   └──────────────┘
```

**Components:**

1. **Python CLI (`ru-safety`)**: Core tool for validation, planning, and content generation
2. **Pydantic Models**: Type-safe profile definitions with validation
3. **YAML Profiles**: Declarative infrastructure description
4. **Jinja2 Templates**: Generate Markdown leaflets for stakeholders
5. **Configuration Templates**: Static snippets for network devices (copy-paste-adapt approach)
6. **Docker Logging Stack**: Example setup for centralized log collection

## Requirements

### System Requirements

- **Operating System:** Linux (Ubuntu 20.04+, Debian 11+, RHEL 8+, Rocky Linux 8+) or macOS
- **Python:** 3.9 or higher
- **Disk Space:** ~100 MB for the toolkit and dependencies
- **Memory:** 512 MB RAM minimum
- **Network:** Internet access for dependency installation

### Access Requirements

- Standard user account (no root required for running CLI)
- `sudo` access for deploying configurations to network devices

### Optional Dependencies

- **Docker & Docker Compose:** For running the centralized logging stack
- **Network Devices:** OpenWrt, pfSense, or MikroTik RouterOS for applying configurations
- **PDF Generator:** Pandoc or similar tool for converting Markdown leaflets to PDF

## Quick Start (TL;DR)

Get started in 5 minutes:

```bash
# 1. Clone the repository
git clone https://github.com/ranas-mukminov/ru-edu-it-safety-kit.git
cd ru-edu-it-safety-kit

# 2. Install the toolkit
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# 3. Validate a sample school profile
ru-safety validate configs/topologies/single_isp_school.yml

# 4. Generate a safety plan
ru-safety plan configs/topologies/single_isp_school.yml

# 5. Generate educational leaflets
ru-safety generate-leaflets configs/topologies/single_isp_school.yml --output-dir ./output
```

**Next Steps:**

- Create your own school profile: `cp configs/topologies/single_isp_school.yml my-school.yml`
- Edit `my-school.yml` with your network details
- Apply generated configurations to your network devices
- Print and distribute leaflets to parents, students, and teachers

## Detailed Installation

### Install on Ubuntu / Debian

```bash
# Install Python 3.9+ and venv
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git

# Clone the repository
git clone https://github.com/ranas-mukminov/ru-edu-it-safety-kit.git
cd ru-edu-it-safety-kit

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the toolkit
pip install -e .
```

### Install on RHEL / Rocky / AlmaLinux

```bash
# Install Python 3.9+ and git
sudo dnf install -y python39 python39-pip git

# Clone the repository
git clone https://github.com/ranas-mukminov/ru-edu-it-safety-kit.git
cd ru-edu-it-safety-kit

# Create virtual environment
python3.9 -m venv .venv
source .venv/bin/activate

# Install the toolkit
pip install -e .
```

### Development Installation

For contributors and developers:

```bash
# Install with development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run linters
ruff check .
black --check .

# Run security checks
bandit -r src/
pip-audit
```

## Configuration

### Creating a School Profile

Create a YAML file describing your network topology:

```yaml
# my-school.yml
name: "МБОУ СОШ №1"
type: school

isps:
  - name: "Rostelecom"
    speed_mbps: 100
    is_primary: true

buildings:
  - name: "Main Building"
    is_hq: true
    vlans:
      - id: 10
        name: "admin"
        role: admin
        subnet: "10.10.10.0/24"
      - id: 20
        name: "teachers"
        role: teacher
        subnet: "10.10.20.0/24"
      - id: 30
        name: "students"
        role: student
        subnet: "10.10.30.0/24"
      - id: 40
        name: "guests"
        role: guest
        subnet: "10.10.40.0/24"
```

**Profile Fields:**

- `name`: School name (any string)
- `type`: `school` or `college`
- `isps`: List of Internet Service Providers
  - `name`: ISP name
  - `speed_mbps`: Connection speed in Mbps
  - `is_primary`: Primary uplink (boolean)
- `buildings`: List of buildings
  - `name`: Building name
  - `is_hq`: Headquarters/main building flag
  - `vlans`: Network segments
    - `id`: VLAN ID (1-4094)
    - `name`: VLAN name
    - `role`: `admin`, `teacher`, `student`, or `guest`
    - `subnet`: IP subnet in CIDR notation

### Example Profiles

The toolkit includes two reference profiles:

- **`configs/topologies/single_isp_school.yml`**: Small school, single ISP, one building
- **`configs/topologies/multi_building_college.yml`**: College with multiple buildings and VPN interconnect

### Network Device Configurations

Configuration templates are located in `configs/`:

- **`configs/openwrt/`**: OpenWrt VLAN and firewall configurations
- **`configs/pfsense/`**: pfSense VLAN and filtering rules
- **`configs/routeros/`**: MikroTik RouterOS interface and firewall scripts
- **`configs/logging/`**: Docker Compose stack for Loki/Grafana logging

These templates are **not fully automated**—they serve as copy-paste-adapt references. You must manually apply them to your devices.

## Usage & Common Tasks

### Validate a School Profile

Check if your YAML profile is syntactically and logically correct:

```bash
ru-safety validate my-school.yml
```

Output:
```
✅ Profile 'МБОУ СОШ №1' is valid.
⚠️  Warning: No backup ISP configured - consider redundancy.
```

### Generate Safety Plan

Create a checklist of recommended security measures:

```bash
ru-safety plan my-school.yml
```

Output:
```
🛡️  Safety Plan for: МБОУ СОШ №1

Technical Measures:
 - Configure VLAN segmentation (4 VLANs detected)
 - Enable DNS-based content filtering for student network
 - Configure firewall rules to isolate student VLAN from admin/teacher networks
 - Enable DHCP snooping on switches
 - Configure centralized logging

Organizational Measures:
 - Create acceptable use policy for students
 - Train teachers on network security basics
 - Establish incident response procedure
 - Document network topology and configurations
```

### Generate Educational Leaflets

Create Markdown documents for stakeholders:

```bash
ru-safety generate-leaflets my-school.yml --output-dir ./leaflets
```

Output files:
- `leaflets/parents.md`: IT safety rules for parents
- `leaflets/students.md`: IT safety rules for students
- `leaflets/teachers.md`: IT safety guidelines for teachers

Convert to PDF using Pandoc:

```bash
pandoc leaflets/parents.md -o leaflets/parents.pdf --pdf-engine=xelatex -V mainfont="DejaVu Sans"
```

### Apply Network Configurations

1. Review the appropriate template:
   - For OpenWrt: `configs/openwrt/vlan_config.conf`
   - For pfSense: `configs/pfsense/firewall_rules.xml`
   - For RouterOS: `configs/routeros/firewall.rsc`

2. Adapt the template to your topology (replace placeholder IPs, VLAN IDs)

3. Apply manually via device WebUI or CLI

4. Test connectivity for each VLAN

### Start Centralized Logging (Optional)

```bash
cd configs/logging/loki-stack
docker-compose up -d
```

Access Grafana at `http://<YOUR_SERVER_IP>:3000` (default credentials: `admin/admin`)

Configure your network devices to send logs to the Loki endpoint.

## Update / Upgrade

### Update the Toolkit

```bash
cd ru-edu-it-safety-kit
git pull origin main

# Reinstall dependencies
source .venv/bin/activate
pip install -e .
```

### Migrate Profiles

If the profile schema changes, migration instructions will be provided in `CHANGELOG.md`. Always validate your profiles after updating:

```bash
ru-safety validate my-school.yml
```

## Logs, Monitoring, and Troubleshooting

### Check CLI Logs

The CLI outputs directly to stdout/stderr. Use shell redirection for logging:

```bash
ru-safety plan my-school.yml 2>&1 | tee plan-output.log
```

### Common Issues

**Issue:** `ru-safety: command not found`

**Solution:** Activate the virtual environment:
```bash
source .venv/bin/activate
```

**Issue:** YAML validation fails with "invalid schema"

**Solution:** Check for typos in field names. Compare with examples in `configs/topologies/`. Ensure VLAN IDs are integers, not strings.

**Issue:** No data in Grafana dashboards

**Solution:**
- Check Docker containers: `docker-compose ps`
- Verify network device log forwarding configuration
- Check Loki logs: `docker-compose logs loki`

**Issue:** Permission denied when running scripts

**Solution:** Ensure scripts are executable:
```bash
chmod +x scripts/*.sh
```

### Network Device Troubleshooting

**OpenWrt:**
```bash
# Check VLAN configuration
cat /etc/config/network

# View firewall rules
iptables -L -v -n
```

**pfSense:**
- Navigate to Diagnostics → States → Show States
- Check Firewall Logs under Status → System Logs → Firewall

**MikroTik RouterOS:**
```bash
/interface vlan print
/ip firewall filter print
```

## Security Notes

### Baseline Security Checklist

- **Change default passwords:** Update default credentials on all network devices
- **Enable HTTPS:** Use TLS for WebUI access to routers and switches
- **Restrict management access:** Limit admin VLAN to specific IP ranges
- **DNS filtering:** Force student network through content filtering DNS (e.g., SkyDNS, Yandex.DNS)
- **Regular updates:** Keep network device firmware and toolkit dependencies up-to-date
- **Access logs:** Enable and regularly review connection logs for anomalies
- **Physical security:** Secure network equipment in locked cabinets
- **Firewall rules:** Block inter-VLAN traffic except for necessary services (e.g., DNS, NTP)

### Content Filtering

This toolkit **does not include circumvention tools**. It provides configurations for legal content filtering solutions compliant with Russian regulations.

Recommended DNS filtering providers for schools:
- SkyDNS (Школьный фильтр)
- Yandex.DNS (Семейный режим)
- Custom DNS blacklists based on Roskomnadzor registry

### Secrets Management

- **No hardcoded secrets:** All example configurations use placeholders like `<YOUR_PASSWORD>`
- **Environment variables:** Store sensitive data in `.env` files (add to `.gitignore`)
- **Access control:** Limit repository access to IT staff only

### Regulatory Compliance

This toolkit aligns with:
- **Federal Law 436-FZ:** Protection of children from harmful information
- **Order 1274:** Requirements for educational institution networks
- **FSTEC recommendations:** Baseline security measures for educational organizations

**Legal Disclaimer:** The provided templates and documents are **examples only** and do not constitute legal advice. All policies and configurations must be reviewed and approved by your institution's administration and legal department.

## Project Structure

```
ru-edu-it-safety-kit/
├── src/
│   └── ru_edu_it_safety_kit/      # Python package
│       ├── cli.py                  # CLI entry point (Click)
│       ├── models/                 # Pydantic data models
│       ├── validators/             # Profile validation logic
│       └── generators/             # Safety planner & leaflet generator
├── configs/
│   ├── topologies/                 # Example school profiles (YAML)
│   ├── openwrt/                    # OpenWrt configuration templates
│   ├── pfsense/                    # pfSense configuration templates
│   ├── routeros/                   # MikroTik RouterOS scripts
│   └── logging/                    # Centralized logging stack (Docker)
├── policy_templates/               # Markdown templates for stakeholders
│   ├── it_rules_for_parents.ru.md
│   ├── it_rules_for_students.ru.md
│   └── it_rules_for_teachers.ru.md
├── tests/                          # Pytest unit and integration tests
├── docs/                           # Additional documentation
├── .github/
│   └── workflows/
│       └── ci.yml                  # GitHub Actions CI pipeline
├── pyproject.toml                  # Python project metadata
├── LICENSE                         # Apache-2.0 license
└── README.md                       # This file
```

## Roadmap / Plans

**Version 0.2.0 (Q2 2025):**
- Interactive profile builder (`ru-safety init`)
- Export safety plan to PDF
- Support for dual-ISP failover configurations
- Ansible playbooks for automated device configuration

**Version 0.3.0 (Q3 2025):**
- Web UI for profile management
- Pre-built Grafana dashboards for network monitoring
- Integration with Russian DPI solutions (TSPU compliance)

**Community Requests:**
- Support for Cisco IOS templates
- Integration with Russian SIEM systems
- Multi-language support (Tatar, Bashkir, other regional languages)

See the [GitHub Issues](https://github.com/ranas-mukminov/ru-edu-it-safety-kit/issues) for detailed discussions.

## Contributing

Contributions are welcome! This project is open-source and community-driven.

### How to Contribute

1. **Report issues:** Use [GitHub Issues](https://github.com/ranas-mukminov/ru-edu-it-safety-kit/issues) to report bugs or request features
2. **Submit pull requests:**
   - Fork the repository
   - Create a feature branch: `git checkout -b feature/my-improvement`
   - Make your changes
   - Run tests: `pytest`
   - Run linters: `ruff check . && black --check .`
   - Submit a PR with a clear description

### Code Style Guidelines

- **Python:** Follow PEP 8, use type hints, max line length 120
- **YAML:** 2-space indentation, use safe_load
- **Markdown:** Use headings, lists, and code blocks for readability
- **Shell scripts:** Use `shellcheck` for validation

### Testing Requirements

All new features must include:
- Unit tests for logic (`tests/unit/`)
- Integration tests for CLI commands (`tests/integration/`)
- Example configurations demonstrating the feature

Run the full test suite before submitting:
```bash
pytest --cov=src/ru_edu_it_safety_kit tests/
```

## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for full text.

The Apache 2.0 license allows:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Patent use
- ✅ Private use

**Copyright © 2025 run-as-daemon.ru**

## Author and Commercial Support

**Author:** [Ranas Mukminov](https://github.com/ranas-mukminov)  
**GitHub:** [@ranas-mukminov](https://github.com/ranas-mukminov)

This is an open-source project maintained by **run-as-daemon.ru**, a DevOps consulting and infrastructure automation company specializing in Russian enterprise and educational IT.

### Commercial Services

For production deployments, customization, and ongoing support, we offer:

- **School IT Infrastructure Audits:** Evaluate current security posture and provide detailed improvement plans
- **Custom Setup and Configuration:** End-to-end implementation of secure school networks with VLAN segmentation, content filtering, and centralized monitoring
- **Training and Knowledge Transfer:** Hands-on workshops for IT administrators and teachers
- **Managed Support:** Ongoing maintenance, incident response, and compliance consulting
- **Custom Development:** Tailored features, integrations with existing school systems (1C, ERP, LMS)

**Contact:** Visit [https://run-as-daemon.ru](https://run-as-daemon.ru) or reach out via the [GitHub profile](https://github.com/ranas-mukminov).

---

**Support this project:** If this toolkit helps your institution, please ⭐ star the repository and share it with other schools!
