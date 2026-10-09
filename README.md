# Hermes Tool Agent

## Assignment Objective
Build a single-agent tool-using system with Hermes Agent.

## Planned Features
- Tool selection and execution
- Project initialization and testing
- Documentation and version control

## Python Utility vs. Hermes Agent Workflow

- The Python script (`file_analysis_agent.py`) is a standalone, pure-standard-library utility.
- The Hermes Agent does not call it via `hermes_tools.execute_code`; instead, Hermes Desktop invokes its own available tools (e.g., `execute_code` / `terminal`) to run the script, inspect output, and verify results.
- The script never moves, deletes, or modifies files.

## Assignment Resources

- [Hermes Agent vs. LangChain Agents Comparison (HERMES_VS_LANGCHAIN.md)](HERMES_VS_LANGCHAIN.md)
- [Collaborative Workflow — Sequential Researcher → Writer (collaborative_workflow.md)](collaborative_workflow.md)

### Running the Utility and Tests

The file‑analysis utility (`file_analysis_agent.py`) and its unit tests (`test_file_analysis.py`) are designed to run from the project root using the terminal (standard Hermes Desktop tool). Ensure you are in `E:\hermes-tool-agent` first.

```cmd
# Run the analysis on a directory, e.g. sample-data
cd E:\hermes-tool-agent
python file_analysis_agent.py sample-data

# Run the unit tests (all included in test_file_analysis.py)
python -m unittest -v test_file_analysis.py
```

The utility scans the supplied directory, counts files by extension, identifies the largest files, and prints a human‑readable report. The unit tests cover normal scanning, extension counts, largest‑file detection, report formatting, invalid directories, and empty directories. All tests pass on a clean Windows command prompt.
