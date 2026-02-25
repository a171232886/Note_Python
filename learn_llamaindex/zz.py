import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import heapq
from typing import List, Tuple, Set
import random

class HNSWNode:
    """HNSW图中的节点"""
    def __init__(self, vector: np.ndarray, level: int, node_id: int):
        self.vector = vector          # 节点的向量表示
        self.id = node_id              # 节点唯一标识
        self.level = level             # 节点所在的最大层
        self.neighbors = {}             # 每层的邻居列表 {level: [neighbor_ids]}
        
    def add_neighbor(self, neighbor_id: int, level: int):
        """添加邻居"""
        if level not in self.neighbors:
            self.neighbors[level] = []
        if neighbor_id not in self.neighbors[level]:
            self.neighbors[level].append(neighbor_id)
    
    def __repr__(self):
        return f"Node(id={self.id}, level={self.level}, neighbors={self.neighbors})"

class SimpleHNSW:
    """简化的HNSW实现"""
    
    def __init__(self, dim: int = 2, max_elements: int = 100, M: int = 8, ef_construction: int = 200):
        """
        初始化HNSW
        
        参数:
        dim: 向量维度
        max_elements: 最大元素数量
        M: 每个节点的最大邻居数
        ef_construction: 构建时的动态候选列表大小
        """
        self.dim = dim
        self.max_elements = max_elements
        self.M = M
        self.ef_construction = ef_construction
        
        # 存储所有节点
        self.nodes = {}
        
        # 最大层数 - 根据元素数量计算
        self.max_level = int(np.log2(max_elements)) - 1
        if self.max_level < 1:
            self.max_level = 1
        
        # 随机选择的入口点（最高层的节点）
        self.entry_point = None
        
        # 记录每层的节点数
        self.level_nodes = {}
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """计算余弦相似度"""
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0
        return np.dot(vec1, vec2) / (norm1 * norm2)
    
    def cosine_distance(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """计算余弦距离（1 - 余弦相似度）"""
        return 1 - self.cosine_similarity(vec1, vec2)
    
    def random_level(self) -> int:
        """随机生成节点的层数（指数衰减）"""
        level = 0
        # 使用指数分布，确保高层节点更少
        while random.random() < 0.5 and level < self.max_level:
            level += 1
        return level
    
    def search_layer(self, query: np.ndarray, entry_points: List[int], level: int, ef: int) -> List[int]:
        """
        在指定层搜索最近的节点
        
        参数:
        query: 查询向量
        entry_points: 起始搜索点
        level: 搜索的层
        ef: 动态候选列表大小
        
        返回:
        最近的节点ID列表
        """
        # 已访问的节点
        visited = set(entry_points)
        
        # 候选列表（最小堆，按距离排序）
        candidates = []
        for ep in entry_points:
            dist = self.cosine_distance(query, self.nodes[ep].vector)
            heapq.heappush(candidates, (dist, ep))
        
        # 结果列表（最大堆，按距离排序，用于淘汰最差的结果）
        results = []
        for ep in entry_points:
            dist = self.cosine_distance(query, self.nodes[ep].vector)
            heapq.heappush(results, (-dist, ep))  # 负距离，这样堆顶是最大距离
        
        # 遍历候选列表
        while candidates:
            # 获取最近的候选点
            dist_cand, cand_id = heapq.heappop(candidates)
            
            # 如果这个点比当前最差结果还差，停止搜索
            if results and -results[0][0] < dist_cand and len(results) >= ef:
                break
            
            # 检查该点的所有邻居
            node = self.nodes[cand_id]
            if level in node.neighbors:
                for neighbor_id in node.neighbors[level]:
                    if neighbor_id not in visited:
                        visited.add(neighbor_id)
                        
                        # 计算距离
                        dist = self.cosine_distance(query, self.nodes[neighbor_id].vector)
                        
                        # 添加到候选列表
                        heapq.heappush(candidates, (dist, neighbor_id))
                        
                        # 如果结果列表未满，直接添加
                        if len(results) < ef:
                            heapq.heappush(results, (-dist, neighbor_id))
                        else:
                            # 如果这个点比当前最差结果好，替换最差结果
                            if dist < -results[0][0]:
                                heapq.heappushpop(results, (-dist, neighbor_id))
        
        # 返回最近的节点（按距离排序）
        return [node_id for _, node_id in sorted([(-d, nid) for d, nid in results])]
    
    def insert(self, vector: np.ndarray):
        """插入一个向量到HNSW中"""
        node_id = len(self.nodes)
        level = self.random_level()
        
        # 创建新节点
        new_node = HNSWNode(vector, level, node_id)
        
        if self.entry_point is None:
            # 第一个节点
            self.nodes[node_id] = new_node
            self.entry_point = node_id
            return
        
        # 从入口点开始搜索
        curr_obj = self.entry_point
        
        # 从上到下搜索，找到各层的最近邻
        for curr_level in range(self.max_level, level, -1):
            # 在当前层搜索，找到最近的一个点
            candidates = self.search_layer(vector, [curr_obj], curr_level, 1)
            if candidates:
                curr_obj = candidates[0]
        
        # 从当前层往下，找到每层的近邻并连接
        for curr_level in range(min(level, self.max_level), -1, -1):
            # 搜索该层的最近邻（使用ef_construction）
            candidates = self.search_layer(vector, [curr_obj], curr_level, self.ef_construction)
            
            # 选择最近的M个作为邻居
            selected_neighbors = candidates[:min(self.M, len(candidates))]
            
            # 连接新节点和选中的邻居
            for neighbor_id in selected_neighbors:
                new_node.add_neighbor(neighbor_id, curr_level)
                self.nodes[neighbor_id].add_neighbor(node_id, curr_level)
            
            # 更新当前层的最优节点，作为下一层的入口
            if candidates:
                curr_obj = candidates[0]
        
        # 保存新节点
        self.nodes[node_id] = new_node
        
        # 更新入口点（如果新节点在最高层）
        if level > self.nodes[self.entry_point].level:
            self.entry_point = node_id
    
    def search(self, query: np.ndarray, k: int = 5, ef: int = 50) -> List[Tuple[int, float]]:
        """
        搜索K个最近邻
        
        返回:
        列表，包含 (node_id, similarity) 元组
        """
        if not self.nodes:
            return []
        
        # 从入口点开始
        curr_obj = self.entry_point
        
        # 从上到下搜索
        for level in range(self.max_level, 0, -1):
            # 在当前层找到最近的点，作为下一层的入口
            candidates = self.search_layer(query, [curr_obj], level, 1)
            if candidates:
                curr_obj = candidates[0]
        
        # 在最底层搜索K个最近邻
        final_candidates = self.search_layer(query, [curr_obj], 0, max(ef, k))
        
        # 计算相似度并返回
        results = []
        for node_id in final_candidates[:k]:
            similarity = self.cosine_similarity(query, self.nodes[node_id].vector)
            results.append((node_id, similarity))
        
        return results
    
    def visualize(self, query=None, results=None):
        """可视化HNSW图（仅限2D向量）"""
        if self.dim != 2:
            print("可视化仅支持2维向量")
            return
        
        plt.figure(figsize=(12, 8))
        
        # 绘制所有节点
        x_coords = [node.vector[0] for node in self.nodes.values()]
        y_coords = [node.vector[1] for node in self.nodes.values()]
        
        # 按层绘制节点 - 修复alpha值范围
        for level in range(self.max_level + 1):
            level_nodes = [node for node in self.nodes.values() if node.level >= level]
            if level_nodes:
                x = [n.vector[0] for n in level_nodes]
                y = [n.vector[1] for n in level_nodes]
                # 确保alpha在0到1之间
                alpha = min(0.3 + 0.2 * level, 1.0)
                plt.scatter(x, y, alpha=alpha, label=f'Layer {level}', s=50)
        
        # 绘制边（仅底层连接）
        for node in self.nodes.values():
            if 0 in node.neighbors:
                for neighbor_id in node.neighbors[0]:
                    if neighbor_id > node.id:  # 避免重复绘制
                        neighbor = self.nodes[neighbor_id]
                        plt.plot([node.vector[0], neighbor.vector[0]], 
                               [node.vector[1], neighbor.vector[1]], 
                               'gray', alpha=0.2, linewidth=0.5)
        
        # 标记入口点
        if self.entry_point is not None:
            entry = self.nodes[self.entry_point]
            plt.scatter([entry.vector[0]], [entry.vector[1]], 
                       color='red', s=200, marker='*', label='Entry Point', zorder=5)
        
        # 标记查询点和结果
        if query is not None:
            plt.scatter([query[0]], [query[1]], 
                       color='green', s=200, marker='P', label='Query', zorder=5)
        
        if results:
            result_nodes = [self.nodes[node_id] for node_id, _ in results]
            x = [n.vector[0] for n in result_nodes]
            y = [n.vector[1] for n in result_nodes]
            plt.scatter(x, y, color='orange', s=100, marker='X', label='Results', zorder=4)
        
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('HNSW Graph Visualization')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.show()

# ==================== 演示示例 ====================

def demo_1_simple_insertion():
    """演示1：简单的插入和搜索"""
    print("="*50)
    print("演示1：简单的HNSW插入和搜索")
    print("="*50)
    
    # 创建一些2D点作为示例数据
    np.random.seed(42)
    data_points = np.array([
        [0, 0],
        [1, 2],
        [2, 1],
        [3, 3],
        [4, 2],
        [5, 0],
        [2, 4],
        [1, 5],
        [4, 4],
        [5, 5]
    ])
    
    print(f"创建了{len(data_points)}个数据点")
    
    # 创建HNSW索引
    hnsw = SimpleHNSW(dim=2, max_elements=100, M=4, ef_construction=50)
    
    # 插入数据
    for i, point in enumerate(data_points):
        hnsw.insert(point)
        print(f"插入点 {i}: {point}")
    
    print(f"\n插入完成，共{len(hnsw.nodes)}个节点")
    print(f"入口节点ID: {hnsw.entry_point}")
    
    # 搜索演示
    query = np.array([3, 2])
    print(f"\n查询向量: {query}")
    
    results = hnsw.search(query, k=3)
    print("搜索结果（按相似度排序）:")
    for node_id, similarity in results:
        print(f"  点{node_id}: {hnsw.nodes[node_id].vector}, 相似度: {similarity:.4f}")
    
    # 可视化
    hnsw.visualize(query, results)

def demo_2_random_data():
    """演示2：使用随机生成的数据"""
    print("\n" + "="*50)
    print("演示2：随机生成的数据点")
    print("="*50)
    
    # 生成3个簇的随机数据
    np.random.seed(43)
    n_samples = 50
    centers = 3
    
    X, y = make_blobs(n_samples=n_samples, centers=centers, 
                      n_features=2, cluster_std=1.0, random_state=42)
    
    print(f"生成了{n_samples}个数据点，分布在{centers}个簇中")
    
    # 创建HNSW索引
    hnsw = SimpleHNSW(dim=2, max_elements=100, M=6, ef_construction=100)
    
    # 插入数据
    for point in X:
        hnsw.insert(point)
    
    print(f"插入完成，共{len(hnsw.nodes)}个节点")
    print(f"入口节点ID: {hnsw.entry_point}")
    
    # 搜索演示 - 从不同位置查询
    queries = [
        np.array([0, 0]),
        np.array([5, 5]),
        np.array([-2, -2])
    ]
    
    for i, query in enumerate(queries):
        print(f"\n查询 {i+1}: {query}")
        results = hnsw.search(query, k=5)
        print("  最近的5个点:")
        for node_id, similarity in results:
            print(f"    点{node_id}: {hnsw.nodes[node_id].vector}, 相似度: {similarity:.4f}")
    
    # 可视化
    hnsw.visualize(queries[0], results)

def demo_3_performance_comparison():
    """演示3：HNSW vs 线性搜索的性能对比"""
    print("\n" + "="*50)
    print("演示3：HNSW vs 线性搜索性能对比")
    print("="*50)
    
    # 生成更多数据点
    np.random.seed(44)
    n_samples = 1000
    dimensions = 10  # 使用10维向量
    
    print(f"生成{n_samples}个{dimensions}维向量...")
    data = np.random.randn(n_samples, dimensions)
    
    # 创建HNSW索引
    hnsw = SimpleHNSW(dim=dimensions, max_elements=n_samples, M=16, ef_construction=200)
    
    # 测量插入时间
    import time
    start_time = time.time()
    for point in data:
        hnsw.insert(point)
    insert_time = time.time() - start_time
    print(f"HNSW索引构建时间: {insert_time:.4f}秒")
    
    # 随机选择10个查询点
    n_queries = 10
    queries = data[np.random.choice(n_samples, n_queries, replace=False)]
    k = 10
    
    # 线性搜索
    print(f"\n进行{n_queries}次查询，每次找{k}个最近邻...")
    
    # HNSW搜索
    hnsw_times = []
    hnsw_accuracies = []
    
    for i, query in enumerate(queries):
        # HNSW搜索
        start_time = time.time()
        hnsw_results = hnsw.search(query, k=k, ef=100)
        hnsw_time = time.time() - start_time
        hnsw_times.append(hnsw_time)
        
        # 线性搜索（基准真相）
        start_time = time.time()
        distances = [(idx, hnsw.cosine_similarity(query, data[idx])) for idx in range(n_samples)]
        true_results = sorted(distances, key=lambda x: -x[1])[:k]
        linear_time = time.time() - start_time
        
        # 计算召回率（HNSW结果中有多少在真实最近邻中）
        hnsw_ids = set([idx for idx, _ in hnsw_results])
        true_ids = set([idx for idx, _ in true_results])
        intersection = hnsw_ids.intersection(true_ids)
        recall = len(intersection) / k
        
        hnsw_accuracies.append(recall)
        
        if i < 3:  # 只显示前3个查询的详细信息
            print(f"\n查询 {i+1}:")
            print(f"  HNSW时间: {hnsw_time:.6f}秒")
            print(f"  线性搜索时间: {linear_time:.6f}秒")
            print(f"  速度提升: {linear_time/hnsw_time:.2f}倍")
            print(f"  召回率: {recall:.2%}")
    
    # 统计结果
    print(f"\n=== 统计结果（{n_queries}次查询）===")
    print(f"HNSW平均查询时间: {np.mean(hnsw_times)*1000:.3f}毫秒")
    print(f"线性搜索平均时间: {linear_time*1000:.3f}毫秒")
    print(f"平均速度提升: {linear_time/np.mean(hnsw_times):.2f}倍")
    print(f"平均召回率: {np.mean(hnsw_accuracies):.2%}")
    
    # 绘制性能图表
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.bar(['Linear Search', 'HNSW'], 
            [linear_time*1000, np.mean(hnsw_times)*1000])
    plt.ylabel('Time (ms)')
    plt.title('Average Query Time Comparison')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.hist(hnsw_accuracies, bins=10, edgecolor='black')
    plt.xlabel('Recall')
    plt.ylabel('Frequency')
    plt.title('HNSW Recall Distribution')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def demo_4_parameter_impact():
    """演示4：不同参数对HNSW性能的影响"""
    print("\n" + "="*50)
    print("演示4：HNSW参数影响分析")
    print("="*50)
    
    # 生成测试数据
    np.random.seed(45)
    n_samples = 500
    dimensions = 8
    
    print(f"生成{n_samples}个{dimensions}维测试数据...")
    data = np.random.randn(n_samples, dimensions)
    
    # 测试不同的M值
    M_values = [4, 8, 16, 32]
    ef_values = [50, 100, 200]
    
    results = []
    
    import time
    
    for M in M_values:
        for ef in ef_values:
            print(f"\n测试 M={M}, ef={ef}")
            
            # 构建索引
            hnsw = SimpleHNSW(dim=dimensions, max_elements=n_samples, 
                             M=M, ef_construction=ef)
            
            start_time = time.time()
            for point in data:
                hnsw.insert(point)
            build_time = time.time() - start_time
            
            # 测试查询性能
            n_queries = 20
            queries = data[np.random.choice(n_samples, n_queries, replace=False)]
            k = 10
            
            search_times = []
            recalls = []
            
            for query in queries:
                # HNSW搜索
                start_time = time.time()
                hnsw_results = hnsw.search(query, k=k, ef=ef)
                search_time = time.time() - start_time
                search_times.append(search_time)
                
                # 线性搜索（基准）
                distances = [(idx, hnsw.cosine_similarity(query, data[idx])) 
                           for idx in range(n_samples)]
                true_results = set([idx for idx, _ in 
                                   sorted(distances, key=lambda x: -x[1])[:k]])
                
                hnsw_ids = set([idx for idx, _ in hnsw_results])
                recall = len(hnsw_ids.intersection(true_results)) / k
                recalls.append(recall)
            
            results.append({
                'M': M,
                'ef': ef,
                'build_time': build_time,
                'search_time': np.mean(search_times),
                'recall': np.mean(recalls)
            })
            
            print(f"  构建时间: {build_time:.3f}秒")
            print(f"  平均搜索时间: {np.mean(search_times)*1000:.3f}毫秒")
            print(f"  平均召回率: {np.mean(recalls):.2%}")
    
    # 绘制结果
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    for ef in ef_values:
        ef_results = [r for r in results if r['ef'] == ef]
        M_vals = [r['M'] for r in ef_results]
        
        # 构建时间
        axes[0].plot(M_vals, [r['build_time'] for r in ef_results], 
                    marker='o', label=f'ef={ef}')
        
        # 搜索时间
        axes[1].plot(M_vals, [r['search_time']*1000 for r in ef_results], 
                    marker='s', label=f'ef={ef}')
        
        # 召回率
        axes[2].plot(M_vals, [r['recall']*100 for r in ef_results], 
                    marker='^', label=f'ef={ef}')
    
    axes[0].set_xlabel('M')
    axes[0].set_ylabel('Build Time (s)')
    axes[0].set_title('Build Time vs M')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    axes[1].set_xlabel('M')
    axes[1].set_ylabel('Search Time (ms)')
    axes[1].set_title('Search Time vs M')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    axes[2].set_xlabel('M')
    axes[2].set_ylabel('Recall (%)')
    axes[2].set_title('Recall vs M')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# ==================== 主程序 ====================

if __name__ == "__main__":
    print("HNSW (Hierarchical Navigable Small World) 演示程序")
    print("作者：一个简化的HNSW实现")
    print("="*60)
    
    # 运行所有演示
    demo_1_simple_insertion()
    # demo_2_random_data()
    # demo_3_performance_comparison()
    # demo_4_parameter_impact()
    
    print("\n" + "="*60)
    print("演示完成！")
    print("="*60)