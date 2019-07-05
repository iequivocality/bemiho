class TraversalClassNotFound(Exception):
    def __init__(self, content):
        self.message = f'Traversal class not found for content {content}'