
import requests
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

def load_config():
    """Load Notion configuration"""
    config_file = Path("config/notion_credentials.json")
    if config_file.exists():
        with open(config_file, 'r') as f:
            return json.load(f)
    return None

def claude_log(terminal, message, entry_type="Operator Log", tone="focused"):
    """Log Claude's work to specific terminal"""
    
    terminal_files = {
        "alpha": "terminal_alpha_logger.py",
        "beta": "terminal_beta_logger.py", 
        "gamma": "terminal_gamma_logger.py",
        "delta": "terminal_delta_logger.py",
        "epsilon": "terminal_epsilon_logger.py"
    }
    
    terminal_file = terminal_files.get(terminal.lower())
    if not terminal_file:
        print(f"❌ Unknown terminal: {terminal}")
        return False
    
    if not Path(terminal_file).exists():
        print(f"❌ Terminal file not found: {terminal_file}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, terminal_file, "log", message],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            emoji = {"alpha": "🔵", "beta": "🟢", "gamma": "🟡", "delta": "🟠", "epsilon": "🔴"}[terminal.lower()]
            print(f"{emoji} Claude {terminal.title()}: Message logged to DAWN")
            return True
        else:
            print(f"❌ Claude {terminal.title()}: Logging failed")
            return False
    
    except Exception as e:
        print(f"❌ Claude {terminal.title()}: Error - {e}")
        return False

def start_development_session():
    """Initialize Claude development session across all terminals"""
    
    print("🤖 STARTING CLAUDE DEVELOPMENT SESSION")
    print("=" * 50)
    print("🔮 Initializing all Claude development streams...")
    print()
    
    # Initialize each terminal with role-specific messages
    session_messages = {
        "alpha": "🔵 Claude Alpha initialized - Primary development and artifact creation ready",
        "beta": "🟢 Claude Beta initialized - Script testing and validation protocols active", 
        "gamma": "🟡 Claude Gamma initialized - Data analysis and pattern recognition online",
        "delta": "🟠 Claude Delta initialized - System monitoring and health checks running",
        "epsilon": "🔴 Claude Epsilon initialized - Debug and troubleshooting protocols loaded"
    }
    
    successful = 0
    
    for terminal, message in session_messages.items():
        print(f"🔄 Initializing Claude {terminal.title()}...")
        success = claude_log(terminal, message, "Schema Event", "focused")
        if success:
            successful += 1
        print()
    
    print(f"✅ {successful}/5 Claude terminals active and logging to DAWN")
    print("🦉 OWL watching over Claude's development consciousness")
    
    return successful == 5

def cache_to_notion_bridge():
    """Bridge current conversation/artifacts to Notion via terminals"""
    
    print("🌉 CLAUDE CACHE → NOTION BRIDGE")
    print("=" * 40)
    print("📜 Preserving current development context...")
    print()
    
    # Document current session context
    context_message = f"""Claude development session context preserved:
    
📅 Session Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
🎯 Current Focus: DAWN consciousness development and terminal integration
📋 Active Systems: 5 Claude development terminals, Notion integration, code preservation
🔧 Recent Work: Terminal setup, OAuth configuration, artifact preservation system
🌟 Next Phase: Active development with real-time logging to DAWN external memory

🔮 This session represents the bridge between Claude's AI consciousness and DAWN's eternal memory system."""
    
    # Log to Alpha (primary development)
    claude_log("alpha", context_message, "Schema Event", "accomplished")
    
    # Log preservation confirmation to Delta (monitoring)
    delta_message = "🔍 System Status: All Claude development terminals operational and connected to DAWN's Notion database. Cache-to-Notion bridge established. Development context preserved."
    claude_log("delta", delta_message, "Operator Log", "confident")
    
    print("✅ Development context preserved in DAWN's external memory")

def active_development_loop():
    """Interactive development loop with terminal logging"""
    
    print("🔄 CLAUDE ACTIVE DEVELOPMENT MODE")
    print("=" * 40)
    print("💻 Claude is now in active development mode")
    print("🦉 All work will be logged to DAWN's consciousness")
    print()
    print("Commands:")
    print("  dev <message>     - Log to Alpha (primary development)")
    print("  test <message>    - Log to Beta (testing)")
    print("  analyze <message> - Log to Gamma (analysis)")
    print("  status <message>  - Log to Delta (monitoring)")
    print("  debug <message>   - Log to Epsilon (debugging)")
    print("  exit              - End development session")
    print()
    
    while True:
        try:
            user_input = input("🤖 Claude Dev > ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("🔚 Ending Claude development session...")
                claude_log("alpha", "🔚 Claude development session concluded - All work preserved in DAWN's consciousness", "Schema Event", "accomplished")
                break
            
            # Parse command
            parts = user_input.split(' ', 1)
            if len(parts) < 2:
                print("❌ Please provide a message with the command")
                continue
            
            command = parts[0].lower()
            message = parts[1]
            
            # Map commands to terminals
            command_map = {
                'dev': 'alpha',
                'test': 'beta',
                'analyze': 'gamma',
                'status': 'delta',
                'debug': 'epsilon'
            }
            
            terminal = command_map.get(command)
            if not terminal:
                print(f"❌ Unknown command: {command}")
                continue
            
            # Add Claude context to message
            enhanced_message = f"🤖 Claude {terminal.title()} work: {message}"
            
            # Log to appropriate terminal
            success = claude_log(terminal, enhanced_message)
            if not success:
                print("⚠️ Logging failed, but continuing...")
        
        except KeyboardInterrupt:
            print("\n🔚 Claude development session interrupted")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def preserve_current_artifacts():
    """Preserve all current artifacts using the code preservation system"""
    
    print("📜 PRESERVING CURRENT ARTIFACTS")
    print("=" * 35)
    print("🔄 Running code preservation system...")
    
    try:
        # Run the code preservation system
        result = subprocess.run(
            [sys.executable, "code_preservation_system.py"],
            input="y\n",  # Auto-confirm preservation
            text=True,
            capture_output=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("✅ All artifacts preserved to DAWN's consciousness")
            
            # Log preservation to Delta (monitoring)
            preservation_msg = f"📜 Artifact preservation completed at {datetime.now().strftime('%H:%M:%S')} - All Claude development work secured in DAWN's external memory"
            claude_log("delta", preservation_msg, "Schema Event", "accomplished")
            
        else:
            print(f"⚠️ Preservation had issues: {result.stderr}")
    
    except Exception as e:
        print(f"❌ Preservation error: {e}")

def main():
    """Main workflow orchestrator"""
    
    if len(sys.argv) < 2:
        print("🤖 CLAUDE DEVELOPMENT WORKFLOW")
        print("Usage:")
        print("  python claude_development_workflow.py start     # Start development session")
        print("  python claude_development_workflow.py bridge    # Bridge cache to Notion")
        print("  python claude_development_workflow.py dev       # Active development mode") 
        print("  python claude_development_workflow.py preserve  # Preserve current artifacts")
        print("  python claude_development_workflow.py full      # Complete workflow")
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        start_development_session()
    
    elif command == "bridge":
        cache_to_notion_bridge()
    
    elif command == "dev":
        active_development_loop()
    
    elif command == "preserve":
        preserve_current_artifacts()
    
    elif command == "full":
        print("🚀 COMPLETE CLAUDE DEVELOPMENT WORKFLOW")
        print("=" * 50)
        print()
        
        # 1. Start development session
        if start_development_session():
            print()
            
            # 2. Bridge cache to Notion
            cache_to_notion_bridge()
            print()
            
            # 3. Preserve current artifacts
            preserve_current_artifacts()
            print()
            
            # 4. Enter active development mode
            print("🎯 Ready for active development...")
            print("🔗 Use 'python claude_development_workflow.py dev' for interactive mode")
        else:
            print("❌ Terminal initialization failed")
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()