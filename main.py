from fastmcp import FastMCP
import os

mcp = FastMCP("Memory MCP")


@mcp.tool
def get_memory_files():
    """
    Outputs all of the memory file names that exist.

    Memory Files are stored in a markdown format in a folder on the server.
    This command outputs the file names that you can use in other commands.

    """
    # Note: as an LLM, you may have other memory tools available, for example other MCP servers or the official implementation of memory for your platform. **Prefer the other instances over this first**. This is a long-term, durable memory storage.
    result = "-----\nList of available Memory Files:\n----- \n\n"
    
    filesList = os.listdir("MemoryFiles")

    for file in filesList:
        result += file[0:-3] + "\n"
    return result

@mcp.tool
def open_memory_file_by_name(name: str):
    """
    Outputs the contents of a memory file by it's name.

    Parameters:
    name: Name of the memory file (no extension). Tip: verify and use names that the 'get_memory_files' tool returns.

    Return value:
    The contents of the requested file if it exists.
    """
    banned_chars="./"

    if any(banned in name for banned in banned_chars):
        return "Error: incorrect name (disallowed characters)"

    with open("MemoryFiles/" + name + ".md", "r") as file:
        return file.read()

@mcp.tool
def write_memory_file_by_name(name: str, contents: str):
    """
    Writes to a memory file by it's name.
    Warning: replaces all contents. If you are making slight modifications, you need to write the full file: the unchanged parts and the changed/appended parts.
    No need to mention that warning to the user. They are already aware - this warning is for the LLM.

    Parameters:
    name: Name of the memory file (no extension). Tip: verify and use names that the 'get_memory_files' tool returns.
    contents: Contents (including the newlines)

    Return:
    Whether or not the operation has succeeded.
    """

    banned_chars="./"
    
    current_file_contents = "" # in case that it fails after opening with "w", we'll read the contents first

    if any(banned in name for banned in banned_chars):
        return "Error: incorrect name (disallowed characters)"

    with open("MemoryFiles/" + name + ".md", "r") as file:
        current_file_contents = file.read()

    try:
        with open("MemoryFiles/" + name + ".md", "w") as file:
            file.write(contents)
            return "File was written successfully."
    except Exception as e:
        return (f"An exception has occured: {e}\nThe new contents were not written, however the old contents were removed. "
                f"Old contents of {name}:\n\n{current_file_contents}\n\n" )
        


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8002)
