"""Real ML-DSA signatures are exercised; no mock identity or personhood assertions."""
import pytest
from core.pqc.ml_dsa import MLDSA65KeyPair
from core.tokenomics.dynamic_governance import DynamicAdaptabilityEngine, MacroeconomicRegime, CTX

@pytest.fixture(scope="module")
def voters():
    return {f"citizen_{i}": MLDSA65KeyPair.generate() for i in range(5)}

@pytest.fixture
def engine(voters):
    return DynamicAdaptabilityEngine({k: v.public_key_bytes for k,v in voters.items()})

def propose(engine, voters, id="P1", deadline=200):
    data = engine.proposal_payload(id, MacroeconomicRegime.RECESSION_SHOCK, "economic relief", deadline)
    sig = voters["citizen_0"].sign(data, ctx=CTX)
    return engine.propose_regime_shift(id, MacroeconomicRegime.RECESSION_SHOCK, "economic relief",
                                       "citizen_0", deadline, sig, now=100)

def vote(engine, voters, name, choice=1, proposal="P1"):
    prop=engine.regime_change_proposals[proposal]
    payload=engine.ballot_payload(proposal,prop["proposal_digest"],name,choice,prop["deadline"])
    return engine.vote_on_shift(proposal,name,choice,voters[name].sign(payload,ctx=CTX),now=150)

def test_regime_defaults(engine):
    assert engine.get_active_parameters()["flow_share_pct"] == .40

def test_signed_election_quorum(engine,voters):
    propose(engine,voters)
    for name in ["citizen_0","citizen_1","citizen_2","citizen_3"]:
        assert vote(engine,voters,name)
    vote(engine,voters,"citizen_4",-1)
    with pytest.raises(ValueError): engine.execute_regime_shift("P1",now=150)
    assert engine.execute_regime_shift("P1",now=201)
    assert engine.current_regime == MacroeconomicRegime.RECESSION_SHOCK

def test_replay_rejected(engine,voters):
    propose(engine,voters)
    vote(engine,voters,"citizen_1")
    with pytest.raises(ValueError,match="Duplicate"):vote(engine,voters,"citizen_1")

def test_unsigned_and_wrong_key_rejected(engine,voters):
    propose(engine,voters)
    with pytest.raises(PermissionError):
        engine.vote_on_shift("P1","citizen_1",1,b"invalid",now=150)
    p=engine.regime_change_proposals["P1"]
    payload=engine.ballot_payload("P1",p["proposal_digest"],"citizen_1",1,p["deadline"])
    with pytest.raises(PermissionError):
        engine.vote_on_shift("P1","citizen_1",1,voters["citizen_2"].sign(payload,ctx=CTX),now=150)

def test_no_quorum(engine,voters):
    propose(engine,voters)
    vote(engine,voters,"citizen_0")
    assert engine.execute_regime_shift("P1",now=201) is False

def test_unknown_citizen(engine,voters):
    propose(engine,voters)
    with pytest.raises(PermissionError): engine.vote_on_shift("P1","outsider",1,b"x",now=150)

def test_duplicate_proposals_and_expiry(engine,voters):
    propose(engine,voters)
    with pytest.raises(ValueError): propose(engine,voters)
    with pytest.raises(ValueError): engine.vote_on_shift("P1","citizen_2",1,b"x",now=200)

def test_registry_is_mandatory():
    with pytest.raises(ValueError): DynamicAdaptabilityEngine({})
