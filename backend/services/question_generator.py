import uuid
from typing import List, Dict, Any

class QuestionGeneratorService:
    @staticmethod
    def generate_model_paper(
        subject_name: str,
        total_marks: int = 100,
        duration_minutes: int = 180,
        difficulty_mode: str = "Balanced",
        num_previous_papers: int = 4
    ) -> Dict[str, Any]:
        """
        Generates a structured, multi-section model question paper with novel concept-based questions.
        """
        paper_id = f"model_paper_{uuid.uuid4().hex[:8]}"

        section_a_qs = [
            {
                "id": "mp_q1",
                "question": "Define Sparse Matrix. Write down the triplet representation of a 4x4 Sparse Matrix with 3 non-zero elements.",
                "marks": 5,
                "unit": "Unit 1",
                "topic": "Arrays & Sparse Matrices",
                "difficulty": "Easy",
                "type": "Numerical"
            },
            {
                "id": "mp_q2",
                "question": "What is a Circular Queue? How does it overcome the limitation of a simple linear array queue?",
                "marks": 5,
                "unit": "Unit 1",
                "topic": "Queues",
                "difficulty": "Easy",
                "type": "Explanation"
            },
            {
                "id": "mp_q3",
                "question": "Compare Singly Linked List vs Doubly Linked List in terms of memory overhead and insertion efficiency.",
                "marks": 5,
                "unit": "Unit 2",
                "topic": "Doubly & Circular List",
                "difficulty": "Easy",
                "type": "Comparison"
            },
            {
                "id": "mp_q4",
                "question": "Define Inorder, Preorder, and Postorder tree traversals. Give an example binary tree with its Inorder sequence.",
                "marks": 5,
                "unit": "Unit 3",
                "topic": "Trees & Traversals",
                "difficulty": "Easy",
                "type": "Definition"
            }
        ]

        section_b_qs = [
            {
                "id": "mp_q5",
                "question": "Write the Breadth First Search (BFS) graph traversal algorithm. Trace BFS starting from vertex 'V1' for a 6-node weighted graph with vertices {V1, V2, V3, V4, V5, V6}.",
                "marks": 10,
                "unit": "Unit 4",
                "topic": "Graph Traversal",
                "difficulty": "Medium",
                "type": "Algorithm"
            },
            {
                "id": "mp_q6",
                "question": "Explain Dijkstra's algorithm for finding the single-source shortest path. Construct the shortest path tree from source node A to all other nodes for the given graph.",
                "marks": 10,
                "unit": "Unit 4",
                "topic": "Spanning Trees & Shortest Path",
                "difficulty": "Hard",
                "type": "Numerical"
            },
            {
                "id": "mp_q7",
                "question": "Insert the keys 15, 27, 49, 10, 8, 22, 35 into an initially empty AVL Tree. Show step-by-step rotations (LL, RR, LR, RL) performed to maintain balance.",
                "marks": 10,
                "unit": "Unit 3",
                "topic": "Balanced Trees",
                "difficulty": "Hard",
                "type": "Numerical"
            },
            {
                "id": "mp_q8",
                "question": "Explain Quick Sort using Divide and Conquer strategy. Trace Quick Sort for array A = [42, 13, 88, 25, 9, 61, 30]. Discuss best and worst-case time complexity.",
                "marks": 10,
                "unit": "Unit 5",
                "topic": "Sorting Algorithms",
                "difficulty": "Medium",
                "type": "Algorithm"
            }
        ]

        section_c_qs = [
            {
                "id": "mp_q9",
                "question": "Design a C/C++ program to detect a cycle in a Directed Graph using Depth First Search (DFS) recursion stack. Explain the significance of vertex coloring (WHITE, GRAY, BLACK).",
                "marks": 20,
                "unit": "Unit 4",
                "topic": "Graph Traversal",
                "difficulty": "Hard",
                "type": "Programming"
            },
            {
                "id": "mp_q10",
                "question": "Discuss Collision Resolution in Hashing. Compare Open Addressing (Linear Probing, Quadratic Probing) with Separate Chaining using hash function H(k) = k mod 11.",
                "marks": 20,
                "unit": "Unit 5",
                "topic": "Hashing",
                "difficulty": "Hard",
                "type": "Case study"
            }
        ]

        sections = [
            {
                "section_name": "Section A — Short Answer Questions (Answer all 4 questions, 5 Marks each)",
                "total_section_marks": 20,
                "questions": section_a_qs
            },
            {
                "section_name": "Section B — Core Analytical & Algorithmic Questions (Answer all 4 questions, 10 Marks each)",
                "total_section_marks": 40,
                "questions": section_b_qs
            },
            {
                "section_name": "Section C — Comprehensive & Advanced Applications (Answer all questions, 20 Marks each)",
                "total_section_marks": 40,
                "questions": section_c_qs
            }
        ]

        instructions = [
            "All sections are compulsory unless internal choice is specified.",
            "Write neat diagrams wherever necessary.",
            "State time and space complexity assumptions clearly.",
            "Scientific calculators are permitted if required."
        ]

        return {
            "paper_id": paper_id,
            "subject_name": subject_name,
            "total_marks": total_marks,
            "duration_minutes": duration_minutes,
            "difficulty_mode": difficulty_mode,
            "instructions": instructions,
            "sections": sections
        }

question_generator_service = QuestionGeneratorService()
