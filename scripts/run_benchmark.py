import sys
from pathlib import Path
import json
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to sys.path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.graph.workflow import MultiAgentWorkflow
from multi_agent_research_lab.evaluation.benchmark import run_benchmark
from multi_agent_research_lab.evaluation.report import render_markdown_report

def baseline_runner(query: str) -> ResearchState:
    state = ResearchState(request=ResearchQuery(query=query))
    client = LLMClient()
    response = client.complete("You are a helpful research assistant.", query)
    state.final_answer = response.content
    state.add_trace_event("baseline_complete", {"cost": response.cost_usd})
    # For baseline, we wrap the result in an AgentResult to make cost calculation consistent
    from multi_agent_research_lab.core.schemas import AgentResult
    state.agent_results.append(AgentResult(agent="baseline", content=response.content, metadata={"cost": response.cost_usd}))
    return state

def multi_agent_runner(query: str) -> ResearchState:
    state = ResearchState(request=ResearchQuery(query=query))
    workflow = MultiAgentWorkflow()
    return workflow.run(state)

def main():
    config_path = Path(__file__).parent.parent / "configs" / "lab_default.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    queries = config["benchmark"]["queries"]
    all_metrics = []
    trace_exports = []
    
    print(f"Starting benchmark for {len(queries)} queries...")
    
    for i, query in enumerate(queries):
        print(f"\n[Query {i+1}] {query}")
        
        # Run Baseline
        print("  Running Baseline...")
        b_state, b_metrics = run_benchmark(f"Baseline Q{i+1}", query, baseline_runner)
        all_metrics.append(b_metrics)
        trace_exports.append({
            "run_name": b_metrics.run_name,
            "query": query,
            "metrics": b_metrics.model_dump(),
            "state_trace": b_state.trace,
            "route_history": b_state.route_history,
            "agent_results": [result.model_dump(mode="json") for result in b_state.agent_results],
            "errors": b_state.errors,
        })
        
        # Run Multi-Agent
        print("  Running Multi-Agent...")
        m_state, m_metrics = run_benchmark(f"Multi-Agent Q{i+1}", query, multi_agent_runner)
        all_metrics.append(m_metrics)
        trace_exports.append({
            "run_name": m_metrics.run_name,
            "query": query,
            "metrics": m_metrics.model_dump(),
            "state_trace": m_state.trace,
            "route_history": m_state.route_history,
            "agent_results": [result.model_dump(mode="json") for result in m_state.agent_results],
            "errors": m_state.errors,
        })
    
    # Generate report
    report = render_markdown_report(all_metrics)
    output_path = Path(__file__).parent.parent / "reports" / "benchmark_report.md"
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        f.write(report)
    
    # Save JSON Traces
    trace_dir = Path(__file__).parent.parent / "reports" / "traces"
    trace_dir.mkdir(exist_ok=True, parents=True)
    trace_path = trace_dir / "benchmark_traces.json"
    with open(trace_path, "w") as f:
        json.dump(trace_exports, f, indent=2, ensure_ascii=False)
    
    print(f"\nBenchmark complete! Report saved to {output_path}")
    print(f"Trace JSON saved to {trace_path}")

if __name__ == "__main__":
    main()
