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
        self.xy =[xcoo,ycoo]

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_x(self,newx):
        self.x = newx
    def sety(self,newy):
        self.y = newy
    def __str__(self):
        return "{" + str(self.x) + "_" + str(self.y) + "}"
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
        toret = []
        for item in list:
            if item == last:
                continue
            toret.append( item)
            last = item
        return toret

    def __init__(self,vertices, edges, pointset,nm="default",dbug = True):
        self.vertices= vertices
        self.edges = edges
        self.pointset = pointset
        random.seed()
        self.name = nm
        self.crossing_number = 0
        self.debug = dbug

    def set_pointset(self,newp):
        self.pointset=newp
    def get_pointset(self):
        return self.pointset

    def create_random_line_graph(self,num_vertices = 25,low_end = -10,high_end = 10,integer=True):
        #removes any vertices or edges that already exist
        self.vertices = []
        self.edges = []
        newps = self.create_random_pointset(low_end,high_end,num_vertices,integer)
        self.set_pointset(newps)
        count = 0
        for pt in self.pointset:
            self.vertices.append(Vertex(chr(count + 65), Point(pt[0], pt[1])))
            count =count + 1

        for i in range(len(self.get_pointset())-1):
            try:
                self.add_edge(Edge(self.vertices[i], self.vertices[i + 1]))
            except(IndexError):
                print("index error... graph:")
                print(self)

        self.compute_crossing_number_quad()

    def create_random_pointset(self,lower_bound,upper_bound,num_points = 25,integer=True):
        random.seed()
        ps = []
        for i in range(num_points):
            if integer:
                ps.append([random.randint(lower_bound, upper_bound),random.randint(lower_bound, upper_bound)])
            else:
                ps.append([random.random() * abs(upper_bound-lower_bound)+lower_bound, random.random() * abs(upper_bound-lower_bound)+lower_bound])
        ps=sorted(ps)
        new = Graph.unique(ps)
        return new

    def add_vertex(self,v):
        for ver in self.vertices:
            if ver == v:
                return
        self.vertices.append(v)

    def add_point(self,p):
        for po in self.pointset:
            if po == p:
                return
        self.pointset.append(p)

    def add_edge(self,newe):
        for e in self.edges:
            #enforce uniqueness by undirected edge equality
            if e.undirected_eq(newe):
                return
        self.edges.append(newe)

    def add_edge_by_vname(self,vertexa,vertexb):
        toadd = Edge(None,None)
        for v in self.vertices:
            if v.name == vertexa:
                toadd.set_start_vertex(v)
            if v.name == vertexb:
                toadd.set_end_vertex(v)
        self.add_edge(toadd)

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def edge_swap(self, edge, recompute_cross_num = False):
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
        if recompute_cross_num:
            self.compute_crossing_number_quad()

    def edge_swap_by_vertex_names(self, vertexa, vertexb,recompute_crossing_num = True):
        for e in self.edges:
            if e.start.name == vertexa and e.end.name == vertexb:
                self.edge_swap(e,recompute_crossing_num)
                return

    def vertex_swap(self,vertexa,vertexb,recompute_cross_num = False):
        start_point = None
        end_point = None
        #swaps vertex and b - finds the vertices by name
        for v in self.vertices:
            if v.name == vertexa:
                start_point = v.location
            if v.name == vertexb:
                end_point = v.location
        if start_point and end_point:
            for v in self.vertices:
                if v.name == vertexa:
                    v.location = end_point
                if v.name == vertexb:
                    v.location = start_point
            if recompute_cross_num:
                return self.compute_crossing_number_quad()
        else:
            return "vertex not found"

    def compute_crossing_number_quad(self):#quadratic time implementation
        count = 1
        cross_num = 0
        for e in self.edges:
            #line for first edge is 1start + x 1end, where x
            first_start = e.start.location
            try:
                first_end = Point(e.end.location.x-e.start.location.x,e.end.location.y - e.start.location.y)
            except AttributeError:
                print("err")
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
                        print("found crossing between edges " + str(e) + " and " + str(self.edges[check_inx+count]))
            count = count + 1
        self.crossing_number = cross_num
        return cross_num

    def draw(self,save = False):
        plt.close()
        plt.title(self.name)
        leg_str = "crossing number: " + str(self.crossing_number)
        plt.figtext(0.12,0.85,leg_str)
        for e in self.edges:
            e.draw()
        if save:
            plt.savefig(self.name)

        plt.show()

    def print(self,name):
        #does nothing if name not specified
        if name != 'sys.stdout':
            fl = open(name,'w')
            print(self,file = fl)

    def __str__(self):
        returnstr = self.name + " "
        for e in self.edges:
            returnstr = returnstr + str(e)
        return returnstr + "\n"

    def save_to_file(self, filenam):
        f = open(filenam,'a+')
        f.write(self.__str__())
        f.close()

    def import_from_string(self,line):
        try:
            self.name, dat = line.split(" ")
            edges = dat.split(";")
            if edges[-1] == '\n':
                edges = edges[:-1]
            for edge in edges:
                edge = edge[1:-1]
                vertices = edge.split(",")
                nms = []
                for v in vertices:
                    v = v[1:-2]
                    nm, point = v.split(":")
                    nms.append(nm)
                    point = point[1:]
                    xo, yo = point.split("_")
                    x = float(xo)
                    y = float(yo)
                    p = Point(x, y)
                    self.add_vertex(Vertex(nm, p))
                    self.add_point(p)
                self.add_edge_by_vname(nms[0], nms[1])
        except ValueError:
            print("value error something went wrong!")
        self.compute_crossing_number_quad()
        return self

    def read_from_open_file(self,f):
        line = f.readline()
        self.import_from_string(line)

        self.compute_crossing_number_quad()
        return self

    def read_from_file(self,filename):
        try:
            f = open(filename,'r')
            self.read_from_open_file(f)
            f.close()
        except FileNotFoundError:
            print("file not found")
        return self

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
        return self

    def randomize_vertex_locations(self):
        #randomizes point set assignments - assumes count of point set is same as num vertices

        ps = np.random.permutation(self.pointset)
        count = 0
        for v in self.vertices:
            v.location = Point(ps[count][0],ps[count][1])
            count = count + 1
        self.crossing_number = self.compute_crossing_number_quad()
        return self

    def test_edge_swaps_nonstrictly_increasing_crossings(self,debug = False,draw=False):
        #returns false if does not find an edge that decreases the number of swaps
        #returns true if all swaps keep the same or larger crossing number
        start_num = self.crossing_number
        for edge in self.edges:
            #try swapping along edge
            self.edge_swap(edge, True)
            if debug:
                input("edge " + str(edge) + " swapped. press enter to continue")
            if draw:
                self.draw()

            if self.crossing_number < start_num and start_num != 0:
                return False
            #undo swap
            self.edge_swap(edge, True)

        return True

    def test_edge_swaps_strictly_increasing_crossings(self,debug=False,draw=False):
        #returns true if all swaps increase the number of crossings
        #assumes start crossing is not zero
        start_num = self.crossing_number
        for edge in self.edges:
            self.edge_swap(edge, True)
            if (draw):
                input("performed swap on edge " + str(edge) + ". Press enter to continue.")
            if draw:
                self.draw()

            if self.crossing_number <= start_num:
                return False
            #undo swap
            self.edge_swap(edge)
        return True

    def test_vertex_swaps_strictly_increasing_crossings(self,debug=False,draw=False):
        #run through all n choose 2 vertex choices, swap them, and compute crossing number
        start_num = self.crossing_number
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)-i-1):
                if draw:
                    self.draw()
                self.vertex_swap(self.vertices[i].name,self.vertices[i+j+1].name,True)
                if debug:
                    print("swapped vertex " + self.vertices[i].name + " and " + self.vertices[i+j+1].name)
                if draw:
                    self.draw()
                if self.crossing_number <= start_num:
                    return False


                #swap back
                self.vertex_swap(self.vertices[i].name,self.vertices[i+j+1].name,True)
        return True


def test_random_swaps(num_graphs,fn,debug=True,draw=True,integer = True,num_vertices = 25,test_to_run = "edge swaps strictly increasing crossing number"):
    #create a bunch of random line graphs
    graphs = []
    if debug:
        print("beginning test...")
        print("creating graphs...")
    for i in range(num_graphs):
        graphs.append(Graph([],[],[],"graph_"+str(i),dbug=False))
        graphs[i].create_random_line_graph(num_vertices= num_vertices,integer=integer)
        graphs[i].compute_crossing_number_quad()
    if debug:
        print("done.")
        print("starting swaps...")
    result_graphs = []
    count = 0
    for g in graphs:
        if debug:
            print("performing all swaps on graph " + str(count) + ": " + str(g))
        start_crosses = g.crossing_number

        while start_crosses == 0 :
            g.randomize_vertex_locations()
            start_crosses=g.crossing_number
        if test_to_run == "edge swaps strictly increasing crossing number":
            swap_found_indicator = g.test_edge_swaps_strictly_increasing_crossings(debug,draw)
        elif test_to_run == "vertex swaps strictly increasing crossing number":
            swap_found_indicator = g.test_vertex_swaps_strictly_increasing_crossings(debug,draw)
        elif test_to_run == "edge swaps non strictly increasing crossing number":
            swap_found_indicator = g.test_edge_swaps_nonstrictly_increasing_crossings(debug, draw)
        else:
            swap_found_indicator = g.test_edge_swaps_strictly_increasing_crossings(debug,draw)

        if swap_found_indicator:
            if debug:
                if test_to_run == "edge swaps strictly increasing crossing number":
                    print("graph found for which all edge swaps strictly increase crossing number")
                elif test_to_run == "vertex swaps strictly increasing crossing number":
                    print("graph found for which all vertex swaps strictly increase crossing number")
            result_graphs.append(g)
        if debug:
            print("done.")
        count = count+1

    if result_graphs:
        if test_to_run == "edge swaps strictly increasing crossing number":
            print("graph found for which all edge swaps strictly increase crossing number")
        elif test_to_run == "vertex swaps strictly increasing crossing number":
            print("graph found for which all vertex swaps strictly increase crossing number")
        if debug:
            print(str(result_graphs))
        for g in result_graphs:
            g.save_to_file(fn)
    elif debug:
        if test_to_run == "edge swap strictly increasing crossing number":
            print("no graph found for which all edge swaps strictly increase crossing number")
        elif test_to_run == "vertex swap strictly increasing crossing number":
            print("no graph found for which all vertex swaps strictly increase crossing number")

    return result_graphs

def load_graph_from_file_and_draw(filename):
    g = Graph([],[],[])
    g.read_from_file(filename)
    g.draw()

def load_all_graphs_from_file_and_draw(filename):
    f = open(filename,'r')
    lines = f.readlines()
    for l in lines:
        g = Graph([],[],[])
        g.import_from_string(l)
        g.draw()
        input("press enter for next graph")


# if __name__ == "__main__":
    #load_all_graphs_from_file_and_draw("test")

    #create a random sampling of graphs
    # uncrossable = test_random_swaps(10000,"test",debug=False,draw=False,integer=False,num_vertices=5,test_to_run="edge swaps strictly increasing crossing number")
    # if (uncrossable):
    #     print("Graphs found for which there is no swap to decrease the number of crossings.")
    #     for g in uncrossable:
    #         print(str(g))
    #         g.draw()
    #         input("press enter for next graph")
    # else:
    #     print("no graphs discovered.")


    # g = Graph([Vertex("A",Point(5,5)),Vertex("B",Point(-5,-3)),Vertex("C",Point(-5.5,-6)),Vertex("D",Point(-3,-6)),Vertex("E",Point(-3,-4)),Vertex("F",Point(-5,5)),Vertex("G",Point(-6,6)),Vertex("H",Point(-7,5)),Vertex("I",Point(-6,3)),Vertex("J",Point(5,3)),Vertex("Start",Point(7,7)),Vertex("End",Point(7,2))],[],[],"test")
    # g.add_edge_by_vname("Start","A")
    # g.add_edge_by_vname("A", "B")
    # g.add_edge_by_vname("B", "C")
    # g.add_edge_by_vname("C","D")
    # g.add_edge_by_vname("D", "E")
    # g.add_edge_by_vname("E", "F")
    # g.add_edge_by_vname("F", "G")
    # g.add_edge_by_vname("G", "H")
    # g.add_edge_by_vname("H", "I")
    # g.add_edge_by_vname("I","J")
    # g.add_edge_by_vname("End", "J")
    # g.compute_crossing_number_quad()
    # g.draw()
    #
    # g.vertex_swap("A","E")
    # g.compute_crossing_number_quad()
    # g.draw()

    # if g.test_vertex_swaps_strictly_increasing_crossings(True,True):
    #     print("true")
    # else:
    #     print("false")


    # h = Graph([],[],[],"path edge swap counter ex")
    # f = open("test")
    # lines = f.readlines()
    # h.import_from_string(lines[0])
    # h.draw()
    # h.test_edge_swaps_strictly_increasing_crossings(debug=False,draw=True)
    #
    # test = Graph([],[],[],"Swapping Along Path")
    # #test.import_from_string("graph001 [(A:{0.925102539854235_-6.4913894645684}),(B:{5.0744512190386555_0.07406038703589068})];[(B:{5.0744512190386555_0.07406038703589068}),(C:{-0.8098839793382488_2.885357906603561})];[(C:{-0.8098839793382488_2.885357906603561}),(D:{-8.014684207276694_-1.062338745843423})];[(D:{-8.014684207276694_-1.062338745843423}),(E:{4.338677299678215_-4.2107695421734554})];")
    # test.create_random_line_graph(5,-5,5,False)
    # test.randomize_vertex_locations()
    # test.compute_crossing_number_quad()
    # test.draw()
    #test.test_edge_swaps_strictly_increasing_crossings(True,True)