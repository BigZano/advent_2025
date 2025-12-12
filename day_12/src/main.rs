use std::collections::HashSet;
use std::fs;

type Cell = (i32, i32);

#[derive(Debug, Clone)]
struct Shape {
    cells: Vec<Cell>,
}

impl Shape {
    fn normalize(cells: &[Cell]) -> Vec<Cell> {
        if cells.is_empty() {
            return vec![];
        }
        let min_r = cells.iter().map(|(r, _)| *r).min().unwrap();
        let min_c = cells.iter().map(|(_, c)| *c).min().unwrap();
        let mut normalized: Vec<_> = cells
            .iter()
            .map(|(r, c)| (r - min_r, c - min_c))
            .collect();
        normalized.sort();
        normalized
    }

    fn rotations_and_flips(&self) -> Vec<Vec<Cell>> {
        let mut variants = Vec::new();
        let mut current = self.cells.clone();

        for _ in 0..4 {
            current = current.iter().map(|(r, c)| (*c, -*r)).collect();
            let norm = Self::normalize(&current);
            if !norm.is_empty() {
                variants.push(norm.clone());
            }

            let flipped: Vec<_> = current.iter().map(|(r, c)| (*r, -*c)).collect();
            let flipped_norm = Self::normalize(&flipped);
            if !flipped_norm.is_empty() {
                variants.push(flipped_norm);
            }
        }

        let mut seen = HashSet::new();
        variants.retain(|v| seen.insert(v.clone()));
        variants
    }

    fn generate_placements(&self, height: i32, width: i32) -> Vec<Vec<Cell>> {
        let mut placements = Vec::new();

        for variant in self.rotations_and_flips() {
            let max_r = variant.iter().map(|(r, _)| *r).max().unwrap_or(0);
            let max_c = variant.iter().map(|(_, c)| *c).max().unwrap_or(0);
            let h = max_r + 1;
            let w = max_c + 1;

            if h > height || w > width {
                continue;
            }

            for base_r in 0..=(height - h) {
                for base_c in 0..=(width - w) {
                    let placed: Vec<_> = variant
                        .iter()
                        .map(|(r, c)| (base_r + r, base_c + c))
                        .collect();
                    placements.push(placed);
                }
            }
        }

        placements
    }
}

#[derive(Clone)]
struct Grid {
    width: i32,
    height: i32,
    occupied: Vec<bool>,
}

impl Grid {
    fn new(width: i32, height: i32) -> Self {
        Grid {
            width,
            height,
            occupied: vec![false; (width * height) as usize],
        }
    }

    fn can_place(&self, placement: &[Cell]) -> bool {
        for &(r, c) in placement {
            let idx = (r * self.width + c) as usize;
            if self.occupied[idx] {
                return false;
            }
        }
        true
    }

    fn place(&mut self, placement: &[Cell]) {
        for &(r, c) in placement {
            let idx = (r * self.width + c) as usize;
            self.occupied[idx] = true;
        }
    }

    fn unplace(&mut self, placement: &[Cell]) {
        for &(r, c) in placement {
            let idx = (r * self.width + c) as usize;
            self.occupied[idx] = false;
        }
    }

    #[allow(dead_code)]
    fn find_first_empty(&self) -> Option<(i32, i32)> {
        for i in 0..self.occupied.len() {
            if !self.occupied[i] {
                let r = (i as i32) / self.width;
                let c = (i as i32) % self.width;
                return Some((r, c));
            }
        }
        None
    }
}

fn parse_input(path: &str) -> (Vec<Shape>, Vec<(i32, i32, Vec<usize>)>) {
    let content = fs::read_to_string(path).expect("Failed to read input");
    let lines: Vec<&str> = content.lines().collect();

    let mut shapes = vec![Shape { cells: vec![] }; 6];
    let mut grids = Vec::new();
    let mut section = "";
    let mut shape_id = 0;
    let mut shape_lines: Vec<String> = Vec::new();

    for line in lines {
        let line = line.trim();
        
        if line == "SHAPES" {
            section = "SHAPES";
            continue;
        } else if line == "GRIDS" {
            if !shape_lines.is_empty() {
                let mut cells = Vec::new();
                for (r, row) in shape_lines.iter().enumerate() {
                    for (c, ch) in row.chars().enumerate() {
                        if ch == '#' {
                            cells.push((r as i32, c as i32));
                        }
                    }
                }
                shapes[shape_id] = Shape { cells: Shape::normalize(&cells) };
                shape_lines.clear();
            }
            section = "GRIDS";
            continue;
        }

        if section == "SHAPES" {
            if line.ends_with(':') {
                if !shape_lines.is_empty() {
                    let mut cells = Vec::new();
                    for (r, row) in shape_lines.iter().enumerate() {
                        for (c, ch) in row.chars().enumerate() {
                            if ch == '#' {
                                cells.push((r as i32, c as i32));
                            }
                        }
                    }
                    shapes[shape_id] = Shape { cells: Shape::normalize(&cells) };
                    shape_lines.clear();
                }
                shape_id = line.trim_end_matches(':').parse().unwrap();
            } else if !line.is_empty() {
                shape_lines.push(line.to_string());
            }
        } else if section == "GRIDS" && !line.is_empty() {
            let parts: Vec<&str> = line.split(": ").collect();
            let dims: Vec<i32> = parts[0].split('x').map(|s| s.parse().unwrap()).collect();
            let counts: Vec<usize> = parts[1]
                .split_whitespace()
                .map(|s| s.parse().unwrap())
                .collect();
            grids.push((dims[0], dims[1], counts));
        }
    }

    (shapes, grids)
}

fn can_fit(
    width: i32,
    height: i32,
    shape_counts: &[usize],
    all_placements: &[Vec<Vec<Cell>>],
) -> bool {
    // Quick feasibility checks
    for (sid, &count) in shape_counts.iter().enumerate() {
        if count > 0 && all_placements[sid].is_empty() {
            return false;
        }
    }

    let total_needed: usize = shape_counts.iter().sum();
    if total_needed == 0 {
        return true;
    }

    // For large grids with many shapes, use a simpler heuristic
    // Check if the total area is sufficient
    let total_area = (width * height) as usize;
    let mut total_cells_needed = 0;
    for (sid, &count) in shape_counts.iter().enumerate() {
        if count > 0 && !all_placements[sid].is_empty() {
            let cells_per_shape = all_placements[sid][0].len();
            total_cells_needed += cells_per_shape * count;
        }
    }

    if total_cells_needed > total_area {
        return false;
    }

    let mut grid = Grid::new(width, height);
    let mut remaining = shape_counts.to_vec();

    fn backtrack(
        grid: &mut Grid,
        remaining: &mut [usize],
        placements: &[Vec<Vec<Cell>>],
        depth: usize,
    ) -> bool {
        // Aggressive depth limit
        if depth > 500 {
            return false;
        }

        // Try to place the next needed shape
        let mut best_shape = None;
        let mut max_remaining = 0;

        for (shape_idx, &count) in remaining.iter().enumerate() {
            if count > max_remaining {
                max_remaining = count;
                best_shape = Some(shape_idx);
            }
        }

        match best_shape {
            None => return true, // All shapes placed
            Some(shape_idx) => {
                if remaining[shape_idx] == 0 {
                    return backtrack(grid, remaining, placements, depth + 1);
                }

                // Try placements for this shape, prioritizing near filled areas
                let placements_to_try = &placements[shape_idx];
                
                for placement in placements_to_try {
                    // Check bounds
                    if !placement.iter().all(|&(r, c)| {
                        0 <= r && r < grid.height && 0 <= c && c < grid.width
                    }) {
                        continue;
                    }

                    if !grid.can_place(placement) {
                        continue;
                    }

                    grid.place(placement);
                    remaining[shape_idx] -= 1;

                    if backtrack(grid, remaining, placements, depth + 1) {
                        return true;
                    }

                    remaining[shape_idx] += 1;
                    grid.unplace(placement);
                }

                false
            }
        }
    }

    backtrack(&mut grid, &mut remaining, all_placements, 0)
}

fn main() {
    let (shapes, grids) = parse_input("input.txt");

    let mut count = 0;
    for (i, (width, height, shape_counts)) in grids.iter().enumerate() {
        if (i + 1) % 100 == 0 {
            println!("Progress: {}/{}", i + 1, grids.len());
        }

        let all_placements: Vec<_> = shapes
            .iter()
            .map(|shape| shape.generate_placements(*height, *width))
            .collect();

        if can_fit(*width, *height, shape_counts, &all_placements) {
            count += 1;
        }
    }

    println!("Answer: {}", count);
}
