# DAWN Installation Guide

## Requirements

- Python 3.8 or higher
- Required Python packages:
  - PyYAML (for configuration loading)
  - asyncio (for async operations)
  - logging (for system logging)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-org/DAWN.git
cd DAWN
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Optional Dependencies

- PyYAML: For YAML configuration support
  - If not installed, the system will fall back to JSON configuration
  - To install: `pip install PyYAML`

## Configuration

The system can use either YAML or JSON configuration files. If PyYAML is not installed, the system will automatically fall back to JSON format.

Example configuration files are provided in the `config/` directory:
- `pulse_config.yaml` (or `pulse_config.json`)
- `thermal_config.yaml` (or `thermal_config.json`)

## Troubleshooting

If you encounter issues with configuration loading:
1. Check that PyYAML is installed: `pip install PyYAML`
2. Verify configuration file format (YAML or JSON)
3. Check file permissions
4. Review logs for specific error messages 