(define (problem BLOCKS-5-1)
(:domain BLOCKS)
(:objects A D C E B )
(:INIT (CLEAR B) (CLEAR A) (CLEAR C) (ONTABLE D) (ONTABLE E) (ONTABLE C)
 (ON B D) (ON A E) (HANDEMPTY))
(:goal (AND (ON D C) (ON C B) (ON B A) (ON A E)))
)