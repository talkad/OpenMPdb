
int do_some(int i) {
    printf("you picked %d", i);
    return 0;
}

int do_some2(int i) {
    printf("you picked %d", i);
    return 0;
}

int main() {

    int i, sum = 0;

    #pragma omp parallel for
    for(i = 0; i < 10; i++){
        do_some(i);
        do_some2(i);
    }
}