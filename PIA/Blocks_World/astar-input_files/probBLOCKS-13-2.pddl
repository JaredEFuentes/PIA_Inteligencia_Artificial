(define (problem BLOCKS-13-2)
(:domain BLOCKS)
(:objects L D I A K C B F G J M E H )
(:INIT (CLEAR D) (CLEAR A) (CLEAR H) (ONTABLE E) (ONTABLE G) (ONTABLE H)
 (ON D F) (ON F I) (ON I C) (ON C E) (ON A L) (ON L K) (ON K J) (ON J B) 
 (ON B M) (ON M G) (HANDEMPTY))
(:goal (AND (ON H I) (ON I K) (ON K D) (ON D E) (ON E A) (ON A M) (ON M B)
            (ON B C) (ON C L) (ON L J) (ON J F) (ON F G)))
)