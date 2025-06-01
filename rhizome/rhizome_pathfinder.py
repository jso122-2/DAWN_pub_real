# /rhizome/rhizome_pathfinder.py
from collections import deque

from utils.vector_math import similarity  # assumes you have a cosine similarity function

def find_path(seed_start, seed_goal, nodes, max_depth=5):
    """
    Lightweight BFS from seed_start to seed_goal.
    Stops at max_depth to avoid global recompute.
    Returns a list of seed_ids forming the path, or None.
    """
    if seed_start not in nodes or seed_goal not in nodes:
        return None

    visited = set()
    queue = deque([(seed_start, [seed_start])])

    while queue:
        current, path = queue.popleft()
        if current == seed_goal:
            return path
        if len(path) > max_depth:
            continue

        for neighbor in nodes[current].edges:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None

def find_path_semantic(seed_start, seed_goal, nodes, max_depth=6, threshold=0.8):
    """
    Semantic-aware pathfinder with fallback.
    Uses cosine similarity and hop penalty to find aligned paths.
    Falls back to regular path if goal unreachable or vectors missing.
    """
    if seed_start not in nodes or seed_goal not in nodes:
        return None

    goal_vec = nodes[seed_goal].semantic_vector
    if not goal_vec:
        return find_path(seed_start, seed_goal, nodes, max_depth)

    visited = set()
    queue = deque([(seed_start, [seed_start])])

    best_path = None
    best_score = -1.0

    while queue:
        current, path = queue.popleft()
        if len(path) > max_depth:
            continue

        curr_node = nodes[current]
        curr_vec = curr_node.semantic_vector
        if not curr_vec:
            continue

        for neighbor in curr_node.edges:
            if neighbor in visited:
                continue

            neighbor_vec = nodes[neighbor].semantic_vector
            if not neighbor_vec:
                continue

            sim_score = similarity(neighbor_vec, goal_vec)
            hop_penalty = len(path) / max_depth
            score = sim_score - hop_penalty

            if score > best_score and sim_score >= threshold:
                best_score = score
                best_path = path + [neighbor]

            visited.add(neighbor)
            queue.append((neighbor, path + [neighbor]))

    return best_path if best_path else find_path(seed_start, seed_goal, nodes, max_depth)


def find_nearest_nodes(seed_origin, nodes, radius=2):
    """
    Return all nodes within N edge-hops from seed_origin.
    Used for broadcast or passive nutrient flow.
    """
    if seed_origin not in nodes:
        return []

    visited = set()
    queue = deque([(seed_origin, 0)])
    nearby = []

    while queue:
        current, depth = queue.popleft()
        if depth > radius:
            continue
        visited.add(current)
        nearby.append(current)

        for neighbor in nodes[current].edges:
            if neighbor not in visited:
                queue.append((neighbor, depth + 1))

    return nearby
