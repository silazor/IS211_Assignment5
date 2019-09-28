import random

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        # return TRUE if self.items euqal empty array
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Server:
    # The server class tracks if it has a task
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        #print('tic')
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                print(f"Setting current task to NONE!!!! {self.time_remaining}")
                self.current_task = None
        else:
            print(self.current_task)

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self,new_task):
        self.current_task = new_task
        #self.time_remaining = new_task.get_pages() * 60 / self.process_time
        self.time_remaining = new_task.get_process_time()

class Request:
    # A single Server request
    def __init__(self, request):
        self.simulation_time = request[0]
        self.file_to_get = request[1]
        self.process_time = request[2]

    def get_stamp(self):
        return self.timestamp

    def get_process_time(self):
        print(f"process time is {self.process_time}")
        return self.process_time

    def wait_time(self, current_time):
        #return current_time - self.simulation_time
        return 0

def simulateOneServer(input_file_name):
    '''
    The simulateOneServer() function is responsible for printing out the average wait time for a request (i.e.,
how long, on average, did a request stay in the server queue before being processed). The simulate function
should return this average.
    for line in open('./source.txt'):
        print line
    '''
    #7, /images/test.gif, 1
    requests = [ [7, '/images/test.gif', 1], [8, '/faart/burp.gif', 10], [8, '/eat/shit.jpg', 2] ]
    one_server = Server()
    waiting_times = []
    server_queue = Queue()
    for client_request in requests:
        request_object = Request(client_request)
        # 7, 1 sec to process
        server_queue.enqueue(request_object)
        print(f"Is the server busy? --> {one_server.busy()}")
        print(f"Is the Queue empty? --> {server_queue.is_empty()}")
        if (not one_server.busy()): # and (not server_queue.is_empty()):
            next_task = server_queue.dequeue()
            waiting_times.append(next_task.wait_time(client_request[0]))
            print(f"Working on {client_request[1]}")
            one_server.start_next(next_task)
        else:
            print(f'fng busy brah Server:{one_server.busy()} Queue:{server_queue.is_empty()}')

        while one_server.time_remaining > 0:
            one_server.tick()
    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining."
    %(average_wait, server_queue.size()))

def main():
    # TODO add argparse to point to file
    simulateOneServer('./source.txt')

if __name__ == '__main__':
    main()
