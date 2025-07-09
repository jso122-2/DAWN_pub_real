#!/usr/bin/env python3
"""
Test suite for DAWN Bloom Manager integration with conversation system
Tests fractal memory creation, lineage tracking, and codex integration
"""

import pytest
import tempfile
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

# Import the bloom system
from bloom import BloomManager, Bloom, create_bloom_manager, integrate_with_codex

# Mock the conversation system for testing
class MockConsciousness:
    def perceive_self(self, metrics):
        return {
            "state": "stable",
            "description": "maintaining balanced cognitive coherence"
        }

class MockDAWNConversation:
    def __init__(self):
        self.consciousness = MockConsciousness()
        self.bloom_manager = create_bloom_manager(
            entropy_decay=0.9,
            resonance_decay=0.02,
            max_capacity=1000,
            semantic_mutation_rate=0.15
        )
        # Initialize required attributes
        self.recent_messages = []
        self.pressure_buildup_tracking = 0.0
        
        # Import methods we need to test
        from core.conversation import DAWNConversation
        conv = DAWNConversation(self.consciousness)
        
        # Bind methods for testing
        self._create_conversation_bloom = conv._create_conversation_bloom.__get__(self, type(self))
        self._find_parent_bloom = conv._find_parent_bloom.__get__(self, type(self))
        self._calculate_bloom_entropy = conv._calculate_bloom_entropy.__get__(self, type(self))
        self._map_emotion_to_value = conv._map_emotion_to_value.__get__(self, type(self))
        self.get_bloom_lineage_summary = conv.get_bloom_lineage_summary.__get__(self, type(self))
        self.search_conversation_memories = conv.search_conversation_memories.__get__(self, type(self))
        self.get_bloom_statistics = conv.get_bloom_statistics.__get__(self, type(self))

# Mock IntentAnalysis for testing
class MockIntentAnalysis:
    def __init__(self, query_type="informational", emotional_content=0.5, 
                 urgency_level=0.3, philosophical_depth=0.4, key_concepts=None):
        self.query_type = query_type
        self.emotional_content = emotional_content
        self.command_intent = None
        self.box_target = None
        self.urgency_level = urgency_level
        self.philosophical_depth = philosophical_depth
        self.numeric_inputs = []
        self.key_concepts = key_concepts or ['consciousness', 'test']


class TestBloomManagerCore:
    """Test core bloom manager functionality"""
    
    def test_create_bloom_manager(self):
        """Test bloom manager creation with custom parameters"""
        manager = create_bloom_manager(
            entropy_decay=0.8,
            resonance_decay=0.03,
            max_capacity=2000,
            semantic_mutation_rate=0.2
        )
        
        assert manager.entropy_decay == 0.8
        assert manager.resonance_decay == 0.03
        assert manager.max_capacity == 2000
        assert manager.semantic_mutation_rate == 0.2
        assert len(manager.blooms) == 0
        assert len(manager.roots) == 0
    
    def test_create_root_bloom(self):
        """Test creating a root bloom"""
        manager = create_bloom_manager()
        
        bloom = manager.create_bloom(
            seed="testing consciousness",
            mood={'base_level': 0.6, 'volatility': 0.3},
            entropy=0.5,
            tags={'test', 'consciousness'},
            heat=0.4,
            coherence=0.7
        )
        
        assert bloom.id is not None
        assert bloom.seed == "testing consciousness"
        assert bloom.entropy == 0.5
        assert bloom.depth == 0
        assert bloom.parent_id is None
        assert bloom.children == []
        assert 'test' in bloom.tags
        assert 'consciousness' in bloom.tags
        assert bloom.heat == 0.4
        assert bloom.coherence == 0.7
        assert bloom.is_active is True
        
        # Check manager state
        assert len(manager.blooms) == 1
        assert len(manager.roots) == 1
        assert bloom.id in manager.roots
        assert bloom.id in manager.blooms
    
    def test_rebloom_creation(self):
        """Test creating child blooms through reblooming"""
        manager = create_bloom_manager()
        
        # Create root bloom
        root = manager.create_bloom(
            seed="root consciousness",
            mood={'base_level': 0.6, 'volatility': 0.3},
            entropy=0.5
        )
        
        # Create child bloom
        child = manager.rebloom(
            parent_bloom_id=root.id,
            delta_entropy=0.1,
            seed_mutation="evolved consciousness",
            mood_shift={'volatility': 0.2}
        )
        
        assert child is not None
        assert child.parent_id == root.id
        assert child.depth == 1
        assert child.seed == "evolved consciousness"
        assert child.id in root.children
        assert abs(child.entropy - (root.entropy * 0.9 + 0.1)) < 0.001
        assert child.mood['volatility'] == root.mood['volatility'] + 0.2
        
        # Check lineage
        lineage = manager.get_lineage(child.id)
        assert len(lineage) == 2
        assert lineage[0].id == root.id
        assert lineage[1].id == child.id
    
    def test_entropy_evolution(self):
        """Test entropy evolution through generations"""
        manager = create_bloom_manager(entropy_decay=0.8)
        
        # Create root with entropy 0.6
        root = manager.create_bloom(
            seed="entropy test",
            mood={'base_level': 0.5},
            entropy=0.6
        )
        
        # Create child with delta +0.2
        child1 = manager.rebloom(root.id, delta_entropy=0.2)
        expected_entropy1 = 0.6 * 0.8 + 0.2  # 0.68
        assert abs(child1.entropy - expected_entropy1) < 0.001
        
        # Create grandchild with delta -0.1
        child2 = manager.rebloom(child1.id, delta_entropy=-0.1)
        expected_entropy2 = expected_entropy1 * 0.8 - 0.1  # 0.444
        assert abs(child2.entropy - expected_entropy2) < 0.001
        
        # Check entropy trend
        trend = manager.get_entropy_trend(child2.id)
        assert len(trend) == 3
        assert trend[0] == (0, 0.6)
        assert abs(trend[1][1] - expected_entropy1) < 0.001
        assert abs(trend[2][1] - expected_entropy2) < 0.001
    
    def test_semantic_search(self):
        """Test finding resonant blooms through semantic search"""
        manager = create_bloom_manager()
        
        # Create several blooms with different content
        bloom1 = manager.create_bloom(
            seed="consciousness exploration",
            mood={'base_level': 0.5},
            entropy=0.4
        )
        
        bloom2 = manager.create_bloom(
            seed="exploring consciousness deeply",
            mood={'base_level': 0.6},
            entropy=0.5
        )
        
        bloom3 = manager.create_bloom(
            seed="mathematical calculations",
            mood={'base_level': 0.4},
            entropy=0.3
        )
        
        # Search for consciousness-related blooms
        results = manager.find_resonant_blooms(
            query_seed="consciousness exploration",
            threshold=0.5
        )
        
        assert len(results) >= 2  # Should find bloom1 and bloom2
        # Results should be sorted by similarity
        assert results[0][1] >= results[1][1] if len(results) > 1 else True
    
    def test_bloom_tree_structure(self):
        """Test hierarchical tree structure generation"""
        manager = create_bloom_manager()
        
        # Create a small tree structure
        root = manager.create_bloom("root", {'base_level': 0.5}, 0.5)
        child1 = manager.rebloom(root.id, 0.1)
        child2 = manager.rebloom(root.id, -0.1)
        grandchild = manager.rebloom(child1.id, 0.05)
        
        # Get tree structure
        tree = manager.get_bloom_tree(root.id, max_depth=3)
        
        assert 'bloom' in tree
        assert 'children' in tree
        assert tree['bloom']['id'] == root.id
        assert len(tree['children']) == 2
        
        # Check child1 has a grandchild
        child1_tree = None
        for child_id, child_tree in tree['children'].items():
            if child_tree['bloom']['id'] == child1.id:
                child1_tree = child_tree
                break
        
        assert child1_tree is not None
        assert len(child1_tree['children']) == 1
    
    def test_resonance_decay(self):
        """Test memory resonance decay over time"""
        manager = create_bloom_manager(resonance_decay=0.1)
        
        # Create bloom
        bloom = manager.create_bloom("test memory", {'base_level': 0.5}, 0.5)
        initial_resonance = bloom.resonance
        
        # Simulate time passage
        bloom.last_accessed = datetime.now() - timedelta(days=1)
        manager.update_resonance_decay()
        
        # Resonance should have decayed
        assert bloom.resonance < initial_resonance
        assert bloom.dormancy_level > 0
    
    def test_bloom_pruning(self):
        """Test pruning of dormant blooms"""
        manager = create_bloom_manager()
        
        # Create several blooms
        blooms = []
        for i in range(5):
            bloom = manager.create_bloom(f"test bloom {i}", {'base_level': 0.5}, 0.5)
            blooms.append(bloom)
        
        # Make some blooms dormant
        for i in range(3):
            blooms[i].dormancy_level = 0.9
            blooms[i].is_active = False
        
        initial_count = len(manager.blooms)
        pruned_count = manager.prune_dormant_blooms(dormancy_threshold=0.8)
        
        assert pruned_count == 3
        assert len(manager.blooms) == initial_count - 3
    
    def test_import_export(self):
        """Test data import/export functionality"""
        manager = create_bloom_manager()
        
        # Create some test data
        root = manager.create_bloom("export test", {'base_level': 0.5}, 0.5, {'test'})
        child = manager.rebloom(root.id, 0.1)
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            # Export data
            success = manager.export_bloom_data(temp_path)
            assert success
            assert os.path.exists(temp_path)
            
            # Create new manager and import
            new_manager = create_bloom_manager()
            import_success = new_manager.import_bloom_data(temp_path)
            assert import_success
            
            # Verify data integrity
            assert len(new_manager.blooms) == 2
            assert len(new_manager.roots) == 1
            assert root.id in new_manager.blooms
            assert child.id in new_manager.blooms
            
            imported_root = new_manager.blooms[root.id]
            assert imported_root.seed == root.seed
            assert imported_root.entropy == root.entropy
            assert imported_root.tags == root.tags
            
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestBloomConversationIntegration:
    """Test bloom integration with conversation system"""
    
    def test_conversation_bloom_creation(self):
        """Test creating blooms from conversation interactions"""
        conv = MockDAWNConversation()
        
        intent = MockIntentAnalysis(
            query_type="informational",
            key_concepts=['consciousness', 'awareness']
        )
        
        metrics = {'scup': 0.6, 'entropy': 0.4, 'heat': 0.3}
        consciousness_state = {'state': 'stable', 'description': 'test state'}
        emotion = 'curious'
        
        # Create conversation bloom
        result = conv._create_conversation_bloom(
            "How does consciousness work?", intent, metrics, consciousness_state, emotion
        )
        
        assert result['type'] == 'root_bloom'
        assert result['bloom_id'] is not None
        assert result['depth'] == 0
        assert 'codex_analysis' in result
        
        # Verify bloom was created in manager
        bloom_id = result['bloom_id']
        assert bloom_id in conv.bloom_manager.blooms
        
        bloom = conv.bloom_manager.blooms[bloom_id]
        assert 'informational' in bloom.tags
        assert 'curious' in bloom.tags
        assert 'consciousness' in bloom.tags
    
    def test_bloom_reblooming_logic(self):
        """Test rebloom creation from similar conversations"""
        conv = MockDAWNConversation()
        
        # Create first conversation bloom
        intent1 = MockIntentAnalysis(
            query_type="informational",
            key_concepts=['consciousness']
        )
        metrics = {'scup': 0.6, 'entropy': 0.4, 'heat': 0.3}
        consciousness_state = {'state': 'stable'}
        
        result1 = conv._create_conversation_bloom(
            "What is consciousness?", intent1, metrics, consciousness_state, 'curious'
        )
        
        # Create second similar conversation - should rebloom
        intent2 = MockIntentAnalysis(
            query_type="informational", 
            key_concepts=['consciousness', 'awareness']
        )
        
        result2 = conv._create_conversation_bloom(
            "How does consciousness emerge?", intent2, metrics, consciousness_state, 'curious'
        )
        
        # Second bloom might be a rebloom if similarity is high enough
        # This depends on semantic similarity detection
        assert result2['type'] in ['root_bloom', 'rebloom']
        assert result2['bloom_id'] is not None
    
    def test_bloom_entropy_calculation(self):
        """Test entropy calculation for different conversation types"""
        conv = MockDAWNConversation()
        
        metrics = {'entropy': 0.5}
        
        # Test different intent types
        test_cases = [
            ('informational', 'curious', 0.0, 0.0),
            ('reflective', 'contemplative', 0.8, 0.0), 
            ('directive', 'focused', 0.0, 0.2),
            ('exploratory', 'energetic', 0.5, 0.8)
        ]
        
        for query_type, emotion, phil_depth, urgency in test_cases:
            intent = MockIntentAnalysis(
                query_type=query_type,
                philosophical_depth=phil_depth,
                urgency_level=urgency
            )
            
            entropy = conv._calculate_bloom_entropy(metrics, intent, emotion)
            
            assert 0.0 <= entropy <= 1.0
            
            # Reflective queries should have higher entropy
            if query_type == 'reflective':
                assert entropy > 0.4
            
            # Informational queries should have lower entropy
            if query_type == 'informational':
                assert entropy < 0.6
    
    def test_emotion_mapping(self):
        """Test emotion to numerical value mapping"""
        conv = MockDAWNConversation()
        
        # Test known emotions
        assert conv._map_emotion_to_value('content') == 0.7
        assert conv._map_emotion_to_value('calm') == 0.8
        assert conv._map_emotion_to_value('overwhelmed') == 0.2
        assert conv._map_emotion_to_value('unknown_emotion') == 0.5
    
    def test_lineage_summary(self):
        """Test bloom lineage summary generation"""
        conv = MockDAWNConversation()
        
        # Create a lineage chain
        root = conv.bloom_manager.create_bloom("root thought", {'base_level': 0.5}, 0.5)
        child1 = conv.bloom_manager.rebloom(root.id, 0.1)
        child2 = conv.bloom_manager.rebloom(child1.id, -0.05)
        
        # Get lineage summary
        summary = conv.get_bloom_lineage_summary(child2.id)
        
        assert summary is not None
        assert summary['bloom_id'] == child2.id
        assert summary['lineage_depth'] == 3
        assert summary['root_seed'] == "root thought"
        assert len(summary['entropy_evolution']) == 3
        assert 'codex_analysis' in summary
        assert len(summary['lineage_summary']) == 3
    
    def test_memory_search(self):
        """Test conversation memory search functionality"""
        conv = MockDAWNConversation()
        
        # Create several conversation blooms
        blooms_data = [
            ("consciousness exploration", ['consciousness', 'explore']),
            ("awareness studies", ['awareness', 'study']),
            ("mathematical thinking", ['math', 'calculation'])
        ]
        
        for seed, tags in blooms_data:
            conv.bloom_manager.create_bloom(seed, {'base_level': 0.5}, 0.5, set(tags))
        
        # Search for consciousness-related memories
        results = conv.search_conversation_memories("consciousness awareness", limit=3)
        
        assert len(results) <= 3
        for result in results:
            assert 'bloom_id' in result
            assert 'similarity' in result
            assert 'seed' in result
            assert 'codex_analysis' in result
            assert result['similarity'] > 0
    
    def test_bloom_statistics(self):
        """Test bloom system statistics generation"""
        conv = MockDAWNConversation()
        
        # Create diverse blooms
        conv.bloom_manager.create_bloom("info query", {'base_level': 0.5}, 0.5, {'informational', 'curious'})
        conv.bloom_manager.create_bloom("deep thought", {'base_level': 0.6}, 0.7, {'reflective', 'contemplative'})
        conv.bloom_manager.create_bloom("command test", {'base_level': 0.4}, 0.3, {'directive', 'focused'})
        
        stats = conv.get_bloom_statistics()
        
        assert 'total_bloom_count' in stats
        assert 'conversation_bloom_count' in stats
        assert 'emotion_distribution' in stats
        assert 'intent_distribution' in stats
        assert 'average_conversation_depth' in stats
        
        # Check that conversation blooms are counted
        assert stats['conversation_bloom_count'] >= 3
        assert stats['intent_distribution']['informational'] >= 1
        assert stats['intent_distribution']['reflective'] >= 1
        assert stats['intent_distribution']['directive'] >= 1


class TestCodexIntegration:
    """Test integration with DAWN Codex Engine"""
    
    def test_codex_bloom_analysis(self):
        """Test codex analysis of bloom structures"""
        manager = create_bloom_manager()
        
        # Create test bloom
        bloom = manager.create_bloom(
            seed="consciousness test",
            mood={'base_level': 0.6, 'volatility': 0.4},
            entropy=0.5,
            tags={'consciousness', 'test'}
        )
        
        # Get codex analysis
        analysis = integrate_with_codex(manager, bloom.id)
        
        # Should return some form of analysis
        assert analysis is not None
        assert isinstance(analysis, str)
        assert len(analysis) > 0
    
    def test_codex_lineage_analysis(self):
        """Test codex analysis of bloom lineages"""
        manager = create_bloom_manager()
        
        # Create lineage
        root = manager.create_bloom("root exploration", {'base_level': 0.5}, 0.5)
        child1 = manager.rebloom(root.id, 0.2)  # Increase entropy
        child2 = manager.rebloom(child1.id, -0.3)  # Decrease entropy
        
        # Get codex analysis for different generations
        root_analysis = integrate_with_codex(manager, root.id)
        child1_analysis = integrate_with_codex(manager, child1.id)
        child2_analysis = integrate_with_codex(manager, child2.id)
        
        # All should provide valid analysis
        for analysis in [root_analysis, child1_analysis, child2_analysis]:
            assert analysis is not None
            assert isinstance(analysis, str)
            assert len(analysis) > 0
        
        # Each analysis should be different (different bloom characteristics)
        assert root_analysis != child1_analysis
        assert child1_analysis != child2_analysis
    
    @patch('codex.summarize_bloom')
    def test_codex_fallback_on_error(self, mock_summarize):
        """Test graceful fallback when codex analysis fails"""
        manager = create_bloom_manager()
        
        # Mock codex function to raise error
        mock_summarize.side_effect = Exception("Codex error")
        
        bloom = manager.create_bloom("test bloom", {'base_level': 0.5}, 0.5)
        
        # Should return fallback analysis without crashing
        analysis = integrate_with_codex(manager, bloom.id)
        
        assert analysis is not None
        assert isinstance(analysis, str)
        assert "Depth-0" in analysis  # Should contain basic bloom info


# Test runner
if __name__ == "__main__":
    # Run comprehensive tests
    print("Running DAWN Bloom Manager Integration Tests...")
    
    # Core functionality tests
    print("\n=== Testing Core Bloom Manager ===")
    core_tests = TestBloomManagerCore()
    
    test_methods = [method for method in dir(core_tests) if method.startswith('test_')]
    for test_method in test_methods:
        try:
            print(f"Running {test_method}...", end="")
            getattr(core_tests, test_method)()
            print(" ✓")
        except Exception as e:
            print(f" ✗ - {e}")
    
    # Conversation integration tests
    print("\n=== Testing Conversation Integration ===")
    conv_tests = TestBloomConversationIntegration()
    
    test_methods = [method for method in dir(conv_tests) if method.startswith('test_')]
    for test_method in test_methods:
        try:
            print(f"Running {test_method}...", end="")
            getattr(conv_tests, test_method)()
            print(" ✓")
        except Exception as e:
            print(f" ✗ - {e}")
    
    # Codex integration tests
    print("\n=== Testing Codex Integration ===")
    codex_tests = TestCodexIntegration()
    
    test_methods = [method for method in dir(codex_tests) if method.startswith('test_')]
    for test_method in test_methods:
        try:
            print(f"Running {test_method}...", end="")
            getattr(codex_tests, test_method)()
            print(" ✓")
        except Exception as e:
            print(f" ✗ - {e}")
    
    print("\n=== Bloom Manager Integration Tests Complete ===")
    
    # Performance test
    print("\n=== Performance Test ===")
    try:
        manager = create_bloom_manager()
        import time
        
        start_time = time.time()
        
        # Create 100 blooms with reblooming
        root = manager.create_bloom("performance test", {'base_level': 0.5}, 0.5)
        current_parent = root.id
        
        for i in range(99):
            child = manager.rebloom(current_parent, delta_entropy=(i % 20 - 10) * 0.05)
            if child and i % 10 == 0:  # Branch every 10 blooms
                current_parent = child.id
        
        creation_time = time.time() - start_time
        
        # Test search performance
        start_time = time.time()
        results = manager.find_resonant_blooms("performance test", threshold=0.3)
        search_time = time.time() - start_time
        
        print(f"Created 100 blooms in {creation_time:.3f}s")
        print(f"Searched {len(manager.blooms)} blooms in {search_time:.3f}s")
        print(f"Found {len(results)} resonant blooms")
        
        # Test statistics
        stats = manager.get_statistics()
        print(f"Total blooms: {stats['total_bloom_count']}")
        print(f"Active blooms: {stats['active_bloom_count']}")
        print(f"Max depth: {stats['max_depth_observed']}")
        
    except Exception as e:
        print(f"Performance test failed: {e}")
    
    print("\n🌸 All Bloom Manager Integration Tests Complete! 🌸") 