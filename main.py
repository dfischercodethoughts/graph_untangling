import numpy as np
import matplotlib.pyplot as plt
import random


#todo: read/write graphs to/from file
#todo: read graphs from plantri output
#todo: function to create random sequence of swaps


class Point:
    def __init__(self,xcoo,ycoo):
        self.x = xcoo
        self.y = ycoo

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_x(self,newx):
        self.x = newx
    def sety(self,newy):
        self.y = newy
    def __str__(self):
        return "{" + str(self.x) + "," + str(self.y) + "}"
    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False


class Vertex:
    color = 'ko'

    def __init__(self,name,point):
        self.name = name
        self.location = point
    def get_name(self):
        return self.name
    def get_location(self):
        return self.location
    def set_name(self,newname):
        self.name = newname
    def set_location(self,newloc):
        self.location = newloc
    def __str__(self):
        return "(" + str(self.name) + ":" + str(self.location) + ")"
    def draw(self):
        plt.plot(self.location.get_x(),self.location.get_y(),self.color)
        plt.text(self.location.get_x()+.1,self.location.get_y()+.1,self.name)
    def __eq__(self, other):
        if self.name == other.name or (self.location == other.location):
            return True
        return False


class Edge:
    def __init__(self,startv,endv,clr='k'):
        self.start = startv
        self.end = endv
        self.color = clr

    def get_start_vertex(self):
        return self.start
    def get_end_vertex(self):
        return self.end
    def get_color(self):
        return self.color
    def set_start_vertex(self,news):
        self.start = news
    def set_end_vertex(self,newe):
        self.end = newe
    def set_color(self,newc):
        self.color = newc
    def __str__(self):
        return "[" + str(self.start) + "," + str(self.end) + "];"
    def draw(self):
        self.start.draw()
        self.end.draw()
        #create line segment from start to end
        plt.plot((self.start.location.x,self.end.location.x),(self.start.location.y,self.end.location.y),self.color)
    def __eq__(self, other):
        #default == operator is for directed edges - see undirected eq method
        if self.start.name == other.start.name and self.end.name == other.end.name:
            return True
        return False
    def undirected_eq(self,other):
        if self == other and other == self:
            return True
        return False

class Graph:
    ASCII_A =65

    @staticmethod
    def unique(list):
        #helper method to ensure unique points in pointset
        #assume list sorted
        last = None
        for item in list:
            if item == last:
                continue
            yield item
            last = item

    def __init__(self,vertices, edges, pointset,nm="default",dbug = True):
        self.vertices= vertices
        self.edges = edges
        self.pointset = pointset
        random.seed()
        self.name = nm
        self.crossing_number = 0
        self.debug = dbug

        if not vertices and not edges and not pointset:
            #default init creates 25 vertices in a line with random coordinates
            self.create_random_line_graph()

    def create_random_line_graph(self,num_vertices = 25,low_end = -10,high_end = 10):
        #removes any vertices or edges that already exist
        self.vertices = []
        self.edges = []
        self.pointset = self.create_random_pointset(low_end,high_end,num_vertices)
        count = 0
        for pt in self.pointset:
            self.vertices.append(Vertex(chr(count + 65), Point(pt[0], pt[1])))
            count =count + 1

        for i in range(num_vertices-1):
            try:
                self.add_edge(Edge(self.vertices[i], self.vertices[i + 1]))
            except(IndexError):
                print("index error... graph:")
                print(self)

        self.compute_crossing_number_quad()

    def create_random_pointset(self,lower_bound,upper_bound,num_points = 25):
        ps = []
        for i in range(num_points):
            ps.append([random.randint(lower_bound, upper_bound),random.randint(lower_bound, upper_bound)])
        return Graph.unique(sorted(ps))

    def add_vertex(self,v):
        for ver in self.vertices:
            if ver == v:
                return
        self.vertices.append(v)

    def add_edge(self,newe):
        for e in self.edges:
            #enforce uniqueness by undirected edge equality
            if e.undirected_eq(newe):
                return
        self.edges.append(newe)

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def swap(self,edge):
        startx = edge.start.location.x
        starty = edge.start.location.y
        endx = edge.end.location.x
        endy = edge.end.location.y
        #swaps the locations of the vertices at the ends of the edge
        for i in self.vertices:
            if i.name == edge.start.name:
                i.location.x = endx
                i.location.y = endy
            if i.name == edge.end.name:
                i.location.x = startx
                i.location.y = starty

    def swap_by_vertex_names(self,vertexa,vertexb):
        for e in self.edges:
            if e.start.name == vertexa and e.end.name == vertexb:
                self.swap(e)
                return

    def compute_crossing_number_quad(self):#quadratic time implementation
        count = 1
        cross_num = 0
        for e in self.edges:
            #line for first edge is 1start + x 1end, where x
            first_start = e.start.location
            first_end = Point(e.end.location.x-e.start.location.x,e.end.location.y - e.start.location.y)
            for check_inx in range(len(self.edges) - count):
                #credit to "Intersection of two lines in three-space" by Ronald Goldman, published in Graphics Gems, page 304
                #line for second edge is 2start + y 2end
                second_start = self.edges[check_inx+count].start.location
                second_end = Point(self.edges[check_inx+count].end.location.x - second_start.x,self.edges[check_inx+count].end.location.y - second_start.y)

                #want to find vals for x and y in 1start + x 1end = 2start + y 2end
                #can use cross product to solve for x and y - (1start + x 1end) cross 2end = (2start + 2end y)cross 2end
                                                            #  1start cross 2end + x 1end cross 2end = 2start cross 2end
                                                            # x = (2start cross 2end - 1start cross 2end)/(1end cross 2end)
                denom = (np.cross([second_end.x,second_end.y],[first_end.x,first_end.y]))
                if (denom == 0):#avoid dividing by zero
                    continue
                x = (np.cross([second_start.x,second_start.y],[second_end.x,second_end.y])-np.cross([first_start.x,first_start.y],[second_end.x,second_end.y]))/(-1*denom)
                #similar for y
                y = (np.cross([first_start.x-second_start.x,first_start.y-second_start.y],[first_end.x,first_end.y]))/denom
                #now, if x and y are in [0,1] we have an intersection. if not, we dont
                if 0 < x and x < 1 and 0 < y and y< 1:
                    cross_num = cross_num+1
                    if (self.debug):
                        print("found crossing on between edges " + str(e) + " and " + str(self.edges[check_inx+count]))
            count = count + 1
        self.crossing_number = cross_num
        return cross_num

    def draw(self):
        plt.close()
        plt.title(self.name)
        plt.legend("crossing number: " + str(self.crossing_number))
        for e in self.edges:
            e.draw()
        plt.show()

    def print(self,name):
        #does nothing if name not specified
        if name != 'sys.stdout':
            fl = open(name,'w')
            print(self,file = fl)

    def __str__(self):
        returnstr = "Graph: "
        for e in self.edges:
            returnstr = returnstr + str(e)
        return returnstr + "\n"

    def import_plantri_file(self,filename):
        file = open(filename,'r')
        line = file.readline()#plantri outputs one graph on each line
        parts = line.split(' ')
        try:
            num_vertices = int(parts[0])
            self.create_random_pointset(-10, 10, num_vertices)
            for i in range(num_vertices):
                self.add_vertex(Vertex(chr(65 + i),self.pointset[i]))

        except(TypeError):
            print("type error while importing plantri file")
            return




if __name__ == "__main__":
    G = Graph([],[],[],"First Graph")
    G.draw()
    print(G)

    #by creation of G, pointset is sorted by x coordinate
    #swap any two adjacent vertices so this is not the case
    print("crossing number: " + str(G.crossing_number) + "performing a series of swaps...")
    swaps = []

    for i in range(20):
        swaps.append(random.randint(0,len(G.edges)-1))
    for swap in swaps:
        print("swapping edge: "+str(swap) + ": " + str(G.edges[swap]))
        G.swap(G.edges[swap])

    G.draw()
    print("recomputing crossing number...")
    G.compute_crossing_number_quad()
    print("new crossing number: " + str(G.crossing_number))
    G.draw()
    print(G)
