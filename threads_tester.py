import time
import threading
import itertools

rLock = threading.RLock()


# common_data_print = "Common data"
# shared_buffer = []


def data_visualization_calculations(visual):
    # global shared_buffer
    rLock.acquire()
    print("data_visualization_thread")
    # shared_buffer.append("done visualization")
    rLock.release()
    time.sleep(1)

    visual = "visual obj"
    print("ending visual thread")
    return visual


def a_star_run_wrapper(path, total_cost, stop_event: threading.Event):
    # global shared_buffer

    while not stop_event.is_set():
        # while True:
        rLock.acquire()
        print("astar_thread")
        # shared_buffer.append("atar")
        rLock.release()
        time.sleep(2)

    path = "some path"
    total_cost= 100
    print("Ending astar thread")
    return path, total_cost


def timer_thread(delay_duration: int, stop_event: threading.Event, a_star_thread: threading.Thread):
    time.sleep(delay_duration)
    if a_star_thread.is_alive():
        print("stopping astar from timer thread: ", stop_event.set())


if __name__ == "__main__":
    duration = 5

    path = None
    total_cost = None
    visual = None

    astar_stop_event = threading.Event()
    astar_thread = threading.Thread(target=a_star_run_wrapper, args=(path, total_cost, astar_stop_event,))

    data_visual_thread = threading.Thread(target=data_visualization_calculations, args=(visual,))

    timer_thread = threading.Thread(target=timer_thread, args=(duration, astar_stop_event, astar_thread))

    timer_thread.start()
    data_visual_thread.start()
    astar_out = astar_thread.start()

    visual = data_visual_thread.join()
    print(f"path: {path}, totalCost:{total_cost}, visual:{visual}")

    path, total_cost =  astar_thread.join()
    print(f"path: {path}, totalCost:{total_cost}, visual:{visual}")

    print("all threads ended ")
    # print("shared buffer ", shared_buffer)
