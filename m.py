def transform_skill_demands(demand_list):
    skills = []
    demands = []
    for item in demand_list:
        # Split into parts and separate the numeric demand from the skill name
        parts = item.split()
        if not parts:
            continue  # skip empty entries
        
        # The last part should be the demand number
        try:
            demand = int(parts[-1])
            skill_name = ' '.join(parts[:-1])  # all parts except last form the skill name
            skills.append(skill_name)
            demands.append(demand)
        except (ValueError, IndexError):
            # Handle cases where last part isn't a number or item is malformed
            print(f"Skipping malformed skill-demand pair: {item}")
            continue
            
    return skills, demands

    
print(transform_skill_demands(["Web APIs 55", "Python 34", "Amazon Web Services 66"]))