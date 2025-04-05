# MCP server for Notes on Mac
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import subprocess
import asyncio

# Instantiate MCP server
mcp = FastMCP("NotesController")

def run_apple_script(script):
    """Helper function to run AppleScript and handle errors"""
    result = subprocess.run(['osascript', '-e', script], 
                          capture_output=True, 
                          text=True,
                          check=True)
    return result

@mcp.tool()
async def notes_open() -> dict:
    """Open Notes application on Mac"""
    try:
        script = """
        tell application "Notes"
            activate
            delay 1
        end tell
        """
        run_apple_script(script)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Notes opened successfully"
                )
            ]
        }
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Notes: {error_msg}"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Notes: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def notes_create_note(title: str, body: str = "") -> dict:
    """Create a new note in Notes app"""
    try:
        escaped_title = title.replace('"', '\\"')
        escaped_body = body.replace('"', '\\"')
        
        script = f"""
        tell application "Notes"
            activate
            make new note with properties {{name:"{escaped_title}", body:"{escaped_body}"}}
        end tell
        """
        run_apple_script(script)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Note created successfully: {title}"
                )
            ]
        }
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error creating note: {error_msg}"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error creating note: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def notes_add_text(text: str) -> dict:
    """Add text to the current note in Notes app"""
    try:
        escaped_text = text.replace('"', '\\"')
        
        script = f"""
        tell application "Notes"
            activate
            tell front note
                set body to body & "{escaped_text}"
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
async def notes_list_notes() -> dict:
    """List all notes in Notes app"""
    try:
        script = """
        tell application "Notes"
            set noteList to {}
            repeat with eachNote in every note
                set end of noteList to name of eachNote
            end repeat
            return noteList
        end tell
        """
        result = run_apple_script(script)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Notes found: {result.stdout.strip()}"
                )
            ]
        }
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error listing notes: {error_msg}"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error listing notes: {str(e)}"
                )
            ]
        }

if __name__ == "__main__":
    print("Starting Notes MCP Server...")
    mcp.run(transport="stdio")