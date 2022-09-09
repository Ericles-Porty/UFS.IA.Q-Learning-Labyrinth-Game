from views.pygame import pygame_start_game, thread_verificadora
import threading

if __name__ == "__main__":
    thread_option = int(input("1 - Usar Threads\n0 - No Threads\n"))
    if thread_option == 1:
        quantidade_threads = int(input("Quantas threads deseja utilizar? "))
        threads = []
        for i in range(quantidade_threads):
            t = threading.Thread(target=pygame_start_game)
            t.daemon = True
            threads.append(t)

        e = threading.Thread(target=thread_verificadora)
        e.daemon = True

        for t in threads:
            t.start()
        e.start()
        for t in threads:
            t.join()
        e.join()
    else:
        t1 = threading.Thread(target=pygame_start_game)
        t1.daemon = True
        t2 = threading.Thread(target=thread_verificadora)
        t2.daemon = True
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    