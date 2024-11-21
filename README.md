# **Dan at Dawn: Human-in-the-Loop LLM-Powered Compliance Tool**

## **Overview**

**Dan at Dawn** is a compliance assessment tool designed to evaluate microservice applications against the principles of the **Dawn Methodology**. By leveraging an **LLM (Large Language Model)** and providing actionable feedback on key aspects like **debugging**, **reliability**, **security**, and **minimalism**, the tool helps developers maintain high-quality codebases.

This tool is currently a **demo** using mock data but is structured to evolve into a production-ready solution that integrates with CI/CD pipelines for real-world applications.

---

## **Features**

### **1. Mock Data Analysis**

- Analyze sample code snippets with insights into:
  - **Debugging**: Exception handling, error logging.
  - **Reliability**: Test coverage, error recovery.
  - **Security**: Vulnerability detection, best practices.
  - **Minimalism**: Redundancies, complexity reduction.

### **2. Human-in-the-Loop Feedback**

- Generate compliance reports as drafts.
- Simulate feedback from **Dan** using an LLM trained on his writing style.
- Refine reports iteratively before finalization.

### **3. LLM Integration**

- Customizable prompts stored in `prompts.json`.
- Uses a sample report template for formatting (`sample-report.md`).

### **4. Report Generation**

- Outputs reports in **Markdown** format:
  - **Draft Compliance Report**.
  - **Final Compliance Report** (with feedback applied).

---

## **Setup**

### **1. Prerequisites**

- Python 3.9+.
- API key for OpenAI's GPT-4 or similar LLM.
- A virtual environment for dependency management.

### **2. Installation**

1. Clone the repository:
   1. `git clone https://github.com/griffinclark/Dan-at-Dawn`
   2. `cd Dan-at-Dawn`
2. Create a virtual env
   1. `python3 -m venv .venv`
   2. `source .venv/bin/activate`
3. Install dependencies
   1. `pip install -r requirements.txt`
4. Add your OPENAI_API_KEY to a .env file
   1. OPENAI_API_KEY=your_openai_api_key

### **3. Usage**

You can run the demo using `python app/main.py`
