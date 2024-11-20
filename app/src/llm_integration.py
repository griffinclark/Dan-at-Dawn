import os
import json
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI

# Load environment variables from the .env file
load_dotenv()

def load_model_config(config_file="config.json"):
    """
    Load the model configuration from a JSON file.
    
    Args:
        config_file (str): The path to the config JSON file.
    
    Returns:
        dict: The model configuration dictionary.
    """
    # Get the absolute path of the config file relative to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    config_path = os.path.join(script_dir, "..", "llm", config_file)  # Build the correct path
    
    # Check if the file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")
    
    # Open the config file
    with open(config_path, "r") as f:
        config = json.load(f)
    
    return config

def load_prompts(prompts_file="prompts.json"):
    """
    Load the prompts and suffix from a JSON file.
    
    Args:
        prompts_file (str): The path to the prompts JSON file.
    
    Returns:
        dict: The prompts dictionary.
    """
    # Get the absolute path of the prompts file relative to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    prompts_path = os.path.join(script_dir, "..", "llm", "prompts.json")  # Build the correct path
    
    # Check if the file exists
    if not os.path.exists(prompts_path):
        raise FileNotFoundError(f"Prompts file not found at {prompts_path}")
    
    # Open the prompts file
    with open(prompts_path, "r") as f:
        prompts = json.load(f)
    
    return prompts

def initialize_llm(model_type, temperature=0.7, config_file="config.json"):
    """
    Initializes and returns an LLM (Large Language Model) instance based on the selected model.
    
    Args:
        model_type (str): The type of model to use ("fast" or "smart").
        temperature (float): Controls the randomness of the model's output.
        config_file (str): Path to the configuration file containing model settings.
    
    Returns:
        ChatOpenAI instance.
    """
    # Load the model configuration
    config = load_model_config(config_file)
    
    # Get the model name based on the selected model type
    model_name = config["model"].get(model_type, "gpt-4o")  # Default to "gpt-4o" if no match

    # Get the OpenAI API key from the environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")
    
    # Initialize the LLM with the provided API key and selected model
    llm = ChatOpenAI(model=model_name, temperature=temperature, openai_api_key=api_key)
    return llm

def generate_analysis(llm, code_snippet, principle, prompts, suffix):
    """
    Generate an analysis for the provided code snippet based on the specified principle.
    
    Args:
        llm (ChatOpenAI): The initialized LLM instance.
        code_snippet (str): The code to analyze.
        principle (str): The principle to analyze for (e.g., "Debugging", "Reliability").
        prompts (dict): The prompts dictionary loaded from prompts.json.
        suffix (str): The suffix to be appended for conciseness and clarity.
    
    Returns:
        str: The analysis from the LLM.
    """
    prompt = prompts["application"]["analyze_code"].format(principle=principle, code_snippet=code_snippet) + "\n\n" + suffix
    response = llm.invoke(prompt)  # This returns an AIMessage object
    return response.content if hasattr(response, 'content') else str(response)  # Extract plain text

def generate_recommendations(llm, code_snippet, principle, prompts, suffix):
    """
    Generate actionable recommendations for improving the code based on the specified principle.
    
    Args:
        llm (ChatOpenAI): The initialized LLM instance.
        code_snippet (str): The code to analyze.
        principle (str): The principle to recommend improvements for (e.g., "Debugging", "Security").
        prompts (dict): The prompts dictionary loaded from prompts.json.
        suffix (str): The suffix to be appended for conciseness and clarity.
    
    Returns:
        str: The recommendations from the LLM.
    """
    prompt = prompts["application"]["generate_recommendations"].format(principle=principle, code_snippet=code_snippet) + "\n\n" + suffix
    response = llm.invoke(prompt)  # This returns an AIMessage object
    return response.content if hasattr(response, 'content') else str(response)  # Extract plain text

def analyze_codebase(llm, code_snippets, principles=["Debugging", "Reliability", "Security", "Minimalism"]):
    """
    Analyze a list of code snippets for all principles and generate both analysis and recommendations.
    
    Args:
        llm (ChatOpenAI): The initialized LLM instance.
        code_snippets (list): A list of code snippets to analyze.
        principles (list): A list of principles to evaluate (default: ["Debugging", "Reliability", "Security", "Minimalism"]).
    
    Returns:
        dict: A dictionary containing analysis and recommendations for each principle.
    """
    prompts = load_prompts()
    suffix = prompts["suffix"]["general"]  # Use the general suffix
    
    results = {}

    for principle in principles:
        principle_analysis = []
        principle_recommendations = []

        for snippet in code_snippets:
            analysis = generate_analysis(llm, snippet["code"], principle, prompts, suffix)
            recommendations = generate_recommendations(llm, snippet["code"], principle, prompts, suffix)

            principle_analysis.append(analysis)  # Ensure plain strings
            principle_recommendations.append(recommendations)  # Ensure plain strings

        results[principle] = {
            "analysis": principle_analysis,
            "recommendations": principle_recommendations
        }

    return results

def format_for_report(llm, analysis_results, prompts_file="app/llm/prompts.json", sample_report_path="app/llm/context/sample-report.md", feedback=None):
    """
    Format the analysis and recommendations into a report using the LLM and a formatting prompt from prompts.json.
    
    Args:
        llm (ChatOpenAI): The initialized LLM instance.
        analysis_results (dict): The results from the analyze_codebase function.
        prompts_file (str): Path to the prompts JSON file.
        sample_report_path (str): Path to the sample report for formatting instructions.
        feedback (str): Optional feedback content to include in the final report.
    
    Returns:
        str: The formatted compliance report in markdown.
    """
    # Load prompts from the JSON file
    prompts = load_prompts(prompts_file)
    format_prompt_template = prompts["application"]["format_report"]
    
    # Load the sample report content
    if not os.path.exists(sample_report_path):
        raise FileNotFoundError(f"Sample report not found at {sample_report_path}")
    
    with open(sample_report_path, "r") as f:
        sample_report_content = f.read()
    
    # Add feedback if provided
    feedback_section = f"\n\n## Dan's Feedback\n\n{feedback}" if feedback else ""
    
    # Format the prompt
    format_prompt = format_prompt_template.format(
        sample_report=sample_report_content,
        analysis_results=json.dumps(analysis_results, indent=2)
    ) + feedback_section
    
    # Invoke the LLM with the formatted prompt
    response = llm.invoke(format_prompt)
    
    # Extract and return the formatted report
    return response.content if hasattr(response, 'content') else str(response)

def simulate_dan_feedback(llm, compliance_report, prompts_file="app/llm/prompts.json", context_path="app/llm/context/dan.txt"):
    """
    Simulate feedback from Dan based on the generated compliance report and his writings.
    
    Args:
        llm (ChatOpenAI): The initialized LLM instance.
        compliance_report (str): The generated compliance report in markdown format.
        prompts_file (str): Path to the prompts JSON file.
        context_path (str): Path to the file containing Dan's writings.
    
    Returns:
        str: Dan's feedback on the compliance report.
    """
    # Load prompts from JSON
    prompts = load_prompts(prompts_file)
    simulate_dan_prompt_template = prompts["Dan"]["simulate_dan"]
    
    # Load Dan's writings for context
    if not os.path.exists(context_path):
        raise FileNotFoundError(f"Dan's writings not found at {context_path}")
    
    with open(context_path, "r") as f:
        context = f.read()
    
    # Format the prompt
    simulate_dan_prompt = simulate_dan_prompt_template.format(
        context=context,
        compliance_report=compliance_report
    )
    
    # Invoke the LLM with the formatted prompt
    response = llm.invoke(simulate_dan_prompt)
    
    # Extract and return the feedback
    return response.content if hasattr(response, 'content') else str(response)
