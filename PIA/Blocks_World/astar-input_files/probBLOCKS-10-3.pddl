(define (problem BLOCKS-10-3)
(:domain BLOCKS)
(:objects B G E D F H I A C J )
(:INIT (CLEAR J) (ONTABLE A) (ON J I) (ON I H) (ON H E) (ON E B) (ON B G)
 (ON G F) (ON F D) (ON D C) (ON C A) (HANDEMPTY))
(:goal (AND (ON A B) (ON B C) (ON C D) (ON D E) (ON E F) (ON F G) (ON G H)
            (ON H I) (ON I J)))
)