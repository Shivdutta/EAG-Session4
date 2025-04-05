# MCP server for Pages on Mac
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import subprocess
import asyncio

# Instantiate MCP server
mcp = FastMCP("PagesController")

def run_apple_script(script):
    """Helper function to run AppleScript and handle errors"""
    result = subprocess.run(['osascript', '-e', script], 
                          capture_output=True, 
                          text=True,
                          check=True)
    return result

@mcp.tool()
async def pages_open() -> dict:
    """Open Pages application on Mac with a new document"""
    try:
        script = """
        tell application "Pages"
            activate
            make new document
            delay 1
        end tell
        """
        result = run_apple_script(script)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Pages opened successfully with new document"
                )
            ]
        }
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Pages: {error_msg}"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Pages: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def pages_add_text(text: str) -> dict:
    """Add text to the Pages document"""
    try:
        escaped_text = text.replace('"', '\\"')
        
        script = f"""
        tell application "Pages"
            tell front document
                set the selection to the end of the body text
                set the selected text to "{escaped_text}"
            end tell
        end tell
        """
        run_apple_script(script)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Text added successfully: {text[:30]}..." if len(text) > 30 else f"Text added successfully: {text}"
                )
            ]
        }
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error adding text: {error_msg}"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error adding text: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def pages_add_heading(text: str, level: int = 1) -> dict:
    """Add a heading to the Pages document with specified level (1-9)"""
    try:
        if level < 1 or level > 9:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Error: Heading level must be between 1 and 9"
                    )
                ]
            }
        
        escaped_text = text.replace('"', '\\"')
        
        script = f"""
        tell application "Pages"
            tell front document
                set the selection to the end of the body text
                set the selected text to "{escaped_text}"
                set paragraph style of the selection to paragraph style "Heading {level}"
            end tell
        end tell
        """
        run_apple_script(script)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Heading level {level} added successfully: {text}"
                )
            ]
        }
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error adding heading: {error_msg}"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error adding heading: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def pages_add_image(width: int = 400, height: int = 300) -> dict:
    """Add a sample image shape to the Pages document"""
    try:
        script = f"""
        tell application "Pages"
            tell front document
                set the selection to the end of the body text
                make new image with properties {{width:{width}, height:{height}}}
            end tell
        end tell
        """
        run_apple_script(script)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Image placeholder added with dimensions {width}x{height}"
                )
            ]
        }
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error adding image: {error_msg}"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error adding image: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def pages_save_document(filename: str) -> dict:
    """Save the Pages document with the specified filename"""
    try:
        script = f"""
        tell application "Pages"
            set desktopPath to (path to desktop) as text
            set docPath to desktopPath & "{filename}.pages"
            save front document in docPath
        end tell
        """
        run_apple_script(script)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Document saved as '{filename}.pages' on the desktop"
                )
            ]
        }
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error saving document: {error_msg}"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error saving document: {str(e)}"
                )
            ]
        }

if __name__ == "__main__":
    print("Starting Pages MCP Server...")
    mcp.run(transport="stdio")