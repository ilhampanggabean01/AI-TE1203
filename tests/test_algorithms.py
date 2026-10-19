import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from maze_solver.algorithms import breadth_first_search, depth_first_search
from maze_solver.expert_system import diagnose


class SearchAlgorithmTests(unittest.TestCase):
    def test_bfs_finds_shortest_path_on_open_grid(self):
        result = breadth_first_search(3, 3, set(), (0, 0), (2, 2))
        self.assertTrue(result.found)
        self.assertEqual(result.steps, 4)
        self.assertEqual(result.path[0], (0, 0))
        self.assertEqual(result.path[-1], (2, 2))

    def test_search_reports_no_path_when_goal_is_sealed(self):
        walls = {(0, 1), (1, 0)}
        result = breadth_first_search(3, 3, walls, (0, 0), (2, 2))
        self.assertFalse(result.found)

    def test_dfs_can_find_path(self):
        result = depth_first_search(3, 3, set(), (0, 0), (2, 2))
        self.assertTrue(result.found)
        self.assertEqual(result.path[0], (0, 0))
        self.assertEqual(result.path[-1], (2, 2))

    def test_expert_system_explains_bfs_result(self):
        result = breadth_first_search(3, 3, set(), (0, 0), (2, 2))
        message = diagnose(result, "BFS", (0, 0), (2, 2))
        self.assertIn("jumlah langkah minimum", message)

    def test_expert_system_explains_unreachable_goal(self):
        walls = {(0, 1), (1, 0)}
        result = breadth_first_search(3, 3, walls, (0, 0), (2, 2))
        message = diagnose(result, "BFS", (0, 0), (2, 2))
        self.assertIn("tidak dapat dijangkau", message)

    def test_bfs_path_avoids_walls(self):
        walls = {(1, 1), (1, 2)}
        result = breadth_first_search(
            3, 3, walls, (0, 0), (2, 2)
        )
        self.assertTrue(result.found)
        self.assertTrue(
            all(cell not in walls for cell in result.path)
        )


if __name__ == "__main__":
    unittest.main()
