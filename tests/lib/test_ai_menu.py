#!/usr/bin/env python3
"""
Comprehensive tests for AI/ML menu in enhanced_menu_ui
"""

import os
import sys
from unittest.mock import MagicMock, patch
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from lib.enhanced_menu_ui import MenuItem, EnhancedMenuUI, HELP_DESCRIPTIONS


class TestAIMLMenu:
    """Test AI/ML menu structure and functionality"""

    @pytest.fixture
    def menu_ui(self):
        """Create EnhancedMenuUI instance with mocked console"""
        with patch("lib.enhanced_menu_ui.Console"):
            return EnhancedMenuUI()

    def test_ai_ml_category_exists(self, menu_ui):
        """Test that AI/ML category is added to root menu"""
        assert "ai-ml" in menu_ui.menu_items
        ai_ml = menu_ui.menu_items["ai-ml"]
        assert ai_ml.is_category
        assert ai_ml.parent == "root"
        assert ai_ml.label == "🤖 AI & Machine Learning"
        assert ai_ml.emoji == "🤖"

        # Check it's in root's children
        root = menu_ui.menu_items["root"]
        assert "ai-ml" in root.children

    def test_ai_ml_subcategories(self, menu_ui):
        """Test all AI/ML subcategories exist"""
        ai_ml = menu_ui.menu_items["ai-ml"]
        expected_subcategories = ["ai-cli-tools", "ml-frameworks", "image-generation", "local-llm-uis", "ai-agents"]

        assert set(ai_ml.children) == set(expected_subcategories)

        # Check each subcategory
        for subcat_id in expected_subcategories:
            assert subcat_id in menu_ui.menu_items
            subcat = menu_ui.menu_items[subcat_id]
            assert subcat.is_category
            assert subcat.parent == "ai-ml"

    def test_ai_cli_tools_menu(self, menu_ui):
        """Test AI CLI tools submenu"""
        cli_tools = menu_ui.menu_items["ai-cli-tools"]
        assert cli_tools.label == "🤖 AI CLI Tools"
        assert cli_tools.emoji == "🤖"

        expected_tools = ["ollama", "aichat", "gemini-cli", "claude-cli", "gptcli", "pygpt"]
        assert set(cli_tools.children) == set(expected_tools)

        # Check specific tools
        ollama = menu_ui.menu_items["ollama"]
        assert ollama.label == "🦙 Ollama"
        assert ollama.emoji == "🦙"
        assert ollama.default is True  # Should be selected by default
        assert ollama.parent == "ai-cli-tools"
        assert ollama.help_text is not None
        assert "Ollama makes running large language models locally" in ollama.help_text

    def test_ml_frameworks_menu(self, menu_ui):
        """Test ML frameworks submenu"""
        ml_frameworks = menu_ui.menu_items["ml-frameworks"]
        assert ml_frameworks.label == "🧠 ML Frameworks"
        assert ml_frameworks.emoji == "🧠"

        expected_tools = [
            "pytorch",
            "tensorflow",
            "jupyter-lab",
            "scikit-learn",
            "pandas-numpy",
            "huggingface-cli",
            "cuda-toolkit",
        ]
        assert set(ml_frameworks.children) == set(expected_tools)

        # Check PyTorch
        pytorch = menu_ui.menu_items["pytorch"]
        assert pytorch.label == "🔥 PyTorch"
        assert pytorch.emoji == "🔥"
        assert pytorch.default is True
        assert pytorch.help_text is not None
        assert "most popular deep learning framework" in pytorch.help_text

        # Check JupyterLab
        jupyter = menu_ui.menu_items["jupyter-lab"]
        assert jupyter.label == "📓 JupyterLab"
        assert jupyter.emoji == "📓"
        assert jupyter.default is True
        assert jupyter.help_text is not None
        assert "next-gen interface for Jupyter notebooks" in jupyter.help_text

    def test_image_generation_menu(self, menu_ui):
        """Test image generation tools submenu"""
        image_gen = menu_ui.menu_items["image-generation"]
        assert image_gen.label == "🎨 Image Generation"
        assert image_gen.emoji == "🎨"

        expected_tools = ["stable-diffusion-webui", "comfyui", "invokeai", "fooocus"]
        assert set(image_gen.children) == set(expected_tools)

        # Check Stable Diffusion WebUI
        sd_webui = menu_ui.menu_items["stable-diffusion-webui"]
        assert sd_webui.label == "🖼️ AUTOMATIC1111 WebUI"
        assert sd_webui.emoji == "🖼️"
        assert sd_webui.default is True
        assert sd_webui.help_text is not None
        assert "most popular Stable Diffusion interface" in sd_webui.help_text

    def test_local_llm_uis_menu(self, menu_ui):
        """Test local LLM UI tools submenu"""
        llm_uis = menu_ui.menu_items["local-llm-uis"]
        assert llm_uis.label == "💬 Local LLM UIs"
        assert llm_uis.emoji == "💬"

        expected_tools = ["text-generation-webui", "lm-studio", "gpt4all", "jan-ai", "open-webui"]
        assert set(llm_uis.children) == set(expected_tools)

        # Check Text Generation WebUI
        text_gen = menu_ui.menu_items["text-generation-webui"]
        assert text_gen.label == "🌐 Text Generation WebUI"
        assert text_gen.emoji == "🌐"
        assert text_gen.default is True
        assert text_gen.help_text is not None
        assert "Oobabooga's interface" in text_gen.help_text

    def test_ai_agents_menu(self, menu_ui):
        """Test AI agent frameworks submenu"""
        ai_agents = menu_ui.menu_items["ai-agents"]
        assert ai_agents.label == "🔧 AI Agent Frameworks"
        assert ai_agents.emoji == "🔧"

        expected_tools = ["langchain", "langgraph", "crewai", "autogen", "langflow", "flowise"]
        assert set(ai_agents.children) == set(expected_tools)

        # Check LangChain
        langchain = menu_ui.menu_items["langchain"]
        assert langchain.label == "🔗 LangChain"
        assert langchain.emoji == "🔗"
        assert langchain.default is True
        assert langchain.help_text is not None
        assert "build applications powered by language models" in langchain.help_text

    def test_ai_ml_default_selections(self, menu_ui):
        """Test that appropriate AI/ML tools are selected by default"""
        default_tools = [
            "ollama",  # AI CLI
            "pytorch",  # ML framework
            "jupyter-lab",  # ML framework
            "scikit-learn",  # ML framework
            "pandas-numpy",  # ML framework
            "stable-diffusion-webui",  # Image generation
            "text-generation-webui",  # Local LLM UI
            "langchain",  # AI agents
        ]

        for tool_id in default_tools:
            tool = menu_ui.menu_items[tool_id]
            assert tool.default is True
            assert tool.selected is True
            assert tool_id in menu_ui.selected_items

    def test_ai_ml_help_descriptions(self, menu_ui):
        """Test that key AI/ML tools have help descriptions"""
        tools_with_help = [
            "ollama",
            "pytorch",
            "jupyter-lab",
            "stable-diffusion-webui",
            "text-generation-webui",
            "langchain",
        ]

        for tool_id in tools_with_help:
            assert tool_id in HELP_DESCRIPTIONS
            tool = menu_ui.menu_items[tool_id]
            assert tool.help_text == HELP_DESCRIPTIONS[tool_id]
            assert len(tool.help_text) > 50  # Meaningful description

    def test_ai_ml_selection_indicators(self, menu_ui):
        """Test selection indicators for AI/ML categories"""
        # Test subcategory indicators work correctly
        # ML Frameworks should have partial selection (some defaults selected)
        ml_frameworks = menu_ui.menu_items["ml-frameworks"]

        # Count selections
        selected = sum(1 for child_id in ml_frameworks.children if menu_ui.menu_items[child_id].selected)
        total = len(ml_frameworks.children)

        # We have some defaults (pytorch, jupyter-lab, etc.) but not all
        assert selected > 0
        assert selected < total

        indicator = menu_ui.get_selection_indicator(ml_frameworks)
        assert indicator == "◎"  # Partial selection

        # Select all AI CLI tools
        cli_tools = menu_ui.menu_items["ai-cli-tools"]
        for tool_id in cli_tools.children:
            tool = menu_ui.menu_items[tool_id]
            tool.selected = True
            menu_ui.selected_items.add(tool_id)

        # Check CLI tools indicator
        indicator = menu_ui.get_selection_indicator(cli_tools)
        assert indicator == "◉"  # All selected

    def test_ai_ml_menu_navigation(self, menu_ui):
        """Test navigating to AI/ML menus"""
        # Navigate to AI/ML category
        menu_ui.current_menu = "ai-ml"
        items = menu_ui.get_current_menu_items()
        item_ids = [item.id for item in items]

        expected = ["ai-cli-tools", "ml-frameworks", "image-generation", "local-llm-uis", "ai-agents"]
        assert set(item_ids) == set(expected)

        # Navigate to ML frameworks
        menu_ui.current_menu = "ml-frameworks"
        items = menu_ui.get_current_menu_items()
        item_ids = [item.id for item in items]

        assert "pytorch" in item_ids
        assert "tensorflow" in item_ids
        assert "jupyter-lab" in item_ids

    def test_ai_ml_tool_count(self, menu_ui):
        """Test total count of AI/ML tools"""
        # Count all AI/ML tools (non-category items)
        ai_tools = []

        def collect_tools(category_id):
            category = menu_ui.menu_items[category_id]
            for child_id in category.children:
                child = menu_ui.menu_items[child_id]
                if child.is_category:
                    collect_tools(child_id)
                else:
                    ai_tools.append(child_id)

        collect_tools("ai-ml")

        # We should have 28 AI/ML tools total
        assert len(ai_tools) == 28

        # Verify some key tools are present
        assert "ollama" in ai_tools
        assert "pytorch" in ai_tools
        assert "stable-diffusion-webui" in ai_tools
        assert "langchain" in ai_tools

    def test_emoji_consistency(self, menu_ui):
        """Test that all AI/ML items have appropriate emojis"""

        def check_emojis(item_id):
            item = menu_ui.menu_items[item_id]
            assert item.emoji != "", f"{item_id} is missing emoji"

            if item.is_category:
                for child_id in item.children:
                    check_emojis(child_id)

        check_emojis("ai-ml")

    def test_parent_child_relationships(self, menu_ui):
        """Test all AI/ML items have correct parent-child relationships"""

        def verify_relationships(parent_id):
            parent = menu_ui.menu_items[parent_id]
            for child_id in parent.children:
                child = menu_ui.menu_items[child_id]
                assert child.parent == parent_id, f"{child_id} has wrong parent"
                if child.is_category:
                    verify_relationships(child_id)

        verify_relationships("ai-ml")


class TestAIMLConfiguration:
    """Test AI/ML configuration saving and loading"""

    @pytest.fixture
    def menu_ui(self):
        """Create EnhancedMenuUI with mocked console"""
        with patch("lib.enhanced_menu_ui.Console"):
            return EnhancedMenuUI()

    def test_ai_ml_in_saved_config(self, menu_ui):
        """Test that AI/ML selections are included in saved configuration"""
        # Select some AI tools
        menu_ui.selected_items = {"ollama", "pytorch", "langchain"}

        # Generate config structure
        config = {"selected_items": sorted(menu_ui.selected_items), "configurable_items": {}}

        assert "ollama" in config["selected_items"]
        assert "pytorch" in config["selected_items"]
        assert "langchain" in config["selected_items"]

    def test_ai_ml_menu_completeness(self, menu_ui):
        """Test that AI/ML menu is complete and well-structured"""

        # Every item should have required fields
        def check_item_completeness(item_id):
            item = menu_ui.menu_items[item_id]
            assert item.id is not None
            assert item.label is not None
            assert item.description is not None
            assert len(item.label) > 0
            assert len(item.description) > 0

            if item.is_category:
                assert len(item.children) > 0
                for child_id in item.children:
                    check_item_completeness(child_id)

        check_item_completeness("ai-ml")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
