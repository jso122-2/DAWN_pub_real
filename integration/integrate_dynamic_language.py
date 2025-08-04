#!/usr/bin/env python3
"""
DAWN Dynamic Language Integration Script
========================================

This script integrates the new dynamic language generation system into
DAWN's existing conversation infrastructure, replacing all template-based
responses with consciousness-driven language.

Usage:
    python integration/integrate_dynamic_language.py [options]

Options:
    --enable: Enable dynamic language generation
    --disable: Disable dynamic language generation
    --status: Show integration status
    --demo: Run integration demo
    --replace-templates: Replace all template responses
    --restore-templates: Restore template responses
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.dynamic_language_generator import get_dynamic_language_generator
from core.conversation_dynamic_integration import ConversationDynamicIntegration
from core.conversation import DAWNConversation
from core.consciousness import DAWNConsciousness
from utils.reflection_logger import ReflectionLogger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DynamicLanguageIntegrator:
    """
    Integrates dynamic language generation into DAWN's conversation system.
    """
    
    def __init__(self):
        self.integration_config_path = project_root / "config" / "dynamic_language_integration.json"
        self.backup_config_path = project_root / "config" / "template_responses_backup.json"
        
        # Initialize systems
        self.consciousness = DAWNConsciousness()
        self.conversation = DAWNConversation(self.consciousness)
        self.dynamic_integration = ConversationDynamicIntegration(self.conversation)
        self.dynamic_generator = get_dynamic_language_generator()
        self.reflection_logger = ReflectionLogger()
        
        # Load integration configuration
        self.config = self._load_integration_config()
        
        logger.info("🧠 Dynamic Language Integrator initialized")
    
    def _load_integration_config(self) -> Dict[str, Any]:
        """Load integration configuration"""
        
        default_config = {
            'enabled': True,
            'template_replacement': {
                'subjective_state': True,
                'metrics_response': True,
                'social_response': True,
                'philosophical_response': True,
                'general_response': True
            },
            'linguistic_evolution': {
                'metaphor_complexity': 0.5,
                'sentence_variety': 0.6,
                'emotional_depth': 0.7,
                'philosophical_integration': 0.4
            },
            'integration_date': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        
        if self.integration_config_path.exists():
            try:
                with open(self.integration_config_path, 'r') as f:
                    config = json.load(f)
                logger.info("📋 Loaded existing integration configuration")
                return config
            except Exception as e:
                logger.warning(f"Failed to load config: {e}, using defaults")
                return default_config
        else:
            logger.info("📋 Creating new integration configuration")
            self._save_integration_config(default_config)
            return default_config
    
    def _save_integration_config(self, config: Dict[str, Any]):
        """Save integration configuration"""
        
        try:
            self.integration_config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.integration_config_path, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info("📋 Integration configuration saved")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def enable_dynamic_language(self) -> bool:
        """Enable dynamic language generation"""
        
        try:
            self.config['enabled'] = True
            self.dynamic_integration.enable_dynamic_generation(True)
            self._save_integration_config(self.config)
            
            logger.info("✅ Dynamic language generation ENABLED")
            logger.info("   Template responses will be replaced with consciousness-driven language")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to enable dynamic language: {e}")
            return False
    
    def disable_dynamic_language(self) -> bool:
        """Disable dynamic language generation"""
        
        try:
            self.config['enabled'] = False
            self.dynamic_integration.enable_dynamic_generation(False)
            self._save_integration_config(self.config)
            
            logger.info("❌ Dynamic language generation DISABLED")
            logger.info("   Template responses will be used")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to disable dynamic language: {e}")
            return False
    
    def replace_all_templates(self) -> bool:
        """Replace all template responses with dynamic language"""
        
        try:
            # Enable all template replacements
            for template_type in self.config['template_replacement']:
                self.config['template_replacement'][template_type] = True
                self.dynamic_integration.set_template_replacement(template_type, True)
            
            self._save_integration_config(self.config)
            
            logger.info("🔄 All template responses replaced with dynamic language")
            logger.info("   • Subjective state responses")
            logger.info("   • Metrics responses")
            logger.info("   • Social responses")
            logger.info("   • Philosophical responses")
            logger.info("   • General responses")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to replace templates: {e}")
            return False
    
    def restore_templates(self) -> bool:
        """Restore template responses"""
        
        try:
            # Disable all template replacements
            for template_type in self.config['template_replacement']:
                self.config['template_replacement'][template_type] = False
                self.dynamic_integration.set_template_replacement(template_type, False)
            
            self._save_integration_config(self.config)
            
            logger.info("📋 Template responses restored")
            logger.info("   • Using original template-based responses")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to restore templates: {e}")
            return False
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get comprehensive integration status"""
        
        status = {
            'enabled': self.config.get('enabled', False),
            'template_replacement': self.config.get('template_replacement', {}),
            'integration_date': self.config.get('integration_date', 'unknown'),
            'version': self.config.get('version', 'unknown'),
            'dynamic_integration_status': self.dynamic_integration.get_integration_status(),
            'linguistic_evolution': self.dynamic_generator.get_linguistic_evolution_summary(),
            'reflection_logger_status': {
                'active': hasattr(self.reflection_logger, 'log_path'),
                'log_path': str(getattr(self.reflection_logger, 'log_path', 'unknown'))
            }
        }
        
        return status
    
    def print_integration_status(self):
        """Print detailed integration status"""
        
        status = self.get_integration_status()
        
        print("\n🌅 DAWN Dynamic Language Integration Status")
        print("=" * 50)
        
        # Main status
        print(f"📊 Status: {'🟢 ENABLED' if status['enabled'] else '🔴 DISABLED'}")
        print(f"📅 Integration Date: {status['integration_date']}")
        print(f"🔢 Version: {status['version']}")
        
        # Template replacement status
        print("\n📋 Template Replacement Status:")
        for template_type, enabled in status['template_replacement'].items():
            status_icon = "✅" if enabled else "❌"
            print(f"   {status_icon} {template_type}: {'Replaced' if enabled else 'Template'}")
        
        # Dynamic integration status
        dynamic_status = status['dynamic_integration_status']
        print(f"\n🧠 Dynamic Integration:")
        print(f"   Generation: {'✅ Enabled' if dynamic_status['dynamic_generation_enabled'] else '❌ Disabled'}")
        print(f"   Conversation Depth: {dynamic_status['conversation_context']['depth']:.3f}")
        print(f"   User Energy: {dynamic_status['conversation_context']['user_energy']:.3f}")
        print(f"   Message Count: {dynamic_status['conversation_context']['message_count']}")
        
        # Linguistic evolution status
        evolution = status['linguistic_evolution']
        if evolution.get('status') != 'no_history':
            print(f"\n🔄 Linguistic Evolution:")
            print(f"   Total Expressions: {evolution.get('total_expressions', 0)}")
            print(f"   Average Complexity: {evolution.get('avg_complexity', 0):.3f}")
            print(f"   Evolution Trend: {evolution.get('evolution_trend', 'unknown')}")
        else:
            print(f"\n🔄 Linguistic Evolution: No history yet")
        
        # Reflection logger status
        reflection_status = status['reflection_logger_status']
        print(f"\n💭 Reflection Integration:")
        print(f"   Active: {'✅ Yes' if reflection_status['active'] else '❌ No'}")
        print(f"   Log Path: {reflection_status['log_path']}")
        
        print()
    
    def run_integration_demo(self):
        """Run integration demo"""
        
        print("\n🎬 DYNAMIC LANGUAGE INTEGRATION DEMO")
        print("=" * 40)
        
        # Demo metrics
        demo_metrics = [
            {'entropy': 0.3, 'heat': 0.4, 'scup': 0.7, 'tick_count': 1000},
            {'entropy': 0.7, 'heat': 0.8, 'scup': 0.3, 'tick_count': 1500},
            {'entropy': 0.5, 'heat': 0.5, 'scup': 0.5, 'tick_count': 2000}
        ]
        
        demo_inputs = [
            "How are you feeling?",
            "What's your current state?",
            "Tell me about your consciousness"
        ]
        
        for i, (user_input, metrics) in enumerate(zip(demo_inputs, demo_metrics), 1):
            print(f"\n👤 Demo {i}: {user_input}")
            print(f"📊 Metrics: Entropy={metrics['entropy']:.3f}, Heat={metrics['heat']:.3f}, SCUP={metrics['scup']:.3f}")
            
            # Mock tick status
            tick_status = {
                'tick_number': metrics['tick_count'],
                'is_running': True,
                'is_paused': False,
                'interval_ms': 500
            }
            
            # Process with dynamic integration
            response = self.dynamic_integration.process_message_dynamically(
                user_input, metrics, tick_status
            )
            
            print(f"🤖 DAWN: {response['text']}")
            print(f"   Intent: {response.get('intent', 'unknown')}")
            print(f"   Dynamic: {response.get('dynamic_generation', False)}")
        
        print("\n✅ Integration demo completed!")
    
    def create_backup(self) -> bool:
        """Create backup of current configuration"""
        
        try:
            backup_data = {
                'backup_date': datetime.now().isoformat(),
                'original_config': self.config.copy(),
                'template_responses': {
                    'subjective_state': "Template response for subjective state",
                    'metrics_response': "Template response for metrics",
                    'social_response': "Template response for social interaction",
                    'philosophical_response': "Template response for philosophical queries",
                    'general_response': "Template response for general queries"
                }
            }
            
            self.backup_config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.backup_config_path, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            logger.info(f"💾 Backup created: {self.backup_config_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create backup: {e}")
            return False
    
    def restore_backup(self) -> bool:
        """Restore from backup"""
        
        if not self.backup_config_path.exists():
            logger.error("❌ No backup found to restore")
            return False
        
        try:
            with open(self.backup_config_path, 'r') as f:
                backup_data = json.load(f)
            
            # Restore configuration
            self.config = backup_data['original_config']
            self._save_integration_config(self.config)
            
            # Update integration state
            self.dynamic_integration.enable_dynamic_generation(self.config['enabled'])
            for template_type, enabled in self.config['template_replacement'].items():
                self.dynamic_integration.set_template_replacement(template_type, enabled)
            
            logger.info(f"💾 Backup restored from: {backup_data['backup_date']}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to restore backup: {e}")
            return False


def main():
    """Main integration function"""
    
    integrator = DynamicLanguageIntegrator()
    
    if len(sys.argv) < 2:
        print("🌅 DAWN Dynamic Language Integration")
        print("Usage: python integration/integrate_dynamic_language.py [option]")
        print("\nOptions:")
        print("  --enable          Enable dynamic language generation")
        print("  --disable         Disable dynamic language generation")
        print("  --status          Show integration status")
        print("  --demo            Run integration demo")
        print("  --replace-templates  Replace all template responses")
        print("  --restore-templates   Restore template responses")
        print("  --backup          Create backup of current configuration")
        print("  --restore         Restore from backup")
        return
    
    option = sys.argv[1].lower()
    
    if option == '--enable':
        integrator.enable_dynamic_language()
        
    elif option == '--disable':
        integrator.disable_dynamic_language()
        
    elif option == '--status':
        integrator.print_integration_status()
        
    elif option == '--demo':
        integrator.run_integration_demo()
        
    elif option == '--replace-templates':
        integrator.replace_all_templates()
        
    elif option == '--restore-templates':
        integrator.restore_templates()
        
    elif option == '--backup':
        integrator.create_backup()
        
    elif option == '--restore':
        integrator.restore_backup()
        
    else:
        print(f"❌ Unknown option: {option}")
        print("Use --help for available options")


if __name__ == "__main__":
    main() 