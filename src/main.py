from views.pygame import pygame_start_game
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

        for t in threads:
            t.start()
            
        for t in threads:
            t.join()
    else:
        pygame_start_game()