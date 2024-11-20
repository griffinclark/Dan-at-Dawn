import logging
from src.llm_integration import initialize_llm, analyze_codebase, format_for_report

# Mock data for testing
code_snippets = [
    {
        "code": """
def example_function():
    try:
        # Some operation
        pass
    except Exception as e:
        print(f'Error: {e}')
    finally:
        pass
""",
        "description": "Function with basic error handling"
    },
    {
        "code": """
def another_function():
    # No error handling, just an operation
    x = 10 / 0
""",
        "description": "Function with error (divide by zero)"
    }
]

# Mock recommendations
mock_recommendations = {
    "Debugging": "Add more contextual logging, such as request ID and user context. Use structured logging.",
    "Reliability": "Increase test coverage and add error recovery mechanisms.",
    "Security": "Move sensitive keys and secrets to environment variables or a secure vault.",
    "Minimalism": "Remove unnecessary dependencies and simplify the function design."
}

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
    # Set the model type dynamically (either "smart" or "fast")
    model_type = "fast"  # You can change this to "smart" to use the smart model

    # Step 1: Initialize the LLM (using the model type from config.json)
    logging.info(f"Initializing LLM with model type: {model_type}")
    llm = initialize_llm(model_type=model_type, temperature=0.7)
    logging.info("LLM initialized successfully.")

    # Step 2: Analyze the codebase using the LLM
    logging.info("Starting code analysis...")
    analysis_results = analyze_codebase(llm, code_snippets)
    logging.info("Code analysis complete.")

    # Step 3: Format the results for the report
    logging.info("Formatting the results for the report...")
    formatted_results = format_for_report(
        llm=llm,
        analysis_results=analysis_results,
        prompts_file="app/llm/prompts.json",
        sample_report_path="app/llm/context/sample-report.md"
    )
    logging.info("Results formatted successfully.")

    # Step 4: Save the report directly as markdown
    output_path = "./compliance_report.md"
    logging.info(f"Saving the report to {output_path}...")
    with open(output_path, "w") as report_file:
        report_file.write(formatted_results)
    logging.info(f"Report saved successfully at {output_path}.")


if __name__ == "__main__":
    main()
