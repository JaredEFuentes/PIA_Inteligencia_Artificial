(define (problem BLOCKS-11-3)
(:domain BLOCKS)
(:objects A C E G I K B D F H J )
(:INIT (CLEAR B) (CLEAR I) (ONTABLE K) (ONTABLE G) (ON B C) (ON C F) 
 (ON F E) (ON E K) (ON I D) (ON D J) (ON J H) (ON H A) (ON A G)
 (HANDEMPTY))
(:goal (AND (ON A C) (ON C E) (ON E G) (ON G I) (ON I K) (ON K B) (ON B D)
            (ON D F) (ON F H) (ON H J)))
)