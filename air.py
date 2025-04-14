import sys
import heapq
import customtkinter as ctk
from tkinter import messagebox
import math

# Define air route graph as adjacency list
graph = {
    'CHANDIGARH': {'DELHI': 4, 'AMBALA': 3},
    'DELHI': {'CHANDIGARH': 4, 'SHIMLA': 5, 'AMBALA': 12},
    'AMBALA': {'CHANDIGARH': 3, 'DEHRADUN': 7, 'DELHI': 12, 'HINDON':7},
    'SHIMLA': {'DELHI': 5, 'AMRITSAR': 16},
    'DEHRADUN': {'AMBALA': 7, 'HINDON': 2, 'SHIMLA': 10},
    'HINDON': {'DEHRADUN': 2, 'CHANDIGARH': 5, 'AMBALA': 7},
    'AMRITSAR': {'SHIMLA': 16, 'DELHI': 5}
}

# Positions for heuristic calculations (approximate coordinates)
airport_positions = {
    'CHANDIGARH': (150, 150),
    'DELHI': (400, 150),
    'AMBALA': (275, 275),
    'SHIMLA': (400, 470),
    'DEHRADUN': (275, 400),
    'HINDON': (350, 350),
    'AMRITSAR': (450, 400)
}

# Heuristic function (Euclidean distance)
def heuristic(airport1, airport2):
    x1, y1 = airport_positions[airport1]
    x2, y2 = airport_positions[airport2]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# A* Algorithm
def a_star(graph, start_airport, end_airport):
    open_set = [(0, start_airport)]  # (priority, airport)
    g_score = {airport: sys.maxsize for airport in graph}
    g_score[start_airport] = 0
    f_score = {airport: sys.maxsize for airport in graph}
    f_score[start_airport] = heuristic(start_airport, end_airport)
    previous = {airport: None for airport in graph}

    while open_set:
        _, current_airport = heapq.heappop(open_set)
        
        if current_airport == end_airport:
            route = []
            while current_airport:
                route.append(current_airport)
                current_airport = previous[current_airport]
            return route[::-1], g_score[end_airport]

        for neighbor, weight in graph[current_airport].items():
            tentative_g_score = g_score[current_airport] + weight
            if tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end_airport)
                previous[neighbor] = current_airport
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return [], sys.maxsize  # No path found

# GUI Setup
root = ctk.CTk()
root.title("A* Path Finder")

# Create the canvas
canvas = ctk.CTkCanvas(root, width=500, height=500, bg="white")
canvas.pack(pady=(10, 20))

# Functions to Draw and Highlight
def draw_graph():
    canvas.delete("all")  
    for airport, neighbors in graph.items():
        x1, y1 = airport_positions[airport]
        for neighbor, weight in neighbors.items():
            x2, y2 = airport_positions[neighbor]
            canvas.create_line(x1, y1, x2, y2, fill='gray')
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
            canvas.create_text(mid_x, mid_y, text=str(weight), font=("Arial", 10), fill="black")
        canvas.create_oval(x1-5, y1-5, x1+5, y1+5, fill='blue')
        canvas.create_text(x1, y1-10, text=airport, font=("Arial", 10))

def highlight_path(route):
    for i in range(len(route) - 1):
        x1, y1 = airport_positions[route[i]]
        x2, y2 = airport_positions[route[i + 1]]
        canvas.create_line(x1, y1, x2, y2, fill='red', width=2)

#Graph
draw_graph()

dropdown_frame = ctk.CTkFrame(root)
dropdown_frame.pack(pady=(20, 10))

ctk.CTkLabel(dropdown_frame, text="Starting Port:").grid(row=0, column=0, padx=10)
start_combobox = ctk.CTkComboBox(dropdown_frame, values=list(graph.keys()))
start_combobox.grid(row=0, column=1, padx=10)

ctk.CTkLabel(dropdown_frame, text="Destination Port:").grid(row=0, column=2, padx=10)
end_combobox = ctk.CTkComboBox(dropdown_frame, values=list(graph.keys()))
end_combobox.grid(row=0, column=3, padx=10)

button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=(10, 20))

route_text = ctk.StringVar()
distance_text = ctk.StringVar()

def find_route():
    start_airport = start_combobox.get().strip().upper()
    end_airport = end_combobox.get().strip().upper()

    if start_airport not in graph or end_airport not in graph:
        messagebox.showerror("Error", "Invalid airport code.")
        return

    draw_graph()
    route, distance = a_star(graph, start_airport, end_airport)

    if distance == sys.maxsize:
        messagebox.showinfo("Result", "No route found.")
        return

    highlight_path(route)
    route_text.set(" -> ".join(route))
    distance_text.set(f"{distance} km")

find_button = ctk.CTkButton(button_frame, text="Find Route", command=find_route)
find_button.grid(row=0, column=0, padx=10)

def reset():
    start_combobox.set("")
    end_combobox.set("")
    route_text.set("")
    distance_text.set("")
    draw_graph()

reset_button = ctk.CTkButton(button_frame, text="Reset", command=reset, fg_color="red", hover_color="#cc0000")
reset_button.grid(row=0, column=1, padx=10)

result_frame = ctk.CTkFrame(root)
result_frame.pack(pady=(10, 20))

ctk.CTkLabel(result_frame, text="Shortest Route:", font=("Arial", 12, "bold")).pack()
route_label = ctk.CTkLabel(result_frame, textvariable=route_text, font=("Arial", 12))
route_label.pack()

ctk.CTkLabel(result_frame, text="Shortest Distance:", font=("Arial", 12, "bold")).pack()
distance_label = ctk.CTkLabel(result_frame, textvariable=distance_text, font=("Arial", 12))
distance_label.pack()

root.mainloop()