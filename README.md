# Travel Info CLI Tool

A command-line Python tool that generates structured travel information for any city, tailored to either **leisure** or **business** purposes using **Google Gemini API**.

---

## Features

- Generates structured JSON with:
  - `overview` (3–5 concise bullets)
  - `things_to_know`
  - `nearby_transport`
  - `how_to_get_there`
  - `best_time_to_travel`
- Purpose-aware responses: leisure or business
- Retry mechanism and quota-aware handling
- Free-tier compatible (`gemini-2.5-flash`)
- Defensive JSON parsing to avoid broken outputs

---

## Setup

1. Clone the repository:

```bash
git clone git@github.com:safwanvk/travel-info-cli.git
cd travel-info-cli
````

2. Create and activate a Python virtual environment:

```bash
python3 -m venv env
source env/bin/activate  # Linux/macOS
# env\Scripts\activate    # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your **Gemini API key**:

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_key_here
```

---

## How to Run

```bash
python travel_info.py "Place Name" leisure|business
```

### Examples:

```bash
python travel_info.py "Istanbul" leisure
python travel_info.py "Bengaluru" business
python travel_info.py "Singapore" leisure
```

Output is valid JSON:

```json
{
  "place": "Istanbul",
  "purpose": "leisure",
  "overview": [
    "Explore iconic historical sites like Hagia Sophia and Blue Mosque.",
    "Indulge in vibrant bazaars and diverse culinary delights.",
    "Enjoy scenic Bosphorus cruises connecting two continents.",
    "Discover charming neighborhoods and rich cultural experiences."
  ],
  "things_to_know": [
    "The local currency is Turkish Lira (TRY).",
    "Modest dress is recommended for religious sites; carry a scarf.",
    "Istanbulkart is essential for convenient public transportation.",
    "Bargaining is customary in traditional markets like the Grand Bazaar."
  ],
  ...
}
```

---

## Model Choice Explanation

* **Gemini Flash (`gemini-2.5-flash`)** is used by default:

  * Free-tier compatible
  * Fast responses
  * Structured prompting ensures consistent JSON outputs
* Optional higher-quality model `gemini-2.5-pro` can be enabled for paid usage.

---

## Notes

* The tool includes retry logic and waits for quota resets if `RESOURCE_EXHAUSTED` errors occur.
* JSON parsing is defensive to avoid crashes from incomplete or malformed responses.

---

## License

MIT License
