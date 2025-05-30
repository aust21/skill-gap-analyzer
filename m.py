goals = [
    "Complete a Docker & Kubernetes Course:Learn containerization and orchestration fundamentals to address the top skill gap in your profile.",
    "Build a Cloud-Based Project:Create a small project using AWS or Azure to demonstrate your cloud computing abilities."
]

parsed_goals = [
    {"title": g.split(":", 1)[0].strip(), "description": g.split(":", 1)[1].strip()}
    for g in goals
]

print(parsed_goals)
