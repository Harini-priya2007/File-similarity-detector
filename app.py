from flask import Flask, request, jsonify, render_template
import time

app = Flask(__name__)

# ---------------- Rabin-Karp ----------------
def rabin_karp(text, pattern, prime=101):
    m, n = len(pattern), len(text)
    d = 256
    hpattern = 0
    htext = 0
    h = pow(d, m-1) % prime
    matches = []

    # initial hash
    for i in range(m):
        hpattern = (d * hpattern + ord(pattern[i])) % prime
        htext = (d * htext + ord(text[i])) % prime

    for i in range(n - m + 1):
        if hpattern == htext:
            if text[i:i+m] == pattern:
                matches.append((i, i+m))
        if i < n - m:
            htext = (d * (htext - ord(text[i]) * h) + ord(text[i+m])) % prime
            htext = (htext + prime) % prime
    return matches

# ---------------- KMP ----------------
def kmp(text, pattern):
    m, n = len(pattern), len(text)
    lps = [0] * m
    j = 0
    matches = []

    # build LPS
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length-1]
            else:
                lps[i] = 0
                i += 1

    i = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            matches.append((i-j, i))
            j = lps[j-1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return matches

# ---------------- Similarity ----------------
def calculate_similarity(text1, text2):
    common = set(text1.split()) & set(text2.split())
    total = max(len(set(text1.split())), len(set(text2.split())))
    return round((len(common)/total)*100, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    data = request.json
    text1 = data.get("text1", "")
    text2 = data.get("text2", "")

    start_rk = time.time()
    rk_matches = rabin_karp(text1, text2[:min(50, len(text2))])  # demo: first 50 chars
    rk_time = round((time.time() - start_rk)*1000, 3)

    start_kmp = time.time()
    kmp_matches = kmp(text1, text2[:min(50, len(text2))])
    kmp_time = round((time.time() - start_kmp)*1000, 3)

    similarity = calculate_similarity(text1, text2)

    return jsonify({
        "similarity": similarity,
        "rabin_karp": {"matches": rk_matches, "time": rk_time},
        "kmp": {"matches": kmp_matches, "time": kmp_time},
        "better": "Rabin-Karp" if rk_time < kmp_time else "KMP"
    })

if __name__ == "__main__":
    app.run(debug=True)
