"""
Rich sample dataset for SmartExam AI.
Includes complete Syllabus, Question Papers (2022-2025), Extracted Questions,
Prediction Scores, Quizzes, and Study Plans for Data Structures & Algorithms and Operating Systems.
"""

SAMPLE_SYLLABI = {
    "dsa": {
        "subject_id": "dsa",
        "subject_name": "Data Structures & Algorithms",
        "units": [
            {
                "unit": "Unit 1",
                "title": "Arrays, Stacks & Queues",
                "topics": [
                    {"name": "Arrays & Sparse Matrices", "subtopics": ["Array Operations", "Sparse Matrix Representation"]},
                    {"name": "Stacks", "subtopics": ["Array Implementation", "Infix to Postfix", "Expression Evaluation"]},
                    {"name": "Queues", "subtopics": ["Linear Queue", "Circular Queue", "Priority Queue", "Deque"]}
                ]
            },
            {
                "unit": "Unit 2",
                "title": "Linked Lists & Memory Management",
                "topics": [
                    {"name": "Singly Linked List", "subtopics": ["Insertion & Deletion", "Reversal", "Cycle Detection"]},
                    {"name": "Doubly & Circular List", "subtopics": ["Doubly Linked List", "Circular Linked List"]},
                    {"name": "Applications of Linked List", "subtopics": ["Polynomial Addition", "Memory Allocation"]}
                ]
            },
            {
                "unit": "Unit 3",
                "title": "Trees & Binary Search Trees",
                "topics": [
                    {"name": "Trees & Traversals", "subtopics": ["Binary Tree", "Inorder, Preorder, Postorder", "Threaded Tree"]},
                    {"name": "Binary Search Trees", "subtopics": ["BST Insertion & Deletion", "BST Search Complexity"]},
                    {"name": "Balanced Trees", "subtopics": ["AVL Trees & Rotations", "Red-Black Trees", "B-Trees"]}
                ]
            },
            {
                "unit": "Unit 4",
                "title": "Graphs & Graph Algorithms",
                "topics": [
                    {"name": "Graph Representation", "subtopics": ["Adjacency Matrix", "Adjacency List"]},
                    {"name": "Graph Traversal", "subtopics": ["Breadth First Search (BFS)", "Depth First Search (DFS)"]},
                    {"name": "Spanning Trees & Shortest Path", "subtopics": ["Kruskal's Algorithm", "Prim's Algorithm", "Dijkstra's Algorithm"]}
                ]
            },
            {
                "unit": "Unit 5",
                "title": "Sorting, Searching & Hashing",
                "topics": [
                    {"name": "Searching Algorithms", "subtopics": ["Linear Search", "Binary Search"]},
                    {"name": "Sorting Algorithms", "subtopics": ["Bubble Sort", "Merge Sort", "Quick Sort", "Heap Sort"]},
                    {"name": "Hashing", "subtopics": ["Hash Functions", "Collision Resolution", "Chaining & Open Addressing"]}
                ]
            }
        ]
    },
    "os": {
        "subject_id": "os",
        "subject_name": "Operating Systems",
        "units": [
            {
                "unit": "Unit 1",
                "title": "OS Introduction & Process Management",
                "topics": [
                    {"name": "System Structure", "subtopics": ["Dual Mode", "System Calls", "OS Architecture"]},
                    {"name": "Process Management", "subtopics": ["Process Control Block (PCB)", "Process States", "Context Switch"]}
                ]
            },
            {
                "unit": "Unit 2",
                "title": "CPU Scheduling & Synchronization",
                "topics": [
                    {"name": "CPU Scheduling", "subtopics": ["FCFS", "SJF", "Round Robin", "Priority Scheduling"]},
                    {"name": "Process Synchronization", "subtopics": ["Critical Section Problem", "Semaphores", "Monitors", "Mutex"]}
                ]
            },
            {
                "unit": "Unit 3",
                "title": "Deadlocks",
                "topics": [
                    {"name": "Deadlock Fundamentals", "subtopics": ["Characterization", "Resource Allocation Graph"]},
                    {"name": "Deadlock Handling", "subtopics": ["Banker's Algorithm", "Deadlock Prevention", "Deadlock Detection"]}
                ]
            },
            {
                "unit": "Unit 4",
                "title": "Memory Management & Virtual Memory",
                "topics": [
                    {"name": "Main Memory", "subtopics": ["Paging", "Segmentation", "Fragmentation"]},
                    {"name": "Virtual Memory", "subtopics": ["Demand Paging", "Page Replacement (FIFO, LRU, Optimal)"]}
                ]
            },
            {
                "unit": "Unit 5",
                "title": "File & Storage Systems",
                "topics": [
                    {"name": "File Systems", "subtopics": ["File Allocation Methods", "Directory Structure"]},
                    {"name": "Disk Management", "subtopics": ["Disk Scheduling (FCFS, SSTF, SCAN, C-SCAN)", "RAID Levels"]}
                ]
            }
        ]
    }
}

SAMPLE_QUESTIONS = {
    "dsa": [
        # Unit 4: Graphs (High Priority)
        {
            "id": "q_dsa_01",
            "question": "Explain Breadth First Search (BFS) graph traversal algorithm with a suitable example and analyze its time and space complexity.",
            "year": 2023,
            "marks": 10,
            "unit": "Unit 4",
            "topic": "Graph Traversal",
            "subtopic": "Breadth First Search (BFS)",
            "question_type": "Algorithm",
            "difficulty": "Medium"
        },
        {
            "id": "q_dsa_02",
            "question": "Describe the BFS algorithm for graph traversal. Trace BFS starting from vertex A for a given 5-node graph.",
            "year": 2024,
            "marks": 10,
            "unit": "Unit 4",
            "topic": "Graph Traversal",
            "subtopic": "Breadth First Search (BFS)",
            "question_type": "Algorithm",
            "difficulty": "Medium"
        },
        {
            "id": "q_dsa_03",
            "question": "Write the algorithm for BFS traversal of a graph using a Queue data structure.",
            "year": 2025,
            "marks": 5,
            "unit": "Unit 4",
            "topic": "Graph Traversal",
            "subtopic": "Breadth First Search (BFS)",
            "question_type": "Algorithm",
            "difficulty": "Easy"
        },
        {
            "id": "q_dsa_04",
            "question": "Differentiate between BFS and DFS. Explain Dijkstra's Single Source Shortest Path algorithm with an example graph.",
            "year": 2022,
            "marks": 10,
            "unit": "Unit 4",
            "topic": "Spanning Trees & Shortest Path",
            "subtopic": "Dijkstra's Algorithm",
            "question_type": "Comparison",
            "difficulty": "Hard"
        },
        {
            "id": "q_dsa_05",
            "question": "Construct Minimum Spanning Tree using Prim's algorithm for the given weighted graph and state its time complexity.",
            "year": 2024,
            "marks": 10,
            "unit": "Unit 4",
            "topic": "Spanning Trees & Shortest Path",
            "subtopic": "Prim's Algorithm",
            "question_type": "Numerical",
            "difficulty": "Medium"
        },
        {
            "id": "q_dsa_06",
            "question": "Explain Kruskal's algorithm to find Minimum Spanning Tree using Disjoint Set Union (DSU).",
            "year": 2025,
            "marks": 10,
            "unit": "Unit 4",
            "topic": "Spanning Trees & Shortest Path",
            "subtopic": "Kruskal's Algorithm",
            "question_type": "Algorithm",
            "difficulty": "Medium"
        },

        # Unit 3: Trees
        {
            "id": "q_dsa_07",
            "question": "What is a Binary Search Tree (BST)? Explain deletion of a node with two children in a BST with an example.",
            "year": 2023,
            "marks": 10,
            "unit": "Unit 3",
            "topic": "Binary Search Trees",
            "subtopic": "BST Insertion & Deletion",
            "question_type": "Explanation",
            "difficulty": "Medium"
        },
        {
            "id": "q_dsa_08",
            "question": "Construct an AVL Tree by inserting the sequence of keys: 10, 20, 30, 40, 50, 25. Show LL, RR, LR, and RL rotations.",
            "year": 2024,
            "marks": 10,
            "unit": "Unit 3",
            "topic": "Balanced Trees",
            "subtopic": "AVL Trees & Rotations",
            "question_type": "Numerical",
            "difficulty": "Hard"
        },
        {
            "id": "q_dsa_09",
            "question": "Explain AVL tree rotations with diagrams. Why is balancing required in Binary Search Trees?",
            "year": 2025,
            "marks": 10,
            "unit": "Unit 3",
            "topic": "Balanced Trees",
            "subtopic": "AVL Trees & Rotations",
            "question_type": "Diagram",
            "difficulty": "Medium"
        },
        {
            "id": "q_dsa_10",
            "question": "Write recursive C functions for Inorder, Preorder, and Postorder traversals of a Binary Tree.",
            "year": 2022,
            "marks": 5,
            "unit": "Unit 3",
            "topic": "Trees & Traversals",
            "subtopic": "Inorder, Preorder, Postorder",
            "question_type": "Programming",
            "difficulty": "Medium"
        },

        # Unit 5: Sorting
        {
            "id": "q_dsa_11",
            "question": "Explain Quick Sort algorithm using Divide and Conquer strategy. Trace Quick Sort for array [38, 27, 43, 3, 9, 82, 10].",
            "year": 2023,
            "marks": 10,
            "unit": "Unit 5",
            "topic": "Sorting Algorithms",
            "subtopic": "Quick Sort",
            "question_type": "Numerical",
            "difficulty": "Medium"
        },
        {
            "id": "q_dsa_12",
            "question": "Describe Merge Sort algorithm. Derive its time complexity recurrence relation T(n) = 2T(n/2) + O(n).",
            "year": 2024,
            "marks": 10,
            "unit": "Unit 5",
            "topic": "Sorting Algorithms",
            "subtopic": "Merge Sort",
            "question_type": "Derivation",
            "difficulty": "Hard"
        },
        {
            "id": "q_dsa_13",
            "question": "Explain Collision Resolution Techniques in Hashing: Separate Chaining vs Linear Probing with examples.",
            "year": 2025,
            "marks": 5,
            "unit": "Unit 5",
            "topic": "Hashing",
            "subtopic": "Collision Resolution",
            "question_type": "Comparison",
            "difficulty": "Medium"
        },

        # Unit 1 & Unit 2
        {
            "id": "q_dsa_14",
            "question": "Convert the infix expression A + (B * C - (D / E ^ F) * G) * H into postfix notation using Stack.",
            "year": 2023,
            "marks": 5,
            "unit": "Unit 1",
            "topic": "Stacks",
            "subtopic": "Infix to Postfix",
            "question_type": "Numerical",
            "difficulty": "Medium"
        },
        {
            "id": "q_dsa_15",
            "question": "Explain Circular Queue implementation using an array. State the overflow and underflow conditions.",
            "year": 2024,
            "marks": 5,
            "unit": "Unit 1",
            "topic": "Queues",
            "subtopic": "Circular Queue",
            "question_type": "Explanation",
            "difficulty": "Easy"
        },
        {
            "id": "q_dsa_16",
            "question": "Write a C function to reverse a Singly Linked List in-place without using extra memory.",
            "year": 2025,
            "marks": 5,
            "unit": "Unit 2",
            "topic": "Singly Linked List",
            "subtopic": "Reversal",
            "question_type": "Programming",
            "difficulty": "Medium"
        }
    ]
}
