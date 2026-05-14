from enum import Enum
from typing import List

class ConsensusResult(Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    TIE = "tie"

class SwarmConsensus:
    """
    Implements a consensus algorithm for multi-agent decision making.
    Mimics Ruflo's Byzantine Fault Tolerance patterns.
    """
    def evaluate_action(self, agents_votes: List[bool]):
        """
        Simple majority consensus. 
        In real Ruflo, this would use Raft or Byzantine Fault Tolerance.
        """
        approvals = sum(1 for v in agents_votes if v)
        rejections = len(agents_votes) - approvals
        
        if approvals > rejections:
            return ConsensusResult.APPROVED
        elif rejections > approvals:
            return ConsensusResult.REJECTED
        return ConsensusResult.TIE

# Singleton instance
swarm_consensus = SwarmConsensus()
