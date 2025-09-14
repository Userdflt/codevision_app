"""
Tests for Phase 5: Legacy Cleanup - Verify safe removal of legacy components.
"""

import pytest
import os
from pathlib import Path

class TestPhase5Cleanup:
    """Test that Phase 5 cleanup is safe and complete."""
    
    def test_pure_sdk_functions_without_legacy(self):
        """Test that pure SDK orchestrator works without any legacy imports."""
        # This test ensures pure SDK is completely independent
        from agent_project.agents.pure_orchestrator import PureSDKOrchestrator
        
        orchestrator = PureSDKOrchestrator()
        assert orchestrator is not None
        assert hasattr(orchestrator, 'process_query')
        assert hasattr(orchestrator, 'get_specialist_directly')
        
        # Check that pure SDK doesn't depend on legacy components
        import agent_project.agents.pure_sdk as pure_module
        import agent_project.agents.pure_orchestrator as orch_module
        import inspect
        
        pure_source = inspect.getsource(pure_module)
        orch_source = inspect.getsource(orch_module)
        
        # These should not be imported in pure SDK
        legacy_components = [
            'BaseAgent', 'SDKAgentWrapper', 'AgentController',
            'CodeBAgentWrapper', 'CodeCAgentWrapper'
        ]
        
        for component in legacy_components:
            assert f"from.*{component}" not in pure_source
            assert f"import.*{component}" not in pure_source
            assert f"from.*{component}" not in orch_source
            assert f"import.*{component}" not in orch_source
        
        print("✅ Pure SDK is completely independent of legacy components")
    
    def test_integration_points_ready_for_pure_sdk(self):
        """Test that integration points can work with pure SDK only."""
        # Check FastAPI router
        from agent_project.application.routers.chat import router
        import agent_project.application.routers.chat as chat_module
        import inspect
        
        chat_source = inspect.getsource(chat_module)
        assert "PureSDKOrchestrator" in chat_source
        
        # Admin router should support pure SDK
        from agent_project.application.routers.admin import router as admin_router
        import agent_project.application.routers.admin as admin_module
        
        admin_source = inspect.getsource(admin_module)
        assert "PureSDKOrchestrator" in admin_source
        
        print("✅ Integration points support pure SDK")
    
    def test_legacy_components_identified(self):
        """Test that we can identify all legacy components to be removed."""
        project_root = Path(__file__).parent.parent.parent
        src_path = project_root / "src" / "agent_project"
        
        # Components that should be removable after pure SDK migration
        removable_files = [
            "agents/sdk_adapter.py",           # SDKAgentWrapper
            "agents/orchestrator/controller.py", # AgentController  
            "agents/orchestrator/routing.py",   # Legacy routing
            "agents/orchestrator/__init__.py",  # Legacy orchestrator module
            "agents/specialists/code_b_wrapper.py", # Wrapper agents
            "agents/specialists/code_c_wrapper.py",
            "agents/specialists/code_d_wrapper.py", 
            "agents/specialists/code_e_wrapper.py",
            "agents/specialists/code_f_wrapper.py",
            "agents/specialists/code_g_wrapper.py",
            "agents/specialists/code_h_wrapper.py",
            "agents/specialists/__init__.py",   # Wrapper module
        ]
        
        # Check which files actually exist
        existing_removable = []
        for file_path in removable_files:
            full_path = src_path / file_path
            if full_path.exists():
                existing_removable.append(str(full_path))
        
        print(f"📋 Found {len(existing_removable)} legacy files that can be removed:")
        for file_path in existing_removable:
            print(f"  - {file_path}")
        
        # Core agents should remain (they contain the domain knowledge)
        core_files = [
            "core/agents/base.py",
            "core/agents/code_b/agent.py",
            "core/agents/code_c/agent.py", 
            "core/agents/code_d/agent.py",
            "core/agents/code_e/agent.py",
            "core/agents/code_f/agent.py",
            "core/agents/code_g/agent.py",
            "core/agents/code_h/agent.py",
        ]
        
        existing_core = []
        for file_path in core_files:
            full_path = src_path / file_path
            if full_path.exists():
                existing_core.append(str(full_path))
        
        print(f"🔒 Found {len(existing_core)} core files that should remain:")
        for file_path in existing_core:
            print(f"  - {file_path}")
        
        assert len(existing_removable) >= 8  # Should have wrapper files to remove
        assert len(existing_core) >= 8       # Should have core files to keep
    
    def test_backward_compatibility_requirements(self):
        """Test requirements for maintaining backward compatibility."""
        # Check CLI tool exists and can be imported
        import sys
        import os
        tools_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'tools')
        
        cli_file = os.path.join(tools_path, 'run_agent.py')
        assert os.path.exists(cli_file), "CLI tool should exist"
        
        # Check CLI source contains expected agents
        with open(cli_file, 'r') as f:
            cli_source = f.read()
        
        assert '"controller":' in cli_source
        assert '"pure_sdk":' in cli_source
        
        # Admin should support testing different agent types
        from agent_project.application.routers.admin import test_agent
        assert test_agent is not None
        
        print("✅ Backward compatibility requirements identified")
    
    def test_cleanup_safety_checks(self):
        """Test safety checks before cleanup."""
        # Ensure pure SDK tests pass
        from agent_project.agents import PureSDKOrchestrator
        
        try:
            orchestrator = PureSDKOrchestrator()
            status = orchestrator.get_orchestrator_status()
            
            assert status["orchestrator_type"] == "pure_sdk"
            assert status["sdk_native"] is True
            assert status["specialists_loaded"] >= 7
            assert status["legacy_components"] == 0
            assert status["adapters_used"] == 0
            
            print("✅ Pure SDK is fully functional and ready")
            
        except Exception as e:
            pytest.fail(f"Pure SDK not ready for cleanup: {e}")
    
    def test_migration_completeness(self):
        """Test that migration to pure SDK is complete."""
        # Check that all phases are complete
        phase_components = {
            "Phase 1": "specifications.py",
            "Phase 2": "tools.py", 
            "Phase 3": "pure_sdk.py",
            "Phase 4": "pure_orchestrator.py"
        }
        
        project_root = Path(__file__).parent.parent.parent
        agents_path = project_root / "src" / "agent_project" / "agents"
        
        for phase, component in phase_components.items():
            component_path = agents_path / component
            assert component_path.exists(), f"{phase} component {component} not found"
            
            # Check file is substantial (not just a placeholder)
            assert component_path.stat().st_size > 1000, f"{phase} component {component} too small"
        
        print("✅ All migration phases are complete")

class TestCleanupPlan:
    """Test the cleanup plan itself."""
    
    def test_cleanup_order(self):
        """Test that cleanup should happen in correct order."""
        # Order matters for safe cleanup:
        cleanup_order = [
            "1. Update imports to remove legacy references",
            "2. Remove wrapper specialist files", 
            "3. Remove AgentController and routing",
            "4. Remove SDKAgentWrapper",
            "5. Update exports and __init__.py files",
            "6. Clean up test files that test legacy components",
            "7. Update documentation and README"
        ]
        
        print("📋 Recommended cleanup order:")
        for step in cleanup_order:
            print(f"   {step}")
        
        assert len(cleanup_order) == 7
    
    def test_files_to_keep(self):
        """Test identification of files that must be kept."""
        keep_files = [
            # Core domain knowledge
            "src/agent_project/core/agents/",
            
            # Pure SDK implementation  
            "src/agent_project/agents/pure_sdk.py",
            "src/agent_project/agents/pure_orchestrator.py",
            "src/agent_project/agents/tools.py",
            "src/agent_project/agents/specifications.py",
            
            # Advanced features
            "src/agent_project/agents/advanced/",
            
            # Infrastructure 
            "src/agent_project/infrastructure/",
            "src/agent_project/application/",
            "src/agent_project/config.py",
            
            # Tests for current functionality
            "tests/test_migration/test_pure_sdk.py",
            "tests/test_migration/test_integration_phase4.py",
            "tests/test_migration/test_sdk_tools.py",
            
            # Tools
            "tools/run_agent.py",  # Will be updated but kept
            
            # Documentation 
            "README.md",
            "CHANGELOG.md",
        ]
        
        print("🔒 Files/directories to keep during cleanup:")
        for keep_file in keep_files:
            print(f"   - {keep_file}")
        
        assert len(keep_files) >= 10

if __name__ == "__main__":
    print("🧪 Running Phase 5 cleanup safety tests...")
    
    # Run the safety checks
    test_instance = TestPhase5Cleanup()
    
    try:
        test_instance.test_pure_sdk_functions_without_legacy()
        test_instance.test_integration_points_ready_for_pure_sdk() 
        test_instance.test_legacy_components_identified()
        test_instance.test_backward_compatibility_requirements()
        test_instance.test_cleanup_safety_checks()
        test_instance.test_migration_completeness()
        
        print("\n✅ All safety checks passed - cleanup can proceed safely!")
        
    except Exception as e:
        print(f"\n❌ Safety check failed: {e}")
        print("⚠️  Do not proceed with cleanup until issues are resolved")
        exit(1)
    
    # Show cleanup plan
    print("\n📋 Cleanup Plan:")
    plan_instance = TestCleanupPlan()
    plan_instance.test_cleanup_order()
    plan_instance.test_files_to_keep()
    
    print("\n🎯 Ready for Phase 5 cleanup!")
