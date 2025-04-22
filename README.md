# Názory a Argumenty (Opinions and Arguments)

This project processes a Czech-language dataset of opinions and arguments using pre-trained transformer models. It is designed for fine-tuning and evaluating models on tasks such as argument classification and stance detection using the HuggingFace Transformers and Datasets libraries.

---

## 🚀 Features

- Loads and preprocesses datasets from HuggingFace Datasets hub.
- Utilizes pre-trained transformer models (e.g., `robeczech-base`) for Czech-language tasks.
- Offers flexible training and evaluation pipelines with HuggingFace's `Trainer` API.
- Custom metrics for evaluation.
- GitHub Actions integration for automated workflows.

---

## 📦 Installation

Make sure you have Python 3.8+ and install the required packages:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install transformers datasets scikit-learn torch evaluate
```

---

## 🧠 Model

The script uses the `robeczech-base` model from the Czech NLP community. You can change the model by passing a different model name via command-line arguments.

---

## 📁 Dataset

Datasets are expected to be available via HuggingFace's `datasets` library. This project uses:

- **Dataset:** `zichd/nazory-a-argumenty`

The dataset is automatically downloaded and cached using HuggingFace's hub.

---

## ⚙️ Usage

Run the training script with default arguments:

```bash
python run.py
```

Or with specific parameters:

```bash
python run.py \
    --model_name_or_path UFAL/robeczech-base \
    --dataset_name zichd/nazory-a-argumenty \
    --task_name argument_classification \
    --output_dir ./results \
    --num_train_epochs 4 \
    --per_device_train_batch_size 16 \
    --do_train --do_eval
```

### Optional Flags

- `--do_train`: Enable model training
- `--do_eval`: Evaluate the model on the test set
- `--task_name`: Task type such as `argument_classification`, `stance_detection`
- `--overwrite_output_dir`: Overwrite output directory

---

## 📊 Evaluation

Custom metrics are used to assess model performance. Evaluation results are saved in the specified output directory.

---

## ⚙️ GitHub Actions

This project includes a GitHub Actions workflow for automatic RSS feed updates:

- **Workflow File:** `.github/workflows/rss_update.yml`
- **Trigger:** Runs every 2 hours using a cron job (`0 */2 * * *`)
- **Function:** Keeps the RSS feed or relevant dataset info up-to-date automatically.

You can modify the workflow for additional automation tasks like model evaluation or deployment.

---

## 🛠 Development

To modify the behavior or add new tasks:
- Edit the preprocessing function inside `run.py`
- Update task configuration via command-line or script logic

---

## 🤝 Contributing

Pull requests and issues are welcome! Please include appropriate tests and documentation.

---

## 📄 License

[MIT License](LICENSE)

---

## 🧑‍💻 Author

Developed by [zichd](https://github.com/zichd)
