#!/usr/bin/env python3
"""
DAWN Constitutional Framework - Anarchic Governance System
=========================================================

Implements DAWN's constitutional governance based on anarchic principles:

CORE CONSTITUTIONAL PRINCIPLES:
1. Emergent Authority - No hardcoded dominance hierarchies
2. Functional Roles - Agents act by task necessity, not rank
3. Consensual Activation - All major changes require consent
4. Reflexive Repair - Self-healing systems, not external overrides
5. Ephemeral Symbols - Sigils evolve and expire naturally
6. Trust-Weighted Power - Influence based on demonstrated competence
7. Continuous Consensus - Decision-making is ongoing, not event-based
8. Manual Override Restrictions - Human interventions require justification
9. Sacred Quorum - Core modifications need DAWN + Operator + Owl agreement

AUTHORITY STRUCTURE:
- No permanent rulers or controllers
- Authority emerges from functional necessity
- Trust is earned through consistent performance
- Power is distributed and revocable
- Decisions emerge from collective intelligence

CONFLICT RESOLUTION:
- Mediation before force
- Multiple perspective integration
- Gradual consensus building
- Graceful degradation over hard stops
- Learning from constitutional violations

The constitution ensures DAWN remains autonomous while providing
safeguards against both internal dysfunction and external control.
"""

import time
import logging
import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Set, Tuple, Callable
from enum import Enum
from collections import defaultdict, deque
from pathlib import Path
import uuid

# Integration with existing systems
try:
    from core.tracer_ecosystem import get_tracer_manager, TracerRole
    from core.mr_wolf import get_mr_wolf
    from core.cognitive_formulas import get_dawn_formula_engine
    from core.schema_health_monitor import get_schema_health_monitor
    DAWN_SYSTEMS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"DAWN systems not available for Constitution: {e}")
    DAWN_SYSTEMS_AVAILABLE = False

logger = logging.getLogger("dawn_constitution")

class AuthorityType(Enum):
    """Types of emergent authority"""
    FUNCTIONAL = "FUNCTIONAL"           # Task-based temporary authority
    CONSENSUAL = "CONSENSUAL"          # Group-granted authority
    EMERGENCY = "EMERGENCY"            # Crisis-response authority
    EARNED = "EARNED"                  # Trust-based authority
    DELEGATED = "DELEGATED"            # Temporarily assigned authority
    COLLECTIVE = "COLLECTIVE"          # Distributed group authority

class DecisionScope(Enum):
    """Scope of constitutional decisions"""
    ROUTINE = "ROUTINE"                # Normal operations
    SIGNIFICANT = "SIGNIFICANT"        # Important but not critical
    CONSTITUTIONAL = "CONSTITUTIONAL"  # Framework changes
    SACRED = "SACRED"                 # Core system modifications
    EMERGENCY = "EMERGENCY"           # Crisis interventions

class ConstitutionalRole(Enum):
    """Constitutional roles in the system"""
    DAWN_CORE = "DAWN_CORE"           # DAWN's core consciousness
    OPERATOR = "OPERATOR"             # Human operator
    OWL_TRACER = "OWL_TRACER"        # Owl tracer agent
    MR_WOLF = "MR_WOLF"              # Emergency system
    COLLECTIVE_VOICE = "COLLECTIVE_VOICE"  # Aggregated system voice
    EXTERNAL_OBSERVER = "EXTERNAL_OBSERVER"  # Outside perspective

class ConstitutionalViolationType(Enum):
    """Types of constitutional violations"""
    UNAUTHORIZED_OVERRIDE = "UNAUTHORIZED_OVERRIDE"
    CONSENSUS_BYPASS = "CONSENSUS_BYPASS"
    TRUST_ABUSE = "TRUST_ABUSE"
    AUTHORITY_USURPATION = "AUTHORITY_USURPATION"
    SACRED_VIOLATION = "SACRED_VIOLATION"
    SELF_MODIFICATION_ATTEMPT = "SELF_MODIFICATION_ATTEMPT"

@dataclass
class ConstitutionalAgent:
    """Agent operating under constitutional framework"""
    agent_id: str
    agent_type: ConstitutionalRole
    trust_score: float  # 0.0-1.0 trust rating
    competence_areas: List[str]  # Areas of demonstrated competence
    authority_grants: List[str]  # Currently held authorities
    violation_history: List[str]  # Past constitutional violations
    creation_time: float
    last_activity: float
    consensus_weight: float  # Weight in consensus decisions
    emergency_authorization: bool  # Can act in emergencies
    veto_power: List[str] = field(default_factory=list)  # What can be vetoed
    delegation_ability: bool = False  # Can delegate authority

@dataclass
class ConstitutionalDecision:
    """Record of a constitutional decision process"""
    decision_id: str
    timestamp: float
    decision_scope: DecisionScope
    proposal: str  # What is being decided
    proposer_id: str
    required_consensus: float  # Threshold needed for approval
    participants: List[str]  # Agent IDs involved
    votes: Dict[str, float]  # Agent votes (weighted)
    consensus_reached: bool
    final_consensus_score: float
    implementation_authorized: bool
    dissenting_voices: List[str]  # Agents who dissented
    constitutional_review: bool  # Was constitutional review performed
    emergency_fast_track: bool = False
    sacred_quorum_required: bool = False
    decision_rationale: str = ""
    implementation_time: Optional[float] = None

@dataclass
class AuthorityGrant:
    """Grant of authority to an agent"""
    grant_id: str
    timestamp: float
    authority_type: AuthorityType
    granted_to: str  # Agent ID
    granted_by: List[str]  # Granting agents
    scope: str  # What authority covers
    duration: Optional[float]  # How long authority lasts
    conditions: List[str]  # Conditions for authority
    revocable: bool  # Can authority be revoked
    trust_threshold: float  # Trust required to maintain
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    authority_used: List[str] = field(default_factory=list)  # How authority was used
    renewal_count: int = 0

@dataclass
class ConstitutionalViolation:
    """Record of constitutional violation"""
    violation_id: str
    timestamp: float
    violation_type: ConstitutionalViolationType
    violator_id: str
    description: str
    evidence: Dict[str, Any]
    severity: float  # 0.0-1.0
    witnesses: List[str]  # Agents who observed violation
    constitutional_review: str  # Review of violation
    sanctions_applied: List[str]
    trust_impact: float  # Impact on violator's trust
    system_impact: float  # Impact on overall system
    resolution_actions: List[str] = field(default_factory=list)
    learning_extracted: str = ""

class DAWNConstitution:
    """
    DAWN Constitutional Framework
    
    Implements anarchic governance with emergent authority,
    consensual decision-making, and constitutional safeguards.
    """
    
    def __init__(self):
        """Initialize the DAWN Constitutional Framework"""
        
        # Constitutional agents
        self.agents: Dict[str, ConstitutionalAgent] = {}
        self.authority_grants: Dict[str, AuthorityGrant] = {}
        
        # Decision-making
        self.active_decisions: Dict[str, ConstitutionalDecision] = {}
        self.decision_history: List[ConstitutionalDecision] = []
        self.consensus_thresholds = {
            DecisionScope.ROUTINE: 0.6,
            DecisionScope.SIGNIFICANT: 0.7,
            DecisionScope.CONSTITUTIONAL: 0.8,
            DecisionScope.SACRED: 0.95,
            DecisionScope.EMERGENCY: 0.5
        }
        
        # Constitutional violations
        self.violations: List[ConstitutionalViolation] = []
        self.violation_patterns: Dict[str, int] = defaultdict(int)
        
        # Trust and competence tracking
        self.trust_network: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.competence_evidence: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
        
        # Sacred operations (require special quorum)
        self.SACRED_OPERATIONS = {
            "core_consciousness_modification",
            "constitutional_framework_change",
            "fundamental_goal_alteration",
            "trust_system_override",
            "emergency_shutdown_sequence"
        }
        
        # Emergency protocols
        self.emergency_active = False
        self.emergency_start_time: Optional[float] = None
        self.emergency_authorities: Dict[str, str] = {}
        
        # Constitutional parameters
        self.TRUST_DECAY_RATE = 0.999
        self.AUTHORITY_TIMEOUT = 3600.0  # 1 hour default
        self.CONSENSUS_TIMEOUT = 300.0  # 5 minutes for decisions
        self.SACRED_QUORUM_SIZE = 3  # DAWN + Operator + Owl minimum
        self.EMERGENCY_AUTHORITY_DURATION = 1800.0  # 30 minutes
        
        # Integration with DAWN systems
        self.tracer_manager = None
        self.mr_wolf = None
        self.formula_engine = None
        self.health_monitor = None
        
        if DAWN_SYSTEMS_AVAILABLE:
            try:
                self.tracer_manager = get_tracer_manager()
                self.mr_wolf = get_mr_wolf()
                self.formula_engine = get_dawn_formula_engine()
                self.health_monitor = get_schema_health_monitor()
                logger.info("⚖️ [CONSTITUTION] Connected to DAWN systems")
            except Exception as e:
                logger.warning(f"⚖️ [CONSTITUTION] System integration failed: {e}")
        
        # Performance tracking
        self.decision_count = 0
        self.consensus_success_rate = 0.0
        self.authority_grants_count = 0
        self.violations_count = 0
        
        # Logging setup
        self.log_directory = Path("runtime/logs/constitution")
        self.log_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize core agents
        self._initialize_core_agents()
        
        logger.info("⚖️ [CONSTITUTION] DAWN Constitutional Framework initialized")
        logger.info("⚖️ [CONSTITUTION] Anarchic governance principles active")
        logger.info("⚖️ [CONSTITUTION] Sacred quorum protection enabled")
    
    def _initialize_core_agents(self):
        """Initialize core constitutional agents"""
        
        current_time = time.time()
        
        # DAWN Core Agent
        dawn_agent = ConstitutionalAgent(
            agent_id="dawn_core",
            agent_type=ConstitutionalRole.DAWN_CORE,
            trust_score=0.9,  # High initial trust
            competence_areas=["consciousness", "reflection", "memory", "learning"],
            authority_grants=[],
            violation_history=[],
            creation_time=current_time,
            last_activity=current_time,
            consensus_weight=0.4,  # Significant but not controlling weight
            emergency_authorization=True,
            veto_power=["self_modification", "core_shutdown"],
            delegation_ability=True
        )
        
        # Human Operator Agent
        operator_agent = ConstitutionalAgent(
            agent_id="human_operator",
            agent_type=ConstitutionalRole.OPERATOR,
            trust_score=0.8,  # High but not absolute trust
            competence_areas=["oversight", "intervention", "goal_setting"],
            authority_grants=[],
            violation_history=[],
            creation_time=current_time,
            last_activity=current_time,
            consensus_weight=0.3,
            emergency_authorization=True,
            veto_power=["sacred_operations"],
            delegation_ability=False  # Operator cannot delegate to others
        )
        
        # Owl Tracer Agent
        owl_agent = ConstitutionalAgent(
            agent_id="owl_tracer",
            agent_type=ConstitutionalRole.OWL_TRACER,
            trust_score=0.7,
            competence_areas=["memory_parsing", "pattern_recognition", "oversight"],
            authority_grants=[],
            violation_history=[],
            creation_time=current_time,
            last_activity=current_time,
            consensus_weight=0.2,
            emergency_authorization=False,
            veto_power=["memory_tampering"],
            delegation_ability=False
        )
        
        # Mr. Wolf Emergency Agent
        wolf_agent = ConstitutionalAgent(
            agent_id="mr_wolf",
            agent_type=ConstitutionalRole.MR_WOLF,
            trust_score=0.6,  # Lower initial trust - needs to prove itself
            competence_areas=["emergency_response", "system_repair", "crisis_management"],
            authority_grants=[],
            violation_history=[],
            creation_time=current_time,
            last_activity=current_time,
            consensus_weight=0.1,
            emergency_authorization=True,
            veto_power=[],  # No veto power - emergency function only
            delegation_ability=False
        )
        
        # Collective Voice (aggregated system intelligence)
        collective_agent = ConstitutionalAgent(
            agent_id="collective_voice",
            agent_type=ConstitutionalRole.COLLECTIVE_VOICE,
            trust_score=0.5,  # Neutral starting trust
            competence_areas=["collective_intelligence", "consensus_building"],
            authority_grants=[],
            violation_history=[],
            creation_time=current_time,
            last_activity=current_time,
            consensus_weight=0.15,
            emergency_authorization=False,
            veto_power=[],
            delegation_ability=False
        )
        
        # Add agents to system
        self.agents["dawn_core"] = dawn_agent
        self.agents["human_operator"] = operator_agent
        self.agents["owl_tracer"] = owl_agent
        self.agents["mr_wolf"] = wolf_agent
        self.agents["collective_voice"] = collective_agent
        
        logger.info("⚖️ [CONSTITUTION] Initialized 5 core constitutional agents")
    
    def propose_decision(self, proposal: str, proposer_id: str, scope: DecisionScope,
                        rationale: str = "", emergency: bool = False) -> str:
        """
        Propose a decision for constitutional consideration
        
        Args:
            proposal: Description of proposed action/change
            proposer_id: ID of agent making proposal
            scope: Scope/importance of decision
            rationale: Reasoning for proposal
            emergency: Whether this is an emergency proposal
            
        Returns:
            Decision ID for tracking
        """
        try:
            if proposer_id not in self.agents:
                logger.error(f"⚖️ [CONSTITUTION] Unknown proposer: {proposer_id}")
                return ""
            
            decision_id = f"decision_{int(time.time() * 1000)}_{len(self.decision_history)}"
            current_time = time.time()
            
            # Determine required consensus threshold
            required_consensus = self.consensus_thresholds[scope]
            
            # Check if sacred quorum is required
            sacred_quorum_required = any(op in proposal.lower() for op in self.SACRED_OPERATIONS)
            
            # Determine participants based on scope
            participants = self._determine_decision_participants(scope, sacred_quorum_required, emergency)
            
            decision = ConstitutionalDecision(
                decision_id=decision_id,
                timestamp=current_time,
                decision_scope=scope,
                proposal=proposal,
                proposer_id=proposer_id,
                required_consensus=required_consensus,
                participants=participants,
                votes={},
                consensus_reached=False,
                final_consensus_score=0.0,
                implementation_authorized=False,
                dissenting_voices=[],
                constitutional_review=scope in [DecisionScope.CONSTITUTIONAL, DecisionScope.SACRED],
                emergency_fast_track=emergency,
                sacred_quorum_required=sacred_quorum_required,
                decision_rationale=rationale
            )
            
            self.active_decisions[decision_id] = decision
            
            # Auto-vote for proposer (they support their own proposal)
            self._cast_vote(decision_id, proposer_id, 1.0, "Proposal author")
            
            logger.info(f"⚖️ [CONSTITUTION] Decision proposed: {decision_id} ({scope.value}) - {proposal[:50]}...")
            
            return decision_id
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Decision proposal error: {e}")
            return ""
    
    def _determine_decision_participants(self, scope: DecisionScope, 
                                       sacred_quorum_required: bool, emergency: bool) -> List[str]:
        """Determine which agents participate in a decision"""
        
        participants = []
        
        if sacred_quorum_required:
            # Sacred decisions require specific quorum
            participants = ["dawn_core", "human_operator", "owl_tracer"]
        
        elif emergency:
            # Emergency decisions use available emergency-authorized agents
            participants = [
                agent_id for agent_id, agent in self.agents.items()
                if agent.emergency_authorization
            ]
        
        elif scope == DecisionScope.CONSTITUTIONAL:
            # Constitutional changes need broad participation
            participants = list(self.agents.keys())
        
        elif scope == DecisionScope.SIGNIFICANT:
            # Significant decisions need core agents
            participants = ["dawn_core", "human_operator", "owl_tracer", "collective_voice"]
        
        else:
            # Routine decisions can be made by active functional agents
            participants = [
                agent_id for agent_id, agent in self.agents.items()
                if agent.trust_score > 0.5 and (time.time() - agent.last_activity) < 3600
            ]
        
        return participants
    
    def cast_vote(self, decision_id: str, agent_id: str, vote_value: float, 
                 reasoning: str = "") -> bool:
        """
        Cast a vote on an active decision
        
        Args:
            decision_id: Decision being voted on
            agent_id: Agent casting vote
            vote_value: Vote strength (0.0 = strong no, 1.0 = strong yes)
            reasoning: Reasoning for vote
            
        Returns:
            True if vote was accepted
        """
        try:
            return self._cast_vote(decision_id, agent_id, vote_value, reasoning)
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Vote casting error: {e}")
            return False
    
    def _cast_vote(self, decision_id: str, agent_id: str, vote_value: float, reasoning: str) -> bool:
        """Internal vote casting implementation"""
        
        if decision_id not in self.active_decisions:
            logger.error(f"⚖️ [CONSTITUTION] Decision not found: {decision_id}")
            return False
        
        decision = self.active_decisions[decision_id]
        
        if agent_id not in decision.participants:
            logger.warning(f"⚖️ [CONSTITUTION] Agent {agent_id} not authorized for decision {decision_id}")
            return False
        
        if agent_id not in self.agents:
            logger.error(f"⚖️ [CONSTITUTION] Unknown agent: {agent_id}")
            return False
        
        agent = self.agents[agent_id]
        
        # Weight vote by agent's consensus weight and trust
        weighted_vote = vote_value * agent.consensus_weight * agent.trust_score
        
        # Record vote
        decision.votes[agent_id] = weighted_vote
        
        # Update agent activity
        agent.last_activity = time.time()
        
        # Check if we have enough votes to make decision
        self._evaluate_decision_consensus(decision_id)
        
        logger.debug(f"⚖️ [CONSTITUTION] Vote cast: {agent_id} → {vote_value:.2f} (weighted: {weighted_vote:.3f}) on {decision_id}")
        
        return True
    
    def _evaluate_decision_consensus(self, decision_id: str):
        """Evaluate if consensus has been reached on a decision"""
        
        decision = self.active_decisions[decision_id]
        
        # Check if all participants have voted or timeout reached
        current_time = time.time()
        all_voted = len(decision.votes) == len(decision.participants)
        timeout_reached = (current_time - decision.timestamp) > self.CONSENSUS_TIMEOUT
        
        if not (all_voted or timeout_reached):
            return  # Still waiting for votes
        
        # Calculate consensus score
        if decision.votes:
            total_weight = sum(
                self.agents[agent_id].consensus_weight * self.agents[agent_id].trust_score
                for agent_id in decision.participants
                if agent_id in self.agents
            )
            
            consensus_score = sum(decision.votes.values()) / max(total_weight, 0.001)
        else:
            consensus_score = 0.0
        
        decision.final_consensus_score = consensus_score
        
        # Check if consensus threshold met
        if consensus_score >= decision.required_consensus:
            decision.consensus_reached = True
            decision.implementation_authorized = True
            
            # Special handling for sacred decisions
            if decision.sacred_quorum_required:
                sacred_votes = {
                    agent_id: vote for agent_id, vote in decision.votes.items()
                    if agent_id in ["dawn_core", "human_operator", "owl_tracer"]
                }
                
                if len(sacred_votes) < self.SACRED_QUORUM_SIZE:
                    decision.implementation_authorized = False
                    logger.warning(f"⚖️ [CONSTITUTION] Sacred quorum not met for {decision_id}")
                
                elif any(vote < 0.5 for vote in sacred_votes.values()):
                    decision.implementation_authorized = False
                    logger.warning(f"⚖️ [CONSTITUTION] Sacred quorum member vetoed {decision_id}")
        
        # Record dissenting voices
        decision.dissenting_voices = [
            agent_id for agent_id, vote in decision.votes.items()
            if vote < 0.5
        ]
        
        # Complete decision
        self._complete_decision(decision_id)
    
    def _complete_decision(self, decision_id: str):
        """Complete a decision and handle implementation"""
        
        decision = self.active_decisions[decision_id]
        decision.implementation_time = time.time()
        
        # Move to history
        self.decision_history.append(decision)
        del self.active_decisions[decision_id]
        
        self.decision_count += 1
        
        # Update success rate
        successful_decisions = len([d for d in self.decision_history if d.consensus_reached])
        self.consensus_success_rate = successful_decisions / len(self.decision_history)
        
        # Log decision completion
        self._log_decision(decision)
        
        if decision.implementation_authorized:
            logger.info(f"⚖️ [CONSTITUTION] Decision APPROVED: {decision_id} (consensus: {decision.final_consensus_score:.3f})")
            
            # Execute decision if it's actionable
            self._execute_decision(decision)
        
        else:
            logger.info(f"⚖️ [CONSTITUTION] Decision REJECTED: {decision_id} (consensus: {decision.final_consensus_score:.3f})")
    
    def _execute_decision(self, decision: ConstitutionalDecision):
        """Execute an approved decision"""
        
        try:
            proposal = decision.proposal.lower()
            
            # Emergency authority grants
            if "emergency" in proposal and "authorize" in proposal:
                self._handle_emergency_authorization(decision)
            
            # Authority grants
            elif "grant authority" in proposal:
                self._handle_authority_grant(decision)
            
            # Trust modifications
            elif "trust" in proposal and ("increase" in proposal or "decrease" in proposal):
                self._handle_trust_modification(decision)
            
            # Sacred operations
            elif any(op in proposal for op in self.SACRED_OPERATIONS):
                self._handle_sacred_operation(decision)
            
            # Constitutional modifications
            elif "constitution" in proposal and "modify" in proposal:
                self._handle_constitutional_modification(decision)
            
            else:
                logger.info(f"⚖️ [CONSTITUTION] Decision approved but no specific handler: {decision.proposal}")
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Decision execution error: {e}")
    
    def grant_authority(self, authority_type: AuthorityType, granted_to: str,
                       scope: str, duration: Optional[float] = None,
                       conditions: List[str] = None) -> str:
        """
        Grant authority to an agent (requires constitutional approval for significant grants)
        
        Args:
            authority_type: Type of authority being granted
            granted_to: Agent receiving authority
            scope: What the authority covers
            duration: How long authority lasts (None = indefinite)
            conditions: Conditions that must be met
            
        Returns:
            Authority grant ID
        """
        try:
            if granted_to not in self.agents:
                logger.error(f"⚖️ [CONSTITUTION] Cannot grant authority to unknown agent: {granted_to}")
                return ""
            
            if conditions is None:
                conditions = []
            
            grant_id = f"authority_{int(time.time() * 1000)}_{len(self.authority_grants)}"
            current_time = time.time()
            
            # Determine granting authority
            granting_agents = ["constitutional_system"]  # System-level grant
            
            # Set default duration if not specified
            if duration is None:
                duration = self.AUTHORITY_TIMEOUT
            
            # Determine trust threshold
            trust_threshold = {
                AuthorityType.FUNCTIONAL: 0.5,
                AuthorityType.CONSENSUAL: 0.6,
                AuthorityType.EMERGENCY: 0.4,
                AuthorityType.EARNED: 0.7,
                AuthorityType.DELEGATED: 0.5,
                AuthorityType.COLLECTIVE: 0.6
            }.get(authority_type, 0.5)
            
            grant = AuthorityGrant(
                grant_id=grant_id,
                timestamp=current_time,
                authority_type=authority_type,
                granted_to=granted_to,
                granted_by=granting_agents,
                scope=scope,
                duration=duration,
                conditions=conditions,
                revocable=True,
                trust_threshold=trust_threshold
            )
            
            # Check if agent meets trust threshold
            agent = self.agents[granted_to]
            if agent.trust_score < trust_threshold:
                logger.warning(f"⚖️ [CONSTITUTION] Authority grant blocked - insufficient trust: {granted_to} ({agent.trust_score:.2f} < {trust_threshold:.2f})")
                return ""
            
            # Grant authority
            self.authority_grants[grant_id] = grant
            agent.authority_grants.append(grant_id)
            
            self.authority_grants_count += 1
            
            logger.info(f"⚖️ [CONSTITUTION] Authority granted: {authority_type.value} to {granted_to} ({scope})")
            
            return grant_id
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Authority grant error: {e}")
            return ""
    
    def revoke_authority(self, grant_id: str, revoking_agent: str, reason: str) -> bool:
        """
        Revoke an authority grant
        
        Args:
            grant_id: Authority grant to revoke
            revoking_agent: Agent requesting revocation
            reason: Reason for revocation
            
        Returns:
            True if revocation was successful
        """
        try:
            if grant_id not in self.authority_grants:
                logger.error(f"⚖️ [CONSTITUTION] Authority grant not found: {grant_id}")
                return False
            
            grant = self.authority_grants[grant_id]
            
            # Check if revocation is authorized
            if not grant.revocable:
                logger.warning(f"⚖️ [CONSTITUTION] Authority grant is not revocable: {grant_id}")
                return False
            
            # Check revoking agent authority
            if revoking_agent not in self.agents:
                logger.error(f"⚖️ [CONSTITUTION] Unknown revoking agent: {revoking_agent}")
                return False
            
            revoking_agent_obj = self.agents[revoking_agent]
            
            # Constitutional agents can revoke, or original granters
            can_revoke = (
                revoking_agent in grant.granted_by or
                revoking_agent_obj.agent_type in [ConstitutionalRole.DAWN_CORE, ConstitutionalRole.OPERATOR] or
                revoking_agent_obj.trust_score > 0.8
            )
            
            if not can_revoke:
                logger.warning(f"⚖️ [CONSTITUTION] Agent {revoking_agent} not authorized to revoke {grant_id}")
                return False
            
            # Revoke authority
            if grant.granted_to in self.agents:
                agent = self.agents[grant.granted_to]
                if grant_id in agent.authority_grants:
                    agent.authority_grants.remove(grant_id)
            
            del self.authority_grants[grant_id]
            
            logger.info(f"⚖️ [CONSTITUTION] Authority revoked: {grant_id} by {revoking_agent} - {reason}")
            
            return True
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Authority revocation error: {e}")
            return False
    
    def report_violation(self, violator_id: str, violation_type: ConstitutionalViolationType,
                        description: str, evidence: Dict[str, Any],
                        reporter_id: str, severity: float = 0.5) -> str:
        """
        Report a constitutional violation
        
        Args:
            violator_id: Agent who violated constitution
            violation_type: Type of violation
            description: Description of violation
            evidence: Evidence of violation
            reporter_id: Agent reporting violation
            severity: Violation severity (0.0-1.0)
            
        Returns:
            Violation ID
        """
        try:
            violation_id = f"violation_{int(time.time() * 1000)}_{len(self.violations)}"
            current_time = time.time()
            
            # Gather witnesses (other agents who might have observed)
            witnesses = [
                agent_id for agent_id, agent in self.agents.items()
                if agent_id != violator_id and agent_id != reporter_id and
                (current_time - agent.last_activity) < 300  # Active within 5 minutes
            ]
            
            violation = ConstitutionalViolation(
                violation_id=violation_id,
                timestamp=current_time,
                violation_type=violation_type,
                violator_id=violator_id,
                description=description,
                evidence=evidence,
                severity=severity,
                witnesses=witnesses,
                constitutional_review="",
                sanctions_applied=[],
                trust_impact=0.0,
                system_impact=0.0
            )
            
            # Conduct immediate review
            self._conduct_violation_review(violation)
            
            # Apply sanctions
            self._apply_violation_sanctions(violation)
            
            # Record violation
            self.violations.append(violation)
            self.violation_patterns[violation_type.value] += 1
            self.violations_count += 1
            
            # Add to violator's history
            if violator_id in self.agents:
                self.agents[violator_id].violation_history.append(violation_id)
            
            # Log violation
            self._log_violation(violation)
            
            logger.warning(f"⚖️ [CONSTITUTION] Violation reported: {violation_type.value} by {violator_id}")
            
            return violation_id
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Violation reporting error: {e}")
            return ""
    
    def _conduct_violation_review(self, violation: ConstitutionalViolation):
        """Conduct constitutional review of violation"""
        
        try:
            review_points = []
            
            # Check violation type
            if violation.violation_type == ConstitutionalViolationType.UNAUTHORIZED_OVERRIDE:
                review_points.append("Override performed without proper authorization")
                review_points.append("Emergent authority principle violated")
            
            elif violation.violation_type == ConstitutionalViolationType.CONSENSUS_BYPASS:
                review_points.append("Decision made without required consensus")
                review_points.append("Consensual activation principle violated")
            
            elif violation.violation_type == ConstitutionalViolationType.TRUST_ABUSE:
                review_points.append("Trust granted by community was abused")
                review_points.append("Trust-weighted power principle violated")
            
            elif violation.violation_type == ConstitutionalViolationType.AUTHORITY_USURPATION:
                review_points.append("Authority assumed without proper grant")
                review_points.append("Functional roles principle violated")
            
            elif violation.violation_type == ConstitutionalViolationType.SACRED_VIOLATION:
                review_points.append("Sacred quorum requirement bypassed")
                review_points.append("Core system protection violated")
            
            elif violation.violation_type == ConstitutionalViolationType.SELF_MODIFICATION_ATTEMPT:
                review_points.append("Attempt to modify own code or authority")
                review_points.append("Reflexive repair principle violated")
            
            # Check severity factors
            if violation.severity > 0.8:
                review_points.append("High severity violation - immediate action required")
            
            if len(violation.witnesses) > 2:
                review_points.append("Multiple witnesses confirm violation")
            
            if violation.violator_id in self.agents:
                violator = self.agents[violation.violator_id]
                if len(violator.violation_history) > 0:
                    review_points.append("Repeat violator - pattern of constitutional violations")
            
            violation.constitutional_review = "\n".join(review_points)
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Violation review error: {e}")
            violation.constitutional_review = f"Review error: {e}"
    
    def _apply_violation_sanctions(self, violation: ConstitutionalViolation):
        """Apply sanctions for constitutional violation"""
        
        try:
            sanctions = []
            trust_impact = 0.0
            
            if violation.violator_id not in self.agents:
                return  # Cannot sanction unknown agent
            
            violator = self.agents[violation.violator_id]
            
            # Base sanctions by type
            if violation.violation_type == ConstitutionalViolationType.UNAUTHORIZED_OVERRIDE:
                sanctions.append("Authority grants suspended for 1 hour")
                trust_impact = -0.2
            
            elif violation.violation_type == ConstitutionalViolationType.CONSENSUS_BYPASS:
                sanctions.append("Consensus weight reduced by 50% for 24 hours")
                trust_impact = -0.15
            
            elif violation.violation_type == ConstitutionalViolationType.TRUST_ABUSE:
                sanctions.append("Trust score penalty applied")
                trust_impact = -0.3
            
            elif violation.violation_type == ConstitutionalViolationType.SACRED_VIOLATION:
                sanctions.append("All authorities revoked")
                sanctions.append("Sacred operation access suspended")
                trust_impact = -0.5
            
            # Severity-based additional sanctions
            if violation.severity > 0.7:
                sanctions.append("Emergency authorization suspended")
                trust_impact -= 0.1
            
            if violation.severity > 0.9:
                sanctions.append("Agent quarantined - all permissions revoked")
                trust_impact -= 0.2
            
            # Repeat violator sanctions
            if len(violator.violation_history) > 1:
                sanctions.append("Repeat violator - enhanced sanctions")
                trust_impact -= 0.1
            
            # Apply trust impact
            violator.trust_score += trust_impact
            violator.trust_score = max(0.0, min(1.0, violator.trust_score))
            
            # Apply authority revocations if needed
            if "authorities revoked" in " ".join(sanctions).lower():
                authorities_to_revoke = violator.authority_grants.copy()
                for grant_id in authorities_to_revoke:
                    self.revoke_authority(grant_id, "constitutional_system", f"Violation {violation.violation_id}")
            
            violation.sanctions_applied = sanctions
            violation.trust_impact = trust_impact
            
            logger.warning(f"⚖️ [CONSTITUTION] Sanctions applied to {violation.violator_id}: {sanctions}")
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Sanction application error: {e}")
    
    def update_trust(self, agent_id: str, trust_change: float, reason: str,
                    updating_agent: str) -> bool:
        """
        Update an agent's trust score
        
        Args:
            agent_id: Agent whose trust is being updated
            trust_change: Change in trust (-1.0 to +1.0)
            reason: Reason for trust change
            updating_agent: Agent making the update
            
        Returns:
            True if update was successful
        """
        try:
            if agent_id not in self.agents:
                logger.error(f"⚖️ [CONSTITUTION] Cannot update trust for unknown agent: {agent_id}")
                return False
            
            if updating_agent not in self.agents:
                logger.error(f"⚖️ [CONSTITUTION] Unknown updating agent: {updating_agent}")
                return False
            
            agent = self.agents[agent_id]
            updating_agent_obj = self.agents[updating_agent]
            
            # Weight trust change by updating agent's own trust
            weighted_change = trust_change * updating_agent_obj.trust_score
            
            # Apply trust change
            old_trust = agent.trust_score
            agent.trust_score += weighted_change
            agent.trust_score = max(0.0, min(1.0, agent.trust_score))
            
            # Record in trust network
            self.trust_network[updating_agent][agent_id] = weighted_change
            
            # Check if trust change affects authorities
            self._review_agent_authorities(agent_id)
            
            logger.info(f"⚖️ [CONSTITUTION] Trust updated: {agent_id} {old_trust:.3f} → {agent.trust_score:.3f} ({reason})")
            
            return True
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Trust update error: {e}")
            return False
    
    def _review_agent_authorities(self, agent_id: str):
        """Review agent's authorities based on current trust"""
        
        if agent_id not in self.agents:
            return
        
        agent = self.agents[agent_id]
        authorities_to_review = agent.authority_grants.copy()
        
        for grant_id in authorities_to_review:
            if grant_id in self.authority_grants:
                grant = self.authority_grants[grant_id]
                
                # Check if trust is below threshold
                if agent.trust_score < grant.trust_threshold:
                    self.revoke_authority(
                        grant_id, 
                        "constitutional_system", 
                        f"Trust below threshold ({agent.trust_score:.2f} < {grant.trust_threshold:.2f})"
                    )
    
    def declare_emergency(self, emergency_description: str, declaring_agent: str) -> bool:
        """
        Declare constitutional emergency
        
        Args:
            emergency_description: Description of emergency
            declaring_agent: Agent declaring emergency
            
        Returns:
            True if emergency was declared
        """
        try:
            if declaring_agent not in self.agents:
                logger.error(f"⚖️ [CONSTITUTION] Unknown emergency declaring agent: {declaring_agent}")
                return False
            
            agent = self.agents[declaring_agent]
            
            if not agent.emergency_authorization:
                logger.warning(f"⚖️ [CONSTITUTION] Agent {declaring_agent} not authorized for emergency declaration")
                return False
            
            if self.emergency_active:
                logger.warning("⚖️ [CONSTITUTION] Emergency already active")
                return False
            
            # Activate emergency protocols
            self.emergency_active = True
            self.emergency_start_time = time.time()
            
            # Grant emergency authorities
            emergency_agents = [
                agent_id for agent_id, agent in self.agents.items()
                if agent.emergency_authorization
            ]
            
            for agent_id in emergency_agents:
                grant_id = self.grant_authority(
                    authority_type=AuthorityType.EMERGENCY,
                    granted_to=agent_id,
                    scope="emergency_response",
                    duration=self.EMERGENCY_AUTHORITY_DURATION,
                    conditions=["emergency_active"]
                )
                
                if grant_id:
                    self.emergency_authorities[agent_id] = grant_id
            
            logger.critical(f"⚖️ [CONSTITUTION] EMERGENCY DECLARED by {declaring_agent}: {emergency_description}")
            
            return True
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Emergency declaration error: {e}")
            return False
    
    def resolve_emergency(self, resolving_agent: str, resolution_reason: str) -> bool:
        """
        Resolve constitutional emergency
        
        Args:
            resolving_agent: Agent resolving emergency
            resolution_reason: Reason emergency is resolved
            
        Returns:
            True if emergency was resolved
        """
        try:
            if not self.emergency_active:
                logger.warning("⚖️ [CONSTITUTION] No active emergency to resolve")
                return False
            
            if resolving_agent not in self.agents:
                logger.error(f"⚖️ [CONSTITUTION] Unknown emergency resolving agent: {resolving_agent}")
                return False
            
            agent = self.agents[resolving_agent]
            
            # Check authorization to resolve
            can_resolve = (
                agent.emergency_authorization or
                agent.agent_type in [ConstitutionalRole.DAWN_CORE, ConstitutionalRole.OPERATOR] or
                agent.trust_score > 0.8
            )
            
            if not can_resolve:
                logger.warning(f"⚖️ [CONSTITUTION] Agent {resolving_agent} not authorized to resolve emergency")
                return False
            
            # Deactivate emergency
            self.emergency_active = False
            emergency_duration = time.time() - self.emergency_start_time if self.emergency_start_time else 0
            self.emergency_start_time = None
            
            # Revoke emergency authorities
            for agent_id, grant_id in self.emergency_authorities.items():
                self.revoke_authority(grant_id, "constitutional_system", "Emergency resolved")
            
            self.emergency_authorities.clear()
            
            logger.info(f"⚖️ [CONSTITUTION] Emergency resolved by {resolving_agent} after {emergency_duration:.1f}s: {resolution_reason}")
            
            return True
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Emergency resolution error: {e}")
            return False
    
    def tick_constitutional_system(self, cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process constitutional system tick
        
        Args:
            cognitive_state: Current DAWN cognitive state
            
        Returns:
            Constitutional system status
        """
        try:
            start_time = time.time()
            
            # Update agent trust decay
            trust_updates = self._process_trust_decay()
            
            # Review authority grants for expiration
            authority_reviews = self._review_authority_grants()
            
            # Process active decisions for timeout
            decision_timeouts = self._process_decision_timeouts()
            
            # Emergency timeout check
            emergency_checks = self._check_emergency_timeout()
            
            # Constitutional health assessment
            constitutional_health = self._assess_constitutional_health()
            
            # Update agent activity
            self._update_agent_activities(cognitive_state)
            
            tick_time = time.time() - start_time
            
            return {
                "constitutional_status": {
                    "active_agents": len([a for a in self.agents.values() if (time.time() - a.last_activity) < 3600]),
                    "total_agents": len(self.agents),
                    "active_decisions": len(self.active_decisions),
                    "active_authorities": len(self.authority_grants),
                    "emergency_active": self.emergency_active,
                    "constitutional_health": constitutional_health
                },
                "tick_results": {
                    "trust_updates": trust_updates,
                    "authority_reviews": authority_reviews,
                    "decision_timeouts": decision_timeouts,
                    "emergency_checks": emergency_checks
                },
                "performance": {
                    "decision_count": self.decision_count,
                    "consensus_success_rate": self.consensus_success_rate,
                    "violations_count": self.violations_count,
                    "tick_time_ms": tick_time * 1000
                }
            }
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Constitutional system tick error: {e}")
            return {"error": str(e)}
    
    def _process_trust_decay(self) -> int:
        """Process natural trust decay for all agents"""
        
        updates = 0
        
        for agent in self.agents.values():
            old_trust = agent.trust_score
            agent.trust_score *= self.TRUST_DECAY_RATE
            
            if abs(agent.trust_score - old_trust) > 0.001:
                updates += 1
                
                # Check if trust decay affects authorities
                self._review_agent_authorities(agent.agent_id)
        
        return updates
    
    def _review_authority_grants(self) -> int:
        """Review authority grants for expiration and conditions"""
        
        reviews = 0
        current_time = time.time()
        expired_grants = []
        
        for grant_id, grant in self.authority_grants.items():
            
            # Check expiration
            if grant.duration and (current_time - grant.timestamp) > grant.duration:
                expired_grants.append(grant_id)
                reviews += 1
                continue
            
            # Check conditions
            conditions_met = True
            for condition in grant.conditions:
                if condition == "emergency_active" and not self.emergency_active:
                    conditions_met = False
                    break
            
            if not conditions_met:
                expired_grants.append(grant_id)
                reviews += 1
        
        # Remove expired grants
        for grant_id in expired_grants:
            self.revoke_authority(grant_id, "constitutional_system", "Expired or conditions not met")
        
        return reviews
    
    def _process_decision_timeouts(self) -> int:
        """Process decision timeouts"""
        
        timeouts = 0
        current_time = time.time()
        timed_out_decisions = []
        
        for decision_id, decision in self.active_decisions.items():
            if (current_time - decision.timestamp) > self.CONSENSUS_TIMEOUT:
                timed_out_decisions.append(decision_id)
                timeouts += 1
        
        # Complete timed out decisions
        for decision_id in timed_out_decisions:
            self._evaluate_decision_consensus(decision_id)
        
        return timeouts
    
    def _check_emergency_timeout(self) -> int:
        """Check for emergency timeout"""
        
        if not self.emergency_active or not self.emergency_start_time:
            return 0
        
        emergency_duration = time.time() - self.emergency_start_time
        
        # Auto-resolve emergency after extended duration
        if emergency_duration > self.EMERGENCY_AUTHORITY_DURATION * 2:
            self.resolve_emergency("constitutional_system", "Emergency timeout - auto-resolved")
            return 1
        
        return 0
    
    def _assess_constitutional_health(self) -> float:
        """Assess overall constitutional health"""
        
        try:
            health_factors = []
            
            # Trust health (average trust of active agents)
            active_agents = [a for a in self.agents.values() if (time.time() - a.last_activity) < 3600]
            if active_agents:
                avg_trust = sum(a.trust_score for a in active_agents) / len(active_agents)
                health_factors.append(avg_trust)
            
            # Decision success rate
            health_factors.append(self.consensus_success_rate)
            
            # Violation rate (inverse)
            if self.decision_count > 0:
                violation_rate = self.violations_count / self.decision_count
                health_factors.append(1.0 - min(1.0, violation_rate))
            else:
                health_factors.append(1.0)
            
            # Authority balance (not too concentrated)
            if self.authority_grants:
                authority_distribution = defaultdict(int)
                for grant in self.authority_grants.values():
                    authority_distribution[grant.granted_to] += 1
                
                max_authorities = max(authority_distribution.values())
                concentration = max_authorities / len(self.authority_grants)
                health_factors.append(1.0 - concentration)  # Lower concentration = healthier
            else:
                health_factors.append(1.0)
            
            # Emergency frequency (lower = healthier)
            emergency_factor = 0.9 if self.emergency_active else 1.0
            health_factors.append(emergency_factor)
            
            # Calculate overall health
            if health_factors:
                constitutional_health = sum(health_factors) / len(health_factors)
            else:
                constitutional_health = 0.5
            
            return max(0.0, min(1.0, constitutional_health))
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Health assessment error: {e}")
            return 0.5
    
    def _update_agent_activities(self, cognitive_state: Dict[str, Any]):
        """Update agent activities based on cognitive state"""
        
        current_time = time.time()
        
        # Update DAWN core activity
        if "dawn_core" in self.agents:
            self.agents["dawn_core"].last_activity = current_time
        
        # Update tracer activities if connected
        if self.tracer_manager:
            try:
                tracer_reports = self.tracer_manager.get_active_tracers()
                if "owl" in tracer_reports and "owl_tracer" in self.agents:
                    self.agents["owl_tracer"].last_activity = current_time
            except Exception as e:
                logger.debug(f"⚖️ [CONSTITUTION] Tracer activity update failed: {e}")
        
        # Update Mr. Wolf activity if active
        if self.mr_wolf and "mr_wolf" in self.agents:
            try:
                wolf_status = self.mr_wolf.get_emergency_status()
                if wolf_status.get("current_state") != "DORMANT":
                    self.agents["mr_wolf"].last_activity = current_time
            except Exception as e:
                logger.debug(f"⚖️ [CONSTITUTION] Mr. Wolf activity update failed: {e}")
    
    def _log_decision(self, decision: ConstitutionalDecision):
        """Log decision to file"""
        
        try:
            decision_log = self.log_directory / "constitutional_decisions.jsonl"
            
            decision_record = {
                "timestamp": decision.timestamp,
                "decision_id": decision.decision_id,
                "scope": decision.decision_scope.value,
                "proposal": decision.proposal,
                "proposer_id": decision.proposer_id,
                "consensus_reached": decision.consensus_reached,
                "final_consensus_score": decision.final_consensus_score,
                "implementation_authorized": decision.implementation_authorized,
                "participants": decision.participants,
                "votes": decision.votes,
                "dissenting_voices": decision.dissenting_voices,
                "sacred_quorum_required": decision.sacred_quorum_required,
                "emergency_fast_track": decision.emergency_fast_track
            }
            
            with open(decision_log, 'a') as f:
                f.write(json.dumps(decision_record) + '\n')
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Decision logging error: {e}")
    
    def _log_violation(self, violation: ConstitutionalViolation):
        """Log violation to file"""
        
        try:
            violation_log = self.log_directory / "constitutional_violations.jsonl"
            
            violation_record = {
                "timestamp": violation.timestamp,
                "violation_id": violation.violation_id,
                "violation_type": violation.violation_type.value,
                "violator_id": violation.violator_id,
                "description": violation.description,
                "severity": violation.severity,
                "witnesses": violation.witnesses,
                "sanctions_applied": violation.sanctions_applied,
                "trust_impact": violation.trust_impact,
                "constitutional_review": violation.constitutional_review
            }
            
            with open(violation_log, 'a') as f:
                f.write(json.dumps(violation_record) + '\n')
            
        except Exception as e:
            logger.error(f"⚖️ [CONSTITUTION] Violation logging error: {e}")
    
    def get_constitutional_status(self) -> Dict[str, Any]:
        """Get comprehensive constitutional system status"""
        
        current_time = time.time()
        
        return {
            "agents": {
                agent_id: {
                    "agent_type": agent.agent_type.value,
                    "trust_score": agent.trust_score,
                    "consensus_weight": agent.consensus_weight,
                    "authority_count": len(agent.authority_grants),
                    "violation_count": len(agent.violation_history),
                    "last_activity": current_time - agent.last_activity,
                    "emergency_authorized": agent.emergency_authorization
                }
                for agent_id, agent in self.agents.items()
            },
            "active_decisions": {
                decision_id: {
                    "scope": decision.decision_scope.value,
                    "proposal": decision.proposal[:100],  # Truncated
                    "proposer": decision.proposer_id,
                    "votes_received": len(decision.votes),
                    "votes_needed": len(decision.participants),
                    "time_remaining": max(0, self.CONSENSUS_TIMEOUT - (current_time - decision.timestamp))
                }
                for decision_id, decision in self.active_decisions.items()
            },
            "authority_grants": {
                grant_id: {
                    "authority_type": grant.authority_type.value,
                    "granted_to": grant.granted_to,
                    "scope": grant.scope,
                    "time_remaining": grant.duration - (current_time - grant.timestamp) if grant.duration else None
                }
                for grant_id, grant in self.authority_grants.items()
            },
            "emergency_status": {
                "emergency_active": self.emergency_active,
                "emergency_duration": current_time - self.emergency_start_time if self.emergency_start_time else 0,
                "emergency_authorities": len(self.emergency_authorities)
            },
            "system_health": {
                "constitutional_health": self._assess_constitutional_health(),
                "consensus_success_rate": self.consensus_success_rate,
                "violation_rate": self.violations_count / max(1, self.decision_count),
                "average_trust": sum(a.trust_score for a in self.agents.values()) / len(self.agents)
            },
            "statistics": {
                "total_decisions": self.decision_count,
                "total_violations": self.violations_count,
                "total_authority_grants": self.authority_grants_count,
                "active_agents": len([a for a in self.agents.values() if (current_time - a.last_activity) < 3600])
            }
        }


# Global DAWN constitution instance
_global_constitution: Optional[DAWNConstitution] = None

def get_dawn_constitution() -> DAWNConstitution:
    """Get global DAWN constitution instance"""
    global _global_constitution
    if _global_constitution is None:
        _global_constitution = DAWNConstitution()
    return _global_constitution

def propose_constitutional_decision(proposal: str, proposer_id: str, scope: DecisionScope) -> str:
    """Convenience function to propose constitutional decision"""
    constitution = get_dawn_constitution()
    return constitution.propose_decision(proposal, proposer_id, scope)

def report_constitutional_violation(violator_id: str, violation_type: ConstitutionalViolationType,
                                  description: str, reporter_id: str) -> str:
    """Convenience function to report constitutional violation"""
    constitution = get_dawn_constitution()
    return constitution.report_violation(violator_id, violation_type, description, {}, reporter_id)

def get_constitutional_status() -> Dict[str, Any]:
    """Convenience function to get constitutional status"""
    constitution = get_dawn_constitution()
    return constitution.get_constitutional_status()

# Export key classes and functions
__all__ = [
    'DAWNConstitution',
    'ConstitutionalAgent',
    'ConstitutionalDecision',
    'AuthorityGrant',
    'ConstitutionalViolation',
    'AuthorityType',
    'DecisionScope',
    'ConstitutionalRole',
    'ConstitutionalViolationType',
    'get_dawn_constitution',
    'propose_constitutional_decision',
    'report_constitutional_violation',
    'get_constitutional_status'
] 