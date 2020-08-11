#!/usr/bin/env python
# coding: utf-8

# In[202]:


import re

with open('game02.txt') as gamefile:
    chatlog = gamefile.readlines()


# In[203]:


# Petesuchos sells 2 shares IC and receives $500
# Korval receive $10 from Chicago and Western Indiana
# jjrbedford receives $30
# jjrbedford pars GT at $100
# NYC's share price changes from $80 to $70


# In[204]:


pc = r'(?P<private_company>Steamboat Company|Michigan Central|Meat Packing Company|Mail Contract|Michigan Southern|Ohio & Indiana|Lake Shore Line|Tunnel Blasting Company|Big 4|Chicago and Western Indiana)'

rr = r"(?P<railroad>PRR|NYC|B\&O|C\&O|ERIE|GT|IC)"

player = r"[^" + rr + "](?P<player>\w+)"
sr = r"(?P<sr>\d+)"
opr = r"(?P<or>\d+\.\d+)"
shares_pct = r"(?P<shares_pct>\d\d)\%"
shares_num = r"(?P<shares_num>\d)"
value = r"\$(?P<price>\d+)"

patterns = {
    "player_name": player + " chooses a company",
    "sr": r"-- Stock Round " + sr + " --",
    "or": r"-- Operating Round "+ opr + " \(of \d\) --",
    "buys_shares": player + " buys a " + shares_pct + " share of " + rr + r" from the (\w+) for " + value,
    "buys_pc": player + " buys " + pc + " for " + value,
    "sells_shares": player + " sells " + shares_num + " shares " + rr + " and receives " + value,
    "collects_pc": player + " receive " + value + " from " + pc,
    "player_receives": "^" + player + " receives " + value,
    "pars": player + " pars " + rr + " at " + value,
    "share_price_change": rr + "'s share price changes from \$\d+ to " + value
}


# In[205]:


p_player_name = re.compile(patterns["player_name"]) #
p_stock_round = re.compile(patterns["sr"]) #
p_operation_round = re.compile(patterns["or"]) #
p_buys_shares = re.compile(patterns["buys_shares"]) #
p_buys_pc = re.compile(patterns["buys_pc"]) #
p_sells_shares = re.compile(patterns["sells_shares"]) #
p_collects = re.compile(patterns["collects_pc"]) #
p_player_receives = re.compile(patterns["player_receives"]) #
p_pars = re.compile(patterns["pars"]) #
p_share_price_change = re.compile(patterns["share_price_change"])#


# In[206]:


pl = {}
rrd = {}
stkr = ""
oper = ""


# In[209]:


for line in chatlog:
    r = p_stock_round.search(line)
    if r:
        stkr = r.group("sr")
    
    r = p_operation_round.search(line)
    if r:
        oper = r.group("or")
    
    r = p_player_name.search(line)
    if r:
        pl[r.group("player")] = {
            "initial_cash_for_players": 400,
            "shares": {},
        }
        print(r.group(0))
    
    r = p_buys_pc.search(line)
    if r:
        pl[r.group("player")]["initial_cash_for_players"] -= int(r.group("price"))
    
    r = p_pars.search(line)
    if r:
        pl[r.group("player")]["shares"][r.group("railroad")] = 2
        rrd[r.group("railroad")] = int(r.group("price"))
    
    r = p_buys_shares.search(line)
    if r:
        if r.group("railroad") not in pl[r.group("player")]["shares"].keys():
            pl[r.group("player")]["shares"][r.group("railroad")] = 0
        pl[r.group("player")]["shares"][r.group("railroad")] += int(r.group("shares_pct")) // 10
        pl[r.group("player")]["initial_cash_for_players"] -= int(r.group("price"))
    
    r = p_sells_shares.search(line)
    if r:
        pl[r.group("player")]["shares"][r.group("railroad")] -= int(r.group("shares_num"))
        pl[r.group("player")]["initial_cash_for_players"] += int(r.group("price"))
        if pl[r.group("player")]["shares"][r.group("railroad")] == 0:
            pl[r.group("player")]["shares"].pop(r.group("railroad"), None)
    
    r = p_player_receives.search(line)
    if r:
        pl[r.group("player")]["initial_cash_for_players"] += int(r.group("price"))
    
    r = p_collects.search(line)
    if r:
        pl[r.group("player")]["initial_cash_for_players"] += int(r.group("price"))
    
    r = p_share_price_change.search(line)
    if r:
        rrd[r.group("railroad")] = int(r.group("price"))
    


# In[208]:


pl.items()


# In[188]:


rrd.items()


# In[ ]:




