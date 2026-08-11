from typing import Dict, Any, List
from .entities import TraceStep
from .norm_matcher import NormMatcher

class InferenceEngine:
    def __init__(self, package_path: str = "packages/msu_ua"):
        self.matcher = NormMatcher(package_path)

    def process(self, verb: str, agent: str) -> Dict[str, Any]:
        cards, warnings = self.matcher.match(verb, agent)
        
        trace = [
            TraceStep(
                label=f"Norm Matching for '{verb}' ({agent})",
                matched_verb=verb,
                modality="matching",
                step_type="norm_matching"
            )
        ]
        
        return {
            "matched_cards": cards,
            "warnings": warnings,
            "trace": trace
        }
