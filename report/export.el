;; UTF-8 as default encoding
(set-language-environment "UTF-8")
(set-default-coding-systems 'utf-8)
(set-keyboard-coding-system 'utf-8-unix)
;; do this especially on Windows, else python output problem
(set-terminal-coding-system 'utf-8-unix)

;; stop creating ~ files
(setq make-backup-files nil) 

;; add a report latex-class which replaces parts with chapters
(require 'ox-latex)
(add-to-list 'org-latex-classes
             '("my-report"
	       "\\documentclass{report}"
	       ("\\chapter{%s}" . "\\part*{%s}")
	       ("\\section{%s}" . "\\chapter*{%s}")
	       ("\\subsection{%s}" . "\\section*{%s}")
	       ("\\subsubsection{%s}" . "\\subsection*{%s}")
	       ("\\subsubsubsection{%s}" . "\\subsubsection*{%s}")
	       ("\\paragraph{%s}" . "\\paragraph*{%s}")
	       ("\\subparagraph{%s}" . "\\subparagraph*{%s}")))

;; This messes with citations for some reason so uncomment at the very end
(setq org-latex-listings 'minted
      org-latex-packages-alist '(("" "minted"))
      org-latex-pdf-process
      '("pdflatex -shell-escape -interaction nonstopmode -output-directory %o %f"
        "pdflatex -shell-escape -interaction nonstopmode -output-directory %o %f"
        "pdflatex -shell-escape -interaction nonstopmode -output-directory %o %f"))

(setq org-latex-minted-options '(("breaklines" "true")
                                 ("breakanywhere" "true")
				 ("linenos")
				 ("frame" "leftline")))

(require 'oc-natbib)

;; Open and export file
(find-file "main.org")
(org-latex-export-to-pdf)
