import numpy
import matplotlib.pyplot as plt
import random

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

    def draw(self):
        plt.plot(self.location.get_x(),self.location.get_y(),self.color)

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
    def draw(self):
        self.start.draw()
        self.end.draw()
        #create line segment from start to end
        plt.plot((self.start.location.x,self.end.location.x),(self.start.location.y,self.end.location.y),self.color)


class graph:
    def __init__(self,vertices = [],edges = [], pointset = {}):
        self.vertices= vertices
        self.edges = edges
        self.pointset = pointset
        random.seed()

        if not vertices and not edges and not pointset:
            #default init creates 25 vertices in a line with random coordinates
            for i in range(25):
                xs = random.randint(-10, 10)
                ys = random.randint(-10, 10)
                self.vertices.append(vertex(chr(i+41),point(xs,ys)))
            for i in range(24):
                self.add_edge(edge(self.vertices[i],self.vertices[i+1]))

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
        for e in self.edges:
            e.draw()
        plt.show()


if __name__ == "__main__":
    G = graph()
    G.draw()