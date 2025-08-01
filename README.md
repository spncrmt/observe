# Observe AI Dashboard

**Observe AI** is a beginner‑friendly AI‑powered observability dashboard. It
allows small engineering teams or solo developers to explore system metrics,
logs, and anomalies while asking questions in plain English. The dashboard
illustrates how to combine simple data processing, charts, basic machine
learning, and the OpenAI API to augment observability workflows. The design
follows principles from Greg Nudelman’s *UX for AI* framework: the AI acts
as a helpful assistant, makes its reasoning transparent, and allows users to
provide feedback.

## Features

- **User authentication** with a simple login and registration system.
- **API key management** for secure OpenAI API access.
- **Synthetic telemetry data** generator to simulate CPU usage, memory usage,
  latency, and logs for seven days.
- **Interactive charts** using Plotly to visualise metrics and highlight
  detected anomalies.
- **Anomaly detection** through rolling z‑scores to spot unusual spikes.
- **Root cause analysis** correlating anomalies with nearby error logs.
- **AI assistant** that answers natural language questions about system health
  and explains its reasoning using the OpenAI API.
- **Feedback loop** where users can rate AI answers as helpful or not, with
  feedback stored locally for future improvements.

## Installation

1. Clone the repository or copy the `observe_ai` folder into your project.
2. Install the dependencies:

```bash
pip install -r observe_ai/requirements.txt
```

3. Run the data generator (optional, the app will generate data on first
   launch if missing):

```bash
python observe_ai/scripts/generate_data.py
```

4. Start the Streamlit app:

```bash
streamlit run observe_ai/app.py
```

5. Open the URL provided by Streamlit in your browser (typically
   `http://localhost:8501`).

## Usage

1. **Log in** using the default credentials `admin` / `admin` or register
   a new account via the sidebar.
2. **Enter your OpenAI API key** in the sidebar to enable AI features. The key is
   stored only in memory during your session.
3. **Explore the metrics** by selecting CPU usage, memory usage, or latency from
   the dropdown. Anomalies detected by the rolling z‑score algorithm are
   highlighted in red.
4. **Ask questions** about your system’s health in natural language. The AI
   assistant will analyse the metrics and logs, then respond with an answer
   and reasoning.
5. **Review root cause analysis** results to see which logs correspond to
   anomalies.
6. **Provide feedback** by clicking “Helpful” or “Not Helpful” after an AI
   response. This feedback is stored in a local `feedback.json` file.

## Extending the Dashboard

- **Replace synthetic data** with real telemetry: connect to Prometheus,
  OpenTelemetry, or your own data sources. Update the data loading
  functions in `app.py` accordingly.
- **Improve authentication** by integrating a proper identity provider or
  adding password hashing with bcrypt.
- **Enhance anomaly detection** with more advanced models (e.g. isolation
  forests, Prophet) using the Pandas data.
- **Iterate on prompts** in `ai_assistant.openai_answer` to produce more
  structured answers and reasoning.
- **Persist feedback** in a database and use it to fine‑tune your own
  summarisation model.

## License

This project is provided for educational purposes and does not include
warranties or guarantees. You are welcome to modify and use it to suit
your needs.