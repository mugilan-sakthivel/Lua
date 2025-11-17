"""Conversation persistence manager for Luna website builder."""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class ConversationManager:
    """Manages conversation history persistence to JSON file."""
    
    def __init__(self, conversation_file: str = "conversation.json"):
        """Initialize conversation manager.
        
        Args:
            conversation_file: Path to conversation JSON file
        """
        self.conversation_file = Path(conversation_file)
        self.conversation_history: List[Dict[str, str]] = []
        self._load_conversation()
    
    def _load_conversation(self):
        """Load existing conversation from file."""
        if self.conversation_file.exists():
            try:
                with open(self.conversation_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversation_history = data.get('messages', [])
                    print(f"📂 Loaded {len(self.conversation_history)} messages from conversation history")
            except json.JSONDecodeError:
                print("⚠️  Conversation file is corrupted. Starting fresh.")
                self.conversation_history = []
            except Exception as e:
                print(f"⚠️  Error loading conversation: {e}. Starting fresh.")
                self.conversation_history = []
        else:
            print("📝 Starting new conversation")
            self.conversation_history = []
    
    def _save_conversation(self):
        """Save conversation to file."""
        try:
            data = {
                "messages": self.conversation_history,
                "last_updated": datetime.now().isoformat(),
                "total_messages": len(self.conversation_history)
            }
            
            with open(self.conversation_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            print(f"⚠️  Error saving conversation: {e}")
    
    def add_user_message(self, content: str):
        """Add a user message to conversation history.
        
        Args:
            content: User message content
        """
        message = {
            "role": "user",
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.append(message)
        self._save_conversation()
    
    def add_assistant_message(self, content: str):
        """Add an assistant message to conversation history.
        
        Args:
            content: Assistant message content
        """
        message = {
            "role": "assistant",
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.append(message)
        self._save_conversation()
    
    def get_messages_for_llm(self) -> List[Dict[str, str]]:
        """Get messages formatted for LLM (without timestamps).
        
        Returns:
            List of messages with 'role' and 'content' only
        """
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.conversation_history
        ]
    
    def clear_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []
        self._save_conversation()
        print("🗑️  Conversation history cleared")
    
    def get_conversation_stats(self) -> Dict[str, int]:
        """Get conversation statistics.
        
        Returns:
            Dictionary with user_count, assistant_count, total_count
        """
        user_count = sum(1 for msg in self.conversation_history if msg["role"] == "user")
        assistant_count = sum(1 for msg in self.conversation_history if msg["role"] == "assistant")
        
        return {
            "user_count": user_count,
            "assistant_count": assistant_count,
            "total_count": len(self.conversation_history)
        }
    
    def export_conversation(self, output_file: str):
        """Export conversation to a readable text file.
        
        Args:
            output_file: Path to output text file
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("Luna Website Builder - Conversation History\n")
                f.write("=" * 80 + "\n\n")
                
                for i, msg in enumerate(self.conversation_history, 1):
                    role = "🤖 You" if msg["role"] == "user" else "✅ Luna"
                    timestamp = msg.get("timestamp", "N/A")
                    content = msg["content"]
                    
                    f.write(f"[{i}] {role} ({timestamp}):\n")
                    f.write(f"{content}\n")
                    f.write("-" * 80 + "\n\n")
                
                stats = self.get_conversation_stats()
                f.write("=" * 80 + "\n")
                f.write(f"Total Messages: {stats['total_count']}\n")
                f.write(f"User Messages: {stats['user_count']}\n")
                f.write(f"Assistant Messages: {stats['assistant_count']}\n")
                f.write("=" * 80 + "\n")
            
            print(f"📄 Conversation exported to {output_file}")
        except Exception as e:
            print(f"⚠️  Error exporting conversation: {e}")


# Global conversation manager instance
_conversation_manager: Optional[ConversationManager] = None


def get_conversation_manager(conversation_file: str = "conversation.json") -> ConversationManager:
    """Get or create the global conversation manager instance.
    
    Args:
        conversation_file: Path to conversation JSON file
    
    Returns:
        ConversationManager instance
    """
    global _conversation_manager
    if _conversation_manager is None:
        _conversation_manager = ConversationManager(conversation_file)
    return _conversation_manager


def reset_conversation_manager():
    """Reset the global conversation manager instance."""
    global _conversation_manager
    _conversation_manager = None
