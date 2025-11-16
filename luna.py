    #!/usr/bin/env python
"""Luna - AI Research Assistant Entry Point.

This is the main entry point for the Luna research assistant.
Use this to run the application with various commands.

Usage:
    python luna.py chat                 # Interactive research mode
    python luna.py build [TARGET]       # Build mode
    python luna.py --help               # Show help
"""

from cli.cli import main

if __name__ == "__main__":
    main()
