BUILTIN_SRC = """
(define >= (lambda (a b) (or (> a b) (= a b))))
(define < (lambda (a b) (not (>= a b))))
(define <= (lambda (a b) (or (< a b) (= a b))))
"""
