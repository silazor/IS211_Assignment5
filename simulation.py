import argparse
import urllib.request
import csv
import codecs

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        # return TRUE if self.items euqal empty array
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Server:
    def __init__(self):
        self.current_task = None
        self.total_time_counter = 0
        self.last_execution_time = 0

    def get_total_time_counter(self):
        return self.total_time_counter

    def work(self, new_task, last_execution_time):
        if self.current_task != None:
            if self.total_time_counter == 0:
                self.total_time_counter = new_task.get_sim_time()
                #print(self.total_time_counter, new_task.get_request_process_time(), last_execution_time)
            else:
                self.total_time_counter = self.total_time_counter +  last_execution_time
                #print(self.total_time_counter, new_task.get_request_process_time(), last_execution_time)
            new_task.end_time = self.total_time_counter
            self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self,new_task):
        self.current_task = new_task

class Request:
    def __init__(self, request):
        self.simulation_time = request[0]
        self.file_to_get = request[1]
        self.process_time = request[2]
        self.end_time = 0

    def get_sim_time(self):
        return self.simulation_time

    def get_request_process_time(self):
        return self.process_time

    def wait_time(self):
        elapsed_time = self.end_time - self.simulation_time
        return int(elapsed_time)

def simulateOneServer(data):
    one_server = Server()
    server_queue = Queue()
    waiting_times = []
    last_task = None
    for client_request in data:
        int_client_request = []
        int_client_request.append(int(client_request[0]))
        int_client_request.append(client_request[1])
        int_client_request.append(int(client_request[2]))
        request_object = Request(int_client_request)

        server_queue.enqueue(request_object)
        #print(f"Is the server busy? --> {one_server.busy()}")
        #print(f"Is the Queue empty? --> {server_queue.is_empty()}")
        #print(f"Size of q is --> {server_queue.size()}")

        if (not one_server.busy())  and (not server_queue.is_empty()):
            if last_task == None:
                last_execution_time = 0
            else:
                last_execution_time = last_task.get_request_process_time()
            next_task = server_queue.dequeue()
            one_server.start_next(next_task)
            #one_server.tick()
            one_server.work(next_task, last_execution_time)
            #print(f"Total time-->{one_server.get_total_time_counter()}.  request time--> {next_task.get_sim_time()}")
            print("Request object lived this long %6.2f" %(one_server.get_total_time_counter() - next_task.get_sim_time()))
            waiting_times.append(next_task.wait_time())
            last_task = next_task

    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining."
    %(average_wait, server_queue.size()))

def simulateManyServers(num_servers, data):
    waiting_times = []
    last_task = None
    server_objects = []
    for server in num_servers:
        s = Server()
        server_objects.append(s)
    q_objects = []
    for q in num_servers:
        q = Queue()
        q_objects.append(q)

    for client_request in data:
        counter = 0
        int_client_request = []
        int_client_request.append(int(client_request[0]))
        int_client_request.append(client_request[1])
        int_client_request.append(int(client_request[2]))
        request_object = Request(int_client_request)

        if counter == len(server_objects):
            counter = 0
        q_objects[counter].enqueue(request_object)
        if (not server_objects[counter].busy())  and (not q_objects[counter].is_empty()):
            if last_task == None:
                last_execution_time = 0
            else:
                last_execution_time = last_task.get_request_process_time()
            next_task = q_objects[counter].dequeue()
            server_objects[counter].start_next(next_task)
            #one_server.tick()
            server_objects[counter].work(next_task, last_execution_time)
            #print(f"Total time-->{server_objects[counter].get_total_time_counter()}.  request time--> {next_task.get_sim_time()}")
            print("Request object lived this long %6.2f" %(server_objects[counter].get_total_time_counter() - next_task.get_sim_time()))
            waiting_times.append(next_task.wait_time())
            last_task = next_task
        counter+=1

    size = 0
    for q in q_objects:
        size = size + q.size()
    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs %3d tasks remaining."
    %(average_wait, size))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--servers')
    args = parser.parse_args()
    csvstream = urllib.request.urlopen(args.url)
    csv_data = csv.reader(codecs.iterdecode(csvstream, 'utf-8'))
    data = list(csv_data)
    if args.servers:
        simulateManyServers(args.servers, data)
    else:
        simulateOneServer(data)

if __name__ == '__main__':
    main()
