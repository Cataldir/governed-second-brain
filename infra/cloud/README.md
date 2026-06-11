# Cloud deployment — placeholder

A real deployment adds infrastructure-as-code here: a resource group, a managed
identity, and a small always-on host for the derived index and the (gated) MCP
server. The canonical deployment this architecture mirrors uses Bicep.

It is intentionally left as a stub. The reference repository demonstrates the
*shape* of the deployment surface and its safe default (the write surface is
off until deliberately enabled), not a specific cloud configuration or bill.
