from .cautomata cimport *
cimport numpy

cdef extern from "complex.h":
    cdef struct Complexe:
        double x, y


cdef extern from "relations.h":
    cdef struct Element:
        int *c  # liste des n coeffs

    cdef struct PlaceArch:
        Complexe *c  # 1, b, b^2, ... for this place

    # class containing the informations needed to compute the relations automaton
    cdef struct InfoBetaAdic:
        int n         # degree
        Element bn    # expression of b^n as a polynome in b of degree < n
        Element b1    # expression of 1/b as a polynome in b of degree < n
        Element *c    # list of digits used for the calculation of relations automaton
        int nc        # number of digits
        int ncmax     # number of allocated digits
        PlaceArch *p  # list of na places
        double *cM    # square of the bound
        int na        # number of places

    Element NewElement(int n)
    void FreeElement(Element e)
    InfoBetaAdic allocInfoBetaAdic(int n, int na, int ncmax, int nhash, bint verb)
    void freeInfoBetaAdic(InfoBetaAdic *iba)
    Automaton RelationsAutomatonT(InfoBetaAdic *iba2, Element t, bint isvide, bint ext, bint verb)

cdef extern from "draw.h":
    ctypedef unsigned char uint8
    cdef struct Color:
        uint8 r
        uint8 g
        uint8 b
        uint8 a
    cdef struct Surface:
        Color **pix
        int sx, sy
    cdef struct Complexe:
        double x
        double y
    cdef struct BetaAdic:
        Complexe b
        Complexe* t  # list of translations
        int n        # number of translations
        Automaton a
    cdef struct BetaAdic2:
        Complexe b
        Complexe* t  # list of translations
        int n        # number of translations
        Automaton* a
        int na
    ctypedef Color* ColorList

    bint HaySDL ()
    void TestSDL()

    void SurfaceToNumpy (Surface *s, numpy.ndarray na)
    Surface NewSurface(int sx, int sy)
    void FreeSurface(Surface s)
    ColorList NewColorList(int n)
    void FreeColorList(ColorList l)
    Color randColor(int a)
    #    Automate NewAutomate (int n, int na)
    #    void FreeAutomate(Automate a)
    void FreeAutomatons(Automaton* a, int n)
    BetaAdic NewBetaAdic(int n)
    void FreeBetaAdic(BetaAdic b)
    BetaAdic2 NewBetaAdic2(int n, int na)
    void FreeBetaAdic2(BetaAdic2 b)
    int *DrawZoom(BetaAdic b, int sx, int sy, int n, int ajust, Color col, int nprec, double sp, int verb)
    Automaton UserDraw(BetaAdic b, int sx, int sy, int n, int ajust, Color col, double sp, int verb)
    #  void WordZone (BetaAdic b, int *word, int nmax)
    int *Draw(BetaAdic b, Surface s, int n, int ajust, Color col, int nprec, double sp, int verb)
    void Draw2(BetaAdic b, Surface s, int n, int ajust, Color col, double sp, int verb)
    void DrawList(BetaAdic2 b, Surface s, int n, int ajust, ColorList lc, double alpha, double sp, int nprec, int verb)
    void print_word(BetaAdic b, int n, int etat)

cdef extern from "numpy/arrayobject.h":
    ctypedef int intp
    ctypedef extern class numpy.ndarray [object PyArrayObject]:
        cdef char *data
        cdef int nd
        cdef intp *dimensions
        cdef intp *strides
        cdef int flags

cdef class BetaAdicSet:
    cdef b
    cdef DetAutomaton a

cdef class BetaBase:
    cdef BetaAdicSet m
    cdef b
