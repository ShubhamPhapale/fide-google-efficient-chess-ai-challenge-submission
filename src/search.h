// Berserk is a UCI compliant chess engine written in C
// Copyright (C) 2021 Jay Honnold

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

#ifndef SEARCH_H
#define SEARCH_H

#include "types.h"

// search specific score evals
#define CHECKMATE INT16_MAX
#define MATE_BOUND 30000
#define TB_WIN_BOUND 20000

// reverse futility pruning values
// these 2 values go 65 -> 135 -> 210 -> 290 -> ...
#define RFP_BASE 65
#define RFP_STEP_RISE 5

// static evaluation pruning
// capture cutoff is linear 70x
// quiet cutoff is quadratic 20x^2
#define SEE_PRUNE_CAPTURE_CUTOFF 70
#define SEE_PRUNE_CUTOFF 20

// delta pruning in QS
#define DELTA_CUTOFF 150

// base window value
#define WINDOW 8

void InitPruningAndReductionTables();

void* UCISearch(void* arg);
int BestMove(Board* board, SearchParams* params, ThreadData* threads);
void* Search(void* arg);
int Negamax(int alpha, int beta, int depth, ThreadData* thread, PV* pv);
int Quiesce(int alpha, int beta, ThreadData* thread, PV* pv);

void PrintInfo(PV* pv, int score, int depth, ThreadData* thread);
void PrintPV(PV* pv);

#endif
