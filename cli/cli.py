"""CLI command handler for Luna website builder."""

import sys
from src.services import create_website_builder_agent, get_langfuse_handler
from src.utils.conversation_manager import get_conversation_manager


def run_interactive_mode():
    """Run the interactive chat mode."""
    agent = create_website_builder_agent()
    langfuse_handler = get_langfuse_handler()
    conversation_mgr = get_conversation_manager()
    
    print("\n" + "=" * 60)
    print("          🎨 Luna Website Builder - Multi-Agent System")
    print("=" * 60)
    print("\nDescribe your website requirements. Type 'exit' or 'quit' to end.")
    print("Type 'clear' to clear conversation history.")
    print("Type 'stats' to see conversation statistics.\n")
    
    # Show conversation stats if there's existing history
    stats = conversation_mgr.get_conversation_stats()
    if stats['total_count'] > 0:
        print(f"💬 Continuing conversation with {stats['total_count']} existing messages\n")
    
    while True:
        try:
            # Get user input
            user_input = input("\n🤖 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye! Thanks for using Deep Agent CLI.\n")
                break
            
            # Handle clear command
            if user_input.lower() == 'clear':
                conversation_mgr.clear_conversation()
                print("✅ Conversation history cleared. Starting fresh.\n")
                continue
            
            # Handle stats command
            if user_input.lower() == 'stats':
                stats = conversation_mgr.get_conversation_stats()
                print(f"\n📊 Conversation Statistics:")
                print(f"   Total messages: {stats['total_count']}")
                print(f"   User messages: {stats['user_count']}")
                print(f"   Assistant messages: {stats['assistant_count']}\n")
                continue
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Add user message to conversation history
            conversation_mgr.add_user_message(user_input)
            
            print("\n🔄 Agent: Thinking...\n")
            
            # Get full conversation history for LLM
            messages_for_llm = conversation_mgr.get_messages_for_llm()
            
            # Invoke the agent with full conversation history
            result = agent.invoke({
                "messages": messages_for_llm},
                config={"callbacks": [langfuse_handler]
            })
            
            # Get the agent's response
            final_message = result["messages"][-1]
            response_content = final_message.content
            
            # Add assistant message to conversation history
            conversation_mgr.add_assistant_message(response_content)
            
            # Print the agent's response
            print(f"\n✅ Agent: {response_content}\n")
            
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
    conversation_mgr = get_conversation_manager()
    
    print("\n" + "=" * 60)
    print("          🎨 Luna Website Builder - Single Prompt")
    print("=" * 60)
    
    # Show conversation stats if there's existing history
    stats = conversation_mgr.get_conversation_stats()
    if stats['total_count'] > 0:
        print(f"\n� Continuing conversation with {stats['total_count']} existing messages")
    
    print(f"\n�📝 Requirement: {prompt}\n")
    print("🔄 Agent: Processing...\n")
    
    try:
        # Add user message to conversation history
        conversation_mgr.add_user_message(prompt)
        
        # Get full conversation history for LLM
        messages_for_llm = conversation_mgr.get_messages_for_llm()
        
        # Invoke the agent with full conversation history
        result = agent.invoke({
            "messages": messages_for_llm},
            config={"callbacks": [langfuse_handler]}
        )
        
        # Get the agent's response
        final_message = result["messages"][-1]
        response_content = final_message.content
        
        # Add assistant message to conversation history
        conversation_mgr.add_assistant_message(response_content)
        
        # Print the agent's response
        print("\n" + "=" * 60)
        print("          ✅ Agent Response")
        print("=" * 60)
        print(f"\n{response_content}\n")
        
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
    ║         🎨 Luna Website Builder - Help                   ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Usage:
        python luna.py [COMMAND] [OPTIONS]
    
    Commands:
        chat                       Start interactive chat mode (default)
        prompt "YOUR PROMPT"       Run agent with a single prompt
        export [FILE]             Export conversation history to text file
        clear                     Clear conversation history
        stats                     Show conversation statistics
        --help, -h                Show this help message
        --version, -v             Show version information
    
    Examples:
        python luna.py chat                          # Start interactive mode
        python luna.py prompt "Build a portfolio"    # Single prompt execution
        python luna.py export conversation.txt       # Export conversation
        python luna.py clear                         # Clear conversation history
        python luna.py stats                         # Show conversation stats
        python luna.py --help                        # Show this help
    
    Interactive Mode (chat):
        - Type your website requirements
        - Type 'exit' or 'quit' to quit
        - Type 'clear' to clear conversation history
        - Type 'stats' to see conversation statistics
        - Press Ctrl+C to quit
    
    Prompt Mode:
        - Execute a single website building request
        - Continues conversation from previous sessions
        - Returns results in the terminal
        - Useful for scripting and automation
    
    Conversation Persistence:
        - All conversations are automatically saved to conversation.json
        - Each new message includes full conversation history
        - Use 'clear' to start fresh or 'export' to save as text
    
    Tips:
        - Be specific about your website requirements
        - The agent will generate all files in the correct locations
        - Check generated files: website_plan.md, design_specs.md, etc.
    """
    print(help_text)


def show_version():
    """Display version information."""
    print("\n🎨 Luna Website Builder v2.0.0 (Multi-Agent System)\n")


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
            print("Usage: python luna.py prompt \"your requirement here\"\n")
            sys.exit(1)
        
        # Join all arguments after 'prompt' to support multi-word prompts
        prompt_text = " ".join(args[1:])
        run_prompt_mode(prompt_text)
    
    # Handle export command
    elif command == 'export':
        from src.utils.conversation_manager import get_conversation_manager
        conversation_mgr = get_conversation_manager()
        
        # Use provided filename or default
        output_file = args[1] if len(args) > 1 else "conversation_export.txt"
        conversation_mgr.export_conversation(output_file)
    
    # Handle clear command
    elif command == 'clear':
        from src.utils.conversation_manager import get_conversation_manager
        conversation_mgr = get_conversation_manager()
        
        print("\n⚠️  Are you sure you want to clear conversation history? (yes/no): ", end="")
        confirmation = input().strip().lower()
        
        if confirmation in ['yes', 'y']:
            conversation_mgr.clear_conversation()
            print("✅ Conversation history cleared.\n")
        else:
            print("❌ Operation cancelled.\n")
    
    # Handle stats command
    elif command == 'stats':
        from src.utils.conversation_manager import get_conversation_manager
        conversation_mgr = get_conversation_manager()
        
        stats = conversation_mgr.get_conversation_stats()
        print("\n" + "=" * 60)
        print("          📊 Conversation Statistics")
        print("=" * 60)
        print(f"\n  Total messages: {stats['total_count']}")
        print(f"  User messages: {stats['user_count']}")
        print(f"  Assistant messages: {stats['assistant_count']}\n")
    
    # Unknown command
    else:
        print(f"\n❌ Unknown command: '{command}'")
        print("Type 'python luna.py --help' for usage information.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
