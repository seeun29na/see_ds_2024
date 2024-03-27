#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PAGE_NUM 10000

typedef struct Node {
    char page[20];
    struct Node* prev;
    struct Node* next;
} Node;

typedef struct {
    Node* head;
    Node* tail;
    int cache_slots;
    int cache_hit;
    int tot_cnt;
} CacheSimulator;

void initCacheSimulator(CacheSimulator* sim, int cache_slots) {
    sim->head = sim->tail = NULL;
    sim->cache_slots = cache_slots;
    sim->cache_hit = 0;
    sim->tot_cnt = 0;
}

void insertPage(CacheSimulator* sim, char* page) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    strcpy(newNode->page, page);
    newNode->next = sim->head;
    newNode->prev = NULL;
    if (sim->head != NULL) sim->head->prev = newNode;
    sim->head = newNode;
    if (sim->tail == NULL) sim->tail = newNode;

    // 캐시 슬롯 수를 초과하는 경우, 가장 오래된 페이지 제거
    if (sim->tot_cnt >= sim->cache_slots) { // tot_cnt가 cache_slots와 같거나 크면 오래된 페이지 제거
        Node* temp = sim->tail;
        sim->tail = sim->tail->prev;
        if (sim->tail != NULL) sim->tail->next = NULL;
        free(temp);
    } else {
        sim->tot_cnt++; // 캐시에 새로운 페이지를 추가하는 경우에만 tot_cnt 증가
    }
}


int isPageInCache(CacheSimulator* sim, char* page) {
    Node* temp = sim->head;
    while (temp != NULL) {
        if (strcmp(temp->page, page) == 0) {
            if (temp->prev != NULL) {
                temp->prev->next = temp->next;
                if (temp->next != NULL) {
                    temp->next->prev = temp->prev;
                } else {
                    sim->tail = temp->prev;
                }
                temp->next = sim->head;
                temp->prev = NULL;
                sim->head->prev = temp;
                sim->head = temp;
            }
            sim->cache_hit++;
            return 1;
        }
        temp = temp->next;
    }
    return 0;
}


void doSim(CacheSimulator* sim, char* page) {
    sim->tot_cnt++; // 전체 페이지 요청 수를 증가
    if (!isPageInCache(sim, page)) {
        insertPage(sim, page);
    }
}


void printStats(CacheSimulator* sim) {
    printf("cache_slot =  %d cache_hit =  %d hit ratio =  %.9f\n",
           sim->cache_slots, sim->cache_hit, (double)sim->cache_hit / sim->tot_cnt);
}

int main() {
    FILE* data_file = fopen("lru_sim/linkbench.trc", "r");
    if (data_file == NULL) {
        printf("File not found\n");
        return 1;
    }
    char line[1024];

    for (int cache_slots = 100; cache_slots <= 1000; cache_slots += 100) {
        CacheSimulator cache_sim;
        initCacheSimulator(&cache_sim, cache_slots);

        while (fgets(line, sizeof(line), data_file)) {
            char* page = strtok(line, " \n");
            doSim(&cache_sim, page);
        }

        printStats(&cache_sim);
        fseek(data_file, 0, SEEK_SET); // 파일 포인터를 다시 파일의 시작으로 이동
    }

    fclose(data_file);
    return 0;
}
