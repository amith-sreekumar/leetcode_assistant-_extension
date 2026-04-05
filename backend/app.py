import os
from flask import jsonify
from flask_cors import CORS
from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

keyword_hints={
    "subarray":"Try sliding window or prefix sum approach",
    "palindrome": "Two pointers from both ends usually works",
    "cycle": "Slow and fast pointer technique might help",
    "sorted": "Binary search could be applicable",
    "bst": "Inorder traversal gives sorted order",
    "maximum": "Think about greedy or DP",
    "minimum": "Check greedy or binary search on answer",
    "window": "Try a fixed or variable sliding window",
    "sum": "Prefix sum or hashmap may help",
    "k consecutive": "Classic sliding window pattern",
    "range": "Prefix sum or difference array might work",
    "reverse": "Two pointers or in-place reversal",
    "anagram": "Frequency count using hashmap",
    "substring": "Sliding window is commonly used",
    "character": "Consider frequency array or hashmap",
    "graph": "Model problem as graph",
    "connected": "DFS or BFS traversal",
    "shortest": "BFS (unweighted) or Dijkstra",
    "cycle detection": "DFS with visited states",
    "topological": "Kahn's algorithm or DFS ordering",
    "dp": "Check overlapping subproblems and optimal substructure",
    "ways": "DP counting problem",
    "maximum sum": "DP or Kadane's algorithm",
    "minimum cost": "DP with state transition",
    "longest": "DP or two pointers depending on constraints",
    "next greater": "Use monotonic stack",
    "previous smaller": "Monotonic stack pattern",
    "parentheses": "Stack-based validation",
    "expression": "Stack for operators and operands",
    "search": "Check if binary search is possible",
    "peak": "Binary search on monotonic property",
    "tree": "Decide traversal strategy (DFS/BFS)",
    "depth": "DFS or BFS level order traversal",
    "height": "Recursive bottom-up approach",
    "ancestor": "Think about LCA logic"
    }

## AI part function
def get_ai_hints(problem):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role":"system",
                    "content": """You are a DSA hint assistant. 
                            Give EXACTLY 3 hints. 
                            Each hint must be maximum 8 words.
                            No code. No explanation. No numbering. No preamble.
                            Just 3 lines, one hint per line.
                            Example output:
                            Use row index simulation
                            Track direction with a flag
                            Append characters to each row"""
                },{
                    "role":"user",
                    "content":problem
                }
            ]
        )
        result = response.choices[0].message.content
        lines =result.split("\n")

        cleaned = []
        for line in lines:
            line = line.strip()
            if line and len(line) < 100:  # ignore long lines
                line = line.lstrip("0123456789. •-`")
                if len(line.split()) <= 12:  # max ~12 words
                    cleaned.append(line)
        return cleaned[:3]


    except Exception as e:
        return ["AI is unavailable. Please try again later."]



@app.route("/", methods=["POST"])
def get_hints():
    
    data=request.get_json()         
    problem=data["problem"].lower()

    keyword_results=[]
    printed=set()

    # keyword logic
    for word,hint in keyword_hints.items():
         if word in problem and hint not in printed:
              keyword_results.append(hint)
              printed.add(hint)
    
    # AI fallback
    if not keyword_results:
        ai_response = get_ai_hints(problem)
        keyword_results.extend(ai_response)
            
    return jsonify({
         "keyword_results": keyword_results
    })

if __name__ == "__main__":
    app.run(debug=True)

