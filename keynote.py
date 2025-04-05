# Updated MCP server for Keynote on Mac
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import os
import subprocess
import time
import asyncio

# Instantiate MCP server
mcp = FastMCP("KeynoteController")

# Keynote-related tools
@mcp.tool()
async def keynote_open() -> dict:
    """Open Keynote application on Mac"""
    try:
        # Open Keynote using AppleScript
        script = """
        tell application "Keynote"
            activate
            delay 1
            make new document
            delay 1
        end tell
        """
        subprocess.run(['osascript', '-e', script])
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Keynote opened successfully with new document"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Keynote: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def draw_rectangle(x1: int, y1: int, x2: int, y2: int) -> dict:
    """Draw a rectangle in Keynote from (x1,y1) to (x2,y2)"""
    try:
        width = x2 - x1
        height = y2 - y1
        
        # Fixed AppleScript - the problem was with the rectangle shape type format
        script = f"""
        tell application "Keynote"
            tell front document
                tell current slide
                    set myShape to make new shape
                    set shape type of myShape to rectangle
                    set position of myShape to {{{x1}, {y1}}}
                    set width of myShape to {width}
                    set height of myShape to {height}
                end tell
            end tell
        end tell
        """
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        
        if result.stderr:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text=f"Error in AppleScript: {result.stderr}"
                    )
                ]
            }
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Rectangle drawn from ({x1},{y1}) to ({x2},{y2})"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing rectangle: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def add_text_in_keynote(text: str) -> dict:
    """Add text box with content in Keynote"""
    try:
        # Also fixed the text item script to use a similar pattern
        script = f"""
        tell application "Keynote"
            tell front document
                tell current slide
                    set newTextItem to make new text item
                    set object text of newTextItem to "{text}"
                    set position of newTextItem to {{500, 300}}
                    set width of newTextItem to 400
                    set height of newTextItem to 200
                end tell
            end tell
        end tell
        """
        
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        
        if result.stderr:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text=f"Error in AppleScript: {result.stderr}"
                    )
                ]
            }
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Text added successfully: {text}"
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

if __name__ == "__main__":
    print("Starting Keynote MCP Server...")
    mcp.run(transport="stdio")