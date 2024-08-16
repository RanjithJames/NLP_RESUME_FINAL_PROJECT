# NLP Resume Parsing and Job Matching

This project leverages NLP and large language models to parse resumes and match them with job descriptions. It consists of a training pipeline for models and Gradio interfaces for interaction.

## Requirements

Before running the project, ensure you have installed all required dependencies. You can do this by running:

```
pip install -r requirements.txt
```

## Steps to Run

### 1. Train the Model

The first step is to train the model. Open and run the `modeltrain.ipynb` notebook. This will:

- Preprocess the data
- Train the NLP model
- Save the trained model for later use

### 2. Launch the Gradio Interfaces

Once the model is trained, you can interact with it using the Gradio interfaces. There are two main interfaces:

#### 2.1 HR Interface

Launch the HR interface by running:

```bash
python HRapp.py
```

This interface allows HR professionals to input job descriptions and get matched resumes.

#### 2.2 User Interface

Launch the User interface by running:

```bash
python UserApp.py
```

This interface allows users to input their resumes and get matched job descriptions.

## Contributing

Please ensure any pull requests or contributions are made against the `main` branch. Feel free to open issues or feature requests.

