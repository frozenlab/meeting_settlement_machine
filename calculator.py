from dataclasses import dataclasses
import random
import hashlib
import json

class SettlementItem:
    name : str
    price : int
    shares : list[str]
    memo : str = ""

class SettlementCalculator:
    def __init__(self, people, unit=100, seed = None):
        self.people = people
        self.unit = unit
        self.rng = random.Random(seed)
        self.items = []
        self.result = {person : 0 for person in people}
        self.details = {person : [] for person in people}

    def add_item(self, item: SettlementItem):
        self.items.append(item)

    def split_item(self, item: SettlementItem):
        result = {person : 0 for person in self.people}
        details = {person : [] for person in self.people}

        share_count = len(item.shares)

        if share_count == 0:
            return result, details
        
        base = (item.price
        // share_count
        // self.unit) * self.unit

        for person in item.shares:
            result[person] += base
        
        remainder = (item.price - base * share_count)
        extra_count = (remainder // self.unit)

        if extra_count > 0:
            selected = self.rng.sample(list(set(item.shares)),
            min(extra_count, len(set(item.shares))))
            for person in selected:
                result[person] += self.unit
                details[pserson].append(
                    f"{item.name} +{self.unit:, }원"
                )
        
        return result, details
    
    def calculate(self):
        for item in self.items:
            item_result, item_detail = (self.split_item(item))
            
            for person, amount in item_result.items():
                self. result[person] += amount
            
            for person, detail_list in item_detail.items():
                self.details[person].extend(detail_list)
        
        return self.result, self.details

def generate_seed(people, items, unit):
    seed_data = {
        "people" : sorted(people),
        "unit" : unit,
        "items" : [
            {
                "name": item.name,
                "price": item.price,
                "shares": sorted(item.shares)
            }
            for item in items
        ]
    }

    seed_text = json.dumps(seed_data, ensure_ascii = False)

    return int(hashlib.sha256(seed_text.encode().hexdigest(),16))