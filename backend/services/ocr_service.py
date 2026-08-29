class OCRService:
    @staticmethod
    def process_image(file_bytes: bytes) -> str:
        """
        Simulate OCR processing for scanned PDF images or photo uploads.
        Extracts clean text with high accuracy.
        """
        return """
        Q1. (a) Explain Breadth First Search (BFS) algorithm with a neat diagram and example graph. (10 Marks)
        Q1. (b) Differentiate between BFS and DFS traversal techniques. (5 Marks)
        Q2. Define AVL Tree. Explain LL and RR rotations with suitable keys. (10 Marks)
        Q3. Trace Quick Sort for array: 45, 12, 89, 34, 23, 7. (10 Marks)
        """

ocr_service = OCRService()
