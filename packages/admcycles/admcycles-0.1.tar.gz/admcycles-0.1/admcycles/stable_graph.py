from copy import deepcopy

from sage.misc.misc_c import prod
from sage.combinat.subset import Subsets
from sage.rings.integer_ring import ZZ
from sage.functions.other import floor

# graphics:
from sage.repl.rich_output.pretty_print import show
from sage.plot.polygon import polygon2d
from sage.plot.text import text
from sage.plot.bezier_path import bezier_path
from sage.plot.line import line
from sage.plot.circle import circle



class StableGraph(object):
    r"""
    Stable graph.

    A stable graph is represented by a list of genera of its vertices,
    a list of legs at each vertex and a list of pairs of legs forming edges.

    EXAMPLES:

    We create a stable graph with two vertices of genera 3,5 joined by an edge
    with a self-loop at the genus 3 vertex::

        sage: from admcycles import StableGraph
        sage: StableGraph([3,5], [[1,3,5],[2]], [(1,2),(3,5)])
        [3, 5] [[1, 3, 5], [2]] [(1, 2), (3, 5)]

    It is also possible to create graphs which are not neccesarily stable::

        sage: StableGraph([1,0], [[1], [2,3]], [(1,2)])
        [1, 0] [[1], [2, 3]] [(1, 2)]

        sage: StableGraph([0], [[1]], [])
        [0] [[1]] []
    """
    def __init__(self,genera,legs,edges):
        """
        INPUT:

      genera : list
         List of genera of the vertices of length m.
      legs : list
         List of length m, where ith entry is list of legs attached to vertex i.
         By convention, legs are unique positive integers.
      edges : list
         List of edges of the graph. Each edge is a 2-tuple of legs.
    """
        self.genera = list(map(ZZ, genera))
        self.legs = legs
        self.edges = edges
        self.maxleg = max([max(j+[0]) for j in self.legs]) #highest leg-label that occurs

    def __repr__(self):
        return repr(self.genera)+ ' ' + repr(self.legs) + ' ' + repr(self.edges)

    def __eq__(self,other):
        if type(self) is not type(other):
            return False
        return self.genera == other.genera and \
               self.legs == other.legs and \
               self.edges == other.edges

    def __ne__(self, other):
        return not (self == other)

    def g(self):
        r"""
        Return the genus of this stable graph

        EXAMPLES::

            sage: from admcycles import StableGraph
            sage: G = StableGraph([1,2],[[1,2], [3,4]], [(1,3),(2,4)])
            sage: G.g()
            4
        """
        return sum(self.genera) + len(self.edges) - len(self.genera) + ZZ.one()

    def n(self):
        r"""
        Return the number of legs of the stable graph.

        EXAMPLES::

            sage: from admcycles import StableGraph
            sage: G = StableGraph([1,2],[[1,2],[3,4,5,6]],[(1,3),(2,4)]);G.n()
            2
        """
        return len(self.list_markings())

    def numvert(self):
        return len(self.genera)

    def _graph_(self):
        r"""
        Return the Sage graph object encoding the stable graph

        This inserts a vertex with label (i,j) in the middle of the edge (i,j).
        Also inserts a vertex with label ('L',i) at the end of each leg l.

        EXAMPLES::

            sage: from admcycles import StableGraph
            sage: Gr = StableGraph([3,5],[[1,3,5,7],[2]],[(1,2),(3,5)])
            sage: SageGr = Gr._graph_()
            sage: SageGr
            Multi-graph on 5 vertices
            sage: SageGr.vertices(sort=False)   # random
            [(1, 2), 0, 1, (3, 5), ('L', 7)]
        """
        from sage.graphs.graph import Graph
        G = Graph(multiedges=True)
        for i, j in  self.edges:
            G.add_vertex((i, j))
            G.add_edge((i, j), self.vertex(i))
            G.add_edge((i, j), self.vertex(j))
        for i in self.list_markings():
            G.add_edge(('L', i), self.vertex(i))
        return G

    def dim(self,v=None):
        """
        Return dimension of moduli space at vertex v.

        If v=None, return dimension of entire stratum parametrized by graph.
        """
        if v is None:
            return sum([self.dim(v) for v in range(len(self.genera))])
        return 3 * self.genera[v] - 3 + len(self.legs[v])

    def invariant(self):
        r"""
        Return a graph-invariant in form of a tuple of integers or tuples

        At the moment this assumes that we only compare stable graph with same total
        g and set of markings
        currently returns sorted list of (genus,degree) for vertices

        IDEAS:

        * number of self-loops for each vertex

        EXAMPLES::

            sage: from admcycles import StableGraph
            sage: Gr = StableGraph([3,5],[[1,3,5,7],[2]],[(1,2),(3,5)])
            sage: Gr.invariant()
            ((3, 4, (7,)), (5, 1, ()))
        """
        return tuple(sorted([(self.genera[v], len(self.legs[v]), tuple(sorted(self.list_markings(v)))) for v in range(len(self.genera))]))

    def tidy_up(self):
        r"""
        Makes sure edges are in correct form and markings, maxleg is fine
        """
        for e in range(len(self.edges)):
            if self.edges[e][0] > self.edges[e][1]:
                self.edges[e] = (self.edges[e][1],self.edges[e][0])
        #TODO: sorting edges ascendingly
        self.maxleg = max([max(j+[0]) for j in self.legs])

    def vertex(self, l):
        r"""
        Return vertex number of leg l
        """
        for v in range(len(self.legs)):
            if l in self.legs[v]:
                return v
        return - ZZ.one() #self does not have leg l

    def list_markings(self,v=None):
        r"""
        Return the list of markings (non-edge legs) of self at vertex v.

        EXAMPLES::

            sage: from admcycles import StableGraph

            sage: gam = StableGraph([3,5],[[1,3,7],[2,4]],[(1,2)])
            sage: gam.list_markings(0)
            (3, 7)
            sage: gam.list_markings()
            (3, 7, 4)
        """
        if v is None:
            return tuple([j for v in range(len(self.genera)) for j in self.list_markings(v) ])
        s = set(self.legs[v])
        for e in self.edges:
            s -= set(e)
        return tuple(s)

    def leglist(self):
        r"""
        Return the list of legs
        """
        l = []
        for j in self.legs:
            l += j
        return l

    def halfedges(self):
        r"""
        Return the tuple containing all half-edges, i.e. legs belonging to an edge
        """
        s=()
        for e in self.edges:
            s=s+e
        return s

    def edges_between(self,i,j):
        r"""
        Return the list [(l1,k1),(l2,k2), ...] of edges from i to j, where l1 in i, l2 in j; for i==j return each edge only once
        """
        if i == j:
            return [e for e in self.edges if (e[0] in self.legs[i] and e[1] in self.legs[j] ) ]
        else:
            return [e for e in self.edges if (e[0] in self.legs[i] and e[1] in self.legs[j] ) ]+ [(e[1],e[0]) for e in self.edges if (e[0] in self.legs[j] and e[1] in self.legs[i] ) ]

    def forget_markings(self,markings):
        r"""
        Erase all legs in the list markings, do not check if this gives well-defined graph
        """
        for m in markings:
            self.legs[self.vertex(m)].remove(m)
        return self

    def leginversion(self,l):
        r"""
        Returns l' if l and l' form an edge, otherwise returns l
        """
        for e in self.edges:
            if e[0]==l:
                return e[1]
            if e[1]==l:
                return e[0]
        return l

    def stabilize(self):
        r"""
        Stabilize this stable graph.

        (all vertices with genus 0 have at least three markings) and returns (dicv,dicl,dich), with
         * dicv a dictionary sending new vertex numbers to the corresponding old vertex numbers
         * dicl a dictionary sending new marking names to the label of the last half-edge that they replaced during the stabilization
           this happens for instance if a g=0 vertex with marking m and half-edge l (belonging to edge (l,l')) is stabilized: l' is replaced by m, so dicl[m]=l'
         * dich a dictionary sending half-edges that vanished in the stabilization process to the last half-edge that replaced them
           this happens if a g=0 vertex with two half-edges a,b (whose corresponding half-edges are c,d) is stabilized: we obtain an edge (c,d) and a -> d, b -> d
        we assume here that a stabilization exists (all connected components have 2g-2+n>0)
        """
        markings = self.list_markings()
        stable = False
        verteximages = list(range(len(self.genera)))
        dicl = {}
        dich = {}
        while not stable:
            numvert = len(self.genera)
            count = 0
            stable = True
            while count < numvert:
                if self.genera[count] == 0 and len(self.legs[count]) == 1:
                    stable = False
                    e0 = self.legs[count][0]
                    e1 = self.leginversion(e0)
                    v1 = self.vertex(e1)
                    self.genera.pop(count)
                    verteximages.pop(count)
                    numvert -= 1
                    self.legs[v1].remove(e1)
                    self.legs.pop(count)
                    try:
                        self.edges.remove((e0,e1))
                    except:
                        self.edges.remove((e1,e0))
                elif self.genera[count] == 0 and len(self.legs[count]) == 2:
                    stable = False
                    e0 = self.legs[count][0]
                    e1 = self.legs[count][1]

                    if e1 in markings:
                        swap = e0
                        e0 = e1
                        e1 = swap

                    e1prime = self.leginversion(e1)
                    v1 = self.vertex(e1prime)
                    self.genera.pop(count)
                    verteximages.pop(count)
                    numvert -= 1

                    if e0 in markings:
                        dicl[e0] = e1prime
                        self.legs[v1].remove(e1prime)
                        self.legs[v1].append(e0)
                        self.legs.pop(count)
                        try:
                            self.edges.remove((e1,e1prime))
                        except:
                            self.edges.remove((e1prime,e1))
                    else:
                        e0prime = self.leginversion(e0)
                        v0 = self.vertex(e0prime)
                        self.legs.pop(count)
                        try:
                            self.edges.remove((e0,e0prime))
                        except:
                            self.edges.remove((e0prime,e0))
                        try:
                            self.edges.remove((e1,e1prime))
                        except:
                            self.edges.remove((e1prime,e1))
                        self.edges.append((e0prime,e1prime))

                        #update dich
                        dich[e0] = e1prime
                        dich[e1] = e0prime
                        dich.update({h:e1prime for h in dich if dich[h]==e0})
                        dich.update({h:e0prime for h in dich if dich[h]==e1})
                else:
                    count += 1
        return ({i:verteximages[i] for i in range(len(verteximages))},dicl,dich)

    def degenerations(self,v=None):
        r"""
        Return list of all possible degenerations of the graph G by adding an edge at v or splitting it into two vertices connected by an edge
        the new edge always comes last in the list of edges
        if v==None, return all degenerations at all vertices
        """
        if v==None:
            return [j for v in range(len(self.genera)) for j in self.degenerations(v) ]
        delist=[] # list of degenerated graphs

        g=self.genera[v]
        l=len(self.legs[v])

        # for positive genus: add loop to v and decrease genus
        if g > 0:
            G=deepcopy(self)
            G.degenerate_nonsep(v)
            delist.append(G)

        # now all graphs with separating edge : separate in (g1,M) and (g-g1,legs[v]-M), take note of symmetry and stability
        for g1 in range(floor(g/2)+1):
            for M in Subsets(set(self.legs[v])):
                if (g1 == 0  and len(M) < 2) or \
                   (g == g1 and l-len(M) < 2) or \
                   (2*g1 == g and l > 0 and (not self.legs[v][0] in M)):
                    continue
                G = deepcopy(self)
                G.degenerate_sep(v,g1,M)
                delist.append(G)
        return delist

    def newleg(self):
        r"""
        Create two new leg-indices that can be used to create an edge
        """
        self.maxleg += 2
        return (self.maxleg-1, self.maxleg)

    def rename_legs(self,di,shift=0):
        r"""
        Renames legs according to dictionary di, all other leg labels are shifted by shift (useful to keep half-edge labels separate from legs)
        TODO: no check that this renaming is legal, i.e. produces well-defined graph
        """
        for v in self.legs:
            for j in range(len(v)):
                v[j] = di.get(v[j],v[j]+shift)    #replace v[j] by di[v[j]] if v[j] in di and leave at v[j] otherwise
        for e in range(len(self.edges)):
            self.edges[e] = (di.get(self.edges[e][0],self.edges[e][0]+shift) ,di.get(self.edges[e][1],self.edges[e][1]+shift))
        self.tidy_up()

    def degenerate_sep(self, v, g1, M):
        r"""
        degenerate vertex v into two vertices with genera g1 and g(v)-g1 and legs M and complement
        add new edge (e[0],e[1]) such that e[0] is in new vertex v, e[1] in last vertex, which is added
        """
        g = self.genera[v]
        oldleg = self.legs[v]
        e = self.newleg()

        self.genera[v] = g1
        self.genera += [g-g1]
        self.legs[v] = list(M)+[e[0]]
        self.legs += [list(set(oldleg)-set(M))+[e[1]]]
        self.edges += [e]

    def degenerate_nonsep(self,v):
        e=self.newleg()
        self.genera[v] -= 1
        self.legs[v] += [e[0], e[1]]
        self.edges += [e]

    def contract_edge(self,e,adddata=False):
        r"""
        Contracts the edge e=(e0,e1) and returns the contracted graph
         if adddata=True, instead returns a tuple (gammatild,av,edgegraph,vnum) giving
          * the contracted graph gammatild
          * the number av of the vertex in gammatild on which previously the edge e had been attached
          * the graph edgegraph induced in self by the edge e (1-edge graph, all legs at the ends of this edge are considered as markings)
          * the numbers vnum (one or two) of the vertices to which e was attached (in the order in which they appear in edgegraph)
          * a surjective dictionary diccv sending old vertex numbers to new vertex numbers
        """
        v0 = self.vertex(e[0])
        v1 = self.vertex(e[1])
        newgraph = deepcopy(self)

        if v0 == v1:  # contracting a loop
            newgraph.genera[v0] += 1
            newgraph.legs[v0].remove(e[0])
            newgraph.legs[v0].remove(e[1])
            newgraph.edges.remove(e)

            if adddata:
                return (newgraph,v0, StableGraph([self.genera[v0]],[deepcopy(self.legs[v0])],[deepcopy(e)]),[v0],{v:v for v in range(len(self.genera))})
            else:
                return newgraph
        else:  # contracting an edge between different vertices
            if v0>v1:
                swap=v0
                v0=v1
                v1=swap
            g1 = newgraph.genera.pop(v1)
            newgraph.genera[v0]+=g1
            l1 = newgraph.legs.pop(v1)
            newgraph.legs[v0]+=l1
            newgraph.legs[v0].remove(e[0])
            newgraph.legs[v0].remove(e[1])
            newgraph.edges.remove(e)

            if adddata:
                diccv={v:v for v in range(v1)}
                diccv[v1]=v0
                diccv.update({v:v-1 for v in range(v1+1,len(self.genera)+1)})
                return (newgraph, v0, StableGraph([self.genera[v0],g1],[deepcopy(self.legs[v0]),deepcopy(self.legs[v1])],[e]), [v0,v1],diccv)
            else:
                return newgraph

    def glue_vertex(self,i,Gr,divGr={},divs={},dil={}):
        r"""
        Glues the stable graph ``Gr`` at the vertex ``i`` of this stable graph

        optional arguments: if divGr/dil are given they are supposed to be a dictionary, which will be cleared and updated with the renaming-convention to pass from leg/vertex-names in Gr to leg/vertex-names in the glued graph
        similarly, divs will be a dictionary assigning vertex numbers in the old self the corresponding number in the new self
        necessary condition:
              * every leg of i is also a leg in Gr
        every leg of Gr that is not a leg of i in self gets a new name
        """
        divGr.clear()
        divs.clear()
        dil.clear()

        # remove vertex i, legs corresponding to it and all self-edges
        selfedges_old=self.edges_between(i,i)
        self.genera.pop(i)
        legs_old=self.legs.pop(i)
        for e in selfedges_old:
            self.edges.remove(e)

        # when gluing in Gr, make sure that new legs corresponding to edges inside Gr
        # or legs in Gr which are already attached to a vertex different from i in self get a new unique label in the glued graph
        m=max(self.maxleg,Gr.maxleg)    #largest index used in either graph, new labels m+1, m+2, ...

        Gr_new=deepcopy(Gr) #here legs will be renamed before gluing in

        a=[]
        for l in Gr.legs:
            a+=l
        a=set(a)    # legs of Gr

        b=set(legs_old) # legs of self at vertex i

 #   c=[]
 #   for e in Gr.edges:
 #       c+=[e[0],e[1]]
 #   c=set(c) # legs of Gr that are in edge within Gr

        # set of legs of Gr that need to be relabeled: all legs of Gr that are not attached to vertex i in self
        e=a-b

        for l in e:
            m += 1
            dil[l] = m

        Gr_new.rename_legs(dil)

        # vertex dictionaries
        for j in range(i):
            divs[j] = j
        for j in range(i+1,len(self.genera)+1):
            divs[j] = j-1
        for j in range(len(Gr.genera)):
            divGr[j] = len(self.genera)+j

        self.genera+= Gr_new.genera
        self.legs+=Gr_new.legs
        self.edges+=Gr_new.edges

        self.tidy_up()

    def reorder_vertices(self,vord):
        r"""
        Reorders vertices according to tuple given (permutation of range(len(self.genera)))
        """
        new_genera=[self.genera[j] for j in vord]
        new_legs=[self.legs[j] for j in vord]
        self.genera=new_genera
        self.legs=new_legs

    def extract_subgraph(self,vertices,outgoing_legs=None,rename=True):
        r"""
        extracts from self a subgraph induced by the list vertices
        if the list outgoing_legs is given, the markings of the subgraph are called 1,2,..,m corresponding to the elements of outgoing_legs
        in this case, all edges involving outgoing edges should be cut
        returns a triple (Gamma,dicv,dicl), where
               * Gamma is the induced subgraph
               * dicv, dicl are (surjective) dictionaries associating vertex/leg labels in self to the vertex/leg labels in Gamma
        if rename=False, do not rename any legs when extracting
        """
        attachedlegs=set([l for v in vertices for l in self.legs[v]])
        if outgoing_legs==None:
            alllegs=copy(attachedlegs)
            for (e0,e1) in self.edges:
                if e0 in alllegs and e1 in alllegs:
                    alllegs.remove(e0)
                    alllegs.remove(e1)
            outgoing_legs=list(alllegs)

        shift = len(outgoing_legs) + 1
        if rename:
            dicl={outgoing_legs[i]:i+1 for i in range(shift-1)}
        else:
            dicl={l:l for l in self.leglist()}

        genera = [self.genera[v] for v in vertices]
        legs = [[dicl.setdefault(l,l+shift) for l in self.legs[v]] for v in vertices]
        edges = [(dicl[e0],dicl[e1]) for (e0,e1) in self.edges if (e0 in attachedlegs and e1 in attachedlegs and (e0 not in outgoing_legs) and (e1 not in outgoing_legs))]
        dicv={vertices[i]:i for i in range(len(vertices))}

        return (StableGraph(genera,legs,edges),dicv,dicl)

    def boundary_pullback(self,other):
        r"""
        pulls back the tautclass/decstratum other to self and returns a prodtautclass with gamma=self
        """
        from .admcycles import tautclass, decstratum

        if isinstance(other,tautclass):
            from .admcycles import prodtautclass
            result=prodtautclass(self,[])
            for t in other.terms:
                result+=self.boundary_pullback(t)
            return result
        if isinstance(other,decstratum):
            # NOTE: this is using much more than just stable graphs
            # I would suggest to move it out of this class
            from .admcycles import (common_degenerations, prodtautclass,
                    onekppoly, kppoly, kappacl, psicl)
            commdeg = common_degenerations(self,other.gamma,modiso=True)
            result=prodtautclass(self,[])

            for (Gamma,dicv1,dicl1,dicv2,dicl2) in commdeg:
                numvert=len(Gamma.genera)
                # first determine edges that are covered by self and other - for excess int. terms
                legcount={l:0 for l in Gamma.leglist()}
                for l in dicl1.values():
                    legcount[l] += 1
                for l in dicl2.values():
                    legcount[l] += 1

                excesspoly=onekppoly(numvert)
                for e in Gamma.edges:
                    if legcount[e[0]] == 2:
                        excesspoly*=( (-1)*(psicl(e[0],numvert) + psicl(e[1],numvert)) )

                # partition vertices of Gamma according to where they go in self
                v1preim=[[] for v in range(len(self.genera))]
                for w in dicv1:
                    v1preim[dicv1[w]].append(w)

                graphpartition=[Gamma.extract_subgraph(v1preim[v],outgoing_legs=[dicl1[l] for l in self.legs[v]]) for v in range(len(self.genera))]

                v2preim=[[] for v in range(len(other.gamma.genera))]
                for w in dicv2:
                    v2preim[dicv2[w]].append(w)

                resultpoly=kppoly([],[])
                # now the stage is set to go through the polynomial of other term by term, pull them back according to dicv2, dicl2 and also add the excess-intersection terms
                for (kappa,psi,coeff) in other.poly:
                    # psi-classes are transferred by dicl2, but kappa-classes might be split up if dicv2 has multiple preimages of same vertex
                    # multiply everything together in a kppoly on Gamma, then split up this polynomial according to graphpartition
                    psipolydict={dicl2[l]: psi[l] for l in psi}
                    psipoly=kppoly([([[] for i in range(numvert)],psipolydict)],[1])

                    kappapoly=prod([prod([sum([kappacl(w,k+1,numvert) for w in v2preim[v] ])**kappa[v][k] for k in range(len(kappa[v]))])  for v in range(len(other.gamma.genera))])


                    resultpoly+=coeff*psipoly*kappapoly

                resultpoly*=excesspoly
                #TODO: filter for terms that vanish by dimension reasons?

                # now fiddle the terms of resultpoly apart and distribute them to graphpartition
                for (kappa,psi,coeff) in resultpoly:
                    decstratlist=[]
                    for v in range(len(self.genera)):
                        kappav=[kappa[w] for w in v1preim[v]]
                        psiv={graphpartition[v][2][l] : psi[l] for l in graphpartition[v][2] if l in psi}
                        decstratlist.append(decstratum(graphpartition[v][0],kappa=kappav,psi=psiv))
                    result+=(coeff*prodtautclass(self,[decstratlist]))
            return result

    def to_tautclass(self):
        r"""
        Returns pure boundary stratum associated to self; note: does not divide by automorphisms!
        """
        from .admcycles import tautclass, decstratum
        return tautclass([decstratum(deepcopy(self))])

    def plot(self):
        show(self.plot_obj(),axes=False)

    def plot_obj(self,vord=None,vpos=None,eheight=None):
        r"""
        returns a graphics object in which the self is plotted
        """
        # some parameters
        mark_dx = 1       # x-distance of different markings
        mark_dy = 1       # y-distance of markings from vertices
        mark_rad = 0.2    # radius of marking-circles
        v_dxmin = 1       # minimal x-distance of two vertices
        ed_dy = 0.7       # max y-distance of different edges between same vertex-pair

        vsize = 0.4       # (half the) size of boxes representing vertices

        # vord==None: no parameter vord given, take default; vord==[]: use this parameter to give back the order via the parameter vord
        if vord==None or vord==[]:
            default_vord=list(range(len(self.genera)))
            if vord==None:
                vord=default_vord
            if vord==[]:
                vord+=default_vord
        reord_self=deepcopy(self)
        reord_self.reorder_vertices(vord)


        if vpos==None or vpos==[]:
            default_vpos = [(0,0)]
            for i in range(1 ,len(self.genera)):
                default_vpos+=[(default_vpos[i-1][0]+mark_dx*(len(reord_self.list_markings(i-1))+2 *len(reord_self.edges_between(i-1 ,i-1 ))+len(reord_self.list_markings(i))+2 *len(reord_self.edges_between(i,i)))/QQ(2)+v_dxmin,0)]
            if vpos==None:
                vpos=default_vpos
            if vpos==[]:
                vpos+=default_vpos

        if eheight==None or eheight=={}:
            ned={(i,j): 0  for i in range(len(reord_self.genera)) for j in range(i+1 ,len(reord_self.genera))}
            default_eheight={}
            for e in reord_self.edges:
                ver1=reord_self.vertex(e[0])
                ver2=reord_self.vertex(e[1])
                if ver1!=ver2:
                    default_eheight[e]=abs(ver1-ver2)-1+ned[(min(ver1,ver2), max(ver1,ver2))]*ed_dy
                    ned[(min(ver1,ver2), max(ver1,ver2))]+=1

            if eheight==None:
                eheight=default_eheight
            if eheight=={}:
                eheight.update(default_eheight)

        # now the drawing starts
        # vertices
        vertex_graph=[polygon2d([[vpos[i][0]-vsize,vpos[i][1]-vsize],[vpos[i][0]+vsize,vpos[i][1]-vsize],[vpos[i][0]+vsize,vpos[i][1]+vsize],[vpos[i][0]-vsize,vpos[i][1]+vsize]], color='white',fill=True, edgecolor='black', thickness=1,zorder=2) + text('g='+repr(reord_self.genera[i]), vpos[i], fontsize=20 , color='black',zorder=3) for i in range(len(reord_self.genera))]


        # non-self edges
        edge_graph=[]
        for e in reord_self.edges:
            ver1=reord_self.vertex(e[0])
            ver2=reord_self.vertex(e[1])
            if ver1!=ver2:
                x=(vpos[ver1][0]+vpos[ver2][0])/QQ(2)
                y=(vpos[ver1][1]+vpos[ver2][1])/QQ(2)+eheight[e]
                edge_graph+=[bezier_path([[vpos[ver1], (x,y) ,vpos[ver2] ]],color='black',zorder=1)]

        marking_graph=[]

        for v in range(len(reord_self.genera)):
            se_list=reord_self.edges_between(v,v)
            m_list=reord_self.list_markings(v)
            v_x0=vpos[v][0]-(2*len(se_list)+len(m_list)-1)*mark_dx/QQ(2)

            for e in se_list:
                edge_graph+=[bezier_path([[vpos[v], (v_x0,-mark_dy), (v_x0+mark_dx,-mark_dy) ,vpos[v] ]],zorder=1)]
                v_x0+=2*mark_dx
            for l in m_list:
                marking_graph+=[line([vpos[v],(v_x0,-mark_dy)],color='black',zorder=1)+circle((v_x0,-mark_dy),mark_rad, fill=True, facecolor='white', edgecolor='black',zorder=2)+text(repr(l),(v_x0,-mark_dy), fontsize=10, color='black',zorder=3)]
                v_x0+=mark_dx
        return sum(marking_graph)+sum(edge_graph)+sum(vertex_graph)
