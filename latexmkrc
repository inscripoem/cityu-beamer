# SPDX-License-Identifier: MIT
# The same configuration is read by latexmk locally and on Overleaf.
$pdf_mode = 5;
$xelatex = 'xelatex -interaction=nonstopmode -halt-on-error -file-line-error %O %S';
$max_repeat = 5;
