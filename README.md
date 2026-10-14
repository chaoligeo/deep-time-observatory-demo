# Deep-time Observatory Demo
## 深时观测台 · 科学数据系统演示

This repository provides a lightweight, practical demonstration of a deep-time scientific data system aligned with the **Deep-time Observatory (DDE · 深时观测台)** architecture.

It focuses on core capabilities used by working earth scientists:

- Geological time scale reference and age conversion
- Sample occurrence / event records with age, location, and taxonomic or lithologic attributes
- Filtering and exploration by time interval, data type, and location
- Simple timeline and distribution visualization

The demo uses synthetic but realistic sample data. It is intended as a starting point for discussing data organization, governance, and pilot applications rather than a production system.

### Quick Start

```bash
# Clone the repository
git clone https://github.com/chaoligeo/deep-time-observatory-demo.git
cd deep-time-observatory-demo

# Install dependencies
pip install -r requirements.txt

# Run the interactive demo
streamlit run app.py
```

### Contents

- `app.py` — Streamlit application for interactive exploration
- `data/` — Sample geological timescale, occurrence records, and key events
- `utils/time_utils.py` — Basic age conversion and interval helpers
- `requirements.txt` — Python dependencies

### Design Notes

- Uses standard earth science terminology (e.g., stages, periods, Ma, occurrence, lithology).
- Emphasizes clear age intervals and uncertainty handling at a basic level.
- Data schema is intentionally simple to illustrate integration points with external resources such as PBDB, Macrostrat, GEOROC, or national geological databases.

### License

MIT License — see LICENSE file.
