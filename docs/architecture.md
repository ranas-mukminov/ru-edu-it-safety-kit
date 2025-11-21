# Architecture

The **ru-edu-it-safety-kit** is designed as a modular toolkit.

## Components

### 1. Core Logic (Python)
- **Models**: Pydantic models (`SchoolProfile`) define the data structure for school infrastructure.
- **Validators**: Ensure that the input YAML profiles are syntactically and logically correct.
- **Generators**:
    - `MeasuresPlanner`: Deterministic rule engine that maps profile attributes (e.g., "has students", "multi-building") to specific safety measures.
    - `LeafletGenerator`: Template engine that produces human-readable Markdown documents for non-technical stakeholders.

### 2. Configuration Templates
- **OpenWrt / pfSense / RouterOS**: Static configuration snippets that serve as a baseline. They are not fully automated "Infrastructure as Code" but rather "Copy-Paste-Adapt" templates.
- **Logging**: Docker-based examples for spinning up a local log aggregation stack.

## Data Flow

1.  **User** creates a `school_profile.yml`.
2.  **CLI** (`ru-safety`) reads and validates the profile.
3.  **CLI** invokes generators to produce:
    - A safety plan (checklist).
    - PDF-ready leaflets (Markdown).
4.  **User** manually applies the recommended network configurations using the provided templates as a reference.
