uv add mcp[cli]==2.0

uv remove fastmcp


 - uncalled-for==0.4.0
(class7) PS C:\DEV\edureka\class7\C15\mcp-demo\first-demo> uv add mcp[cli]==2.0
Resolved 172 packages in 1.73s
Prepared 5 packages in 819ms
Uninstalled 1 package in 98ms
Installed 5 packages in 1.68s
 + httpcore2==2.12.0
 + httpx2==2.12.0
 - mcp==1.29.1
 + mcp==2.0.0
 + mcp-types==2.0.0
 + truststore==0.10.4
(class7) PS C:\DEV\edureka\class7\C15\mcp-demo\first-demo> mcp dev demo.py     
Need to install the following packages:
@modelcontextprotocol/inspector@2.4.0
Ok to proceed? (y) y
npm warn deprecated @modelcontextprotocol/server-legacy@2.0.0: This package is a frozen copy of v1's SSE transport and OAuth Authorization Server helpers for migration purposes only. Use StreamableHTTP from @modelcontextprotocol/server and a dedicated OAuth server in production. Will not receive new features.

This server list was launched with --config or an ad-hoc server and can't be edited here. Changes won't be saved. Use --catalog (or no flag) to manage a writable catalog.
Servers

uv

Disconnected
STDIO

Standard I/O

uv run --with mcp==2.0.0 mcp run demo.py
