:- use_module(library(clpfd)).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%% READING %%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

readString(S) :-
  % disable genius by default |: prompt when reading
  prompt1(''),
  % read from stdin
  read_string(user_input, '\n\t ', '\n\t ', _, S).

readNum(N) :-
  readString(S),
  number_string(N, S).

readGrid(R, C, Grid) :-
  readNum(R),
  readNum(C),
  readRows(R, C, Grid).

readRows(0, _, []).
readRows(Remaining, C, Rows) :-
  readRow(C, R),
  Next is Remaining -1,
  readRows(Next, C, Rs),
  append([R], Rs, Rows).


readRow(0, []).
readRow(Remaining, Row) :-
  readNum(R),
  Next is Remaining - 1,
  readRow(Next, Rs),
  append([R], Rs, Row).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%% Helpers %%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


elem(Grid, R, C, Val) :-
  nth1(R, Grid, Row),
  nth1(C, Row, Val).


matrixByRows([],_,[]).
matrixByRows(L,NumCols,[R|Rows]) :-
	append(R, Temp, L),
	length(R, NumCols),
	matrixByRows(Temp, NumCols, Rows).


% labels each non -1 in the grid to it's corresponding matrix
labelInput(Mat, Grid) :-
  findall(R-C, (elem(Grid, R, C, X), X \= -1), Pairs),
  labelInput(Mat, Grid, Pairs).

labelInput(Mat, Grid, [R-C|RRCC]) :-
  elem(Grid, R, C, X), elem(Mat, R, C, Y),
  Y #= X,
  labelInput(Mat, Grid, RRCC).
labelInput(_,_,[]).
