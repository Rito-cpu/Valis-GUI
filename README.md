# Valis GUI
A desktop graphical user interface for executing and monitoring whole-slide image (WSI) registration workflows using the valis-wsi command-line toolkit.

## Overview
VALIS GUI provides a user-friendly interface for configuring, launching, and visualizing image registration workflows without requiring direct interaction with the command line. The application wraps the valis-wsi backend in a structured, step-by-step workflow that guides users from sample selection through registration and result inspection.

The system is designed to support reproducible image processing, streamlined configuration, and real-time progress monitoring in research and laboratory environments.

## Key Features
- **Guided Registration Workflow**
Step-by-step interface for sample upload, registration configuration, and execution.

- **Docker-Backed Execution**
Runs valis-wsi inside a controlled containerized environment for platform consistency and dependency isolation.

- **Dynamic Settings Panels**
Toggle-based configuration sections bound directly to valis-wsi options.

- **Live Progress Monitoring**
Tracks registration stages and image processing progress in real time.

- **Result Visualization**
Displays registered slide outputs and allows users to inspect different registration types.

- **Session-Based Output Management**
Stores results in user-defined directories alongside the settings used for each run.

## Why this exists
Whole-slide image registration through valis-wsi is powerful but primarily terminal-driven and configuration-heavy. This project was created to make advanced image registration accessible to researchers and analysts by providing an interactive, visual workflow that reduces setup complexity, improves usability, and supports consistent execution across users and systems.

## Project Structure (High-Level)
```
digital-twin-pipeline/
├─ docker/
│  └─ Dockerfile
├─ resources/
│  └─ images/
│     ├─ downloads/
│        └─ image files...
│     ├─ svg_icons/
│        └─ image files...
│     └─ svg_images/
│        └─ image files...
├─ src/
│  ├─ core/
│     ├─ json/
│        ├─ json_encoder.py
│        ├─ json_settings.py
│        └─ json_themes.py
│     ├─ scripts/
│        └─ valis-wsi based scripts for execution...
│     ├─ validation/
│        └─ data validation helper files...
│     ├─ app_config.py
│     ├─ image_functions.py
│     ├─ keyword_store.py
│     └─ pyqt_core.py
│  ├─ gui/
│     ├─ models/
│        └─ custom widget folders...
│     ├─ themes/
│        └─ json files with color schemes for app...
│     └─ views/
│        └─ columns/
│           └─ ui files for window...
│        └─ pages/
│           └─ ui files for window...
│        └─ windows/
│           └─ ui files for window...
│  └─ main_window.py
├─ LICENSE
├─ main.py
├─ main.spec
├─ README.md
├─ settings.json                  # Important app settings config file
├─ tech_doc.MD                  # Important app settings config file
├─ requirements.txt
└─ set_vips_path.py
```

## Requirements
- Python 3.9.10 (recommended)
- PyQt6
- Docker Desktop (installed and running)
- macOS (validated platform)

## How It Works
1. Sample Ingestion
Users select a directory containing whole-slide image samples.

2. Configuration
Registration settings are selected through interactive, toggle-based panels mapped to valis-wsi parameters.

3. Containerized Execution
The GUI launches or connects to a Docker container and executes the registration process using the selected options.

4. Progress Tracking
Output directories and live process logs are monitored to display real-time progress and stage updates.

5. Result Inspection
Registered images and derived outputs are displayed within the results view for validation and review.

## How to Run
1. Clone the repository.
2. Install dependencies: pip install -r requirements.txt
3. Ensure Docker Desktop is running.
4. Open the project in your IDE.
5. Run main.py.
6. Use the main menu to upload samples and configure registration settings.

Note:
*PyInstaller packaging is implemented but not finalized. The application is currently validated for macOS only.*

## Inputs & Outputs
### Inputs
- **Whole-Slide Images**
Directory containing WSI samples supported by valis-wsi.

- **Registration Settings**
User-selected configuration options for rigid or non-rigid workflows.

### Outputs
- **Registered Images**
Transformed slide images saved to a user-defined output directory.

- **Session Metadata**
Settings and logs associated with each registration run.

- **Progress Logs**
Real-time status and stage output from the registration process.

## Status
The core registration pipeline and GUI workflow are operational. Export functionality, information panels, and finalized packaging remain in progress. Compatibility with newer valis-wsi releases should be validated prior to production use.

## LICENSE
This project is licensed under the [MIT License].