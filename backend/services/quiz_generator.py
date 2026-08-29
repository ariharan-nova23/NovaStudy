import uuid
from typing import List, Dict, Any

SAMPLE_QUIZ_POOL = [
    {
        "id": "qz_01",
        "question": "Which data structure is strictly used by Breadth First Search (BFS) for graph traversal?",
        "options": ["Stack", "Queue", "Priority Queue", "Array"],
        "correct_answer_index": 1,
        "explanation": "BFS uses a FIFO (First In First Out) Queue data structure to explore vertices level-by-level starting from the source vertex.",
        "hint": "Think about First-In-First-Out processing level by level.",
        "topic": "Graph Traversal",
        "unit": "Unit 4",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "id": "qz_02",
        "question": "What is the time complexity of BFS traversal on a graph represented using an Adjacency List with V vertices and E edges?",
        "options": ["O(V^2)", "O(V + E)", "O(E log V)", "O(V log E)"],
        "correct_answer_index": 1,
        "explanation": "With an Adjacency List representation, every vertex and every edge is visited once, yielding a time complexity of O(V + E).",
        "hint": "Vertices are enqueued once and adjacency lists are traversed edge by edge.",
        "topic": "Graph Traversal",
        "unit": "Unit 4",
        "difficulty": "Medium",
        "marks": 1
    },
    {
        "id": "qz_03",
        "question": "In an AVL Tree, what is the maximum permissible balance factor for any node to remain balanced?",
        "options": ["-1, 0, or +1", "-2, 0, or +2", "0 only", "-1 or +1 only"],
        "correct_answer_index": 0,
        "explanation": "An AVL tree is a height-balanced BST where the balance factor (Height(Left) - Height(Right)) of every node must be -1, 0, or +1.",
        "hint": "The height difference between left and right subtrees cannot exceed 1 in magnitude.",
        "topic": "Balanced Trees",
        "unit": "Unit 3",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "id": "qz_04",
        "question": "Which single rotation is applied to fix an AVL tree imbalance caused by an insertion into the left subtree of the left child (LL case)?",
        "options": ["Left Rotation", "Right Rotation", "Left-Right Rotation", "Right-Left Rotation"],
        "correct_answer_index": 1,
        "explanation": "For an LL imbalance (insertion in left child's left subtree), a single Right Rotation at the imbalanced node restores balance.",
        "hint": "Left-heavy subtrees are balanced by rotating in the opposite direction.",
        "topic": "Balanced Trees",
        "unit": "Unit 3",
        "difficulty": "Medium",
        "marks": 1
    },
    {
        "id": "qz_05",
        "question": "What is the worst-case time complexity of Quick Sort algorithm?",
        "options": ["O(n log n)", "O(n)", "O(n^2)", "O(log n)"],
        "correct_answer_index": 2,
        "explanation": "Quick Sort takes O(n^2) time in the worst case when the pivot chosen is consistently the smallest or largest element (e.g. sorted array).",
        "hint": "Think about choosing a bad pivot every time on an already sorted array.",
        "topic": "Sorting Algorithms",
        "unit": "Unit 5",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "id": "qz_06",
        "question": "Which sorting algorithm is guaranteed to have an O(n log n) worst-case time complexity and is Stable?",
        "options": ["Quick Sort", "Heap Sort", "Merge Sort", "Selection Sort"],
        "correct_answer_index": 2,
        "explanation": "Merge Sort uses divide-and-conquer to achieve O(n log n) worst-case time complexity and preserves the relative order of equal elements (Stable).",
        "hint": "Divide and conquer sorting algorithm that uses extra array space.",
        "topic": "Sorting Algorithms",
        "unit": "Unit 5",
        "difficulty": "Medium",
        "marks": 1
    },
    {
        "id": "qz_07",
        "question": "When converting an Infix expression to Postfix using a stack, what happens when an operator of lower or equal precedence is encountered?",
        "options": ["Push the new operator immediately", "Pop operators from stack until lower precedence is found, then push new operator", "Clear the entire stack", "Discard the operator"],
        "correct_answer_index": 1,
        "explanation": "Operators with higher or equal precedence are popped from the stack to the output before pushing the current lower-precedence operator.",
        "hint": "Higher precedence operators must execute first in postfix evaluation order.",
        "topic": "Stacks",
        "unit": "Unit 1",
        "difficulty": "Medium",
        "marks": 1
    },
    {
        "id": "qz_08",
        "question": "In a Circular Queue of size N using an array, what is the mathematical formula to increment the 'rear' index?",
        "options": ["rear = rear + 1", "rear = (rear + 1) % N", "rear = (rear + N) / 2", "rear = rear * 2 % N"],
        "correct_answer_index": 1,
        "explanation": "Modular arithmetic (rear = (rear + 1) % N) allows the queue to wrap around to index 0 when it reaches the end of the array.",
        "hint": "Use modulo arithmetic to wrap around array boundaries.",
        "topic": "Queues",
        "unit": "Unit 1",
        "difficulty": "Easy",
        "marks": 1
    },
    {
        "id": "qz_09",
        "question": "What is the single-source shortest path algorithm that works efficiently on non-negative weighted graphs?",
        "options": ["Floyd-Warshall Algorithm", "Bellman-Ford Algorithm", "Dijkstra's Algorithm", "Kruskal's Algorithm"],
        "correct_answer_index": 2,
        "explanation": "Dijkstra's algorithm uses a greedy approach with a priority queue to compute shortest paths from a single source vertex for non-negative edge weights.",
        "hint": "Greedy algorithm developed by Edsger Dijkstra.",
        "topic": "Spanning Trees & Shortest Path",
        "unit": "Unit 4",
        "difficulty": "Medium",
        "marks": 1
    },
    {
        "id": "qz_10",
        "question": "What primary data structure is utilized in Kruskal's algorithm to detect cycles efficiently when adding edges to a Minimum Spanning Tree?",
        "options": ["Adjacency Matrix", "Disjoint Set Union (DSU / Find-Union)", "Hash Table", "Binary Search Tree"],
        "correct_answer_index": 1,
        "explanation": "Kruskal's algorithm uses DSU (Disjoint Set Union) with path compression to quickly check if adding an edge connects two already connected components.",
        "hint": "Union-Find data structure with path compression.",
        "topic": "Spanning Trees & Shortest Path",
        "unit": "Unit 4",
        "difficulty": "Hard",
        "marks": 1
    }
]

class QuizGeneratorService:
    @staticmethod
    def generate_quiz(
        subject_id: str,
        quiz_mode: str = "Quick Quiz",
        num_questions: int = 10,
        difficulty: str = "Adaptive",
        target_topic: str = None
    ) -> Dict[str, Any]:
        quiz_id = f"quiz_{uuid.uuid4().hex[:8]}"

        selected = SAMPLE_QUIZ_POOL[:]
        if target_topic:
            filtered = [q for q in selected if target_topic.lower() in q["topic"].lower()]
            if filtered:
                selected = filtered

        if num_questions < len(selected):
            selected = selected[:num_questions]

        return {
            "quiz_id": quiz_id,
            "subject_id": subject_id,
            "quiz_mode": quiz_mode,
            "difficulty": difficulty,
            "num_questions": len(selected),
            "questions": selected
        }

quiz_generator_service = QuizGeneratorService()
