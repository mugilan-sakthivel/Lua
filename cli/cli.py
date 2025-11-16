"""CLI command handler for Luna website builder."""

import sys
from src.services import create_website_builder_agent, get_langfuse_handler


def run_interactive_mode():
    """Run the interactive chat mode."""
    agent = create_website_builder_agent()
    langfuse_handler = get_langfuse_handler()
    
    print("\n" + "=" * 60)
    print("          🎨 Luna Website Builder - Multi-Agent System")
    print("=" * 60)
    print("\nDescribe your website requirements. Type 'exit' or 'quit' to end.\n")
    
    while True:
        try:
            # Get user input
            user_input = input("\n🤖 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye! Thanks for using Deep Agent CLI.\n")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            print("\n🔄 Agent: Thinking...\n")
            
            # Invoke the agent
            result = agent.invoke({
                "messages": [{"role": "user", "content": user_input}]},
                config={"callbacks": [langfuse_handler]
            })
            
            # Print the agent's response
            final_message = result["messages"][-1]
            print(f"\n✅ Agent: {final_message.content}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using Deep Agent CLI.\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            continue


def run_prompt_mode(prompt: str):
    """Run the agent with a single prompt.
    
    Args:
        prompt: The website building prompt/requirement
    """
    agent = create_website_builder_agent()
    langfuse_handler = get_langfuse_handler()
    
    print("\n" + "=" * 60)
    print("          🎨 Luna Website Builder - Single Prompt")
    print("=" * 60)
    print(f"\n📝 Requirement: {prompt}\n")
    print("🔄 Agent: Processing...\n")
    
    try:
        # Invoke the agent with the prompt
        result = agent.invoke({
            "messages": [{"role": "user", "content": prompt}]},
            config={"callbacks": [langfuse_handler]}
        )
        
        # Print the agent's response
        final_message = result["messages"][-1]
        print("\n" + "=" * 60)
        print("          ✅ Agent Response")
        print("=" * 60)
        print(f"\n{final_message.content}\n")
        
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled.\n")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        import traceback
        traceback.print_exc()


def show_help():
    """Display help information."""
    help_text = """
    ╔═══════════════════════════════════════════════════════════╗
    ║         🧠 Luna Research Assistant - Help                ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Usage:
        python luna.py [COMMAND] [OPTIONS]
    
    Commands:
        chat                       Start interactive research mode (default)
        prompt "YOUR PROMPT"       Run agent with a single prompt/question
        --help, -h                Show this help message
        --version, -v             Show version information
    
    Examples:
        python luna.py chat                          # Start interactive mode
        python luna.py prompt "What is Python?"      # Single prompt execution
        python luna.py --help                        # Show this help
    
    Interactive Mode (chat):
        - Type your research questions
        - Type 'exit' or 'quit' to quit
        - Press Ctrl+C to quit
    
    Prompt Mode:
        - Execute a single research question and get the result
        - Returns results in the terminal
        - Useful for scripting and automation
    
    Tips:
        - Ask detailed questions for comprehensive research
        - The agent will generate reports in final_report.md
        - Original questions are saved in question.txt
    """
    print(help_text)


def show_version():
    """Display version information."""
    print("\n🧠 Luna Research Assistant v1.0.0\n")


def main(args=None):
    """Main CLI entry point.
    
    Args:
        args: Command line arguments (uses sys.argv if None)
    """
    if args is None:
        args = sys.argv[1:]
    
    # No arguments - run interactive mode
    if not args:
        run_interactive_mode()
        return
    
    command = args[0].lower()
    
    # Handle help
    if command in ['--help', '-h', 'help']:
        show_help()
    
    # Handle version
    elif command in ['--version', '-v', 'version']:
        show_version()
    
    # Handle chat/interactive mode
    elif command in ['chat', 'interactive']:
        run_interactive_mode()
    
    # Handle prompt mode
    elif command == 'prompt':
        if len(args) < 2:
            print("\n❌ Error: 'prompt' command requires a prompt argument")
            print("Usage: python luna.py prompt \"your question here\"\n")
            sys.exit(1)
        
        # Join all arguments after 'prompt' to support multi-word prompts
        prompt_text = " ".join(args[1:])
        run_prompt_mode(prompt_text)
    
    # Unknown command
    else:
        print(f"\n❌ Unknown command: '{command}'")
        print("Type 'python luna.py --help' for usage information.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
