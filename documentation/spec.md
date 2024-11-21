# **Dan at Dawn: Human-in-the-Loop LLM-Powered Compliance Tool for the Dawn Methodology**

## **Overview**

**Dan at Dawn** is a Python-based compliance assessment tool designed to evaluate microservice applications against the **Dawn Methodology**. It generates structured, actionable reports with human-in-the-loop feedback, leveraging an **LLM (Large Language Model)** for initial analysis. The tool is currently a **demonstration prototype** using mock data but is structured to evolve into a production-ready CI pipeline integration.

---

## **Primary Functions**

### **1. Mock Data Analysis**

- **Function**: Demonstrates the tool's capabilities using pre-defined sample code snippets (e.g., an authentication server).
- **Input**: Mock data provided as Python code snippets and descriptions.
- **Behavior**:
  - Simulates file parsing and analysis for key areas of concern:
    - **Debugging**: Evaluates error handling and logging.
    - **Reliability**: Assesses test coverage and recovery mechanisms.
    - **Security**: Checks for vulnerabilities, such as hardcoded sensitive data.
    - **Minimalism**: Identifies redundancies or overly complex logic.
- **Output**: Generates compliance reports based on simulated findings.

### **2. LLM Integration**

- **Function**: Uses an LLM (e.g., OpenAI’s GPT-4) to provide insights and recommendations.
- **Input**: Pre-defined prompts and mock data.
- **Behavior**:
  - Processes mock data using customizable prompts stored in `prompts.json`.
  - Analyzes code snippets for adherence to the **Dawn Methodology**.
  - Generates actionable recommendations for improving code quality.
- **Output**: LLM-generated insights for debugging, reliability, security, and minimalism.

### **3. Report Generation**

- **Function**: Creates Markdown-format compliance reports.
- **Input**: Analysis results from the LLM.
- **Behavior**:
  - Formats findings into a structured compliance report based on `sample-report.md`.
  - Saves reports as draft and final versions for review and iteration.
- **Output**: Reports are saved in the project directory with `.md` extensions.

### **4. Feedback Simulation**

- **Function**: Simulates feedback from Dan, the creator of the **Dawn Methodology**.
- **Input**: Compliance report and contextual writings from `context/dan.txt`.
- **Behavior**:
  - Invokes the LLM to emulate Dan’s thought process and writing style.
  - Provides critical feedback on the draft compliance report.
- **Output**: Integrates feedback into the final compliance report.

## **Future Extensions**

### 1. Codebase Exploration

Feature: Add functionality to scan and parse real project files, supporting multiple languages and frameworks.
Implementation:
Develop a scanner.py module to traverse the file system.
Extract meaningful content for analysis, including:

- Code files (.py, .js, etc.).
- Dependency files (requirements.txt, package.json).
- Documentation (README.md).

### 2. CI/CD Pipeline Integration

Feature: Automate compliance checks as part of the development lifecycle.
Implementation:

- Integrate with GitHub Actions or similar CI/CD tools.
- Trigger the tool during pull requests to generate compliance reports automatically.
- Have this create a checklist for use during code review

### 3. Enhanced Feedback Loop

Feature: Extend feedback functionality to include team collaboration.
Implementation:

- Save and version feedback from multiple reviewers.
- Allow for iterative refinement of reports before finalization.
- Implement Griffin's Random Forest of Experts validator to create different versions of Dan, and use a threshold value to ensure the report is sufficiently good
