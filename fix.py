p1 = "src/layer1_sentry/sentry.py"
s1 = open(p1, encoding="utf-8").read()
if "def __init__(self, demo_mode=False)" not in s1:
    s1 = s1.replace(
        "def __init__(self):\n        self.keystore = KeyStore()",
        "def __init__(self, demo_mode=False):\n        self.demo_mode = demo_mode\n        self.keystore = KeyStore()",
        1,
    )
    open(p1, "w", encoding="utf-8").write(s1)
    print("Fixed sentry.py")
else:
    print("sentry.py already fixed")

p2 = "src/layer5_council/dashboard.py"
s2 = open(p2, encoding="utf-8").read()
if "sys.path.insert" not in s2:
    old = '"""HYDRA-GRID Layer 5 - COUNCIL dashboard (Streamlit)."""\nimport streamlit as st'
    new = '"""HYDRA-GRID Layer 5 - COUNCIL dashboard (Streamlit)."""\nimport sys\nimport os\nsys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))\n\nimport streamlit as st'
    s2 = s2.replace(old, new, 1)
    open(p2, "w", encoding="utf-8").write(s2)
    print("Fixed dashboard.py")
else:
    print("dashboard.py already fixed")
