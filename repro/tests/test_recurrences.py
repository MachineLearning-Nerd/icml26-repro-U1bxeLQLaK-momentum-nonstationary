import numpy as np

from quadratic_protocol import QuadraticProtocol, target_walk
from theory_certificates import hb_transition, jump_response_time, stationary_hb_variance, theorem33_drift_term, theorem33_stability_cap


def test_source_target_walk_has_exact_fixed_step_length():
    p=QuadraticProtocol(dimension=7,horizon=19,seeds=2)
    target=target_walk(np.random.default_rng(4),p)
    assert target.shape==(20,7)
    assert np.allclose(np.linalg.norm(np.diff(target,axis=0),axis=1),p.drift)


def test_stability_cap_and_drift_floor_diverge_as_beta_increases():
    low,high=.5,.99
    assert theorem33_stability_cap(1.,1.,high)<theorem33_stability_cap(1.,1.,low)
    low_floor=theorem33_drift_term(1.,.8*theorem33_stability_cap(1.,1.,low),low,.01)
    high_floor=theorem33_drift_term(1.,.8*theorem33_stability_cap(1.,1.,high),high,.01)
    assert high_floor>1000*low_floor


def test_lyapunov_solution_matches_long_stationary_recursion():
    mu,gamma,beta,sigma2=1.,.01,.9,.8
    predicted=stationary_hb_variance(mu,gamma,beta,sigma2)
    rng=np.random.default_rng(9);x=previous=0.;samples=[]
    for t in range(300_000):
        new=x-gamma*(mu*x+rng.normal(scale=np.sqrt(sigma2)))+beta*(x-previous)
        previous,x=x,new
        if t>10_000:samples.append(x*x)
    assert abs(np.mean(samples)-predicted)/predicted<.08


def test_response_time_increases_under_stability_tuning():
    low=.5;high=.99
    t_low=jump_response_time(1.,.8*theorem33_stability_cap(1.,1.,low),low)
    t_high=jump_response_time(1.,.8*theorem33_stability_cap(1.,1.,high),high)
    assert t_high>20*t_low


def test_hb_transition_has_two_state_shape():
    A=hb_transition(1.,.05,.9)
    assert A.shape==(2,2)
    assert np.allclose(A[1],[1.,0.])


def test_stationary_control_can_accelerate_deterministic_convergence():
    """A stationary no-noise control rejects the false claim that momentum always hurts."""
    gamma,beta=.1,.5
    sgd=1.; hb=previous=1.
    for _ in range(11):
        sgd=sgd-gamma*sgd
        nxt=hb-gamma*hb+beta*(hb-previous)
        previous,hb=hb,nxt
    assert hb*hb < sgd*sgd
