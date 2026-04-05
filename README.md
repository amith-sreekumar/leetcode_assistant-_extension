----LeetCode Assistant----
A Chrome extension that gives you DSA hints on LeetCode without giving the full solution.

----How it works----
Open a LeetCode problem → click the extension → get 3 short hints instantly.
The extension scrapes the problem, sends it to a Flask backend, and uses Groq AI to generate hints that guide you — not solve it for you.

----Tech Stack----
Chrome Extension (Manifest V3)
Flask + Python
Groq API (llama-3.1-8b)

----Setup----
pip install flask flask-cors groq
export GROQ_API_KEY=your_key_here
python app.py
Then load the /extension folder as an unpacked extension in chrome://extensions.
