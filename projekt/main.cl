(defmacro adjust-odd (n)
  "Zwiększa n o 1, jeżeli n jest nieparzyste"
  `(if (oddp ,n) (1+ ,n) ,n))

(defun generate-vector (size max-val)
  "Generuje wektor o wielkości size z losowymi liczbami od 0 do max-val-1."
  (make-array size
              :initial-contents
              (loop repeat size collect (random max-val))))

(defun prepare-list-from-vector (vec)
  "Konwertuje wektor vec na listę, zwiększając nieparzyste liczby o 1 z wykorzystaniem makra adjust-odd"
  (loop for x across vec
        collect (adjust-odd x)))

(defun merge (list1 list2)
  "Scala dwie listy posortowane malejąco, zwracając jedną listę malejącą."
  (cond
    ((null list1) list2)
    ((null list2) list1)
    ((>= (car list1) (car list2))
     (cons (car list1)
           (merge (cdr list1) list2)))
    (t
     (cons (car list2)
           (merge list1 (cdr list2))))))

; Zaimplementowany algorytm to rekurencyjny merge-sort
(defun merge-sort (lst)
  "Sortuje listę malejąco za pomocą Merge Sort"
  (if (or (null lst) (null (cdr lst)))
      ;; lista o długości 0 lub 1 jest już posortowana
      lst
      (let* ((mid   (floor (length lst) 2))
             (left  (subseq lst 0 mid))
             (right (subseq lst mid)))

        ;; rekurencyjnie sortujemy obie połowy, a następnie je scalamy
        (merge (merge-sort left)
               (merge-sort right)))))

; Uruchomienie programu
(defun main ()
  (let* ((vec        (generate-vector 100 100))
         (prepared   (prepare-list-from-vector vec))
         (sorted     (merge-sort prepared)))
    (format t "1) Oryginalny wektor: ~a~%" vec)
    (format t "2) Po dostosowaniu (nieparzyste +1): ~a~%" prepared)
    (format t "3) Po sortowaniu: ~a~%" sorted)))

(main)
