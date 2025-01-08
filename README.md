# 🔬 Benchmark FuriosaAI RNGD Across Various LLM Tasks

This project benchmarks the performance of FuriosaAI RNGD for a range of LLM tasks, including:
- 🤖 **RAG (Retrieval-Augmented Generation) Chatbot**: Use databases and QA datasets to test retrieval accuracy and generative capabilities.
- 🌐 **Translation**: Evaluate multi-language translation accuracy and performance.
- 📝 **Summarization**: Test the summarization of large-scale documents.
- 🖼️ **Multi-Modal Agent**: Combine vision models and LLMs for multi-modal understanding and reasoning.

The project enables easy comparisons between GPU and NPU environments using unified APIs and configurable pipelines.

## 📁 Project Structure

The project is organized as follows:

```
├── LICENSE              # Open-source license information
├── README.md            # Project overview and instructions
├── configuration/       # Collection of available configurations for tasks
├── data/
│   ├── translation/     # Translation benchmarking dataset
│   ├── chatbot/         # QA chatbot (RAG) benchmarking dataset
│   ├── summarization/   # Document summarization benchmarking dataset
│   └── multimodal/      # Multimodal (vision+text) benchmarking dataset
├── results/             # Benchmark scores for Leaderboard
│   ├── translation/       
│   ├── chatbot/         
│   ├── summarization/         
│   └── multimodal/      
├── requirements.txt     # List of required Python packages
└── src/                 # Source code for various tasks
    ├── environment/     # Environment detection, configuration loader
    ├── metrics/         # Metric definitions for LLM tasks
    ├── translation/     # Modules for LLM translation
    ├── chatbot/         # Modules for QA chatbot (RAG)
    ├── summarization/   # Modules for summarization
    └── multimodal/      # Modules for multimodal agent
```

## Getting Started

Follow these steps to set up the project locally:

### 1. Clone the repository

```bash
git clone https://github.com/shadow-agent/npu-service-zoo.git
```

### 2. Navigate to the project directory

```bash
cd npu-service-zoo
```

### 3. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 4. Install the required packages

```bash
pip install -r requirements.txt
```

## Usage

Detailed instructions on how to use the chatbot, including data preparation, model training, and running the application, can be found in the `docs` directory.

## Contributing

Contributions are welcome! Please refer to the `CONTRIBUTING.md` file for guidelines on how to contribute to this project.

## License

This project is licensed under the terms of the MIT License.

---

This `README.md` provides a comprehensive overview of the project, including its structure, setup instructions, usage guidelines, and acknowledgements. Feel free to modify any sections to better fit your project's specifics.