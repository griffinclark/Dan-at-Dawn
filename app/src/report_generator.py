import os

class ReportGenerator:
    def __init__(self, output_dir=".", report_name="compliance_report.md"):
        self.output_dir = output_dir
        self.report_name = report_name
        self.report_path = os.path.join(self.output_dir, self.report_name)

    def generate_header(self):
        """
        Generates the header for the compliance report.
        """
        header = "# Dan@Dawn Compliance Report\n\n"
        header += "## Executive Summary\n"
        header += "This is an AI-assisted compliance report based on the analysis of your microservice application. The following sections provide insights into the application’s alignment with the **Dawn Methodology**.\n\n"
        return header

    def generate_analysis_section(self, principle, analysis):
        """
        Generates the analysis section for a specific principle (e.g., Debugging, Reliability, etc.)
        """
        section = f"## {principle} Analysis\n"
        section += f"{analysis}\n\n"
        return section

    def generate_recommendations(self, principle, recommendations):
        """
        Generates the recommendations for improving compliance with a specific principle.
        """
        recommendations_section = f"### {principle} Recommendations\n"
        recommendations_section += f"{recommendations}\n\n"
        return recommendations_section

    def compile_report(self, analyses, recommendations):
        """
        Compiles the full compliance report in Markdown format.
        """
        report = self.generate_header()

        # Add analysis and recommendations for each principle
        for principle, analysis in analyses.items():
            report += self.generate_analysis_section(principle, analysis)
            report += self.generate_recommendations(principle, recommendations.get(principle, "No recommendations available."))

        return report

    def save_report(self, report_content):
        """
        Saves the generated report to a specified file.
        """
        with open(self.report_path, "w") as f:
            f.write(report_content)
        print(f"Report saved to {self.report_path}")

    def generate_and_save_report(self, analyses, recommendations):
        """
        Generates the full report and saves it.
        """
        report_content = self.compile_report(analyses, recommendations)
        self.save_report(report_content)


# Simulate LLM analysis results and recommendations
analyses = {
    "Debugging": "The code base includes basic error handling using try-except blocks. However, logging is minimal and lacks contextual data such as timestamps or request IDs.",
    "Reliability": "Unit tests exist, but coverage is incomplete. There are no system or integration tests in place. No error recovery mechanisms like retries are implemented.",
    "Security": "The application uses basic API key authentication for communication with external services. However, sensitive data is hardcoded, which exposes it to potential breaches.",
    "Minimalism": "The code is relatively simple, but there are some redundant dependencies that could be removed to streamline the service."
}

recommendations = {
    "Debugging": "Improve logging by adding timestamps, request IDs, and user context. Consider adopting structured logging for better analysis and debugging.",
    "Reliability": "Increase test coverage to include system and integration tests. Implement error recovery mechanisms like retries for failed network requests.",
    "Security": "Move sensitive information like API keys to environment variables or a secrets manager. Use secure authentication practices such as OAuth or JWT tokens.",
    "Minimalism": "Review the project's dependencies and remove any unnecessary or unused packages. Refactor code to reduce redundancy and improve clarity."
}

# Example usage
if __name__ == "__main__":
    report_generator = ReportGenerator(output_dir=".", report_name="compliance_report.md")
    report_generator.generate_and_save_report(analyses, recommendations)
