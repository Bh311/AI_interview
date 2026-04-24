KEYWORDS = {
    "python": ["programming", "language", "dynamic", "interpreted"],
    "java": ["oop", "class", "object", "jvm"],
    "c++": ["pointer", "memory", "oop", "compiled"],

    "html": ["structure", "web", "tags", "markup"],
    "css": ["style", "layout", "design", "flexbox"],
    "javascript": ["function", "closure", "event", "async"],
    "react": ["component", "state", "virtual dom", "hooks"],
    "flask": ["framework", "routing", "api", "server"],
    "node.js": ["runtime", "event loop", "server", "javascript"],
    "express.js": ["middleware", "routing", "server", "api"],

    "sql": ["query", "database", "join", "table"],
    "mysql": ["database", "table", "index", "query"],
    "mongodb": ["nosql", "document", "collection", "json"],

    "machine learning": ["model", "training", "data", "prediction"],
    "deep learning": ["neural network", "layers", "training", "backpropagation"],
    "tensorflow": ["library", "tensor", "model", "training"],

    "git": ["version control", "commit", "branch", "repository"],
    "github": ["repository", "pull request", "collaboration", "git"],

    "data structures": ["array", "linked list", "stack", "queue"],
    "algorithms": ["time complexity", "sorting", "searching", "logic"],
    "dsa": ["data structures", "algorithms", "problem solving"],

    "aws": ["cloud", "ec2", "s3", "services"],
    "azure": ["cloud", "services", "microsoft", "compute"],
    "gcp": ["cloud", "google", "storage", "compute"]
}



def evaluate_answers(questions, answers):
    results = []
    total_score = 0

    for q, ans in zip(questions, answers):
        score = 0
        ans_lower = ans.lower()

        # length check
        if len(ans.strip()) > 20:
            score += 1

        # keyword-based relevance
        for key, words in KEYWORDS.items():
            if key in q.lower():
                if any(w in ans_lower for w in words):
                    score += 1

        results.append({
            "question": q,
            "answer": ans,
            "score": score
        })

        total_score += score

    final_score = int((total_score / (len(questions) * 2)) * 100)

    return final_score, results