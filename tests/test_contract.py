from models import new_account
from service import calculate_points, apply_reward_event, flag_repeat_transactions


def test_points_use_floor(): assert calculate_points(19999,1)==1

def test_bonus_then_cap(): assert calculate_points(50000,2,50,6)==6

def test_negative_amount_gives_zero(): assert calculate_points(-10000,1)==0

def test_cap_zero_is_respected(): assert calculate_points(50000,1,cap_points=0)==0

def test_purchase_event_once():
    a=new_account('A'); e={'event_id':'E1','type':'purchase_captured','transaction_id':'T1','amount_paise':25000}; rules={'points_per_100_rupees':1}
    a=apply_reward_event(a,e,rules); b=apply_reward_event(a,e,rules); assert a['points_balance']==2 and b['points_balance']==2 and b['processed_event_ids']==['E1']

def test_input_account_not_mutated():
    a=new_account('A'); out=apply_reward_event(a,{'event_id':'E1','type':'purchase_captured','transaction_id':'T1','amount_paise':25000},{'points_per_100_rupees':1}); assert a['points_balance']==0 and out['points_balance']==2

def test_declined_event_does_not_award():
    out=apply_reward_event(new_account('A'),{'event_id':'E1','type':'purchase_declined','transaction_id':'T','amount_paise':25000},{'points_per_100_rupees':1}); assert out['points_balance']==0

def test_partial_refund_reverses_proportionally():
    rules={'points_per_100_rupees':1}; a=apply_reward_event(new_account('A'),{'event_id':'E1','type':'purchase_captured','transaction_id':'T','amount_paise':100000},rules); b=apply_reward_event(a,{'event_id':'E2','type':'refund_processed','transaction_id':'T','amount_paise':50000},rules); assert b['points_balance']==5 and b['transactions']['T']['reversed_points']==5

def test_invalid_or_excess_refund_ignored():
    rules={'points_per_100_rupees':1}; a=apply_reward_event(new_account('A'),{'event_id':'E1','type':'purchase_captured','transaction_id':'T','amount_paise':100000},rules)
    for amount in [-1,150000]:
        b=apply_reward_event(a,{'event_id':'E2','type':'refund_processed','transaction_id':'T','amount_paise':amount},rules); assert b['transactions']['T']['refunded_paise']==0 and b['points_balance']==10

def test_unknown_refund_safe(): assert apply_reward_event(new_account('A'),{'event_id':'E1','type':'refund_processed','transaction_id':'X','amount_paise':1000},{'points_per_100_rupees':1})['points_balance']==0

def test_repeat_group():
    rows=[{'transaction_id':str(i),'account_id':'A','date':'D','amount_paise':1000} for i in range(3)]; assert flag_repeat_transactions(rows,2)[0]['transaction_ids']==['0','1','2']

def test_different_accounts_not_grouped():
    rows=[{'transaction_id':'1','account_id':'A','date':'D','amount_paise':1000},{'transaction_id':'2','account_id':'B','date':'D','amount_paise':1000}]; assert flag_repeat_transactions(rows,1)==[]

def test_refund_replay_does_not_double_deduct():
    rules = {'points_per_100_rupees': 1}
    acc = new_account('A1')
    acc = apply_reward_event(acc, {'event_id': 'E1', 'type': 'purchase_captured', 'transaction_id': 'T1', 'amount_paise': 80000}, rules)
    refund_ev = {'event_id': 'E2', 'type': 'refund_processed', 'transaction_id': 'T1', 'amount_paise': 40000}
    acc = apply_reward_event(acc, refund_ev, rules)
    acc_again = apply_reward_event(acc, refund_ev, rules)
    assert acc_again['points_balance'] == 4
    assert acc_again['processed_event_ids'] == ['E1', 'E2']

def test_two_partial_refunds_over_limit():
    rules = {'points_per_100_rupees': 1}
    acc = new_account('A1')
    acc = apply_reward_event(acc, {'event_id': 'E1', 'type': 'purchase_captured', 'transaction_id': 'T1', 'amount_paise': 100000}, rules)
    acc = apply_reward_event(acc, {'event_id': 'E2', 'type': 'refund_processed', 'transaction_id': 'T1', 'amount_paise': 70000}, rules)
    acc = apply_reward_event(acc, {'event_id': 'E3', 'type': 'refund_processed', 'transaction_id': 'T1', 'amount_paise': 40000}, rules)
    assert acc['transactions']['T1']['refunded_paise'] == 70000
    assert acc['points_balance'] == 3

def test_bool_refund_is_ignored():
    rules = {'points_per_100_rupees': 1}
    acc = apply_reward_event(new_account('A1'), {'event_id': 'E1', 'type': 'purchase_captured', 'transaction_id': 'T1', 'amount_paise': 50000}, rules)
    acc = apply_reward_event(acc, {'event_id': 'E2', 'type': 'refund_processed', 'transaction_id': 'T1', 'amount_paise': True}, rules)
    assert acc['transactions']['T1']['refunded_paise'] == 0
    assert acc['points_balance'] == 5

def test_negative_bonus_returns_zero():
    assert calculate_points(50000, 1, bonus_percent=-10) == 0

def test_zero_threshold_in_repeats():
    txs = [{'transaction_id': 'T1', 'account_id': 'A1', 'date': '2026-10-21', 'amount_paise': 5000}]
    assert flag_repeat_transactions(txs, threshold=0) == []
