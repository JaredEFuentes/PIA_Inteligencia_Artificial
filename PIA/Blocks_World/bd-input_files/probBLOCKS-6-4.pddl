(define (problem BLOCKS-6-4)
(:domain BLOCKS)
(:objects A B C D E F )
(:INIT (CLEAR D) (ONTABLE C) (ON D A) (ON A F) (ON F E) (ON E B) (ON B C)
 (HANDEMPTY))
(:goal (AND (ON D A) (ON A E) (ON E B) (ON B C) (ON C F)))
)