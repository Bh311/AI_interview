import re


# ✅ Strict skill dictionary (NO short noisy keywords)
SKILLS = {
    "programming": {
        "python": ["python"],
        "java": ["java"],
        "c++": ["c++"]
    },
    "web": {
        "html": ["html"],
        "css": ["css"],
        "javascript": ["javascript"],
        "react": ["react"],
        "flask": ["flask"],
        "node.js": ["node.js"],
        "express.js": ["express.js"]
    },
    "database": {
        "sql": ["sql"],
        "mysql": ["mysql"],
        "mongodb": ["mongodb"]
    },
    "ml": {
        "machine learning": ["machine learning"],
        "deep learning": ["deep learning"],
        "tensorflow": ["tensorflow"]
    },
    "tools": {
        "git": ["git"],
        "github": ["github"]
    },
    "concepts": {
        "data structures": ["data structures"],
        "algorithms": ["algorithms"]
    },
    "cloud": {
        "aws": ["aws"],
        "azure": ["azure"],
        "gcp": ["gcp", "google cloud"]
    }
}


def extract_skills(text):
    text = text.lower()
    found = {}

    for category, skills in SKILLS.items():
        matched = set()

        for skill, keywords in skills.items():
            for word in keywords:

                # 🔥 Special case for C++
                if word == "c++":
                    if "c++" in text:
                        matched.add(skill)
                        break

                # 🔥 STRICT MATCHING
                # Match full words / phrases only
                pattern = r'\b' + re.escape(word.lower()) + r'\b'

                if re.search(pattern, text):
                    matched.add(skill)
                    break

        if matched:
            found[category] = sorted(list(matched))

    return found

# 🔥 Improved extraction function
def extract_skills(text):
    text = text.lower()
    found = {}

    for category, skills in SKILLS.items():
        matched = set()

        for skill, keywords in skills.items():
            for word in keywords:

                # ⚠️ Special case for c++
                if word == "c++":
                    if "c++" in text:
                        matched.add(skill)
                        break

                # ✅ Normal regex match
                if re.search(r'\b' + re.escape(word) + r'\b', text):
                    matched.add(skill)
                    break

        # ✅ Only include non-empty categories
        if matched:
            found[category] = sorted(list(matched))

    return found