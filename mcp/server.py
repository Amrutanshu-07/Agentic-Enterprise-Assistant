from mcp.server.fastmcp import FastMCP

mcp = FastMCP("EnterpriseContextServer")

@mcp.resource("enterprise://policies")
def enterprise_policies():
    return {
        "source": "HCLTech Annual Report 2024–25",
        "usage": "Financial, HR, AI, CSR, Strategy"
    }

@mcp.resource("enterprise://capabilities")
def enterprise_capabilities():
    return {
        "capabilities": [
            "RAG-based QA",
            "Agentic workflows",
            "Function calling",
            "PDF-grounded answers"
        ]
    }

if __name__ == "__main__":
    mcp.run()
