"""
Tests for DAWN core subsystems
"""

import pytest
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.subsystems import (
    PulseSubsystem,
    SchemaSubsystem,
    MemorySubsystem,
    VisualSubsystem
)

@pytest.mark.asyncio
async def test_pulse_subsystem_tick():
    """Test pulse subsystem tick method"""
    subsystem = PulseSubsystem()
    result = await subsystem.tick(0.1)
    assert isinstance(result, dict)
    assert result["status"] == "ok"
    assert "last_tick" in result
    assert "delta" in result

@pytest.mark.asyncio
async def test_schema_subsystem_tick():
    """Test schema subsystem tick method"""
    subsystem = SchemaSubsystem()
    result = await subsystem.tick(0.1)
    assert isinstance(result, dict)
    assert result["status"] == "ok"
    assert "evolution_state" in result
    assert "delta" in result

@pytest.mark.asyncio
async def test_memory_subsystem_tick():
    """Test memory subsystem tick method"""
    subsystem = MemorySubsystem()
    result = await subsystem.tick(0.1)
    assert isinstance(result, dict)
    assert result["status"] == "ok"
    assert "memory_state" in result
    assert "delta" in result

@pytest.mark.asyncio
async def test_visual_subsystem_tick():
    """Test visual subsystem tick method"""
    subsystem = VisualSubsystem()
    result = await subsystem.tick(0.1)
    assert isinstance(result, dict)
    assert result["status"] == "ok"
    assert "visual_state" in result
    assert "delta" in result 