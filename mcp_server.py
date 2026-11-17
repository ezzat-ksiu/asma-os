"""
MCP Server Module for ASMA-OS Mesh Infrastructure.

Provides local server capabilities mecp tools to inspect and operate on
the specification, system components, and operational gates.
"""

from typing import Any, Dict, List
try:
    # MCP Python SDK 2.x exposes the server from this module.
    from mcp.server.mcpserver import MCPServer

    mcp = MCPServer("ASMA-OS Mesh MCP Server")
except ImportError:  # Compatibility with SDK releases that still expose FastMCP.
    try:
        from mcp.server.fastmcp import FastMCP

        mcp = FastMCP("ASMA-OS Mesh MCP Server")
    except ImportError:
        # Keep the inspectable tool functions usable in minimal installations.
        class _LocalServer:
            def tool(self, *args, **kwargs):
                return lambda fn: fn

            def run(self, *args, **kwargs):
                raise RuntimeError("Install the MCP Python SDK to run the MCP server")

        mcp = _LocalServer()
from spec_schema import (
    ASMASpec,
    Architecture,
    AuditLedger,
    BusinessArchitecture,
    ExecutionArchitecture,
    FinancialModel,
    OperationalGates,
    QualityAndSecurityArchitecture,
    ScalingPolicy,
    TechnicalArchitecture,
)

def create_spec_instance() -> ASMASpec:
    """Factory creating full ASMA-OS V6.0 Specification Instance."""
    return ASMASpec(
        business=BusinessArchitecture(
            vision="Unified Autonomous Execution Operating System",
            strategic_pillars=[
                "Self-Healing Topology",
                "Deterministic Security",
                "Zero-Trust Mesh Routing",
            ],
            operational_gates=OperationalGates(),
            financial_model=FinancialModel(),
        ),
        technical=TechnicalArchitecture(
            scaling_policy=ScalingPolicy(),
            quality_security=QualityAndSecurityArchitecture(),
            audit_ledger=AuditLedger(),
        ),
        execution=ExecutionArchitecture(),
    )


GLOBAL_SPEC: ASMASpec = create_spec_instance()


@mcp.tool()
def get_spec_summary() -> Dict[str, Any]:
    """Return high-level specification metadata and validation status."""
    return {
        "version": GLOBAL_SPEC.version,
        "vision": GLOBAL_SPEC.business.vision,
        "gates_count": len(GLOBAL_SPEC.business.operational_gates.gates),
        "pillars": GLOBAL_SPEC.business.strategic_pillars,
    }


@mcp.tool()
def get_gate_status(gate_id: str) -> Dict[str, Any]:
    """
    Retrieve details and status for a specific Operational Gate.

    Args:

        gate_id: Gate identifier (e.g., 'G0', 'G1', 'G6').
    """
    gates = GLOBAL_SPEC.business.operational_gates.gates
    if gate_id in gates:
        gate = gates[gate_id]
        return {
            "id": gate.gate_id,
            "name": gate.name,
            "description": gate.description,
            "criteria": gate.criteria,
            "status": gate.status,
        }
    return {"error": f"Gate '{gate_id}' not found."}


@mcp.tool()
def list_all_gates() -> List[Dict[str, Any]]:
    """List all configured Operational Gates and their current state."""
    return [
        {
            "id": g.gate_id,
            "name": g.name,
            "status": g.status,
            "criteria_count": len(g.criteria),
        }
        for g in GLOBAL_SPEC.business.operational_gates.gates.values()
    ]


@mcp.tool()
def get_system_health() -> Dict[str, Any]:
    """Return status of security, quality metrics, and audit ledger state."""
    sec = GLOBAL_SPEC.technical.quality_security
    ledger = GLOBAL_SPEC.technical.audit_ledger
    return {
        "unit_test_coverage_min": sec.unit_test_coverage_min,
        "security_level": sec.security_level,
        "audit_ledger_status": ledger.status,
        "ledger_entries": len(ledger.entries),
    }


if __name__ == "__main__":
    mcp.run()
