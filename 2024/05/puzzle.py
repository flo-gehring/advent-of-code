from typing import List
from functools import reduce
input = [l.strip() for l in open("2024/05/input.txt").readlines()]
line_separating_rules_and_updates = input.index("")
rules = input[:line_separating_rules_and_updates]
updates = [ [int(s) for s in line.split(",")] for line in input[line_separating_rules_and_updates+1:]]

# Initialize Rule Dict
# each page number in the rules points to a list of page numbers which need to come after it
rule_lookup = dict()
for rule in rules:
    spl = rule.split("|")
    before = int(spl[0])
    after = int(spl[1])
    if before in rule_lookup:
        rule_lookup[before].append(after)
    else:
        rule_lookup[before] = [after] 

def update_ok(update: List[int]) -> bool: 
    for (index, page) in enumerate(update):
        before = update[:index]
        needs_to_be_after = rule_lookup[page] if (page in rule_lookup)else []
        rule_broken = [
            b in needs_to_be_after for b in before
        ]
        if any(rule_broken):
            return False
    return True

ok_updates = [update for update in updates if update_ok(update)]
middle_page = [u[int(len(u) / 2)] for u in ok_updates]
print(sum(middle_page))
not_ok_updates = [update for update in updates if not update_ok(update)]

def correct(update: List[int]) -> List[int]:
    result  = update.copy()
    while not update_ok(result):
        for (index, page) in enumerate(result):
            needs_to_be_after = rule_lookup[page] if (page in rule_lookup)else []
            indices_of_after = [result.index(v) for v in needs_to_be_after if v in result]
            minimum_index = min(indices_of_after) if indices_of_after else index
            if minimum_index < index:
                result.pop(index)
                result.insert(minimum_index, page)
                break
    return result
            

corrected = [correct(update) for update in not_ok_updates]
middle_page = [u[int(len(u) / 2)] for u in corrected]
print(sum(middle_page))

