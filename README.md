# Minesweeper AI
Minesweeper game implementation using Python and Pygame with inference-based AI agent solving capabilities

https://github.com/user-attachments/assets/ae09a705-e142-41a2-bab3-8c51ec65c3ec

## Background
Minesweeper is a puzzle game where players clear a grid by uncovering squares without hitting hidden mines. Each uncovered square shows a number indicating nearby mines, helping players deduce which neighboring squares are safe or contain bombs. Players use logic to mark suspected mines and avoid triggering them, aiming to clear all non-mined squares to win.

## Knowledge
In this approach to knowledge representation in Minesweeper, each logical sentence is structured as `{cells} = count`, where the set of cells represents specific positions on the board, and the count indicates how many of them contain mines. For example, `{A, B, C, D, E, F, G, H} = 1` means that exactly one of those cells is a mine. This representation enables inference: if a sentence’s count is 0, all cells in that set are safe, and if the count equals the number of cells, all are mines. When new information (e.g., a cell being safe or a mine) is gained, sentences are updated, potentially leading to further conclusions. Additionally, subset inference allows the AI to deduce new knowledge. For instance, if `{A, B, C} = 1` and `{A, B, C, D, E} = 2`, then `{D, E} = 1`, indicating one of those two cells is a mine. This structured knowledge representation lets the AI infer safe moves and mines systematically.
