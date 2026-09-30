# IPL 2026 Dashboard Setup Instructions

This document contains all the necessary commands to run the IPL 2026 Analytics Dashboard either locally using a Python virtual environment or via Docker.

## Option 1: Running with Docker (Recommended)

Docker packages the application and its dependencies into a single container, ensuring it runs seamlessly without requiring any local Python setup.

**Run the Docker Container:**
```bash
docker compose up --build
```
The dashboard will be available at: http://localhost:8501

*(Note: To stop the container, you can press `Ctrl+C` in the terminal, or run `docker compose down` in another terminal window).*

---

## Option 2: Running Locally (Python Virtual Environment)

If you prefer to run the application directly on your machine, follow these steps to set up a virtual environment and install the dependencies.

**1. Create a Virtual Environment:**
```bash
python3 -m venv venv
```

**2. Install Dependencies:**
```bash
./venv/bin/pip install -r requirements.txt
```

**3. Run the Streamlit Application:**
```bash
./venv/bin/streamlit run app.py
```
The dashboard will open automatically in your default web browser at http://localhost:8501.
