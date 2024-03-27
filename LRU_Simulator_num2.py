import sys
sys.path.append("C:\\Users\\seeun\\OneDrive\\바탕 화면\\see_2024\\list")


from list.listNode import ListNode
from list.linkedListBasic import LinkedListBasic
from list.circularLinkedList import CircularLinkedList


class CacheSimulator:
    def __init__(self, cache_slots):
        self.cache = CircularLinkedList()
        self.cache_slots = cache_slots
        self.cache_hit = 0
        self.tot_cnt = 1
    
    def do_sim(self, page):
        self.tot_cnt += 1

        # 페이지가 캐시에 이미 있는지 확인
        if self.cache.count(page) > 0:
            # 캐시 히트 발생
            self.cache_hit += 1
            # LRU 전략을 위해, 캐시에서 해당 페이지를 제거하고 다시 삽입하여 가장 최근에 사용된 것으로 만듦
            self.cache.remove(page)
            self.cache.append(page)
        else:
            # 캐시 미스 처리. 캐시가 가득 찼다면, 가장 오래된 항목(첫 번째 항목)을 제거
            if self.cache.size() == self.cache_slots:
                self.cache.pop(0)
            # 새 페이지를 캐시에 추가
            self.cache.append(page)

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