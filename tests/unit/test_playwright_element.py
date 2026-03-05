from unittest.mock import Mock
from src.core.elements.playwright_element import PlaywrightElement

def test_playwright_element_wraps_locator():
    mock_locator = Mock()
    mock_locator.inner_text.return_value = "Submit"
    mock_locator.is_visible.return_value = True

    element = PlaywrightElement(mock_locator, "submit_button")
    
    # Test text
    assert element.get_text() == "Submit"
    mock_locator.inner_text.assert_called_once()
    
    # Test visibility
    assert element.is_visible() is True
    mock_locator.is_visible.assert_called_once()
    
    # Test click logging and forwarding
    element.click(force=True)
    mock_locator.click.assert_called_once_with(force=True)

    # Test fill logging and forwarding
    element.fill("testuser")
    mock_locator.fill.assert_called_once_with("testuser")
