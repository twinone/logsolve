#!/usr/bin/env swipl

:- initialization main.
:- include('gridlib.pl').
:- use_module(library(clpfd)).



main :-
  readGrid(R, C, Grid),

  % create as many variables as in the grid
  Len is R * C,
  length(Vars, Len),

  % have them organized by rows and by columns
  matrixByRows(Vars, C, MatrixByRows),
  transpose(MatrixByRows, MatrixByCols),

  % set the values that we read from the input
  labelInput(MatrixByRows, Grid),

  Vars ins 0..1,
  %write('Mat:'),nl,write(MatrixByRows), nl,nl,
  maplist(restrictSameCount(R), MatrixByRows),
  maplist(restrictSameCount(C), MatrixByCols),
  maplist(solveLine, MatrixByRows),
  maplist(solveLine, MatrixByCols),

  label(Vars),
  %prettyprint(Grid),nl,
  prettyprint(MatrixByRows),nl,
  writeSolutionSteps(Grid, MatrixByRows),
  halt.

solveLine(Line) :-
  length(Line, Len),
  Max is Len - 3 + 1,
  findall(X, between(1, Max, X), R),
  solveLine(Line, R).

solveLine(_, []).
solveLine(Line, [R1|Rs]) :-
  R2 is R1 + 1, R3 is R2 + 1,
  nth1(R1, Line, X1),
  nth1(R2, Line, X2),
  nth1(R3, Line, X3),
  %write('Restricting: '), write([X1,X2,X3]),nl,
  sum([X1, X2, X3], #>, 0),
  sum([X1, X2, X3], #<, 3),
  solveLine(Line, Rs).




%write("sum of "), write(Row), write(' is '), write(Csum),nl,
restrictSameCount(C, Row) :-  Csum is C / 2,  sum(Row, #=, Csum).


prettyprint(Rows) :- member(Row, Rows), prettyprintRow(Row), nl, fail.
prettyprint(_).

prettyprintRow(Row) :- member(X, Row), write(X), write(' '), fail.
prettyprintRow(_).



writeSolutionSteps(Problem, Solution) :-
  elem(Problem, R, C, -1), elem(Solution, R, C, X),
  writeStep(R, C, X), fail.
writeSolutionSteps(_,_).

writeStep(R, C, 0) :- write('click '), write(R), write(' '), write(C), nl.
writeStep(R, C, 1) :- write('dclick '), write(R), write(' '), write(C), nl.



%
