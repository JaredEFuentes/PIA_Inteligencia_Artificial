(define (problem BLOCKS-11-0)
(:domain BLOCKS)
(:objects H E A J C D F G K I B )
(:INIT (CLEAR B) (CLEAR I) (CLEAR M) (ONTABLE K) (ONTABLE G) (ONTABLE M)
 (ON B F) (ON F D) (ON D C) (ON C J) (ON J A) (ON A E) (ON E H) (ON H L)
 (ON L K) (ON I G) (HANDEMPTY))
(:goal (AND (ON A B) (ON B C) (ON C D) (ON D E) (ON E F) (ON F G) (ON G H)
            (ON H I) (ON I J) (ON J K)))
)