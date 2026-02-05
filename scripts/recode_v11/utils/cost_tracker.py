"""
API cost tracking with budget enforcement.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)


@dataclass
class CostEntry:
    """A single API cost entry."""
    timestamp: str
    provider: str
    model: str
    phase: str
    input_tokens: int
    output_tokens: int
    cost: float
    study_id: Optional[str] = None


@dataclass
class CostTracker:
    """Track API costs across the pipeline."""
    budget: float = 50.0
    warning_threshold: float = 40.0
    log_file: str = "data/recode_v11/audit/cost_log.jsonl"
    total_cost: float = 0.0
    entries: list = field(default_factory=list)

    def __post_init__(self):
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
        # Load existing entries
        if Path(self.log_file).exists():
            with open(self.log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        entry = json.loads(line)
                        self.total_cost += entry.get('cost', 0)

    def add(
        self,
        provider: str,
        model: str,
        phase: str,
        input_tokens: int,
        output_tokens: int,
        cost: float,
        study_id: Optional[str] = None
    ) -> bool:
        """
        Add a cost entry. Returns False if budget exceeded.
        """
        entry = CostEntry(
            timestamp=datetime.now().isoformat(),
            provider=provider,
            model=model,
            phase=phase,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            study_id=study_id
        )

        self.total_cost += cost
        self.entries.append(entry)

        # Write to log
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(asdict(entry)) + '\n')

        # Check budget
        if self.total_cost >= self.budget:
            logger.error(f"BUDGET EXCEEDED: ${self.total_cost:.2f} / ${self.budget:.2f}")
            return False
        elif self.total_cost >= self.warning_threshold:
            logger.warning(f"Budget warning: ${self.total_cost:.2f} / ${self.budget:.2f}")

        return True

    def get_summary(self) -> Dict:
        """Get cost summary by phase and provider."""
        summary = {
            'total_cost': self.total_cost,
            'budget': self.budget,
            'remaining': self.budget - self.total_cost,
            'by_phase': {},
            'by_provider': {},
        }

        for entry in self.entries:
            phase = entry.phase
            provider = entry.provider
            summary['by_phase'][phase] = summary['by_phase'].get(phase, 0) + entry.cost
            summary['by_provider'][provider] = summary['by_provider'].get(provider, 0) + entry.cost

        return summary

    def check_budget(self, estimated_cost: float) -> bool:
        """Check if estimated cost fits within remaining budget."""
        return (self.total_cost + estimated_cost) <= self.budget
