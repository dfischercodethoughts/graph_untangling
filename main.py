import numpy
import matplotlib.pyplot as plt
import random


#todo: read/write graphs to/from file
#todo: read graphs from plantri output
#todo: function to create linegraph


class point:
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


class vertex:
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


class edge:
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


class graph:

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

    def __init__(self,vertices, edges, pointset):
        self.vertices= vertices
        self.edges = edges
        self.pointset = pointset
        random.seed()

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
            self.vertices.append(vertex(chr(count + 65), point(pt[0], pt[1])))
            count =count + 1

        for i in range(num_vertices-1):
            try:
                self.add_edge(edge(self.vertices[i], self.vertices[i + 1]))
            except(IndexError):
                print("index error... graph:")
                print(self)

    def create_random_pointset(self,lower_bound,upper_bound,num_points = 25):
        ps = []
        for i in range(num_points):
            ps.append([random.randint(lower_bound, upper_bound),random.randint(lower_bound, upper_bound)])
        return graph.unique(sorted(ps))

    def add_vertex(self,v):
        self.vertices.append(v)

    def add_edge(self,newe):
        self.edges.append(newe)

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def swap(self,edge):
        #swaps the locations of the vertices at the ends of the edge
        for i in self.vertices:
            if i.location.x == edge.start.location.x and i.location.y == edge.start.location.y:
                i.location.x = edge.end.location.x
                i.location.y = edge.end.lcoation.y
            if i.location.x == edge.end.location.x and i.location.y == edge.end.location.y:
                i.location.x = edge.start.location.x
                i.location.y = edge.start.location.y

    def draw(self):
        plt.close()
        for e in self.edges:
            e.draw()
        plt.show()

    def print(self,file = 'sys.stdout'):
        #appends
        if file != 'sys.stdout':
            fl = open(file,'w')
            for e in self.edges:
                print(e,file= fl)
            fl.close()

    def __str__(self):
        returnstr = "Graph: "
        for e in self.edges:
            returnstr = returnstr + str(e)
        return returnstr + "\n"


if __name__ == "__main__":
    G = graph([],[],[])
    G.draw()
    print(G)