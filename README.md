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

## Windows Usage

```cmd
cd E:\hermes-tool-agent
python file_analysis_agent.py E:\sample-dir
python -m unittest test_file_analysis.py
```
