class LRUCache:
    def __init__(self, capacity: int):
        self.cache = []
        self.capacity = capacity

    def get(self, key: int) -> int:
        for i, (k, v) in enumerate(self.cache):
            if k == key:
                # hit: 해당 항목을 MRU로 이동
                self.cache.append(self.cache.pop(i))
                return v
        # miss
        return -1

    def put(self, key: int, value: int) -> None:
        for i, (k, v) in enumerate(self.cache):
            if k == key:
                # Key가 이미 존재하면 값을 업데이트하고 MRU로 이동
                self.cache.pop(i)
                break
        else:
            # 캐시가 가득 찼다면 LRU 항목 제거
            if len(self.cache) >= self.capacity:
                self.cache.pop(0)
        # 새 항목을 MRU 위치에 추가
        self.cache.append((key, value))


class CacheSimulator:
    def __init__(self, cache_slots):
        self.cache_slots = cache_slots
        self.cache = LRUCache(cache_slots)  # 수정된 부분
        self.cache_hit = 0
        self.tot_cnt = 1

    
    def do_sim(self, page):
        self.tot_cnt += 1

        # 페이지가 캐시에 이미 있는지 확인
        if self.cache.get(page) == -1:
            # 캐시 미스 처리
            if len(self.cache.cache) >= self.cache_slots:
                # 캐시가 가득 찼다면, LRUCache 클래스 내부 로직이 가장 오래된 항목을 처리하므로 별도의 처리 불필요
                pass
            # 새 페이지를 캐시에 추가
            self.cache.put(page, 1)  # 페이지 값을 1로 설정 (실제 값은 중요하지 않음, 존재 여부만 중요)
        else:
            # 캐시 히트 발생, LRUCache.get 메서드가 이미 MRU로 업데이트를 처리함
            self.cache_hit += 1


    def get_hit_ratio(self):
        # 캐시 히트 비율 계산
        return self.cache_hit / self.tot_cnt if self.tot_cnt > 0 else 0
         
    def print_stats(self):
        print("cache_slot = ", self.cache_slots, "cache_hit = ", self.cache_hit, "hit ratio = ", self.cache_hit / self.tot_cnt)


if __name__ == "__main__":

    data_file = open("lru_sim/linkbench.trc")
    lines = data_file.readlines()
    for cache_slots in range(100, 1001, 100):
        cache_sim = CacheSimulator(cache_slots)
        for line in lines:
            page = line.split()[0]
            cache_sim.do_sim(page)
        
        cache_sim.print_stats()