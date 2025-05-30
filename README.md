<div align="center"> 
  
  <h1>TaskFlow: LLMs for Android Taint Specification</h1> 


  <p align="center"> In this repository, we host all the data and code related to our paper titled "TaskFlow: LLMs for Android Taint Specification". </p>
</div>

## 📜 Abstract

>Taint analysis is a widely used technique to analyze Android apps, enabling the tracking of data flow within an app. A critical step in this process consists in identifying which methods act as SOURCEs (i.e., where a data of interest originates) and SINKs (where data might be exposed). Researchers have proposed various approaches to identify SOURCE and SINK methods, which typically fall into two categories: ① Handcrafted lists, which suffer from incompleteness and quickly become outdated as APIs evolve; and ② Automated techniques, which, although scalable, tend to over-approximate and produce many false positives, primarily due to the inherent challenge of defining what qualifies as a SOURCE method. Many predefined lists of SOURCEs and SINKs have been proposed. However, while identifying SINKs is generally more straightforward, since they correspond to explicit data exposure points, defining a universal criterion for what constitutes a SOURCE method remains inherently challenging. For example, a method like isMicrophoneMute() may not typically be considered a SOURCE, yet in specific contexts such as targeted surveillance, it could represent a significant privacy concern. This context dependence highlights the limitations of static, generic lists of SOURCE methods. In this paper, we therefore focus on improving the identification of SOURCE methods. To address this, we introduce TASKFLOW, a novel LLM-driven framework for generating task-specific tailored lists of SOURCE methods aligned with specific analysis goals (e.g., tracking location- based data). By reasoning over API semantics and contextual usage, TASKFLOW ① mitigates the noise commonly introduced by overly broad lists, leading to more precise and focused taint analyses; and ② addresses the inherent incompleteness of manual approaches. Our evaluation shows that TASKFLOW is effective in generating task-specific lists of SOURCE methods, achieving high F1 scores across all evaluated tasks. It also benefits from a pre- processing phase that makes the process faster and more efficient

### 🗂️ Repository Organization

The repository is organized into main directories:

* **📁 0_Data**  

  This directory contains all the data related to our experiments.

* **📂 1_Code**  
  Contains all the code relative to our approach. The code is provided into the form of multiple Jupyter Notebooks to facilitate execution.

### 📋 Requirements

#### 🐍 Conda Environment

To launch the Jupyter Notebook, you will need various libraries. We provide a **requirements.txt** file which you can use to create a conda environment.

Follow the steps below:

1. **Create a conda environment named `demoEnv`:**

    ```bash
    conda create --name demoEnv python=3.8
    ```

2. **Activate the newly created environment:**

    ```bash
    conda activate demoEnv
    ```

3. **Install the required packages using `pip` and `requirements.txt`:**

    ```bash
    pip install -r requirements.txt
    ```

Once these steps are complete, your environment will be set up with all the necessary libraries.


#### 🔑 Environment File (.env)

To execute the code, you will need to set up an environment file named `.env` in the main directory of the repository. This file should contain your OpenAI API key.

The API key should be named `OPENAI_API_KEY`.

```
OPENAI_API_KEY = [YOUR_OPENAI_API_KEY]
```

You can obtain your OpenAI API key from the OpenAI platform (<https://platform.openai.com/overview>).

💸 **Note**: Please be aware that using OpenAI’s models may incur costs depending on the volume and type of API usage. Refer to OpenAI's pricing page for details.

### ⚙️ Usage

The provided Jupyter Notebooks facilitates the execution of our approach. The notebooks should be executed in the order listed here to ensure correct data processing and dependencies are met.

1.  **`InitialFiltering.ipynb`**: Run this notebook first to perform the initial filtering of Android API methods (NO_INFORMATION vs ADVANTAGE_GAIN).
2.  **`MethodsEmbedding.ipynb`**: Execute this notebook to generate embeddings for the filtered (only ADVANTAGE_GAIN)Android API methods.
3.  **`MethodsClustering.ipynb`**: This notebook applies clustering algorithms to group the methods into clusters.
4.  **`ClustersLabelling.ipynb`**: Run this notebook to label the generated clusters to categorize the type of information potentially exposed by their return values.
5.  **`TaskSpecificRefining.ipynb`**: Run this notebook for the final task-driven refinement according to the user's task.


#### ⚠️ Note: 
Due to the probabilistic nature of LLMs, outputs may slightly vary between runs. As a result, you might observe small deviations in the generated results compared to those presented in the paper.