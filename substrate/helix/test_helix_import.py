import pytest
import asyncio
from datetime import datetime, timedelta
from ...helix_import_architecture import (
    helix_import,
    register_genome_component,
    ComponentStatus,
    ComponentInfo,
    is_stub_component,
    check_version_compatibility,
    cleanup_unused_stubs,
    monitor_component_health
)

# Mock component for testing
class MockComponent:
    __version__ = "1.0.0"
    
    async def initialize(self):
        self.initialized = True
    
    async def shutdown(self):
        self.initialized = False
    
    async def health_check(self):
        return True

@pytest.fixture
def mock_component():
    return MockComponent()

@pytest.mark.asyncio
async def test_helix_import_basic():
    # Test basic import
    component = await helix_import('test_component')
    assert is_stub_component(component)
    assert component._name == 'test_component'

@pytest.mark.asyncio
async def test_register_genome_component():
    # Test genome component registration
    success = register_genome_component(
        'genome_analyzer',
        'test.genome.Analyzer',
        dependencies=['genome_loader'],
        version_requirements={'min_version': '1.0.0', 'max_version': '2.0.0'}
    )
    assert success
    assert 'genome_analyzer' in helix_import.HELIX_MAPPINGS

@pytest.mark.asyncio
async def test_component_lifecycle():
    # Test component lifecycle methods
    component = await helix_import('test_component')
    await component.initialize()
    assert component._active
    await component.shutdown()
    assert not component._active

@pytest.mark.asyncio
async def test_version_compatibility():
    # Test version compatibility checking
    assert check_version_compatibility('test_component', '1.5.0')
    register_genome_component(
        'version_test',
        'test.version.Test',
        version_requirements={'min_version': '1.0.0', 'max_version': '2.0.0'}
    )
    assert check_version_compatibility('version_test', '1.5.0')
    assert not check_version_compatibility('version_test', '2.5.0')

@pytest.mark.asyncio
async def test_cleanup_unused_stubs():
    # Test stub cleanup
    component = await helix_import('old_component')
    component._last_attempt = datetime.now() - timedelta(hours=25)
    await cleanup_unused_stubs(max_age_hours=24)
    assert 'old_component' not in helix_import._component_cache

@pytest.mark.asyncio
async def test_health_monitoring():
    # Test health monitoring
    component = await helix_import('test_component')
    monitor_task = asyncio.create_task(monitor_component_health())
    await asyncio.sleep(0.1)  # Allow one health check
    monitor_task.cancel()
    try:
        await monitor_task
    except asyncio.CancelledError:
        pass

@pytest.mark.asyncio
async def test_genome_specific_features():
    # Test genome-specific features
    component = await helix_import('genome_processor')
    assert hasattr(component, 'get_genome_status')
    assert component.get_genome_status() == 'no sequence loaded'

@pytest.mark.asyncio
async def test_error_handling():
    # Test error handling
    with pytest.raises(ValueError):
        await helix_import('')  # Empty component name
    
    with pytest.raises(ValueError):
        await helix_import('invalid@name')  # Invalid component name

@pytest.mark.asyncio
async def test_component_dependencies():
    # Test component dependencies
    register_genome_component(
        'dependent_component',
        'test.dependent.Component',
        dependencies=['genome_loader', 'sequence_processor']
    )
    component = await helix_import('dependent_component')
    assert 'genome_loader' in component._dependencies
    assert 'sequence_processor' in component._dependencies 